<template>
  <router-view></router-view>
</template>

<script>
  export default {
    name: 'app',
    methods: {
      initial () {
        this.$store.dispatch('initAccountMapping')
      }
    },
    mounted () {
      this.initial()
    }
  }
</script>


<style>
  @import '../node_modules/vuetify/dist/vuetify.min.css';
  @import 'assets/icons.css';
</style>
