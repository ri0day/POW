<template>
  <v-data-table
    :headers="headers"
    v-model="items"
    hide-actions
  >
    <template slot="items" scope="props">
      <td>
        <v-chip class="secondary secondary--text" label outline>{{ props.item.k }}</v-chip>
      </td>
      <td class="text-xs-right">{{ props.item.v }}</td>
    </template>
  </v-data-table>
</template>


<script>
  export default {
    name: 'kvtable',
    props: {
      items: {
        type: Array,
        default: () => []
      }
    },
    data () {
      return {
        headers: [
          { text: 'Key', value: 'k', left: true },
          { text: 'Value', value: 'v' }
        ]
      }
    }
  }
</script>
