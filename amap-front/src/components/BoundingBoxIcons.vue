<template>
    <div>
      {{coords.left}}
      {{coords.top}}
      {{coords.height}}
      {{coords.width}}

      <q-icon name="keyboard arrow left" :size="deleteIconSize" color="red" class="icon"/>
      <q-icon name="keyboard arrow right" :size="deleteIconSize" color="red" class="icon"/>
      <q-icon name="keyboard arrow up" :size="deleteIconSize" color="red" class="icon"/>
      <q-icon name="keyboard arrow down" :size="deleteIconSize" color="red" class="icon"/>
    </div>
</template>

<script>
import {QIcon} from 'quasar'

export default {
  props: ['coords'],
  components: {
    QIcon
  },
  computed: {
    colorLine: function () {
      if (typeof this['color'] === 'undefined') {
        return 'red'
      } else {
        return this.color
      }
    }
  },
  data () {
    return {}
  }
}
</script>

<style scoped>
.icon {
  position:absolute;
}
</style>
