<template>
  <v-container class="fill-height">
    <v-responsive class="align-center text-center fill-height py-10">

      <h1 class="pretty-title">Sign Up</h1>

      <div class="py-5"></div>

      <SignupForm v-if="step === 1" @signupButton="signupButton" :defUsername="username" :defEmail="email"
        :defPassword="password" />


      <div v-else>
        <v-progress-circular indeterminate color="blue-darken-2"></v-progress-circular>
      </div>

    </v-responsive>
  </v-container>
</template>

<script setup>
import SignupForm from '@/components/SignupForm.vue'

</script>

<script>
import $ from "@/jquery.min.js";
import notify from "@/notify.min.js"

export default {
  data: () => ({
    step: 1,
    steps: [
      'Details',
    ],

    // step 1
    username: 'niryo',
    email: 'niryo@gmail.com',
    password: 'niryo'


  }),
  mounted() {

  },
  methods: {
    signupButton(username, email, password) {
      this.username = username;
      this.email = email;
      this.password = password;
      this.step = 2;

    }
  },
  watch: {
    async step(v) {
      if (v > this.steps.length) {

        const resp = await this.api.post("/signup", {
          username: this.username,
          email: this.email,
          password: this.password
        });

        if (!resp.ok) {
          // show alert
          this.step = 1;
          return;
        }

        console.log(`✅ Signed up! User ID: ${resp.user_id}`)

        // success
        localStorage.setItem("token", resp.data.token);
        localStorage.setItem("username", this.username);
        this.$router.push("/swipe");
      }
    }
  }
}
</script>

