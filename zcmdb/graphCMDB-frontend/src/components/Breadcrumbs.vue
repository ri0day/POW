<template>
  <v-breadcrumbs icons divider="forward">
    <v-breadcrumbs-item v-for="(item, index) in items" :key="item">
      {{ item }}
    </v-breadcrumbs-item>
  </v-breadcrumbs>
</template>


<script>
  export default {
    name: 'breadcrumbs',
    computed: {
      items () {
        let path = this.$route.path.split('/')
        path[0] = '/'
        return path
      }
    }
  }
</script>
