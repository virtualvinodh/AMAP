<template>

  <div>
    <div class="movable" :style="{left: dotCoords[1][0] + 20  + 'px', top: dotCoords[1][1] + 20 + 'px'}"> {{dist}} px </div>
    <div class="dot1 bg-grey-6" :style="{left: dotCoords[0][0]  + 'px', top: dotCoords[0][1] + 'px'}" v-touch-pan="moveDot1"> </div>
    <div class="dot2 bg-grey-6" :style="{left: dotCoords[1][0]  + 'px', top: dotCoords[1][1] + 'px'}" v-touch-pan="moveDot2"> </div>

    <con-line :line1 = "line1" class="movable" :style="{left: dotCoords[0][0]+10  + 'px', top: dotCoords[0][1]+10 + 'px'}"> </con-line>

  </div>
</template>

<script>
import conLine from '../components/conLine.vue'

export default {
  components: {
    conLine
  },
  data () {
    return {
      dotCoords: [
        [40, 40],
        [140, 40]
      ]
    }
  },
  computed: {
    line1: function () {
      return this.dotCoords[0].concat(this.dotCoords[1])
    },
    dist: function () {
      var dist = Math.sqrt((this.line1[0] - this.line1[2]) * (this.line1[0] - this.line1[2]) + (this.line1[1] - this.line1[3]) * (this.line1[1] - this.line1[3]))

      return Math.round(dist)
    }
  },
  methods: {
    moveDot1: function (event, index) {
      this.$set(this.dotCoords[0], 0, this.dotCoords[0][0] + event.delta.x)
      this.$set(this.dotCoords[0], 1, this.dotCoords[0][1] + event.delta.y)
    },
    moveDot2: function (event, index) {
      this.$set(this.dotCoords[1], 0, this.dotCoords[1][0] + event.delta.x)
      this.$set(this.dotCoords[1], 1, this.dotCoords[1][1] + event.delta.y)
    }
  }
}
</script>

<style scoped>
.dot1 {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  display: inline-block;
  position: absolute;
  display: inline-block;
}
.dot2 {
  height: 20px;
  width: 20px;
  border-radius: 50%;
  display: inline-block;
  position: absolute;
  display: inline-block;
}
.movable {
  position: absolute;
  display: inline-block;
  opacity: 0.8;
}
</style>
