<template>
  <v-app id="app" top-toolbar left-sidebar>
    <v-toolbar>
      <v-toolbar-side-icon class="hidden-lg-and-up" @click.native.stop="sidebarShow = !sidebarShow"/>
      <v-toolbar-title>graphCMDB</v-toolbar-title>
      <v-toolbar-items>
        <v-toolbar-item ripple @click.native="logout">Logout</v-toolbar-item>
      </v-toolbar-items>
    </v-toolbar>
    <main>
      <v-sidebar style="min-width: 300px" v-model="sidebarShow" close-on-click>
        <v-list>
          <template v-for="i in items">
            <v-list-item>
              <v-list-tile ripple router :href="i.href">
                <v-list-tile-title>
                  {{ i.title }}
                </v-list-tile-title>
              </v-list-tile>
            </v-list-item>
            <v-divider v-if="i.divider" light></v-divider>
          </template>
        </v-list>
      </v-sidebar>
      <v-content>
        <router-view></router-view>
      </v-content>
    </main>
  </v-app>
</template>

<script>
  import { getArangoData } from '@/api'

  export default {
    name: 'sidebar',
    data () {
      return {
        sidebarShow: '',
        items: [
          { title: 'Dashboard', href: '/', divider: true },
          { title: 'Server', href: '/server' },
          { title: 'NoSQL', href: '/nosql' },
          { title: 'RDBMS', href: '/rdbms' },
          { title: 'LoadBalance', href: '/loadbalance', divider: true },
          { title: 'IpAddress', href: '/ipaddress' },
          { title: 'Application', href: '/application', divider: true }
        ],
        accountMapping: {}
      }
    },
    methods: {
      logout () {
        localStorage.removeItem('Authorization')
        this.$router.replace('/login')
      }
    },
    created () {
      getArangoData('Account').then(data => {
        for (let i = 0; i < data.length; i++) {
          let [k, v] = [data[i]['_key'], data[i]['Name']]
          this.accountMapping[k] = v
        }
      })
    }
  }
</script>
