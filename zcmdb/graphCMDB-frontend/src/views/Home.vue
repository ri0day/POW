<template>
  <v-container fluid class="pr-3 pl-3">
    <v-row>
      <v-col class="mb-3" md6 lg4 v-for="item in computedItems" :key="item.name">
        <v-card hover>
          <v-card-row>
            <v-card-title>
              <span>{{ item.name }}</span>
            </v-card-title>
          </v-card-row>
          <v-card-text>
            <v-card-row>
              <div>
                <v-icon class="mr-5" style="font-size: 60px">pie_chart</v-icon>
              </div>
              <div>
                <div class="title mb-1">Total: {{ item.total }}</div>
                <div class="green--text title mb-1">Online: {{ item.online }}</div>
                <div class="red--text title mb-1">Offline: {{ item.offline }}</div>
              </div>
            </v-card-row>
          </v-card-text>

          <v-divider></v-divider>

          <v-card-row actions>
            <v-btn class="pink--text" flat router :href="item.href">Details</v-btn>
          </v-card-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import { getArangoSummary } from '@/api'

  export default {
    data () {
      return {
        items: [
          {'name': 'Server', 'href': '/server', 'total': 0, 'offline': 0, 'online': 0},
          {'name': 'NoSQL', 'href': '/nosql', 'total': 0, 'offline': 0, 'online': 0},
          {'name': 'RDBMS', 'href': '/rdbms', 'total': 0, 'offline': 0, 'online': 0},
          {'name': 'LoadBalance', 'href': '/loadbalance', 'total': 0, 'offline': 0, 'online': 0},
          {'name': 'Application', 'href': '/application', 'total': 0, 'offline': 0, 'online': 0}
        ]
      }
    },
    methods: {
      getSummary () {
        for (let i in this.items) {
          getArangoSummary(this.items[i]['name']).then(data => {
            for (let j of data) {
              if (j.State === true) {
                this.items[i]['online'] = j.Number
              } else if (j.State === false) {
                this.items[i]['offline'] = j.Number
              }
            }
          })
        }
      }
    },
    computed: {
      computedItems () {
        const ret = []
        for (let i of this.items) {
          i['total'] = i['online'] + i['offline']
          ret.push(i)
        }
        return ret
      }
    },
    created () {
      this.getSummary()
    }
  }
</script>

