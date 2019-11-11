<template>
  <div>
  <div class="container" v-touch-swipe="make3D">
    <transition enter-active-class="animated fadeIn"
      leave-active-class="animated fadeOut">
      <div v-if="threed" class="cube pers650" key="thrd" >
        <img src="../statics/1R_BW.jpg" class="other2" :style="{transform: 'rotateY(70deg) translateZ(' + order['bw'] * 100 + 'px)'}" @click="bringFront('bw')" />
        <img src="../statics/1R.jpg" class="gray" :style="{transform: 'rotateY(70deg) translateZ(' + order['gray'] * 100 + 'px)'}" @click="bringFront('gray')" />
        <img src="../statics/1R.jpg" class="sepia" :style="{transform: 'rotateY(70deg) translateZ(' + order['sepia'] * 100 + 'px)'}" @click="bringFront('sepia')" />
        <img src="../statics/1R.jpg" class="other" :style="{transform: 'rotateY(70deg) translateZ(' + order['original'] * 100 + 'px)'}" @click="bringFront('original')" />
      </div>
      <div v-else class="cube pers650" key="normal">
        <img src="../statics/1R.jpg" v-show="visibility['original']"/>
        <img src="../statics/1R_BW.jpg" v-show="visibility['bw']"/>
        <img src="../statics/1R.jpg" class="sepia" v-show="visibility['sepia']"/>
        <img src="../statics/1R.jpg" class="gray" v-show="visibility['gray']"/>
      </div>
    </transition>
  </div>
</div>
</template>

<script>
export default {
  // name: 'ComponentName',
  // other2 bottom top other
  data () {
    return {
      threed: false,
      order: {
        'original': 3,
        'sepia': 2,
        'gray': 1,
        'bw': 0
      }
    }
  },
  computed: {
    visibility: function () {
      var vis = {}
      vis['original'] = this.order['original'] === 3
      vis['bw'] = this.order['bw'] === 3
      vis['sepia'] = this.order['sepia'] === 3
      vis['gray'] = this.order['gray'] === 3

      return vis
    }
  },
  methods: {
    make3D: function (event) {
      console.log(event)
      if (event.direction === 'right') {
        this.threed = true
      } else if (event.direction === 'left') {
        this.threed = false
      }
    },
    bringFront: function (img) {
      this.order[this.getKeyByValue(this.order, 3)] = this.order[img]
      this.order[img] = 3
    },
    getKeyByValue: function (object, value) {
      return Object.keys(object).find(key => object[key] === value)
    }
  }
}
</script>

<style scoped>
img {
  display: block;
  position: absolute;
  width:200px;
  height:300px;
}
.pers650 {
  perspective: 3500px;
}

.container {
  margin: 100px 100px 100px 100px;
}

.cube {
  width: 100%;
  height: 100%;
  backface-visibility: visible;
  perspective-origin: 250% 250%;
  transform-style: preserve-3d;
}

.sepia {
  filter:sepia(100%);
}

.gray {
  filter:grayscale(100%);
}

.other {
}

.other2 {
}
</style>
