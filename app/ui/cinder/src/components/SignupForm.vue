<template>
  <v-form @submit.prevent ref="form">
    <v-row class="d-flex align-center justify-center">
      <v-col cols="12" md="4">
        <v-text-field v-model="username" validate-on="submit" :rules="usernameRules" required
          type="text">

          <template v-slot:label>
            <v-icon class="mr-1">mdi-badge-account</v-icon>
            Username
          </template>
        </v-text-field>
      </v-col>
    </v-row>

    <v-row class="d-flex align-center justify-center">
      <v-col cols="12" md="4">
        <v-text-field v-model="email" validate-on="submit" :rules="emailRules" required autocomplete="none" type="text"
        >
          <template v-slot:label>
            <v-icon class="mr-1">mdi-at</v-icon>
            Email
          </template>
        </v-text-field>
      </v-col>
    </v-row>

    <v-row class="d-flex align-center justify-center">
      <v-col cols="12" md="4">
        <v-text-field v-model="password" validate-on="submit" :rules="passwordRules" required type="password"
          autocomplete="none">
          <template v-slot:label>
            <v-icon class="mr-1">mdi-form-textbox-password</v-icon>
            Password
          </template>
        </v-text-field>
      </v-col>

    </v-row>

    <div class="py-8"></div>

    <v-row class="d-flex align-center justify-center">
      <v-col cols="12" md="4">
        <v-row class="d-flex align-center justify-center">
          <v-btn prepend-icon="mdi-chevron-right-circle" variant="tonal" block size="x-large" color="light-blue" type="submit"
          @click="validate">
            Continue
          </v-btn>
        </v-row>
      </v-col>
    </v-row>
  </v-form>
</template>

<script >
export default {
  props: {
    defUsername: String,
    defEmail: String,
    defPassword: String
  },
  mounted() {
    this.username = this.defUsername;
    this.email = this.defEmail;
    this.password = this.defPassword;
  },
  data() {
    return {
      valid: false,

      username: '',
      usernameRules: [
        value => value ? true : 'Username is missing.',
        value => value?.length >= 3 && value?.length <= 20 ? true : 'Username must be less 3-20 chars long.',
      ],

      email: '',
      emailRules: [
        value => value ? true : 'Email is missing.',
        value => (/.+@.+\..+/.test(value)) ? true : 'Email must be valid.',
      ],

      password: '',
      passwordRules: [
        value => value ? true : 'Password is missing.',
        value => value?.length >= 4 ? true : 'Password must be at least 4 chars long.',
      ],
    }
  },

  methods: {
    async validate () {
      const { valid } = await this.$refs.form.validate()

      if (valid)
        this.$emit('signupButton', this.username, this.email, this.password)
    }
  }
}
</script>
