<template>
  <div class="touch-surface">
    <q-spinner-gears size="40px" class="tv-icon" color="primary" v-show="progress" />
    <div class="chip">
    <q-chip tag pointing="left" color="brown" icon="repeat" style="width: 125px">
      <label class="ellipsis-2-lines"> {{action}} </label>
    </q-chip>
  </div>
  </div>
</template>

<script>
import FlowKnob from './FlowKnob.vue'
import FlowChip from './FlowChip.vue'
import {QIcon, QSpinnerGears, QPopover, Ripple, QChip} from 'quasar'

export default {
  components: {
    FlowKnob,
    FlowChip,
    QIcon,
    QSpinnerGears,
    QPopover,
    QChip
  },
  directives: {
    Ripple
  },
  props: ['action', 'progress'],
  data () {
    return {
      settingsVis: true,
      parameters: {},
      previewWindow: false
    }
  },
  methods: {
    demo: function () {
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
