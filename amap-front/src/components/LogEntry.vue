<template>
  <q-card inline style="width: 250px">
    <q-card-title>
      {{timestamp}}
    </q-card-title>
      <img :src="input" width="50px" class="q-ml-md q-mr-md">
      <q-icon name="forward" size="20px"/>
      <img :src="output" width="50px" class="q-ml-md q-mr-md">
    <q-card-main v-html="parsePars(parameters)">
    </q-card-main>
    <q-card-separator />
    <q-card-actions>
      <q-btn flat round dense icon="delete" @click="$emit('delete')"/>
      <q-btn flat round dense icon="redo" @click="$emit('rerun')"/>
    </q-card-actions>
  </q-card>
</template>

<script>
import {QCard, QCardTitle, QCardMain, QCardMedia, QCardSeparator, QCardActions} from 'quasar'
export default {
  // name: 'ComponentName',
  components: {
    QCard,
    QCardTitle,
    QCardActions,
    QCardMain,
    QCardMedia,
    QCardSeparator
  },
  props: ['input', 'output', 'timestamp', 'parameters', 'type'],
  data () {
    return {}
  },
  methods: {
    parsParsWordSpot: function (parameters) {

    },
    parsePars: function (parameters) {
      var parametersExpanded = ''
      var count = 1
      for (var i = 0; i < parameters.length; i++) {
        var par = parameters[i]
        if (par === 0) {

        }
        for (var proc in par) {
          parametersExpanded += count + '. ' + proc + '<br/>'
          count += 1

          for (var prop in par[proc]) {
            parametersExpanded += '\t' + prop + ' ' + par[proc][prop] + ' <br/>'
          }
          parametersExpanded += '\n\n'
        }
      }

      return parametersExpanded
    }
  }
}
</script>

<style>
</style>
