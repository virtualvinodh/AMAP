<template>
  <div>
    <div class="icons" v-show="visibleIcons">
      <!-- <q-icon :name="disableChip ? 'lock outline' : 'lock open'" size="30px" @click.native="disableHandler" class="lock" /> -->
      <q-icon :name="visibility ? 'visibility' : 'visibility_off'" size="30px" @click.native="toggleVis" v-if="!loading"/>
      <q-icon :name="bBoxadd ? 'add_circle' : 'add_circle_outline'" size="30px" v-if="!loading"
        @click.native="addbBox" class="q-ml-md"/>
      <q-spinner-gears size="40px" color="primary" :style="{'visibility': !loading ? 'hidden' : ''}"/>
    </div>
    <q-chip tag pointing="left" :color="active ? 'green' : 'red'" :icon="icon">
     <label v-html="text"> </label>
    </q-chip>
  </div>
</template>

<script>
import {QChip, QIcon, QSpinnerGears} from 'quasar'

export default {
  props: ['action', 'active', 'loading', 'visibleIcons'],
  components: {
    QChip,
    QIcon,
    QSpinnerGears
  },
  computed: {
    icon: function () {
      if (this.action === 'segmentLine' || this.action === 'segmentHist' || this.action === 'segmentKraken') {
        return 'view headline'
      } else if (this.action === 'segmentChar') {
        return 'dashboard'
      } else if (this.action === 'textEntry') {
        return 'text fields'
      } else if (this.action === 'textGoogle') {
        return 'text fields'
      }
    },
    text: function () {
      if (this.action === 'segmentLine') {
        return 'Tesseract <br/> Lines'
      } else if (this.action === 'segmentChar') {
        return 'Tesseract <br/> Characters'
      } else if (this.action === 'textEntry') {
        return 'Manual Text'
      } else if (this.action === 'textGoogle') {
        return 'OCR Text'
      } else if (this.action === 'segmentHist') {
        return 'Histogram <br/> Lines'
      } else if (this.action === 'segmentKraken') {
        return 'Kraken <br/> Lines'
      } else if (this.action === 'templateMatch') {
        return 'Match <br/> Template'
      }
    }
  },
  methods: {
    toggleVis: function () {
      this.visibility = !this.visibility
      this.$emit('visibleToggle', this.visibility)
    },
    disableHandler: function () {
      this.disableChip = !this.disableChip
      this.$emit('disableChip', this.disableChip)
      console.log('I am here')
    },
    addbBox: function () {
      this.bBoxadd = !this.bBoxadd
      this.$emit('addbbox', this.bBoxadd)
    }
  },
  data () {
    return {
      visibility: true,
      disableChip: false,
      bBoxadd: false
    }
  }
}
</script>

<style scoped>
label {
  font-size:12px;
}
.icons {
  margin-left:25px;
}
</style>
