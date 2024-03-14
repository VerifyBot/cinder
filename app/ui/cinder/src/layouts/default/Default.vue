<template>
  <v-app>
    <default-bar />

    <default-view />



  </v-app>
</template>

<script setup>
import DefaultBar from './AppBar.vue'
import DefaultView from './View.vue'
</script>

<script>

export default {
  components: {
    DefaultBar,
    DefaultView
  },
  data: () => ({
    isMobile: false,
    username: null,
    isLoggedIn: false
  }),
  mounted() {
    this.username = localStorage.getItem("username");
    this.isLoggedIn = !!localStorage.getItem("token");

    this.isMobile = window.innerWidth < 1283;

    // on screen size change
    window.addEventListener('resize', () => {
      this.isMobile = window.innerWidth < 1283;
    })
  }
}

</script>