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
        :detailFunc="getRDBMSItem"
      ></app-datatable>
    </v-row>
  </v-container>
</template>


<script>
  import { mapState } from 'vuex'
  import Breadcrumbs from '@/components/Breadcrumbs'
  import DataTable from '@/components/DataTable'
  import { expRDBMSItem, getRDBMSList, getRDBMSItem } from '@/api'
  import CsvExportor from 'csv-exportor'

  export default {
    name: 'rdbms',
    components: {
      'app-breadcrumbs': Breadcrumbs,
      'app-datatable': DataTable
    },
    data () {
      return {
        title: 'RDBMS',
        items: [],
        headers: [
          { text: 'DBInstanceId', value: 'DBInstanceId' },
          { text: 'DBInstanceDescription', value: 'DBInstanceDescription' },
          { text: 'ZoneId', value: 'ZoneId' },
          { text: 'DBInstanceStatus', value: 'DBInstanceStatus' },
          { text: 'DBInstanceCPU', value: 'DBInstanceCPU' },
          { text: 'DBInstanceMemory', value: 'DBInstanceMemory' },
          { text: 'DBInstanceStorage', value: 'DBInstanceStorage' },
          { text: 'ExpireTime', value: 'ExpireTime' },
          { text: 'DBInstanceType', value: 'DBInstanceType' },
          { text: 'Account', value: 'Access_key' },  // Access_key => Account
          { text: 'State', value: 'State' },
          { text: 'Detail', value: '_key' }
        ],
        getRDBMSItem  // function
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
        expRDBMSItem().then(data => {
          CsvExportor.downloadCsv(
            data,
            { header: ['DBInstanceId', 'DBInstanceDescription', 'DBInstanceStatus', 'DBInstanceCPU', 'DBInstanceMemory', 'DBInstanceStorage', 'DBInstanceType', 'ConnectionString', 'MaxIOPS', 'CreationTime', 'ExpireTime', 'ZoneId', 'State'] },
            'test-rdbms.csv')
        })
      }
    },
    created () {
      getRDBMSList().then(data => {
        this.items = data
      })
    }
  }
</script>
