<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height py-10">

      <div class="cont-box">
        <h1 class="pretty-title">Log In</h1>

        <div class="py-5"></div>

        <LoginForm v-if="!disabled" @loginButton="loginButton" :defusernameOrEmail="usernameOrEmail"
          :defPassword="password" />

        <div v-else>
          <v-progress-circular indeterminate color="blue-darken-2"></v-progress-circular>
        </div>

        <div class="py-5"></div>
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup>
import LoginForm from '@/components/LoginForm.vue'

</script>

<script>
import $ from "@/jquery.min.js";
import notify from "@/notify.min.js"

export default {
  data: () => ({
    usernameOrEmail: 'niryo',
    password: 'niryo',

    disabled: false
  }),
  mounted() {

  },
  methods: {
    async loginButton(usernameOrEmail, password) {
      this.usernameOrEmail = usernameOrEmail;
      this.password = password;
      this.disabled = true;


      let is_email = RegExp(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/).test(usernameOrEmail);
      let data = {
        username: is_email ? null : usernameOrEmail,
        email: is_email ? usernameOrEmail : null,
        password: password
      }
      const resp = await this.api.post("/login", data);
      // const resp = { ok: true, token: "abcdefg", username: this.usernameOrEmail }

      if (!resp.ok) {
        this.disabled = false;
        return;
      }

      // success
      localStorage.setItem("token", resp.data.token);
      localStorage.setItem("username", resp.data.user.username);
      this.$router.push("/swipe");
    }
  },
  watch: {

  }
}
</script>

<style></style>