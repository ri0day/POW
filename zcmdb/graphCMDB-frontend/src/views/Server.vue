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
        :detailFunc="getServerItem"
      ></app-datatable>
    </v-row>
  </v-container>
</template>


<script>
  import { mapState } from 'vuex'
  import Breadcrumbs from '@/components/Breadcrumbs'
  import DataTable from '@/components/DataTable'
  import { expServerItem, getServerList, getServerItem } from '@/api'
  import CsvExportor from 'csv-exportor'

  export default {
    name: 'server',
    components: {
      'app-breadcrumbs': Breadcrumbs,
      'app-datatable': DataTable
    },
    data () {
      return {
        title: 'Server',
        items: [],
        headers: [
          { text: 'InstanceId', value: 'InstanceId' },
          { text: 'InstanceName', value: 'InstanceName' },
          { text: 'InnerIpAddress', value: 'InnerIpAddress' },
          { text: 'PublicIpAddress', value: 'PublicIpAddress' },
          { text: 'ZoneId', value: 'ZoneId' },
          { text: 'Cpu', value: 'Cpu' },
          { text: 'Memory(MB)', value: 'Memory' },
          { text: 'Disk(GB)', value: 'Disk' },
          { text: 'ExpiredTime', value: 'ExpiredTime' },
          { text: 'Account', value: 'Access_key' },  // Access_key => Account
          { text: 'Tags', value: 'Tags' },
          { text: 'State', value: 'State' },
          { text: 'Detail', value: '_key' }
        ],
        getServerItem
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
        expServerItem().then(data => {
          CsvExportor.downloadCsv(
            data,
            { header: ['InstanceId', 'InstanceName', 'InstanceChargeType', 'InstanceNetworkType', 'InternetMaxBandwidthOut', 'InnerIpAddress', 'PublicIpAddress', 'ZoneId', 'Cpu', 'Memory', 'Disk', 'OSType', 'ExpiredTime', 'CreationTime', 'Description', 'State', 'Tags', 'Account'] },
            'test-server.csv')
        })
      }
    },
    created () {
      getServerList().then(data => {
        this.items = data
      })
    }
  }
</script>
