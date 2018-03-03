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
        :detailFunc="getNoSQLItem"
      ></app-datatable>
    </v-row>
  </v-container>
</template>


<script>
  import { mapState } from 'vuex'
  import Breadcrumbs from '@/components/Breadcrumbs'
  import DataTable from '@/components/DataTable'
  import { expNoSQLItem, getNoSQLList, getNoSQLItem } from '@/api'
  import CsvExportor from 'csv-exportor'

  export default {
    name: 'nosql',
    components: {
      'app-breadcrumbs': Breadcrumbs,
      'app-datatable': DataTable
    },
    data () {
      return {
        title: 'NoSQL',
        items: [],
        headers: [
          { text: 'InstanceId', value: 'InstanceId' },
          { text: 'InstanceName', value: 'InstanceName' },
          { text: 'ZoneId', value: 'ZoneId' },
          { text: 'InstanceStatus', value: 'InstanceStatus' },
          { text: 'InstanceClass', value: 'InstanceClass' },
          { text: 'EndTime', value: 'EndTime' },
          { text: 'Account', value: 'Access_key' },  // Access_key => Account
          { text: 'State', value: 'State' },
          { text: 'Detail', value: '_key' }
        ],
        getNoSQLItem
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
        expNoSQLItem().then(data => {
          CsvExportor.downloadCsv(
            data,
            { header: ['InstanceId', 'InstanceName', 'InstanceStatus', 'InstanceClass', 'ZoneId', 'EndTime', 'Connections', 'ConnectionDomain', 'Port', 'State'] },
            'test-nosql.csv')
        })
      }
    },
    created () {
      getNoSQLList().then(data => {
        this.items = data
      })
    }
  }
</script>
