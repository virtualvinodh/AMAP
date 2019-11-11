<template>
    <div>
    <!-- <svg width="1500" height="1500">
      <line :x1="line1[0]" :y1="line1[1]" :x2="line1[2]" :y2="line1[3]" stroke="red"/>
      <line :x1="line2[0]" :y1="line2[1]" :x2="line2[2]" :y2="line2[3]" stroke="red"/>
    </svg> -->
    <div :style="line1Style" class="line"></div>
    </div>
</template>

<script>
export default {
  created: function () {
    console.log('I am here')
  },
  props: ['line1'],
  data () {
    return {}
  },
  computed: {
    line1Style: function () {
      var dist = Math.sqrt((this.line1[0] - this.line1[2]) * (this.line1[0] - this.line1[2]) + (this.line1[1] - this.line1[3]) * (this.line1[1] - this.line1[3]))
      var angle = Math.atan2(this.line1[3] - this.line1[1], this.line1[2] - this.line1[0]) * 180 / Math.PI
      return {
        transform: 'rotate(' + angle + 'deg)',
        width: dist + 'px'
      }
    }
  }
}
</script>

<style scoped>
.line {
transform-origin: 0 100%;
height: 1px; /* Line width of 3 */
background: grey; /* Black fill */
}
</style>
