<template>
  <!-- consider using vue animations for page flip/other effects -->
  <!-- Look into provide more physical tools like set squares etc -->
  <!-- read the feature sets -->
  <!-- Add an ebook binder and things like that -->
  <!-- The ability to choose directions for the virtual book binder -->
  <!-- zooming in and zooming out -->
  <!-- The ability to lock measurements for angles and rulers -->
  <!-- Display Scaling/Title as properties of the image 
e.g Scaling 2.3, Tilt 0 degrees etc.
  -->
  <!-- Keep track of multiple instruments -->
  <!-- using pins and glues to bind bits of documents -->
  <!-- cut using scissors/blades -->
  <!-- consider using physics engine -->
  <!-- Fix Protractor angle -->
  <!-- Label lines, segmented things -->
  <!-- Allow people to label and select things -->
  <!-- Fix clipping of images -->
  <!-- Restructure bounding boxes -->
  <!-- bounding boxes -> ReferenceImage -> Type -> List --> 
  <!-- use the concept of sticky tags for the image for segmenation and stuff -->
  <!-- allow user crop -->
  <!-- Fix image clipping -->
  <!-- load the images temporarily in the server -->
  <!-- Think about locks to lock the setting -->
  <!-- How to copy settings: Search for a metaphor -->
  <!-- group knobs together -->
  <!-- Selection -->
  <!-- Lock icons for the knobs -->
  <!-- Look into ivolver -->
  <!-- Created drawers etc to hold the knobs/rulers etc -->
  <!-- display metrics such as line count, glyph count etc -->
  <!-- Fix CarbonCopy -->
  <!-- Fix scaling images/knobs -->
  <!-- Fix cropping -->
  <!-- Thnk about a view portig for viewing things -->
  <!-- Add cropping of images -->
  <!-- Accept/Edit automatic suggestions -->
  <!-- ordering of knobs and chips. How to decide the order -->
  <!-- Chips and then sttings or vice versa -->
  <!-- imageRef and clipImage : same behavior or different -->

  <!-- piling and organizing images -->
  <!-- compling them to virtual books -->
  <!-- etc etc -->
  <!-- pins to fix, piling, taking notes -->
  <!-- reverse side scrippling -->
  <!-- folding -->
  <!-- customg action chips -->
  <!-- custom layers -->
  <!-- cannot switch of bounding boxes while connecting lines are shown.. fix -->
  <!-- above means you cannot disconnect the chip -->
  <!-- cut images, fold images -->
  <!-- allow transcription of sgemented section, lines, characters -->
  <!-- And the ablilty to switch bwetween the images and the transcription inline in the main image -->
  <!-- Fix scale with touch point to extend it -->
  <!-- Add property tings to show the scaling, etc, tings applied etc -->
  <!-- Toggle switch to  turn of/turn on things -->
  <!-- group icons -->
  <!-- Fold and cut things -->
  <!-- Turn on/off view of individual flowcharts --> <!-- add visibility icons --> <!-- and group and hide -->
  <!-- only one flowchart maybe visible -->
  <!-- but multiple actionchips/annoataions may be visible -->

  <!-- For demo show protractor and scale as well and copying -->
  <!-- use four fingers to bring it back up -->
  <!-- and long press to send it back -->
  <!-- Send delete request after things flow -->
  <!-- Send delete request for the input image -->
  <!-- Todo select highlight and stuff -->
  <!-- convert between diva and my services -->
  <!-- have different modes basic/advanced -->
  <!-- sit with humanities / know about their requirements -->
  <!-- Talk to NETamil people about the project -->
  <!-- implement segmentation things -->
  <!-- integrate hussein's code -->
  <!-- how to visualize sift and huseein's code -->
  <!-- implement a left toolbar/drawer things -->
  <!-- implement piling, 3D piling and stuff -->
  <!-- combining manuscripts -->
  <!-- impleent folding -->
  <!-- implement image procesing things to applying the stuff to copied segments -->
  <!-- add icons for zooming, rotating, moving etc -->
  <!-- 'inputImage': collection + '/vinodh.jpg' --> <!-- remove hard coding of image extensions -->
  <!-- check if jpg is not hard encoded in the code -->

  <div>
    <q-toolbar color="primary">

    <input type="file" @change="uploadLocalImageM" ref="localUpload" style="display:none"/>

    <q-btn flat round large @click="addLocalImageM">
      <q-icon name="add_circle" /> <label> Image </label>
    </q-btn>

    <q-btn flat round large @click="addRuler">
      <q-icon name="straighten" /> <label> Dist </label>
    </q-btn>      

    <q-btn flat round large @click="addProtractor">
      <q-icon name="aspect_ratio" /> <label> Angle </label>
    </q-btn>  

    <q-btn flat round large @click="toggleconLines">
      <q-icon name="line_style" /> <label> Toggle </label>
    </q-btn>     

    </q-toolbar>

    <!-- Single page manuscript images -->
    <v-touch @click.right="$refs.ctxMenu.open($event, {ref:'imagesM-'+index})" 
             @pan="moveN" @pinch="scaleN" @rotate="rotateN"
             :rotate-options="{ pointers: 3 }"
             v-for="(imageM, index) in imagesM" :key="'imagesM-'+index">      
      <m-image class="movable" :id="'imagesM-'+index"
               :ref="'imagesM'+index" 
               :url="imageM.url" 
               :style="[imagesMStyles[index], settingKnobsTransforms['imagesM'+index]]"
              >
      </m-image>    
    </v-touch> 
    <v-touch @pan="moveN" @pinch="scaleN" @rotate="rotateN"
             :rotate-options="{ pointers: 3 }"
             v-for="(ruler, index) in rulers" :key="'rulers-'+index">

      <ruler class="movable" :id="'rulers-'+index" 
               :width="ruler.width" :tilt="ruler.tilt"
               :style="rulersStyles[index]">
      </ruler>

    </v-touch>

    <v-touch @pan="moveN" @pinch="scaleN" @rotate="rotateN"
             :rotate-options="{ pointers: 3 }"
             v-for="(protractor, index) in protractors" :key="'protractors-'+index"
             :style="imagesMCropStyles[index]">

      <protractor class="movable" :id="'protractors-'+index" 
               :angleTop="protractor.armAngles[0]"
               :angleBot="protractor.armAngles[1]"
               :style="[protractorsStyles[index]]">
      </protractor>

    </v-touch> 

    <!-- calculate scaling before using pinchingg -->
    <!-- how to think about it -->
    <v-touch @tap="copyImage" :tap-options="{taps: 2}"
             v-for="(bBox, index) in boundingBoxes"
             :key="'boundingBoxes'+index">
      <!-- Relative Position for Ripple effect -->
      <bounding-box :style="boundingBoxesStyles[index]" 
                    :id="'boundingBoxes-'+index" 
                    :ref="'boundingBoxes-'+index" 
                    v-ripple>     
      </bounding-box>
      
    </v-touch> 

    <v-touch @pan="moveN" @pinch="scaleN" @rotate="rotateN"
             :rotate-options="{ pointers: 3 }"
             v-for="(imageMCrop, index) in imagesMCrop" :key="'imagesMCrop-'+index">      
      <m-image class="movable" :id="'imagesMCrop-'+index"
               :ref="'imagesMCrop'+index" 
               :url="imageMCrop.url" :style="imagesMCropStyles[index]">
      </m-image>
    </v-touch>

    <con-Line v-for="(lineCon, index) in linesCon" :key="'linesCon-'+index"
              :line1="lineCon.line1" :line2="lineCon.line2" class="movable"
              :style="linesConStyles[index]" v-if="toggleLinesCon">
    </con-Line> 

    <!-- <q-spinner-gears color="secondary" :size="60" /> -->
    <v-touch @pan="moveN" @click.right.native.prevent="disconnectComp" 
             v-for="(settingKnob, index) in settingKnobs"
             :key="'settingKnob-'+index"
             :ref="'settingKnobsTouch'+index">
      <knob-setting v-bind="settingKnob"
                    :ref="'settingKnobs'+index"
                    :id="'settingKnobs-'+index"
                    :disable="settingKnob.disable"
                    :style="settingKnobsStyles[index]"
                    @turned="knobTurned(index,$event)"
                    class="movable"
                    > 
      </knob-setting>
    </v-touch>

    <v-touch @pan="moveN" @click.right.native.prevent="disconnectComp"
             v-for="(chipAction, index) in chipsAction"
             :key="'chipAction-'+index"
             :ref="'chipsActionTouch'+index" class="touch">
      <action-chip v-bind="chipAction"
                   :id="'chipsAction-'+index"
                   :ref="'chipsAction'+index"
                   :style="chipsActionStyles[index]"
                   @visibleToggle="chipsActionToggle(index, 'visibility')"
                   class="movable"
                   >
      </action-chip>
    </v-touch>

    <v-touch @pan="moveN"
             v-for="(actionFlow, index) in actionFlows"
             :key="'actionFlow-'+index"
             :ref="'actionFlowsTouch'+index">
      <flow-action v-bind="actionFlow"
                   :id="'actionFlows-'+index"
                   :ref="'actionFlows'+index"
                   :style="actionFlowsStyles[index]"
                   @updated="flowActionUpdated(index, $event)"
                   class="movable"
                   >
      </flow-action>
    </v-touch>

    <!-- <carbon-copy :style="{left: '200px', top: '300px', height: '400px', width: '400px', position: 'absolute', 'z-index': 200}"> </carbon-copy> -->
    <!-- Creating a pseduomanuscript with bits and pieces from everything else -->

    <context-menu id="context-menu" ref="ctxMenu" @ctx-open="onCtxOpen($event,'hello')">
      <li @click="segmentImagesM(0)">Block Segmentation</li>
      <hr/>
      <li @click="segmentImagesM(1)">Par Segmentation</li>
      <hr/>      
      <li @click="segmentImagesM(2)">Line Segmentation</li>
      <hr/>      
      <li @click="segmentImagesM(3)">Word Segmentation</li>
      <hr/>
      <li @click="segmentImagesM(4)">Symbol Segmentation</li>
      <hr/>
      <li @click="clearBoundingBoxes">Clear</li>      
    </context-menu>

    <q-toolbar color="primary" class="absolute-bottom">

      <q-btn flat round large id="brightness" class="stationary">
        <q-icon name="settings brightness" size="50px" color="orange"/>
        <q-tooltip> Image Settings </q-tooltip>
      </q-btn>      

    <v-touch @pan="attachSettingKnobs">
      <q-btn flat round large id="brightness" class="stationary">
        <q-icon name="brightness_low"/>
        <q-tooltip> Brightness </q-tooltip>
      </q-btn>
    </v-touch>

    <v-touch @pan="attachSettingKnobs">
      <q-btn flat round large id="contrast" class="stationary">
        <q-icon name="brightness_medium" /> 
        <q-tooltip> Contrast </q-tooltip>
      </q-btn>
    </v-touch>

    <v-touch @pan="attachSettingKnobs">
      <q-btn flat round large id="grayscale" class="stationary">
        <q-icon name="format_color_fill" /> 
        <q-tooltip> Greyscale </q-tooltip> 
      </q-btn>
    </v-touch>

    <v-touch @pan="attachSettingKnobs">
      <q-btn flat round large id="invert" class="stationary">
        <q-icon name="invert_colors" /> 
        <q-tooltip> Invert Colors </q-tooltip>
      </q-btn>
    </v-touch>    

    <v-touch @pan="attachSettingKnobs" id="opacity">
      <q-btn flat round large id="opacity" class="stationary">
        <q-icon name="opacity" id="opacity"/> 
        <q-tooltip> Opacity </q-tooltip>
      </q-btn>
    </v-touch>   

    <v-touch @pan="attachSettingKnobs">
      <q-btn flat round large id="hue-rotate" class="stationary">
        <q-icon name="color lens" /> 
        <q-tooltip> Hue Rotate </q-tooltip>
      </q-btn>
    </v-touch>       

    </q-toolbar>

    <q-toolbar class="vertical-middle">
    </q-toolbar>

  </div>    
