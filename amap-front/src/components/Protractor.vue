<template>

  <div>
    <div class="movable" :style="{left: dotCoords[1][0] + 20  + 'px', top: dotCoords[1][1] + 20 + 'px'}"> {{angleDiff}}° </div>
    <div class="dot1 bg-grey-6" :style="{left: dotCoords[0][0]  + 'px', top: dotCoords[0][1] + 'px'}" v-touch-pan="moveDot1"> </div>
    <div class="dot2 bg-grey-10" :style="{left: dotCoords[1][0]  + 'px', top: dotCoords[1][1] + 'px'}" v-touch-pan="moveDot2"> </div>
    <div class="dot3 bg-grey-6" :style="{left: dotCoords[2][0]  + 'px', top: dotCoords[2][1] + 'px'}" v-touch-pan="moveDot3"> </div>

    <con-line :line1 = "line1" class="movable" :style="{left: dotCoords[0][0]+10  + 'px', top: dotCoords[0][1]+10 + 'px'}"> </con-line>
    <con-line :line1 = "line2" class="movable" :style="{left: dotCoords[1][0]+10  + 'px', top: dotCoords[1][1]+10 + 'px'}"> </con-line>

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
        [20, 0],
        [20, 100],
        [120, 100]
      ]
    }
  },
  computed: {
    line1: function () {
      return this.dotCoords[0].concat(this.dotCoords[1])
    },
    line2: function () {
      return this.dotCoords[1].concat(this.dotCoords[2])
    },
    angleDiff: function () {
      var angle1 = Math.atan2(this.line1[3] - this.line1[1], this.line1[2] - this.line1[0])
      var angle2 = Math.atan2(this.line2[3] - this.line2[1], this.line2[2] - this.line2[0])

      var result = (angle2 - angle1) * 180 / Math.PI

      if (result < 0) {
        result += 360
      }

      return Math.round(result - 180)
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
    },
    moveDot3: function (event, index) {
      this.$set(this.dotCoords[2], 0, this.dotCoords[2][0] + event.delta.x)
      this.$set(this.dotCoords[2], 1, this.dotCoords[2][1] + event.delta.y)
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
.dot3 {
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
.line {
}
</style>
