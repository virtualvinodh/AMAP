<template>
  <div :class="loopActive ? 'knobs' : ''">
  <q-knob
      size="80px"
      v-model="valueKnob"
      :min="min"
      :max="max"
      :step="typeof step === 'undefined' ? 1 : step"
      @input="returnValues"
      :disable="loopActive"
      >
      <q-icon name="settings" size="30px" class="icon" />
      <div class="value"> {{valueKnob}} </div>
    </q-knob> <br/>
    <q-icon name="loop" size="40px" class="q-pl-md q-pa-sm"
        :color="loopActive ? '': 'grey'" @click.native="loopActivated" v-if="!loopHide"/>
    <br/>
    <div v-show="loopActive">
          <q-knob
      size="60px"
      class="iteration-knob"
      v-model="initIter"
      :min="min"
      :max="max"
      :step="typeof step === 'undefined' ? 1 : step"
      @input="returnValues"
      > </q-knob>
        <q-knob
      size="60px"
      class="iteration-knob"
      v-model="toIter"
      :min="min"
      :max="max"
      :step="typeof step === 'undefined' ? 1 : step"
      @input="returnValues"
      > </q-knob>
        <q-knob
      size="60px"
      class="iteration-knob"
      v-model="stepIter"
      :min="min"
      :max="max"
      :step="typeof step === 'undefined' ? 1 : step"
      @input="returnValues"
      ></q-knob>
      <br/>
    </div>
    <label v-if="typeof textOptions !== 'undefined'">{{property}} : <br/> {{textOptions[valueKnob]}}</label>
    <label v-else> {{property}} </label>

   </div>
</template>

<script>
import {QKnob, QIcon} from 'quasar'

export default {
  components: {
    QKnob,
    QIcon
  },
  props: ['value', 'min', 'max', 'property', 'textOptions', 'step', 'loopHide'],
  computed: {
  },
  watch: {
    valueKnob: function (val) {
    }
  },
  data () {
    return {
      valueKnob: this.value,
      loopActive: false,
      initIter: this.min,
      toIter: this.max,
      stepIter: typeof this.step === 'undefined' ? 1 : this.step
    }
  },
  methods: {
    loopActivated: function () {
      this.loopActive = !this.loopActive
      console.log('Loop has been activated ' + this.loopActive)
      if (this.loopActive) {
        this.returnValues()
      }
    },
    returnValues: function () {
      console.log('Emitting values')
      console.log(this.loopActive)
      if (typeof this.textOptions === 'undefined') {
        if (this.loopActive) {
          this.$emit('turned', this.property, this.valueKnob, [this.initIter, this.toIter, this.stepIter])
        } else {
          this.$emit('turned', this.property, this.valueKnob, this.loopActive)
        }
      } else {
        if (this.loopActive) {
          this.$emit('turned', this.property, this.textOptions[this.valueKnob], [this.initIter, this.toIter, this.stepIter])
        } else {
          this.$emit('turned', this.property, this.textOptions[this.valueKnob], this.loopActive)
        }
      }
    }
  }
}
</script>

<style scoped>
label {
  text-align:center;
  padding-top:-50px;
  padding-left:0px;
  text-align: center;
  font-size:10px;
  position:absolute;
}
.value {
  clear: both;
  top:53px;
  position:absolute;
  font-size: 12px;
}
.icon{
  position:absolute;
  top:15px;
  padding-bottom: 0px;
  z-index: 1
}
.loop-icon{
  position:inline;
  top:45px;
  left: 95px;
  padding-bottom: 0px;
  z-index: 0
}
.iteration-knob {
  position: inline-block;
}
.knobs {
  width:190px;
}
.flip-list-move {
  transition: transform 1s;
}
</style>
