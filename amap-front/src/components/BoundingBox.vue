<template>
    <div class="box" :style="{border: '1px solid ' + colorLine}">
    </div>
</template>

<script>
import {QIcon} from 'quasar'

export default {
  props: ['color'],
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
.box {
  display: inline-block;
  position: absolute;
  filter: blur(0.5px);
}
.icon-close {
  margin-left: -15px;
  margin-top: -20px;
  text-align: left;
}
.icon-close2 {
  margin-left: -15px;
  margin-top: -20px;
  text-align: right;
}
</style>
