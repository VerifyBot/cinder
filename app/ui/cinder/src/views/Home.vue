<template>
  <NotLogged v-if="state === 'not-logged'"  />
  <HelloWorld v-else />
</template>

<script setup>
import HelloWorld from '@/components/HelloWorld.vue'
import NotLogged from '@/components/NotLogged.vue'

</script>

<script>

export default {
  data() {
    return {
      state: 'not-logged'
    }
  },
}
</script>
