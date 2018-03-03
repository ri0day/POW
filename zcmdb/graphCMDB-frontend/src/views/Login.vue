<template>
  <v-app id="app">
    <form class="elevation-5" @submit.prevent="onSubmit">
      <v-text-field
        name="username"
        label="Username"
        v-model="form.username"
      ></v-text-field>
      <v-text-field
        name="password"
        label="Password"
        type="password"
        v-model="form.password"
        v-bind:rules="[checkAuth]"
      ></v-text-field>
      <v-btn block primary type="submit">Login</v-btn>
    </form>
  </v-app>
</template>

<script>
  import axios from 'axios'

  export default {
    data () {
      return {
        form: {
          username: '',
          password: ''
        },
        authenticated: true
      }
    },
    methods: {
      onSubmit () {
        let authData = {
          username: this.form.username,
          password: this.form.password
        }

        let self = this
        axios.post(process.env.API_URL + '/_open/auth', authData)
          .then(function (response) {
            if (response.status === 200) {
              localStorage.setItem('Authorization', response.data.jwt)
              self.$router.replace('/')
            } else {
              self.authenticated = false
            }
          })
          .catch(function (error) {
            console.log(error.response)
            self.authenticated = false
          })
      }
    },
    computed: {
      checkAuth () {
        if (this.authenticated) {
          return true
        } else {
          return 'Username or Password is incorrect.'
        }
      }
    }
  }
</script>

<style scoped>
  form {
    width: 380px;
    margin: 6em auto;
    padding: 3em 2em 2em 2em;
    background: #fafafa;
  }

  #app {
    background: #2196f3;
  }
</style>
