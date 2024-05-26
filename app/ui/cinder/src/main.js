/**
 * main.js
 *
 * Bootstraps Vuetify and other plugins then mounts the App`
 */

// Components
import App from "./App.vue";

// Composables
import { createApp } from "vue";

// Plugins
import { registerPlugins } from "@/plugins";

import $ from "@/jquery.min.js";
import notify from "@/notify.min.js";
import CryptoJS from "crypto-js";

const app = createApp(App);

class DiffieHellman {
  G;
  P;
  privateKey;

  constructor(g, p) {
    this.G = g;
    this.P = p;
    this.privateKey = this.generatePrivateKey();
  }

  generatePrivateKey() {
    return Math.floor(Math.random() * 10) + 10;
  }

  generatePublicKey() {
    return Math.pow(this.G, this.privateKey) % this.P;
  }

  generateSharedKey(otherPublicKey) {
    console.log(
      `Server Key: ${otherPublicKey}, Client Key: ${this.privateKey}, p: ${this.P}`
    );
    return Math.pow(otherPublicKey, this.privateKey) % this.P;
  }
}

async function sha256(message) {
  // encode as UTF-8
  const msgBuffer = new TextEncoder().encode(message);                    

  // hash the message
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

  // convert ArrayBuffer to Array
  const hashArray = Array.from(new Uint8Array(hashBuffer));

  // convert bytes to hex string                  
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  return hashHex;
}

class ApiClient {
  constructor() {
    this.baseUrl = "http://127.0.0.1:5000";

    this.secure = false;
    this.publicKey = null;
    this.serverPublicKey = null;
    this.sharedKey = null;

    this.diffie = new DiffieHellman(2, 9_007_199_254_740_881);
    this.duringHandshake = true;
    this.doHandshake();
  }

  async doHandshake() {
    this.publicKey = this.diffie.generatePublicKey();

    const js = await this.post("/handshake", { public_key: this.publicKey });

    // no encryption
    if (!js.ok) {
      this.secure = false;
      return;
    }

    this.secure = true;

    console.log(`pk: ${js.data.server_pk}`)
    const sharedKey = this.diffie.generateSharedKey(Number(js.data.server_pk))
    console.log(`sk: ${sharedKey}`)
    this.sharedKey = await sha256(sharedKey);
    console.log(`Shared key: ${this.sharedKey}`)
    this.duringHandshake = false;
  }

  maybeAuth() {
    if (localStorage.getItem("token")) {
      return {
        Authorization: localStorage.getItem("token"),
      };
    }
    return {};
  }

  encryptData(data) {
    if (!this.secure) return data;

    return CryptoJS.AES.encrypt(data, CryptoJS.enc.Hex.parse(this.sharedKey), {
      mode: CryptoJS.mode.ECB,
    }).ciphertext.toString(CryptoJS.enc.Hex);
  }

  decryptData(data) {
    if (!this.secure) return data;

    return CryptoJS.AES.decrypt(
      CryptoJS.enc.Hex.parse(data).toString(CryptoJS.enc.Base64),
      CryptoJS.enc.Hex.parse(this.sharedKey),
      {
        mode: CryptoJS.mode.ECB,
      }
    ).toString(CryptoJS.enc.Utf8);
  }

  maybeSecureHeaders(url) {
    console.log(`s=${this.secure} pk=${this.publicKey}`);
    if ((this.secure && this.publicKey) || url == '/handshake') {
      console.log("sending public key header");
      return {
        "X-Client-Public-Key": this.publicKey,
      };
    }
    return {};
  }

  simpleErrorHandling(js) {
    if (js.error === "InvalidToken") {
      localStorage.removeItem("token");
      window.location.href = "/login";
      return true;
    }
  }

  async get(url, options = {}) {
    while (this.duringHandshake && url != '/handshake') {
      console.log('waiting..')
      await new Promise((resolve) => setTimeout(resolve, 100));
    }

    let js;

    try {
      const response = await fetch(`${this.baseUrl}${url}`, {
        method: "GET",
        headers: { ...this.maybeAuth(), ...this.maybeSecureHeaders() },
        ...options,
      });

      js = JSON.parse(this.decryptData(await response.text()));
    } catch (e) {
      if (e.message.includes("Failed to fetch")) {
        js = {
          error: "Connection Error",
          message: `Server did not respond for ${url}`,
        };
      } else {
        throw e;
      }
    }

    if (js.error && url != '/handshake') {
      if (!this.simpleErrorHandling(js)) {
        notify(`⚠️ ${js.error}: ${js.message}`, {
          position: "bottom left",
          className: "error",
          autoHideDelay: 5000,
        });
      }
    }

    return js;
  }

  async post(url, data, options = {}) {
    while (this.duringHandshake && url != '/handshake') {
      console.log('waiting..')
      await new Promise((resolve) => setTimeout(resolve, 100));
    }

    let js;

    try {
      const response = await fetch(`${this.baseUrl}${url}`, {
        method: "POST",
        body: this.encryptData(JSON.stringify(data)),
        headers: {
          "Content-Type": "application/json",
          ...this.maybeAuth(),
          ...this.maybeSecureHeaders(url),
        },
        ...options,
      });
      js = JSON.parse(this.decryptData(await response.text()));
    } catch (e) {
      if (e.message.includes("Failed to fetch")) {
        js = {
          error: "Connection Error",
          message: `Server did not respond for ${url}`,
        };
      } else {
        throw e;
      }
    }

    if (js.error && url != '/handshake') {
      if (!this.simpleErrorHandling(js)) {
        notify(`⚠️ ${js.error}: ${js.message}`, {
          position: "bottom left",
          className: "error",
          autoHideDelay: 5000,
        });
      }
    }

    return js;
  }
}

app.config.globalProperties.api = new ApiClient();
window.api = app.config.globalProperties.api;

registerPlugins(app);

app.mount("#app");
