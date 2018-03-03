<template>
  <v-container fluid>
    <v-card>
      <v-card-title>
        {{ title }}
        <v-spacer></v-spacer>
        <v-text-field
          append-icon="search"
          label="Search"
          v-model="search"
          single-line
        ></v-text-field>
      </v-card-title>
      <v-data-table
        :headers="headers"
        v-model="items"
        :search="search"
        :rows-per-page="10"
        :rows-per-page-items="[10, 20, 30, { text: 'All', value: -1 }]"
      >
        <template slot="items" scope="props">
          <td class="text-xs-right" nowrap v-for="td in headers.slice(0, -1)">{{ props.item[td.value] }}</td>
          <td class="text-xs-right" v-for="td in headers.slice(-1)">
            <v-btn icon="icon" class="pink--text"
                   @click.native="showModal(props.item[td.value], $event)">
              <v-icon>list</v-icon>
            </v-btn>
          </td>
        </template>
      </v-data-table>

      <!--Detail Modal-->
      <v-dialog v-model="diaShow" fullscreen transition="v-dialog-bottom-transition" :overlay=false>
        <v-card-row>
          <v-toolbar class="secondary">
            <v-btn icon="icon" @click.native="diaShow = false">
              <v-icon>close</v-icon>
            </v-btn>
            <v-toolbar-title>
              <v-chip label class="pink white--text">{{ diaTitle }}</v-chip>
            </v-toolbar-title>
            <v-btn class="white--text" flat="flat" @click.native="diaShow = false">Close</v-btn>
          </v-toolbar>
        </v-card-row>
        <v-card-row>
          <app-kvtable :items="diaData"></app-kvtable>
        </v-card-row>
      </v-dialog>

    </v-card>
  </v-container>
</template>

<script>
  import KVTable from '@/components/KVTable'

  export default {
    name: 'datatable',
    props: {
      title: {
        type: String,
        default: 'Title'
      },
      headers: {
        type: Array,
        default: () => []
      },
      items: {
        type: Array,
        default: () => []
      },
      detailFunc: {
        type: Function,
        required: true
      }
    },
    components: {
      'app-kvtable': KVTable
    },
    data () {
      return {
        search: '',
        diaShow: false,
        diaTitle: '',
        diaData: []
      }
    },
    methods: {
      showModal (iid, event) {
        event.stopPropagation()
        this.diaTitle = iid
        console.log(this.detailFunc)
        this.detailFunc(iid).then(data => {
          let d = data[0]
          for (let k in d) {
            if (d.hasOwnProperty(k)) {
              this.diaData.push({ 'k': k, 'v': d[k] })
            }
          }
          this.diaShow = true
        })
      }
    },
    watch: {
      diaShow: function (val) {
        if (!val) {
          let self = this
          setTimeout(function () {
            self.diaTitle = ''
            self.diaData = []
          }, 500)
        }
      }
    }
  }
</script>
