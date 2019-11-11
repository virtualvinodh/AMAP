<template>
  <div>
  <q-icon name="settings input hdmi" size="20px" class="plug" :color="lineColor"/>
  <q-knob
      size="80px"
      v-model="value"
      :min="min"
      :max="max"
      :step="step"
      :style="style"
      :disable="disable"
      >
      <div class="icon"><q-icon :name="name" size="30px"/> </div>
      <!-- it's not always percentage for everything -->
      <div class="value" v-if="property === 'hue-rotate'"> {{value}}° </div>
      <div class="value" v-else> {{value}}% </div>
    </q-knob> <!-- <q-icon :name="disableKnob ? 'lock' : 'lock open'" size="30px" @click.native="disableKnob = !disableKnob" class="lock" /> <br/> -->
    <label>{{property}}</label>

   </div>
</template>

<script>
import {QKnob, QIcon, QField} from 'quasar'

export default {
  components: {
    QKnob,
    QIcon,
    QField
  },
  props: ['active', 'disable', 'property', 'initValue', 'min', 'max', 'name'],
  mounted: function () {

  },
  computed: {
    lineColor: function () {
      if (this.active) {
        return 'green'
      } else {
        return 'red'
      }
    },
    style: function () {
      return {
        'padding-top': '20px',
        'border-left': '2px ' + 'solid ' + this.lineColor
      }
    }
  },
  watch: {
    value: function (val) {
      this.$emit('turned', val)
    }
  },
  data () {
    return {
      disableKnob: false,
      value: this.initValue,
      step: 1
    }
  }
}
</script>

<style scoped>
label {
  display: block;
  text-align: center;
  margin-left: -30px;
  font-size:12px;
}
.value {
  clear: both;
  bottom: -5px;
  position:absolute;
  font-size:12px;
}
.plug{
  position:absolute;
  left:-9px;
  top:-1px;
  z-index: 1
}
.lock {
  margin-left:-10px;
}
</style>