</template>

<script>
  import { Toast, Ripple, QToolbar, QBtn, QIcon, QChip, QKnob, QSpinnerGears, QInnerLoading, QTooltip, QLayout, QDrawer } from 'quasar'
  import contextMenu from 'vue-context-menu'
  import axios from 'axios'
  import 'jimp/browser/lib/jimp'
  import MImage from './MImage.vue'
  import Ruler from './Ruler.vue'
  import Protractor from './Protractor.vue'
  import BoundingBox from './BoundingBox.vue'
  import MImageClip from './MImageClip.vue'
  import conLine from './conLine.vue'
  import CarbonCopy from './CarbonCopy.vue'
  import KnobSetting from './KnobSetting.vue'
  import ActionChip from './ActionChip.vue'
  import FlowAction from './FlowAction.vue'

  var apiCall = axios.create({
    baseURL: 'http://127.0.0.1:5000/amap/api',
    timeout: 15000
  })

  var diva = axios.create({
    baseURL: 'http://divaservices.unifr.ch/api/v2/',
    timeout: 15000
  })

  export default {
    directives: {
      Ripple
    },
    components: {
      QToolbar,
      QBtn,
      QIcon,
      MImage,
      Toast,
      Ruler,
      Protractor,
      BoundingBox,
      MImageClip,
      conLine,
      contextMenu,
      CarbonCopy,
      QChip,
      QKnob,
      QSpinnerGears,
      KnobSetting,
      ActionChip,
      QInnerLoading,
      FlowAction,
      QTooltip,
      QLayout,
      QDrawer
    },
    data () {
      return {
        // coord: [left, top]
        // delCoord:
        imagesM: [],
        attachingElements: ['imagesM', 'imagesMCrop', 'rulers', 'protractors'],
        attachedElements: ['settingKnobs', 'chipsAction', 'actionFlows'],
        loading: true,
        // x1 y1 x2 y2
        imagesMCrop: [],
        // Change passing expicit colors
        // The component shoudl pass active/inactive etc and the local veu file shold
        actionFlows: [
          {
            coord: [100, 400],
            delCoord: [0, 0],
            active: false,
            processing: 'thresholding',
            controls: [
              {
                value: 2,
                min: 0,
                max: 4,
                property: 'type',
                textOptions: ['THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO', 'THRESH_TOZERO_INV']
              },
              {
                value: 50,
                min: 0,
                max: 255,
                property: 'threshold'
              }
            ],
            previewUrl: '',
            preview: false,
            progress: false
          },
          {
            coord: [300, 400],
            delCoord: [0, 0],
            active: false,
            processing: 'canny',
            controls: [
              {
                value: 100,
                min: 0,
                max: 1000,
                property: 'threshold1'
              },
              {
                value: 200,
                min: 0,
                max: 1000,
                property: 'threshold2'
              }
            ],
            previewUrl: '',
            preview: false,
            progress: false
          },
          {
            coord: [300, 600],
            delCoord: [0, 0],
            active: false,
            processing: 'HistogramEq',
            controls: [],
            previewUrl: '',
            preview: false,
            progress: false
          },
          {
            coord: [500, 500],
            delCoord: [0, 0],
            active: false,
            processing: 'OtsuBinarization',
            service: 'diva',
            serviceUrl: 'http://divaservices.unifr.ch/api/v2/binarization/otsubinarization/1',
            controls: [],
            previewUrl: '',
            preview: false,
            progress: false
          }
        ],
        chipsAction: [
          {
            coord: [100, 400],
            delCoord: [0, 0],
            action: 'segmentLine',
            active: false,
            loading: false
          },
          {
            coord: [200, 400],
            delCoord: [0, 0],
            action: 'segmentChar',
            active: false,
            loading: false
          }
        ],
        settingKnobs: [],
        copiesCarbon: [],
        linesCon: [],
        rulers: [],
        // armAngles: [top, bottom]
        protractors: [],
        // coordinates: [left, top, width, height]
        boundingBoxes: [],
        toggleLinesCon: true
      }
    },
    // Think about removing the constant looping
    // Perhaps it's slowing the process
    computed: {
      settingKnobsTransforms: function () {
        var transforms = {}
        for (var i = 0; i < this.settingKnobs.length; i++) {
          var settingKnob = this.settingKnobs[i]

          if (!settingKnob.disable) {
            if (typeof transforms[settingKnob.refComp + settingKnob.refIndex] === 'undefined') {
              transforms[settingKnob.refComp + settingKnob.refIndex] = {}
            }

            if (typeof transforms[settingKnob.refComp + settingKnob.refIndex]['filter'] === 'undefined') {
              transforms[settingKnob.refComp + settingKnob.refIndex]['filter'] = ''
            }

            var unit = '%'
            if (settingKnob.property === 'hue-rotate') {
              unit = 'deg'
            }
            transforms[settingKnob.refComp + settingKnob.refIndex]['filter'] += settingKnob.property + '(' + settingKnob.value + unit + ')' + ' '
          }
        }
        return transforms
      },
      actionFlowsStyles: function () {
        return this.componentStyles('actionFlows')
      },
      chipsActionStyles: function () {
        console.log('called')
        return this.componentStyles('chipsAction')
      },
      settingKnobsStyles: function () {
        return this.componentStyles('settingKnobs')
      },
      imagesMStyles: function () {
        var style = []
        for (var i = 0; i < this.imagesM.length; i++) {
          var imageM = this.imagesM[i]
          style.push(
            {
              left: imageM.coord[0] + imageM.delCoord[0] + 'px',
              top: imageM.coord[1] + imageM.delCoord[1] + 'px',
              width: imageM.width + 'px',
              transform: 'rotate(' + imageM.tilt + 'deg)'
            }
          )
        }
        return style
      },
      imagesMCropStyles: function () {
        var style = []
        for (var i = 0; i < this.imagesMCrop.length; i++) {
          var imageMCrop = this.imagesMCrop[i]

          // Clipping from top
          var clipTop = imageMCrop.clipCoord[1] / imageMCrop.scale
          // Height of the clip
          var heightClip = (imageMCrop.clipCoord[3] / imageMCrop.scale) + clipTop
          // Clipping from left
          var clipLeft = imageMCrop.clipCoord[0] / imageMCrop.scale
          // width of the clip
          var widthClip = (imageMCrop.clipCoord[2] / imageMCrop.scale) + clipLeft

          style.push(
            {
              left: imageMCrop.coord[0] + imageMCrop.delCoord[0] + 'px',
              top: imageMCrop.coord[1] + imageMCrop.delCoord[1] + 'px',
              width: imageMCrop.width + 'px',
              transform: 'rotate(' + imageMCrop.tilt + 'deg)',
              'clip': 'rect(' + clipTop + 'px, ' + widthClip + 'px, ' + heightClip + 'px, ' + clipLeft + 'px'
            }
          )
        }
        return style
      },
      rulersStyles: function () {
        var style = []
        for (var i = 0; i < this.rulers.length; i++) {
          var ruler = this.rulers[i]
          style.push(
            {
              left: ruler.coord[0] + ruler.delCoord[0] + 'px',
              top: ruler.coord[1] + ruler.delCoord[1] + 'px',
              width: ruler.width + 'px',
              transform: 'rotate(' + ruler.tilt + 'deg)'
            }
          )
        }
        return style
      },
      protractorsStyles: function () {
        var style = []
        for (var i = 0; i < this.protractors.length; i++) {
          var protractor = this.protractors[i]
          style.push(
            {
              left: protractor.coord[0] + protractor.delCoord[0] + 'px',
              top: protractor.coord[1] + protractor.delCoord[1] + 'px'
            }
          )
        }
        return style
      },
      // Fix if the image is tilted
      boundingBoxesStyles: function () {
        // console.log('Updating')
        // console.log(this.boundingBoxes)
        var style = []
        for (var i = 0; i < this.boundingBoxes.length; i++) {
          var bBox = this.boundingBoxes[i]
          // console.log('Updating')

          if (bBox.visibility) {
            var imageM = this[bBox.refComp][bBox.refIndex]
            // console.log(imageM.scale)
            var bBoxLeft = imageM.coord[0] + imageM.delCoord[0] +
                       (bBox.coord[0] / imageM.scale)
            var bBoxTop = imageM.coord[1] + imageM.delCoord[1] +
                       (bBox.coord[1] / imageM.scale)
            var bBoxWidth = bBox.coord[2] / imageM.scale
            var bBoxHeight = bBox.coord[3] / imageM.scale

            style.push(
              {
                left: bBoxLeft + 'px',
                top: bBoxTop + 'px',
                width: bBoxWidth + 'px',
                height: bBoxHeight + 'px',
                transform: 'rotate(' + imageM.tilt + 'deg)',
                'z-index': 201
              })
          }
        }
        return style
      },
      // make it generic
      linesConStyles: function () {
        var style = []
        console.log('updating connecting lines')

        for (var i = 0; i < this.linesCon.length; i++) {
          var lineCon = this.linesCon[i]
          // var comp1 = this[lineCon.comp1][lineCon.index1]
          // var comp2 = this[lineCon.comp2][lineCon.index2]

          var x1 = parseFloat(this.boundingBoxesStyles[lineCon.refIndex1].left.replace('px'))
          var y1 = parseFloat(this.boundingBoxesStyles[lineCon.refIndex1].top.replace('px')) + parseFloat(this.boundingBoxesStyles[lineCon.refIndex1].height.replace('px'))

          var rect = this.imagesMCropStyles[lineCon.refIndex2].clip.replace('rect(', '').replace(')', '').replace(new RegExp(',', 'g'), '').replace(new RegExp('px', 'g'), '').split(' ')

          var x2 = parseFloat(this.imagesMCropStyles[lineCon.refIndex2].left.replace('px')) + parseFloat(rect[3])
          var y2 = parseFloat(this.imagesMCropStyles[lineCon.refIndex2].top.replace('px')) + parseFloat(rect[0])

          lineCon.line1 = [x1, y1, x2, y2]

          console.log(lineCon.line1)

          style.push({
            left: (x1 + 1) + 'px',
            top: (y1 - 2) + 'px'
          })
        }
        return style
      }
    },
    mounted: function () {
      this.getDivaList()
    },
    updated: function () {
      var scaleElements = ['imagesM', 'imagesMCrop']

      for (var i = 0; i < scaleElements.length; i++) {
        var elements = scaleElements[i]
        for (var j = 0; j < this[elements].length; j++) {
          var imageM = this.$refs[elements + j][0].$el
          var scale = imageM.naturalWidth / this[elements][j].width
          this[elements][j].scale = scale
        }
      }
    },
    methods: {
      // http://divaservices.unifr.ch/api/v2/imageprocessing/multiscaleinterestpointdetection/1
      // implement this. add option to read output that has visualization as true
      // think about what to do with methods that return json (points, bounding boxes, polygons)
      // Think about writnig methods for that
      // Cross check with all the methods of diva services and make sure most of them are supported
      // Write mail to marcel about the highlight parameters
      // fix the width button of the chip
      getDivaList: async function (event) {
        console.log('waiting for results')
        var result = await this.getListGet('http://divaservices.unifr.ch/api/v2/')
        console.log(result)
        var relvantMethods = ['Grayification']
        var count = 0
        for (var i = 0; i < result.data.length; i++) {
          if (true) { // relvantMethods.includes(result.data[i].name)
            var methodResult = await this.getListGet(result.data[i].url)
            // Todo the first parameter cannot be a file and it can be somewhere else
            if (methodResult.data.input.length === 2 &&
                typeof methodResult.data.input[0].file['name'] !== 'undefined') {
              console.log('inside here')
              console.log(methodResult)
              this.actionFlows.push({
                coord: [100 + (count * 200), 100],
                delCoord: [0, 0],
                active: false,
                processing: result.data[i].name,
                service: 'diva',
                serviceUrl: result.data[i].url,
                controls: [],
                previewUrl: '',
                preview: false,
                progress: false
              })
              count++
            }
            else if (methodResult.data.input.length > 2 &&
              (result.data[i].name === 'Ocropus Binarization' ||
              result.data[i].name === 'Multi Scale Interest Point Detection')) {
              console.log('greater than one')
              console.log(result.data[i].name)
              var flowOptions = []
              for (var j = 0; j < methodResult.data.input.length; j++) {
                console.log('options' + j)
                var option = methodResult.data.input[j]
                var type = Object.keys(option)[0]
                if (type === 'number') {
                  console.log('number')
                  console.log(option)
                  flowOptions.push({
                    value: typeof option.number.options.default !== 'undefined' ? option.number.options.default : 1,
                    min: typeof option.number.options.min !== 'undefined' ? option.number.options.min : 0,
                    max: typeof option.number.options.max !== 'undefined' ? option.number.options.max : 100,
                    step: typeof option.number.options.steps !== 'undefined' ? option.number.options.steps : 1,
                    property: option.number.name
                  })
                }
                else if (type === 'select') {
                  console.log('select')
                  console.log(option)
                  flowOptions.push({
                    value: option.select.options.default,
                    min: 0,
                    max: option.select.options.values.length - 1,
                    property: option.select.name,
                    textOptions: option.select.options.values
                  })
                }
              }
              console.log(flowOptions)
              this.actionFlows.push({
                coord: [100 + (count * 200), 100],
                delCoord: [0, 0],
                active: false,
                processing: result.data[i].name,
                service: 'diva',
                serviceUrl: result.data[i].url,
                controls: flowOptions,
                previewUrl: '',
                preview: false,
                progress: false
              })
              count++
            }
          }
        }
      },
      getListGet: function (url) {
        return new Promise(resolve => {
          axios.get(url, {})
            .then(function (response) {
              resolve(response)
            })
            .catch(function (error) {
              console.log(error)
            })
        })
      },
      attachSettingKnobs: function (event) {
        if (typeof this.settingKnobs['new'] === 'undefined' || this.settingKnobs['new'] === false) {
          var node = this.getMovableElement(event, 'stationary')
          this.settingKnobs['new'] = true
          this.settingKnobs.push(
            {
              coord: [event.center.x, event.center.y],
              delCoord: [event.deltaX, event.deltaY],
              property: node.id,
              active: false,
              disable: true
            }
          )
        }
        else {
          var settingKnob = this.settingKnobs[this.settingKnobs.length - 1]
          settingKnob.delCoord = [event.deltaX, event.deltaY]

          // Check for collission and attach things
          // add collision detection here

          if (event.isFinal) {
            settingKnob.coord[0] += event.deltaX
            settingKnob.coord[1] += event.deltaY

            settingKnob.delCoord = [0, 0]

            this.settingKnobs['new'] = false
          }
        }
        console.log(this.settingKnobs.length)
      },
      componentStyles: function (elements) {
        var style = []
        for (var i = 0; i < this[elements].length; i++) {
          var element = this[elements][i]
          style.push(
            {
              left: element.coord[0] + element.delCoord[0] + 'px',
              top: element.coord[1] + element.delCoord[1] + 'px'
            }
          )
        }
        return style
      },
      getMovableElement: function (event, type = 'movable') {
        var node = event.target
        var parentCount = 0

        // iterate until you find the parent class with the name 'movable' - which means you can move
        while (typeof node.className.indexOf === 'undefined' ||
          node.className.indexOf(type) === -1) {
          // console.log('here')
          node = node.parentNode
          // console.log(node)
          parentCount++

          if (parentCount > 5) {
            break
          }
        }
        return node
      },
      addLocalImageM: function () {
        console.log('hereeeee')
        this.$refs.localUpload.click()
      },
      uploadLocalImageM: function () {
        var file = this.$refs.localUpload.files[0]
        var reader = new FileReader()
        var dhis = this
        reader.onload = function () {
          var newImage = {
            coord: [0, 80],
            delCoord: [0, 0],
            width: 400,
            tilt: 0,
            urlOrig: reader.result,
            url: reader.result
          }
          dhis.imagesM.push(newImage)
        }
        reader.readAsDataURL(file)
      },
      addRuler: function (event) {
        var newRuler = {
          coord: [0, 300],
          delCoord: [0, 0],
          width: 200,
          tilt: 0
        }
        this.rulers.push(newRuler)
      },
      addProtractor: function (event) {
        var newProtractor = {
          coord: [0, 300],
          delCoord: [0, 0],
          width: 200,
          tilt: 0,
          armAngles: [45, 0]
        }
        this.protractors.push(newProtractor)
      },
      detectCollision: function (object, objectIndex, objectTypes) {
        var obj1 = this.$refs[object + objectIndex][0].$el
        var rect1 = {x: obj1.offsetLeft, y: obj1.offsetTop, width: obj1.offsetWidth, height: obj1.offsetHeight}
        for (var i = 0; i < this[objectTypes].length; i++) {
          var obj2 = this.$refs[objectTypes + i][0].$el
          var rect2 = {x: obj2.offsetLeft, y: obj2.offsetTop, width: obj2.offsetWidth, height: obj2.offsetHeight}
          // console.log(rect1)
          // console.log(rect2)

          var collisionSameObject = (object === objectTypes && parseInt(objectIndex) !== i) ||
                                   (object !== objectTypes)

          if (rect1.x < rect2.x + rect2.width &&
             rect1.x + rect1.width > rect2.x &&
             rect1.y < rect2.y + rect2.height &&
             rect1.height + rect1.y > rect2.y &&
             collisionSameObject) {
            return i
          }
        }
        return false
      },
      flowActionUpdated: function (index, parameters) {
        console.log('Flow Action ' + index + ' updated')

        var actionFlow = this.actionFlows[index]
        actionFlow['parameters'] = parameters

        if (typeof actionFlow.refComp !== 'undefined') {
          this.flowActionProcess(index)
        }
      },
      flowActionProcess: function (index) {
        var dhis = this
        var actionFlow = this.actionFlows[index]

        if (actionFlow.refComp === 'imagesM' || actionFlow.refComp === 'actionFlows') {
          actionFlow.preview = false
          actionFlow.progress = true
          var imageM = this[actionFlow.refComp][actionFlow.refIndex]
          var imgURL = actionFlow.refComp === 'imagesM' ? imageM.urlOrig : imageM.previewUrl
          var postBody = {}

          console.log('We are uploading this')

          if (imgURL.indexOf('base64') !== -1) {
            postBody = {
              'type': 'base64',
              'value': imgURL.split(',')[1],
              'name': 'vinodh',
              'extension': 'jpg'
            }
          }
          else {
            var UrlParts = imgURL.split('/')
            postBody = {
              'type': 'url',
              'value': imgURL,
              'name': UrlParts[UrlParts.length - 1].split('.')[0],
              'extension': UrlParts[UrlParts.length - 1].split('.')[1]
            }
          }

          console.log(postBody)

          if (actionFlow.service === 'diva') {
            diva.post('/collections', {
              'files': [postBody]
            })
              .then(function (response) {
                var collection = response.data.collection
                var uploadResult = {}

                console.log(response)

                if (imgURL.indexOf('base64') !== -1) {
                  uploadResult = {
                    'inputImage': collection + '/vinodh.jpg' // Get the extension from the file // change this
                  }
                }
                else {
                  uploadResult = {
                    'inputImage': collection + '/' + UrlParts[UrlParts.length - 1]
                  }
                }
                console.log(uploadResult)
                console.log('Diva Parameters')
                console.log(actionFlow.parameters)
                axios.post(actionFlow.serviceUrl, {
                  'parameters': actionFlow.parameters,
                  'data': [uploadResult]
                })
                  .then(async function (response) {
                    var result = await dhis.getResult(response.data.results[0].resultLink)
                    var imagesMCon = dhis.getConnectedImageM(index)
                    console.log('Result Received')
                    console.log(result)

                    for (var i = 0; i < result.output.length; i++) {
                      if (typeof result.output[i]['file'] !== 'undefined' &&
                          result.output[i].file.options.visualization) {
                        dhis['imagesM'][imagesMCon].url = result.output[i].file.url
                        actionFlow.previewUrl = result.output[i].file.url
                        console.log('image updated')
                      }
                    }

                    actionFlow.preview = true
                    actionFlow.progress = false
                  })
                  .catch(function (error) {
                    console.log(error)
                  })
              })
              .catch(function (error) {
                console.log(error)
              })
          }
          else {
            apiCall.post('/processing', {
              processing: actionFlow.processing,
              url: imgURL,
              parameters: JSON.stringify(actionFlow.parameters)
            })
              .then(function (response) {
                actionFlow.preview = true
                actionFlow.progress = false

                var actionFlowsCon = dhis.getConnectedActionFlows(index)
                var imagesMCon = dhis.getConnectedImageM(index)

                console.log('connect images ' + imagesMCon)
                console.log('connect actionFlows' + actionFlowsCon)

                dhis['imagesM'][imagesMCon].url = response.data.results
                actionFlow.previewUrl = response.data.results

                if (actionFlowsCon !== false) {
                  console.log('Found connected ' + actionFlowsCon)
                  dhis.flowActionProcess(actionFlowsCon)
                }
              })
              .catch(function (error) {
                console.log(error)
              })
          }
        }
      },
      getResult: function (url) {
        var dhis = this
        return new Promise(resolve => {
          fetch(url, {
            method: 'GET'
          })
            .then(function (res) {
              return res.json()
            })
            .then(function (data) {
              if (data.status === 'done') {
                resolve(data)
              }
              else {
                setTimeout(function () {
                  resolve(dhis.getResult(url))
                }, 1000)
              }
            })
        })
      },
      getConnectedActionFlows: function (index) {
        for (var i = 0; i < this.actionFlows.length; i++) {
          if (this.actionFlows[i].refComp === 'actionFlows' &&
            this.actionFlows[i].refIndex === index) {
            return i
          }
        }
        return false
      },
      getConnectedImageM: function (index) {
        if (this.actionFlows[index].refComp === 'imagesM') {
          return this.actionFlows[index].refIndex
        }
        else if (this.actionFlows[index].refComp === 'actionFlows') {
          return this.getConnectedImageM(this.actionFlows[index].refIndex)
        }
        return false
      },
      moveN: function (event) {
        var node = this.getMovableElement(event)
        var elements = node.id.split('-')[0]

        if (elements === 'protractors') {
          this.moveProtractor(node, event)
        }
        else {
          this.moveGeneric(node, event)
        }
      },
      moveGeneric: function (node, event) {
        var pinchCheck = typeof this.pinchTime === 'undefined' ||
                         Date.now() - this.pinchTime > 300
        var rotateCheck = typeof this.rotateTime === 'undefined' ||
                          Date.now() - this.rotateTime > 300

        if (pinchCheck && rotateCheck) {
          var elements = node.id.split('-')[0]
          var index = node.id.split('-')[1]

          if (this.attachedElements.includes(elements)) {
            // console.log('checking collision of ' + elements)
            var collide = this.detectCollision(elements, index, 'imagesM')

            if (collide !== false) {
              console.log('collision detected')
              this.attachedElementsFix('imagesM', collide, elements, index, event)
            }

            collide = this.detectCollision(elements, index, 'actionFlows')

            if (collide !== false) {
              console.log('collision detected')
              this.attachedElementsFix('actionFlows', collide, elements, index, event)
            }
          }

          if (elements === 'imagesM' || elements === 'actionFlows') {
            this.moveImagesAttach(elements, parseInt(index), event)
          }

          this.moveComponent(elements, index, event)
        }
      },
      attachedElementsFix: function (nonMoving, nonMovingIndex, moving, movingIndex, event) {
        this.$refs[moving + 'Touch' + movingIndex][0].disable('pan')

        this[moving][movingIndex]['refComp'] = nonMoving
        this[moving][movingIndex]['refIndex'] = parseInt(nonMovingIndex)

        console.log(this[moving][movingIndex])

        console.log('fixed ' + nonMoving + ' to ' + moving)

        event.isFinal = true
        if (moving === 'settingKnobs') {
          this.settingKnobs[movingIndex].active = true
          this.settingKnobs[movingIndex].disable = false
        }
        else if (moving === 'chipsAction') {
          if (this.chipsAction[movingIndex].refComp === 'imagesM') {
            this.chipsAction[movingIndex].active = true
            this.chipsAction[movingIndex].loading = true
            this.segmentImagesM(nonMovingIndex, this.chipsAction[movingIndex])
          }
        }
        else if (moving === 'actionFlows') {
          this.actionFlows[movingIndex].active = true
          this.flowActionProcess(movingIndex)
        }
      },
      moveImagesAttach: function (elements, index, event) {
        // Move the knobs associted with the image as well
        for (var i = 0; i < this.attachedElements.length; i++) {
          var elementsType = this.attachedElements[i]
          for (var j = 0; j < this[elementsType].length; j++) {
            var attachedElement = this[elementsType][j]
            if (attachedElement.refComp === elements && attachedElement.refIndex === index) {
              console.log('Moving attachedElement ' + elementsType + j + ' attached to ' + elements + index)
              this.moveComponent(elementsType, j, event)
              this.moveImagesAttach(elementsType, j, event)
            }
          }
        }
      },
      moveComponent: function (elements, index, event) {
        this[elements][index].delCoord[0] = event.deltaX
        this[elements][index].delCoord[1] = event.deltaY

        this.$set(this[elements], index, this[elements][index])

        if (event.isFinal) {
          this[elements][index].coord[0] += event.deltaX
          this[elements][index].coord[1] += event.deltaY

          this[elements][index].delCoord = [0, 0]

          this.$set(this[elements], index, this[elements][index])
        }
      },
      moveProtractor: function (node, event) {
        if (event.target.className.indexOf('arm') !== -1) {
          this.moveProtractorArm(node, event)
        }
        else {
          this.moveGeneric(node, event)
        }
      },
      moveProtractorArm: function (node, event) {
        console.log('Arms')
        console.log(event.target.className)

        var index = node.id.split('-')[1]

        if (event.additionalEvent === 'pandown' ||
            event.additionalEvent === 'panright') {
          if (event.target.className.indexOf('top') !== -1) {
            this.protractors[index].armAngles[0] += 1
          }
          else {
            this.protractors[index].armAngles[1] += 1
          }
        }
        else if (event.additionalEvent === 'panup' ||
          event.additionalEvent === 'panleft') {
          if (event.target.className.indexOf('top') !== -1) {
            this.protractors[index].armAngles[0] -= 1
          }
          else {
            this.protractors[index].armAngles[1] -= 1
          }
        }
        this.$set(this.protractors, index, this.protractors[index])
      },
      scaleN: function (event) {
        var node = this.getMovableElement(event)

        this.scaleGeneric(node, event)
      },
      scaleGeneric: function (node, event) {
        var rotateCheck = typeof this.rotateTime === 'undefined' ||
                          Date.now() - this.rotateTime > 300

        if (rotateCheck) {
          var elements = node.id.split('-')[0]
          var index = node.id.split('-')[1]

          var scaleFactor = 5

          // scale slowly if it's a ruler
          if (elements === 'rulers') {
            scaleFactor = 1
          }

          if (event.additionalEvent === 'pinchout') {
            this[elements][index].width += scaleFactor
          }

          else if (event.additionalEvent === 'pinchin') {
            this[elements][index].width -= scaleFactor
          }

          if (elements === 'imagesM' || elements === 'imagesMCrop') {
            var imageM = this.$refs[elements + index][0].$el
            var scale = imageM.naturalWidth / this[elements][index].width
            this[elements][index].scale = scale
          }

          this.$set(this[elements], index, this[elements][index])

          this.pinchTime = Date.now()
        }
      },
      rotateN: function (event) {
        var node = this.getMovableElement(event)

        this.rotateGeneric(node, event)
      },
      rotateGeneric: function (node, event) {
        var elements = node.id.split('-')[0]
        var index = node.id.split('-')[1]

        var rotate = false
        if (event.velocity === 0) {
          this[elements][index]['initRotation'] = event.rotation
        }
        else {
          this[elements][index]['actRotation'] = this[elements][index].initRotation - event.rotation
          this[elements][index].initRotation = event.rotation
          rotate = true
        }
        if (rotate && Math.abs(this[elements][index].actRotation) < 10) {
          this[elements][index].tilt -= this[elements][index].actRotation
          this.$set(this[elements], index, this[elements][index])
        }

        this.rotateTime = Date.now()
      },
      disconnectComp: function (event) {
        var node = this.getMovableElement(event)
        var elements = node.id.split('-')[0]
        var index = node.id.split('-')[1]

        console.log('here')
        console.log()

        if (this[elements][index].refComp !== '' &&
            typeof this[elements][index].refComp !== 'undefined') {
          this.disconnectCompGeneric(node, event)
        }
      },
      disconnectCompGeneric: function (node, event) {
        var elements = node.id.split('-')[0]
        var index = node.id.split('-')[1]

        this[elements][index].active = false
        this.$refs[elements + 'Touch' + index][0].enable('pan')

        if (elements === 'settingKnobs') {
          this[elements][index].disable = true
          this[elements][index].coord[1] += 10
        }
        else if (elements === 'chipsAction') {
          this[elements][index].coord[0] += 10
          this.chipsActionToggle(index, 'deletion')
        }

        this[elements][index].refComp = ''
        this[elements][index].refIndex = ''
        this.$set(this[elements], index, this[elements][index])
      },
      swipeKnob: function (event) {
        console.log(event)
      },
      copyImage: function (event) {
        console.log(event)
        var index = event.target.id.split('-')[1]

        var bBox = this.boundingBoxes[index]
        var imageM = this[bBox.refComp][bBox.refIndex]

        // var jimpSrc = Buffer.from(imageM.url.replace(/^data:image\/\w+;base64,/, ''), 'base64')

        // var cropUrl = ''

        /* Jimp.read(jimpSrc.buffer).then(function (imgSrc) {
          imgSrc.crop(bBox.coord[0], bBox.coord[1], bBox.coord[2], bBox.coord[3])

          imgSrc.getBase64(Jimp.AUTO, function (err, src) {
              cropUrl = src
          })

          }).catch(function (err) {
          console.error(err)
        }) */

        // Copy image attributes to make sure the copied part is independent of changes in the original image
        var newImageMCrop = {
          coord: [0, 580],
          delCoord: [0, 0],
          width: imageM.width,
          tilt: imageM.tilt,
          scale: imageM.scale,
          url: imageM.url,
          clipCoord: bBox.coord.slice()
        }

        this.imagesMCrop.push(newImageMCrop)

        this.linesCon.push({
          refComp1: 'boundingBoxes',
          refIndex1: index,
          refComp2: 'imagesMCrop',
          refIndex2: this.imagesMCrop.length - 1
        })

        Toast.create({
          html: 'Section copied',
          icon: 'content_copy',
          timeout: 2500
        })
      },
      onCtxOpen: function (locals) {
        this.CtxRef = locals.ref
      },
      segmentImagesM: function (imageRef, actionChip) {
        var dhis = this

        var segmentMode = {
          segmentBlock: 0,
          segmenetPara: 1,
          segmentLine: 2,
          segmentWord: 3,
          segmentChar: 4
        }
        apiCall.post('/segment/tesseract', {
          mode: segmentMode[actionChip.action],
          url: dhis.imagesM[imageRef].url
        })
          .then(function (response) {
            for (var i = 0; i < response.data.boxes.length; i++) {
              dhis.boundingBoxes.push(
                {
                  refComp: 'imagesM',
                  refIndex: imageRef,
                  type: actionChip.action,
                  coord: response.data.boxes[i],
                  visibility: true
                }
              )
              actionChip.loading = false
            }
            // console.log(dhis.boundingBoxes)
            console.log('boundingBoxes added')
          })
          .catch(function (error) {
            console.log(error)
          })
      },
      knobTurned: function (index, event) {
        console.log('knob turned')
        this.settingKnobs[index].value = event
        this.$set(this.settingKnobs, index, this.settingKnobs[index])
      },
      clearBoundingBoxes: function () {
        this.boundingBoxes = []
      },
      chipsActionToggle: function (index, action) {
        if (action === 'deletion') {
          var delBox = []
        }

        var chipAction = this.chipsAction[index]
        console.log(chipAction)

        for (var i = 0; i < this.boundingBoxes.length; i++) {
          var bBox = this.boundingBoxes[i]

          if (bBox.type === chipAction.action &&
              bBox.refComp === chipAction.refComp &&
              bBox.refIndex === chipAction.refIndex) {
            // console.log('removing ' + bBox.type)
            if (action === 'visibility') {
              if (bBox.visibility) {
                bBox.visibility = false
              }
              else {
                bBox.visibility = true
              }
              this.$set(this.boundingBoxes, i, bBox)
            }
            if (action === 'deletion') {
              delBox.push(index)
            }
          }
        }

        console.log(action)
        console.log(delBox)

        // segmenting lines, then segmenting characters
        // and if character tag is detached, it also removes the line segemnts
        // fix this
        if (action === 'deletion') {
          for (i = delBox.length - 1; i >= 0; i--) {
            this.boundingBoxes.splice(delBox[i], 1)
          }
        }

        console.log(this.boundingBoxes)
      },
      toggleconLines: function () {
        if (this.toggleLinesCon) {
          this.toggleLinesCon = false
        }
        else {
          this.toggleLinesCon = true
        }
      }
    }
  }
</script>

<style scoped>
.movable {
  display: inline-block; 
  padding: 0px; 
  position: absolute;
}
</style>
