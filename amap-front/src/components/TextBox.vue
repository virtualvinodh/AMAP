<template>
  <div class="text">
    <q-editor v-model="model" :min-height="height + 'px'" :readonly="disability"
       :toolbar="!disability? [['bold', 'italic', 'strike', 'underline']] : []" :style="{'width': width + 'px', 'display': visibility? 'inherit' : 'none'}"/>
    </div>
</template>

<script>
import {QEditor} from 'quasar'

export default {
  // name: 'ComponentName',
  components: {
    QEditor
  },
  props: ['width', 'height', 'visibility', 'disability', 'text'],
  data () {
    return {
      model: this.text
    }
  }
}
</script>

<style scoped>
.text {
  opacity: 1;
}
</style>
