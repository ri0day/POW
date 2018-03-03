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
        :items="items"
        :detailFunc="getIpAddressItem"
      ></app-datatable>
    </v-row>
  </v-container>
</template>

<script>
  import Breadcrumbs from '@/components/Breadcrumbs'
  import DataTable from '@/components/DataTable'
  import { getIpAddressItem, getIpAddressList } from '@/api'
  import CsvExportor from 'csv-exportor'

  export default {
    name: 'ipaddress',
    components: {
      'app-breadcrumbs': Breadcrumbs,
      'app-datatable': DataTable
    },
    data () {
      return {
        title: 'IpAddress',
        items: [],
        headers: [
          { text: 'IpAddress', value: 'IpAddress' },
          { text: 'Type', value: 'Type' },
          { text: 'Detail', value: '_id' }
        ],
        getIpAddressItem
      }
    },
    methods: {
      exportCsv () {
        CsvExportor.downloadCsv(
          this.items,
          { header: ['IP', 'TYPE', 'ID'] },
          'test-ip.csv')
      }
    },
    created () {
      getIpAddressList().then(data => {
        this.items = data
      })
    }
  }
</script>
