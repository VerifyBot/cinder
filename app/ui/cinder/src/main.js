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

// import CryptoJS from "crypto-js";
// import { ec } from "elliptic";
// import NodeRSA from "node-rsa";

const app = createApp(App);

class ApiClient {
  constructor() {
    this.baseUrl = "http://127.0.0.1:5000";

    this.handshake_state = 0;

    this.secure = false;
    this.publicKey = null;
    this.privateKey = null;
    this.serverPublicKey = null;

    this.secureToken = null;

    // this.doHandshake();
  }

  // async doHandshake() {
  //   let resp;

  //   // valid random rsa private and public keys
  //   // const kp = curve.genKeyPair();
  //   this.privateKey = new NodeRSA({ b: 2048 });
  //   this.publicKey = this.privateKey.exportKey("private");

  //   this.handshake_state = 0.5;  // send pk header

  //   resp = await this.post("/handshake_request", {
  //     public_key: this.publicKey,
  //   });
  //   this.secure = resp.data.handshake_required;

  //   if (!this.secure) return; // no need to do anything else

  //   this.handshake_state = 1;

  //   console.log(`Sending: ${btoa(this.publicKey)}`);
  //   resp = await this.post("/handshake", { public_key: btoa(this.publicKey) });

  //   this.serverPublicKey = atob(resp.data.public_key);

  //   let encryptedToken = atob(resp.data.token);
  //   this.secureToken = CryptoJS.AES.decrypt(
  //     encryptedToken,
  //     this.privateKey
  //   ).toString(CryptoJS.enc.Utf8);

  //   this.secureToken = encryptedToken;
  //   this.handshake_state = 2;
  // }

  maybeAuth() {
    if (localStorage.getItem("token")) {
      return {
        Authorization: localStorage.getItem("token"),
      };
    }
    return {};
  }

  encryptData(data) {
    if (!this.secure || this.handshake_state !== 2) return data;

    return btoa(CryptoJS.AES.encrypt(data, this.secureToken).toString());
  }

  decryptData(data) {
    if (!this.secure || this.handshake_state !== 2) return data;

    return atob(
      CryptoJS.AES.decrypt(data, this.secureToken).toString(CryptoJS.enc.Utf8)
    );
  }

  maybeSecureHeaders() {
    console.log(`s=${this.secure} pk=${this.publicKey}`);
    if ((this.secure && this.publicKey) || this.handshake_state === 0.5) {
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

    if (js.error) {
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
    let js;

    try {
      const response = await fetch(`${this.baseUrl}${url}`, {
        method: "POST",
        body: this.encryptData(JSON.stringify(data)),
        headers: {
          "Content-Type": "application/json",
          ...this.maybeAuth(),
          ...this.maybeSecureHeaders(),
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

    if (js.error) {
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
