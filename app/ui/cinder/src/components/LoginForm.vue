<template>
  <v-form @submit.prevent ref="form">
    <v-row class="d-flex align-center justify-center">
      <v-col cols="12" md="4">
        <v-text-field v-model="usernameOrEmail" :validate-on="submit" :rules="usernameOrEmailRules" required type="text">

          <template v-slot:label>
            <v-icon class="mr-1">mdi-badge-account</v-icon>
            Username/Email
          </template>
        </v-text-field>
      </v-col>
    </v-row>

    <v-row class="d-flex align-center justify-center">
      <v-col cols="12" md="4">
        <v-text-field v-model="password" required type="password"
          autocomplete="none" :validate-on="submit" :rules="passwordRules">
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
    defusernameOrEmail: String,
    defPassword: String
  },
  data: () => ({
    valid: false,

    usernameOrEmail: null,
    usernameOrEmailRules: [
      v => !!v || 'Username or Email is required',
      value => value?.length >= 3 && value?.length <= 20 ? true : 'Too short.',
    ],

    password: null,
    passwordRules: [
    value => value ? true : 'Password is missing.',
        value => value?.length >= 4 ? true : 'Password must be at least 4 chars long.',
     
    ]
  }),
  mounted() {
    this.usernameOrEmail = this.defusernameOrEmail;
    this.password = this.defPassword;
  },


  methods: {
    async validate() {
      const { valid } = await this.$refs.form.validate()

      if (valid) {
        this.$emit('loginButton', this.usernameOrEmail, this.password)
      }
        
    }
  }
}
</script>
