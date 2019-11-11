<template>
  <div class="touch-surface">
    <q-icon :name="'flash_on'" size="50px" color="grey" class="tv-icon" @click.native="activateItem" v-ripple
       v-show="!progress"/>
    <flow-chip :text="processing" :icon="iconName" class="chip"></flow-chip>
    <q-spinner-gears size="40px" class="tv-icon" color="primary" v-show="progress" />
    <q-icon name="settings applications" size="50px" :color="settingsVis? 'grey' : 'black'" class="settings-icon" @click.native="settingsVis = !settingsVis"/>
    <q-icon name="settings input composite" size="30px" class="connection-icon" :color="active? 'green' : 'red'"/>
    <transition
      enter-active-class="animated fadeInUp"
      leave-active-class="animated fadeOutDown">
      <div class="container" v-show="settingsVis" v-if="controls.length > 0">
        <div v-for="(control, index) in controls"
                   v-bind="control"
                   :key="'control' + index">
          <span v-show="toggle[index]">
          <flow-knob :loopHide="true" v-bind="control" @turned="knobTurned(...arguments)" :ref="'controls'+index"> </flow-knob><br/>
        </span>
        </div>
      </div>
    </transition>
    <transition
      enter-active-class="animated fadeInUp"
      leave-active-class="animated fadeOutDown">
      <div class="container2" v-show="settingsVis">
        <div v-for="(connectImage, index) in connectImages"
           :key="index">
          <connect-image  v-bind="connectImage" @click.native="selectImages(index)"
            :style="resultStyles[index]" v-ripple> </connect-image>
          <div v-show="typeof results[index] !== 'undefined'" class="label">{{results[index]}}{{resultText}} </div>
         </div>
      </div>
    </transition>
  </div>
</template>

<script>
import FlowKnob from './FlowKnob.vue'
import ConnectImage from './ConnectImage.vue'
import FlowChip from './FlowChip.vue'
import {QIcon, QSpinnerGears, QPopover, Ripple} from 'quasar'

export default {
  components: {
    FlowKnob,
    FlowChip,
    ConnectImage,
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
        parameters[this.controls[i].property] = this.controls[i].value
      } else {
        parameters[this.controls[i].property] = this.controls[i].textOptions[this.controls[i].value]
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

    console.log(this.parameters)
  },
  computed: {
    resultStyles: function () {
      var style = {}
      for (var key in this.results) {
        var perc = parseInt(this.results[key]) / 100
        var bord1 = (2) + 'px'
        var bord2 = (1) + 'px'
        style[key] = {'box-shadow': bord1 + ' ' + bord1 + ' ' + bord2 + ' ' + this.percentageToHsl(perc, 0, 120)}
      }
      return style
    },
    resultText: function () {
      if (this.type === 'identifyWriters') {
        return '% likely'
      } else if (this.type === 'matchTemplates') {
        return ' matches'
      }

      return ''
    },
    iconName: function () {
      switch (this.type) {
        case 'identifyWriters':
          return 'fingerprint'
        case 'matchTemplates':
          return 'find_in_page'
        default:
          return 'format_paint'
      }
    }
  },
  props: ['active', 'processing', 'progress', 'controls', 'connectImages', 'activeItem', 'results', 'type'],
  data () {
    return {
      settingsVis: true,
      parameters: {},
      toggle: []
    }
  },
  methods: {
    activateItem: function (index) {
      this.parameters['known'] = this.connectImages
      // console.log('Emitting this known images')
      // console.log(this.parameters['known'])
      this.$emit('item_active', this.parameters)
    },
    percentageToHsl: function (percentage, hue0, hue1) {
      var hue = (percentage * (hue1 - hue0)) + hue0
      return 'hsl(' + hue + ', 100%, 50%)'
    },
    selectImages: function (index) {
      this.$emit('select_image', index)
      this.clicked = true
    },
    knobTurned: function (key, value) {
      this.parameters[key] = value
      this.parameters = Object.assign({}, this.parameters, this.parameters)

      for (var i = 0; i < this.controls.length; i++) {
        if (typeof this.controls[i]['dependant'] !== 'undefined' && this.controls[i].dependant[0] === key) {
          var show = this.controls[i].dependant[1] === value
          this.$set(this.toggle, i, show)
        }
      }
      console.log(this.toggle)

      this.parameters['known'] = this.connectImages

      console.log('I am emitting this')

      this.$emit('parameters_change', this.parameters)
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
  margin-left:10px;
  margin-top:137px;
  display:inline-block;
  position:absolute;
  padding-left: 5px;
  padding-right: 5px;
  padding-top: 5px;
  padding-bottom:20px;
  border: 3px solid orange;
}
.container2 {
  margin-left:105px;
  margin-top:137px;
  display:inline-block;
  position:absolute;
  padding-left: 5px;
  padding-right: 5px;
  padding-top: 5px;
  padding-bottom:20px;
  border: 3px solid orange;
}
.borderdot {
  border: 2px dotted red;
}
.touch-surface {
  width: 243px;
  height: 100px;
}
.preview {
  width: 200px;
}
.label {
  margin-top:3px;
  font-size: 10px;
  margin-botto:5px;
}

</style>
