<template>
  <div>
    <q-icon name="fitness center" size="60px"
        :color="!bookFix ? 'grey' : 'dark grey'"
        :class="!bookFix ? 'fix' : 'fixActive'"
        @click.native="changeStatus"/>
    <div :class="stackClass">
      <transition
        leave-active-class="move-leave-active"
        leave-to-class="move-leave-to"
        v-on:leave="stackClass = 'stack-3'"
        v-on:after-leave="afterLeave"
        v-on:enter="stackClass = 'stack-4'"
        mode="out-in">
          <m-image :url="original ? pagesorigCB[activePage] : pagesCB[activePage]" v-touch-swipe="changePage" :key="changePageActive" class="image"
            :width="width" :fix="false" :textBack="comments[activePage]" :colBooksIcon="true"
               @zoomin="zoomin"
               @zoomout="zoomout"
               @rotateright="rotateright"
               @rotateleft="rotateleft"
               @copypage="copyPageA" :tap-options="{taps: 2}"
               @up="changePageClick"
               @showoriginal="showOriginal"
               :showIcons = "showIcons"
            > </m-image>
      </transition>
    </div>
        <div class="stack-1">
          <transition
          leave-active-class="move-reverse-leave-active"
          leave-to-class="move-reverse-leave-to"
          mode="out-in">
            <m-image :url="original ? pagesorigCB[pilePage] : pagesCB[pilePage]" :key="returnPageActive" v-touch-swipe="returnPage" class="subpile"
                :style="{'z-index': pileZIndex}" v-if="pile" :fix="false" :width="width"
                :textBack="comments[pilePage]" :colBooksIcon="true"
               @zoomin="zoomin"
               @zoomout="zoomout"
               @rotateright="rotateright"
               @rotateleft="rotateleft"
               @up="detachPageClick"
               @down="returnPageClick"
               @showoriginal="showOriginal"
               @copypage="copyPageP" :tap-options="{taps: 2}"
               :showIcons = "showIcons"
                > </m-image>
          </transition>
       </div>
  </div>
</template>

<script>
import MImage from '../components/MImage.vue'

export default {
  // name: 'ComponentName',
  props: ['pages', 'width', 'comments', 'showIcons', 'pagesorig'],
  components: {
    MImage
  },
  data () {
    return {
      activePage: 0,
      pagesCB: JSON.parse(JSON.stringify(this.pages)),
      pagesorigCB: JSON.parse(JSON.stringify(this.pagesorig)),
      pilePage: 0,
      pileZIndex: 0,
      bookFix: false,
      fixColor: 'grey',
      pile: false,
      direction: '',
      stackClass: 'stack-4',
      changePageActive: false,
      returnPageActive: false,
      hideDetach: true,
      original: false,
      removedPages: []
    }
  },
  watch: {
    pages (oldV, newV) {
      this.pagesCB = JSON.parse(JSON.stringify(this.pages))
    },
    pagesorig (oldV, newV) {
      this.pagesorigCB = JSON.parse(JSON.stringify(this.pagesorig))
    }
  },
  methods: {
    copyPageA: function () {
      var url = this.original ? this.pagesorigCB[this.activePage] : this.pagesCB[this.activePage]
      this.$emit('copypage', url)
    },
    copyPageP: function () {
      var url = this.original ? this.pagesorigCB[this.pilePage] : this.pagesCB[this.pilePage]
      this.$emit('copypage', url)
    },
    showOriginal: function () {
      this.original = !this.original
      this.$emit('showoriginal', this.original)
    },
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
    detachPageClick: function () {
      var event = {}
      event.direction = 'up'

      this.returnPage(event)
    },
    changePageClick: function () {
      var event = {}
      event.direction = 'up'

      this.changePage(event)
    },
    returnPageClick: function () {
      var event = {}
      event.direction = 'down'

      console.log('I am here oo')

      this.returnPage(event)
    },
    demo: function () {
      console.log('moving collection pages one')
    },
    afterLeave: function (event) {
      this.pilePage = this.activePage - 1
      this.pile = true
      this.pileZIndex = 2
    },
    changePage: function (event) {
      console.log(event.direction)
      if (event.direction === 'up' && this.activePage !== this.pagesCB.length - 1) {
        this.changePageActive = !this.changePageActive
        this.direction = event.direction
        this.pileZIndex = 0
        this.activePage += 1

        this.$emit('pageFlipped', this.activePage)
      }
    },
    returnPage: function (event) {
      console.log(event.direction)
      if (event.direction === 'down') {
        this.activePage -= 1
        this.pilePage -= 1

        this.returnPageActive = !this.returnPageActive
        this.pileZIndex = 2

        if (this.pilePage === -1) {
          this.pile = false
        }

        this.$emit('pageFlipped', this.activePage)
      }
      if (event.direction === 'up') {
        this.$emit('detachpage', this.original ? this.pagesorigCB[this.pilePage] : this.pagesCB[this.pilePage])

        this.pagesCB.splice(this.pilePage, 1)
        this.pagesorigCB.splice(this.pilePage, 1)

        this.pilePage -= 1
        this.activePage -= 1
      }
    },
    changeStatus: function (event) {
      this.bookFix = !this.bookFix

      this.$emit('fixed', !this.bookFix)
    }
  }
}
</script>

<style scoped>
.move-leave-active {
  transition: all 0.25s ease-in;
}
.move-leave-to /* .fade-leave-active below version 2.1.8 */ {
  transform: translateY(-120%)
}
.move-reverse-leave-active {
  transition: all 0.25s ease-out;
}
.move-reverse-leave-to /* .fade-leave-active below version 2.1.8 */ {
  transform: translateY(110%)
}
.fix {
  position:absolute;
  top: -30px;
  left: -30px;
}
.fixActive {
  position:absolute;
  top: -30px;
  left: -30px;
  z-index: 10;
  text-shadow: 2px 2px grey
}
/* https://css-tricks.com/snippets/css/stack-of-paper/ : Vertical stack */;
.stack-4 {
  background: lightgrey;
  position:relative;
  box-shadow:
    /* The top layer shadow */
    0 -1px 1px rgba(0,0,0,0.15),
    /* The second layer */
    0 -10px 0 -5px #eee,
    /* The second layer shadow */
    0 -10px 1px -4px rgba(0,0,0,0.15),
     /* The third layer */
    0 -20px 0 -10px #eee,
    /* The third layer shadow */
    0 -20px 1px -9px rgba(0,0,0,0.15),
     /* The fourth layer */
    0 -30px 0 -15px #eee,
    /* The fourth layer shadow */
    0 -30px 1px -14px rgba(0,0,0,0.15);
}
.stack-3 {
  background: lightgrey;
  box-shadow:
    /* The second layer */
    0 -10px 0 -5px #eee,
    /* The second layer shadow */
    0 -10px 1px -4px rgba(0,0,0,0.15),
    /* The third layer */
    0 -20px 0 -10px #eee,
    /* The third layer shadow */
    0 -20px 1px -9px rgba(0,0,0,0.15);
}
.stack-1 {
  background: lightgrey;
  position: absolute;
  margin-top: -280%;
}
.subpile {
  position: relative;
  z-index: 0;
}
.image {
  position:relative;
  z-index: 1;
}
</style>
