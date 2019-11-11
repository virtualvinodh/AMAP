<template>
  <div class="touch-surface">
    <q-icon :name="'flash_on'" size="50px" color="grey" class="tv-icon" @click.native="activateLoop" v-ripple
       v-show="loopActive && !progress"/>
    <flow-chip :text="processing" class="chip"></flow-chip>
    <q-icon name="tv" size="50px" color="grey" class="tv-icon" v-show="preview && !loopActive" @click="previewWindow = true" v-ripple>
      <q-popover v-model="previewWindow"> <img :src="previewUrl" class="preview" @click="previewWindow = false" /> </q-popover>
    </q-icon>
    <q-icon name="error" size="40px" color="red" class="tv-icon" v-show="error" v-ripple> </q-icon>
    <q-spinner-gears size="40px" class="tv-icon" color="primary" v-show="progress" />
    <q-icon name="settings applications" size="50px" :color="settingsVis? 'grey' : 'black'" class="settings-icon" @click.native="settingsVis = !settingsVis"/>
    <q-icon name="settings input composite" size="30px" class="connection-icon" :color="active? 'green' : 'red'"/>
    <transition
      enter-active-class="animated fadeInUp"
      leave-active-class="animated fadeOutDown">
      <div class="container" v-show="settingsVis" v-if="controls.length > 0">
        <div v-for="(control, index) in controls"
                   v-bind="control"
                   :key="'control' + index + control.value">
          <span v-show="toggle[index]">
          <flow-knob v-bind="control" @turned="knobTurned(...arguments)" :ref="'controls'+index"> </flow-knob> <br/> <br/>
          </span>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import FlowKnob from './FlowKnob.vue'
import FlowChip from './FlowChip.vue'
import {QIcon, QSpinnerGears, QPopover, Ripple} from 'quasar'

export default {
  components: {
    FlowKnob,
    FlowChip,
    QIcon,
    QSpinnerGears,
    QPopover
  },
  directives: {
    Ripple
  },
  created: function () {
    var parameters = {}
    for (var i = 0; i < this.controls.length; i++) {
      if (typeof this.controls[i].textOptions === 'undefined') {
        parameters[this.controls[i].property] = {'value': this.controls[i].value, 'loop': false}
      } else {
        parameters[this.controls[i].property] = {'value': this.controls[i].textOptions[this.controls[i].value], 'loop': false}
      }
    }
    this.parameters = Object.assign({}, this.parameters, parameters)

    var ob = {}

    for (i = 0; i < this.controls.length; i++) {
      if (typeof this.controls[i]['dependant'] === 'undefined') {
        this.toggle[i] = true
        ob['type'] = this.controls[i].property
        if (typeof this.controls[i].textOptions === 'undefined') {
          ob['value'] = this.controls[i].value
        } else {
          ob['value'] = this.controls[i].textOptions[this.controls[i].value]
        }
      }
    }

    console.log(ob)

    for (i = 0; i < this.controls.length; i++) {
      if (typeof this.controls[i]['dependant'] !== 'undefined') {
        if (typeof this.controls[i].textOptions === 'undefined') {
          this.toggle[i] = this.controls[i].dependant[0] === ob['type'] && this.controls[i].dependant[1] === ob['value']
        } else {
          this.toggle[i] = this.controls[i].dependant[0] === ob['type'] && this.controls[i].dependant[1] === this.controls[i].textOptions[ob['value']]
        }
      }
    }

    console.log('The toggles are')

    console.log(this.toggle)
  },
  computed: {
    loopActive: function () {
      var loop = false
      for (var prop in this.parameters) {
        loop = loop || this.parameters[prop]['loop']
      }
      return loop
    }
  },
  props: ['active', 'processing', 'preview', 'progress', 'previewUrl', 'controls', 'error'],
  data () {
    return {
      settingsVis: true,
      parameters: {},
      previewWindow: false,
      toggle: []
    }
  },
  watch: {
    parameters: function () {
      console.log('here')
      if (!this.loopActive) {
        this.$emit('updated', {'parameters': this.parameters, 'loopExists': false, 'loopActive': this.loopActive})
      } else {
        this.$emit('changed', {'parameters': this.parameters, 'loopExists': false, 'loopActive': this.loopActive})
      }
    }
  },
  methods: {
    demo: function () {
    },
    knobTurned: function (key, value, loop) {
      this.parameters[key] = {'value': value, 'loop': loop}
      console.log('The turned parameters are: ')
      console.log(this.parameters)
      this.parameters = Object.assign({}, this.parameters, this.parameters)

      for (var i = 0; i < this.controls.length; i++) {
        if (typeof this.controls[i]['dependant'] !== 'undefined' && this.controls[i].dependant[0] === key) {
          var show = this.controls[i].dependant[1] === value
          this.$set(this.toggle, i, show)
        }
      }
    },
    activateLoop: function () {
      this.$emit('updated', {'parameters': this.parameters, 'loopExists': true, 'loopActive': this.loopActive})
    }
  }
}
</script>

<style scoped>
.tv-icon {
  position: absolute;
  margin-left: 65px;
  margin-top: -3px;
}
.settings-icon {
  position: absolute;
  margin-left: 65px;
  margin-top: 94px;
}
.connection-icon {
  position:absolute;
  margin-top: 71px;
  margin-left:75px;
}

.chip {
  display: inline-block;
  position:absolute;
  margin-top: 40px
}
.knob {
  display: inline-block;
}
.container {
  margin-left:30px;
  margin-top:137px;
  display:inline-block;
  position:absolute;
  padding-left: 5px;
  padding-right: 5px;
  padding-top: 5px;
  padding-bottom:20px;
  border: 3px solid orange;
}
.touch-surface {
  width: 240px;
  height: 50px;
}
.preview {
  width: 200px;
}

</style>
