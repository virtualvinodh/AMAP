<template>
  <div>
    <q-icon name="image" size="50px" class="icon" v-show="iconShow"/>
    <img :src="url" width="50px" v-show="!iconShow"/>
  </div>
</template>

<script>
import {QKnob, QIcon} from 'quasar'

export default {
  components: {
    QKnob,
    QIcon
  },
  props: ['url', 'iconShow', 'type'],
  data () {
    return {
    }
  }
}
</script>

<style scoped>
.icon{
  filter: opacity(0.3)
}
</style>
