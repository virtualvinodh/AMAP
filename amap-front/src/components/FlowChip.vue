<template>
  <div>
    <q-chip tag pointing="left" :color="colorName" :icon="iconName" :style="{'width': typeof widthk === 'undefined' ? '170px' : this.widthk + 'px'}">
     <label v-html="text" class="ellipsis-2-lines"> </label>
    </q-chip>
  </div>
</template>

<script>
import {QChip, QIcon} from 'quasar'

export default {
  props: ['text', 'icon', 'colorbg', 'widthk'],
  computed: {
    iconName: function () {
      if (typeof this.icon === 'undefined') {
        return 'format_paint'
      } else {
        return this.icon
      }
    },
    colorName: function () {
      if (typeof this.colorbg === 'undefined') {
        return 'orange'
      } else {
        return this.colorbg
      }
    }
  },
  components: {
    QChip,
    QIcon
  },
  data () {
    return {
    }
  }
}
</script>

<style>
div {
}
</style>
