<template>
<div>
    <!-- probably make below as absolute -->
    <q-icon name="fitness center" size="50px"
        :color="!bookFix ? 'grey' : 'dark grey'"
        :class="!bookFix ? 'fix' : 'fixActive'"
        @click.native="changeStatus" v-if="fix"/>
      <v-touch  @swipeleft="changeSide" @swiperight="changeSide" :swipe-options="{velocity: 1}"
        @tap="$emit('copypage')" :tap-options="{taps: 2}"
      >
      <div>
        <transition
          :enter-active-class="enterActive"
          :leave-active-class="leaveActive"
          mode="out-in"
        >
          <div :key="change">
            <img :src="url" v-show="!backSide"/>
            <div v-show="backSide">
                  <img :src="url" v-show="backSide" ref="man"
                        :style="{opacity: 1, position: 'absolute', filter: 'blur(3px)', transform: 'scaleX(-1)'}" />
                  <q-editor v-model="backText" :min-height="(heightScale - 38) + 'px'"
                     :style="{opacity: 0.7}" :toolbar="[['bold', 'italic', 'strike', 'underline']]"/>
            </div>
          </div>
        </transition>
      </div>
      <span v-if="original"> Original Image </span>
    </v-touch>
    <div class="icons" v-if="showIcons">
      <q-icon name="zoom in" size="20px" @click.native="zoomin" class="q-mr-sm"/> <br/>
      <q-icon name="zoom out" size="20px" @click.native="zoomout" class="q-mr-sm"/> <br/>
      <q-icon name="rotate left" size="20px" @click.native="rotateleft" class="q-mr-sm"/> <br/>
      <q-icon name="rotate right" size="20px" @click.native="rotateright" class="q-mr-sm"/> <br/>
      <q-icon name="flip" size="20px" @click.native="changeSide" class="q-mr-sm"/> <br/>
      <span v-if="colBooksIcon"> <q-icon name="keyboard arrow up" size="20px" @click.native="$emit('up')" class="q-mr-sm"/><br/></span>
      <span v-if="colBooksIcon"> <q-icon name="keyboard arrow down" size="20px" @click.native="$emit('down')" class="q-mr-sm"/> <br/></span>
      <q-icon name="gps fixed" @click.native="showOriginal" size="20px" class="q-mr-sm"/> <br/>
    </div>
</div>
</template>

<script>
import {QIcon, QEditor} from 'quasar'

export default {
  props: ['url', 'width', 'fix', 'textBack', 'colBooksIcon', 'showIcons'],
  components: {
    QIcon,
    QEditor
  },
  watch: {
    backSide: function () {
      if (typeof this.$refs['man'] !== 'undefined') {
        var heightImg = this.$refs.man.naturalHeight
        var widthImg = this.$refs.man.naturalWidth

        if (typeof this.backText === 'undefined') {
          console.log('I am here')
          this.backText = this.textBack
        }

        console.log(this.width)
        console.log(heightImg)
        console.log(widthImg)
        this.heightScale = heightImg / (widthImg / this.width)
      }
    }
  },
  data () {
    return {
      backText: this.textBack,
      change: true,
      heightScale: 100,
      bookFix: false,
      backSide: false,
      original: false,
      enterActive: '',
      leaveActive: ''
    }
  },
  methods: {
    zoomin: function () {
      this.$emit('zoomin')
    },
    zoomout: function () {
      this.$emit('zoomout')
    },
    rotateleft: function () {
      this.$emit('rotateleft')
    },
    rotateright: function () {
      this.$emit('rotateright')
    },
    changeStatus: function (event) {
      this.bookFix = !this.bookFix

      this.$emit('fixed', !this.bookFix)
    },
    changeSide: function (event) {
      this.enterActive = 'animated flipInY'
      this.leaveActive = 'animated flipOutY'

      this.backSide = !this.backSide
      this.change = !this.change

      console.log('Side changed')

      this.$emit('sidechanged', this.backSide)
    },
    showOriginal: function (event) {
      this.enterActive = 'animated fadeIn'
      this.leaveActive = 'animated fadeOut'

      this.original = !this.original
      this.change = !this.change

      console.log('Show original')

      this.$emit('showoriginal', this.original)
    }
  }
}
</script>

<style scoped>
img {
  width: 100%;
  perspective: 10px;
}
.backside {
  background-color: #f8f5de;
  background-image: linear-gradient(to right, rgba(255,210,0,0.4), rgba(200, 160, 0, 0.1) 11%, rgba(0,0,0,0) 35%, rgba(200, 160, 0, 0.1) 65%);
  box-shadow: inset 0 0 75px rgba(255,210,0,0.3), inset 0 0 20px rgba(255,210,0,0.4), inset 0 0 30px rgba(220,120,0,0.8);
  opacity: 0.5
}
.icons {
  position: absolute;
  left: -25px;
  bottom: 0px;
}
.fix {
  position: absolute;
  margin-left: -30px;
}
.fix {
  position: absolute;
  margin-left: -30px;
}
.fixActive {
  position: absolute;
  margin-left: -30px;
  z-index: 10;
  text-shadow: 2px 2px grey
}
</style>
