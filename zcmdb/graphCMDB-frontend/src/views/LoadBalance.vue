<template>
  <v-container fluid class="pr-3 pl-3">
    <v-row>
      <app-breadcrumbs></app-breadcrumbs>
      <button @click="exportCsv">EXPORT</button>
    </v-row>
    <v-row>
      <app-datatable
        :title="title"
        :headers="headers"
        :items="computedItems"
        :detailFunc="getLoadBalanceItem"
      ></app-datatable>
    </v-row>
  </v-container>
</template>


<script>
  import { mapState } from 'vuex'
  import Breadcrumbs from '@/components/Breadcrumbs'
  import DataTable from '@/components/DataTable'
  import { expLoadBalanceItem, getLoadBalanceList, getLoadBalanceItem } from '@/api'
  import CsvExportor from 'csv-exportor'

  export default {
    name: 'loadbalance',
    components: {
      'app-breadcrumbs': Breadcrumbs,
      'app-datatable': DataTable
    },
    data () {
      return {
        title: 'LoadBalance',
        items: [],
        headers: [
          { text: 'LoadBalancerId', value: 'LoadBalancerId' },
          { text: 'LoadBalancerName', value: 'LoadBalancerName' },
          { text: 'MasterZoneId', value: 'MasterZoneId' },
          { text: 'Address', value: 'Address' },
          { text: 'LoadBalancerStatus', value: 'LoadBalancerStatus' },
          { text: 'Account', value: 'Access_key' },  // Access_key => Account
          { text: 'State', value: 'State' },
          { text: 'Detail', value: '_key' }
        ],
        getLoadBalanceItem
      }
    },
    computed: {
      computedItems () {
        let ret = []
        for (let i = 0; i < this.items.length; i++) {
          let row = this.items[i]
          row['Access_key'] = this.accountMapping[row['Access_key']]
          ret.push(row)
        }
        return ret
      },
      ...mapState({
        accountMapping: state => state.accountMapping
      })
    },
    methods: {
      exportCsv () {
        expLoadBalanceItem().then(data => {
          CsvExportor.downloadCsv(
            data,
            { header: ['LoadBalancerId', 'LoadBalancerName', 'LoadBalancerStatus', 'MasterZoneId', 'SlaveZoneId', 'Address', 'AddressType', 'BackendServers', 'State'] },
            'test-loadbalancer.csv')
        })
      }
    },
    created () {
      getLoadBalanceList().then(data => {
        this.items = data
      })
    }
  }
</script>
