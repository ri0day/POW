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
        :detailFunc="getApplicationItem"
      ></app-datatable>
    </v-row>
  </v-container>
</template>


<script>
  import Breadcrumbs from '@/components/Breadcrumbs'
  import DataTable from '@/components/DataTable'
  import { expApplicationItem, getApplicationList, getApplicationItem } from '@/api'
  import CsvExportor from 'csv-exportor'

  export default {
    name: 'application',
    components: {
      'app-breadcrumbs': Breadcrumbs,
      'app-datatable': DataTable
    },
    data () {
      return {
        title: 'Application',
        items: [],
        headers: [
          { text: 'APPNAME', value: 'APPNAME' },
          { text: 'SLB', value: 'SLB' },
          { text: 'SERVERS', value: 'SERVERS' },
          { text: 'RDBMS', value: 'RDBMS' },
          { text: 'Detail', value: 'APPNAME' }
        ],
        getApplicationItem
      }
    },
    methods: {
      exportCsv () {
        expApplicationItem().then(data => {
          CsvExportor.downloadCsv(
            data,
            { header: ['APPNAME', 'SLB', 'SERVERS', 'RDBMS'] },
            'test-application.csv')
        })
      }
    },
    created () {
      getApplicationList().then(data => {
        this.items = data
      })
    }
  }
</script>
