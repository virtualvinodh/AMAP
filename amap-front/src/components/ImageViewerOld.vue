<template>
  <!-- consider using vue animations for page flip/other effects -->
  <div>
    <q-toolbar color="primary">

    <v-touch @tap="demo" :tap-options="{taps: 2}">
    <q-btn flat round large>
      <q-icon name="photo_size_select_large" />
    </q-btn>
    </v-touch>

    <q-btn flat round large>
      <q-icon name="voicemail" />
    </q-btn>

    </q-toolbar>
    
    <canvas ref='c' id='c' width="600" height="500"></canvas>

  </div>    
</template>

<script>
  import Fabric from 'Fabric'
  import { QToolbar, QBtn, QIcon } from 'quasar'

  export default {
    mounted: function () {
      this.$refs.c.width = window.innerWidth
      this.$refs.c.height = window.innerHeight - 65 // offset for toolbar

      this.canvas = new Fabric.fabric.Canvas('c')

      this.loadImage('statics/manu-images/tibetan/BD00001V1.jpg')
      this.loadImage('statics/manu-images/tamil/1_B_44_22_.jpg')

      this.canvas.renderAll()
    },
    components: {
      QToolbar,
      QBtn,
      QIcon
    },
    methods: {
      loadImage: function (url) {
        var canvas = this.canvas
        Fabric.fabric.Image.fromURL(url, function (img) {
          img.scaleToWidth(300)
          canvas.add(img)
        })
      },
      demo: function (event) {
        console.log(event)
        alert(event)
      }
    },
    data () {
      return {
        canvas: ''
      }
    }
  }
</script>

<style>
canvas {border:1px solid #F23456;}
</style>
