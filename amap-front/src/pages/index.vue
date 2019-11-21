<template>
  <!-- save and load protractors/scales -->
  <!-- delete instruments -->
  <!-- Update screen after fribourg load -->
  <!-- saving and loading the workspace fix it properly -->

  <!-- Fix for collection books -->
  <!-- Fix connecting lines disappearing when pages change -->
  <!-- Send messages -->

  <q-layout>

  <q-layout-header v-model="showHeader">

    <q-toolbar color="dark">

      <input type="file" @change="uploadLocalImageM" ref="localUpload" style="display:none" multiple/>

      <input type="file" @change="loadLocalSave" ref="localSave" style="display:none" multiple/>

      <q-btn flat round large @click="addLocalImageM" icon="add_circle" size="lg">
        <q-tooltip> Add Image </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="saveData" icon="save" size="lg">
        <q-tooltip> Save Workspace </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="loadData" icon="folder open" size="lg">
        <q-tooltip> Load Workspace </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="addRuler" icon="straighten" size="lg">
        <q-tooltip> Ruler </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="addProtractor" icon="aspect ratio" size="lg">
        <q-tooltip> Protractor </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="hideAll" :icon="!hideAllToggle ? 'visibility' : 'visibility off'" size="lg">
        <q-tooltip> Hide all objects </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="selectRectangle" icon="select all" size="lg" :color="selectRect ? 'orange' : '' ">
        <q-tooltip> Selection Rectangle </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="toggleLinesCon = !toggleLinesCon" icon="line style" size="lg">
        <q-tooltip> Toggle Lines </q-tooltip>
      </q-btn>

      <!-- <q-btn flat round large @click="layer3dShow = !layer3dShow" icon="3d rotation" size="lg">
        <q-tooltip> 3D Layers </q-tooltip>
      </q-btn>

      <q-btn flat round large @click="flipbookShow = !flipbookShow" icon="book" size="lg">
        <q-tooltip> Flip Book </q-tooltip>
      </q-btn>

      <q-btn flat round large icon="library books" @click="showLeft = !showLeft" size="lg">
        <q-tooltip> Logs </q-tooltip>
      </q-btn> -->

      <q-btn flat round large icon="tune" @click="showScaleTilt = !showScaleTilt" size="lg">
        <q-tooltip> Show scale and tilt </q-tooltip>
      </q-btn>

      <q-btn flat round large icon="mouse" @click="showIcons = !showIcons" size="lg">
        <q-tooltip> Hide image icons </q-tooltip>
      </q-btn>

      <q-btn flat round large icon="help" @click="showIcons = !showIcons" size="lg">
        <q-tooltip> Help </q-tooltip>
      </q-btn>

    </q-toolbar>

  </q-layout-header>
  <q-page-container>

    <q-icon name="delete forever" :size="deleteIconSize" color="red" class='delete' ref="delete-icon"
      :class="!deleteActive ? 'transparent' : ''" @click.native="deleteActive = !deleteActive"/>

    <!-- <svg height="250" width="500">
      <polygon points="220,10 300,210 170,250 123,234" style="fill:lime;stroke:purple;stroke-width:1" />
    </svg> -->

    <!-- <svg height="100" width="100">
      <circle cx="121" cy="40" r="45" stroke="black" stroke-width="3" fill="red" />
    </svg> -->

    <!-- Images -->

    <v-touch @panstart="rectStart" @panmove="rectMove" @panend="rectEnd"
              @pinchstart="scaleN('start', ...arguments)" @pinchmove="scaleN('move', ...arguments)" @pinchend="scaleN('end', ...arguments)"
             @click.native="imagesMClick(index,...arguments)"
             @rotate="rotateN" :rotate-options="{ pointers: 3 }"
             :class="{transparent: transparentActive['imagesM' + index]}"
             v-for="(imageM, index) in imagesM" :key="'imagesM-'+index">
      <div class="movable" :style="imagesMStylesDerived[index]" v-show="showScaleTilt && !imageM.delete"><small>
        Scale: {{(1/imageM.scale).toFixed(2)}} : Tilt: {{Math.round(imageM.tilt)}} <br/>
        Width: {{Math.round(imageM.widthN/imageM.scale)}} px :
        Height: {{Math.round(imageM.heightN/imageM.scale)}} px </small>
      </div>
      <m-image class="movable" :id="'imagesM-'+index"
               :ref="'imagesM'+index"
               @fixed="fixElements('imagesM', index, ...arguments)"
               @sidechanged="hideBoundingBoxes('imagesM', index, ...arguments)"
               @showoriginal="showOriginalImagesM('imagesM', index, ...arguments)"
               @pinch="scaleN"
               @zoomin="zoomClick('imagesM', index, 'in')"
               @zoomout="zoomClick('imagesM', index, 'out')"
               @rotateright="rotateClick('imagesM', index, 'right')"
               @rotateleft="rotateClick('imagesM', index, 'left')"
               @copypage="copyElements('imagesM', index)"
               v-touch-pan.prevent="demoMove"

               :url="!imageM['showOriginal'] ? imageM.url : imageM.urlOrig"
               :width="imageM.width"
               :textBack="imageM.textBack"
               :fix="true"
               :style="[imagesMStyles[index], settingKnobsTransforms['imagesM'+index]]"

               :showIcons = "showIcons"
              v-ripple>
      </m-image>
    </v-touch>

    <!-- Books Collection -->
    <v-touch @panstart="rectStart" @panmove="rectMove" @panend="rectEnd"
             @click.native="collectionBooksClick(index,...arguments)"
             @pinchstart="scaleN('start', ...arguments)" @pinchmove="scaleN('move', ...arguments)" @pinchend="scaleN('end', ...arguments)"
             :class="{transparent: transparentActive['collectionBooks' + index]}"
             @rotate="rotateN" :rotate-options="{ pointers: 3 }"
             v-for="(collectionBook, index) in collectionBooks" :key="'collectionBooks-'+index">
      <div class="movable" :style="collectionBooksStylesDerived[index]" v-show="showScaleTilt && !collectionBook.delete"><small>
        Scale: {{(1/collectionBook.scale).toFixed(2)}} : Tilt: {{Math.round(collectionBook.tilt)}} <br/>
        Width: {{Math.round(collectionBook.widthN/collectionBook.scale)}} px :
        Height: {{Math.round(collectionBook.heightN/collectionBook.scale)}} px </small>
      </div>
      <book-collection class="movable" :id="'collectionBooks-'+index"
               :ref="'collectionBooks'+index"
               @fixed="fixElements('collectionBooks', index, ...arguments)"
               @pinch="scaleN"
               :width="collectionBook.width"
               :pages="collectionBook.pages"
               :pagesorig = "collectionBook.pagesOrig"
               :comments="collectionBook.comments"
               :style="[collectionBooksStyles[index], settingKnobsTransforms['collectionBooks'+index]]"
               :showIcons = "showIcons"
               v-touch-pan.prevent="demoMove"

               @copypage="copyPage(index, ...arguments)"
               @zoomin="zoomClick('collectionBooks', index, 'in')"
               @zoomout="zoomClick('collectionBooks', index, 'out')"
               @rotateright="rotateClick('collectionBooks', index, 'right')"
               @rotateleft="rotateClick('collectionBooks', index, 'left')"
               @showoriginal="showOriginalCollectionBooks('collectionBooks', index, ...arguments)"

               @detachpage="detachPage(index, $event)"
               @pageFlipped="updateActivePage(index, $event)"
              >
      </book-collection>
    </v-touch>

    <!-- Rulers -->
    <v-touch
             v-for="(ruler, index) in rulers" :key="'rulers-'+index">

      <ruler class="movable" :id="'rulers-'+index">
      </ruler>
    </v-touch>

    <!-- change pinching section as below-->
    <!-- Protractors -->
    <v-touch
             v-for="(protractor, index) in protractors" :key="'protractors-'+index"
             :style="imagesMCropStyles[index]">

      <protractor class="movable" :id="'protractors-'+index"
               :style="[protractorsStyles[index]]">
      </protractor>
    </v-touch>

    <!-- bounding boxes -->
    <div v-for="(bBox, index) in boundingBoxes"
             :key="'boundingBoxes'+index" v-if = "bBox !== null">
      <v-touch @tap="copyImageSelected" :tap-options="{taps: 2}"
               @click.native="hideBoundingBox(index)"
               @pan="boundBoxResizeUL(index,$event)"
               >
        <!-- Relative Position for Ripple effect -->
        <bounding-box :style="boundingBoxesStyles[index]"
                      :id="'boundingBoxes-'+index"
                      :ref="'boundingBoxes-'+index"
                      :color="bBox.color"
                      v-ripple>
        </bounding-box>
      <!-- <bounding-box-icons :coords="boundingBoxesStyles[index]"> </bounding-box-icons> -->
      </v-touch>

       <span class="icon-resize" :style="{'margin-top': (parseFloat(boundingBoxesStyles[index].top.replace('px', ''))-84)+'px', 'margin-left': (parseFloat(boundingBoxesStyles[index].left.replace('px', ''))+parseFloat(boundingBoxesStyles[index].width.replace('px', '')))+'px'}" v-if="boundingBoxesStyles[index] != null">
        <q-icon name="close" color="red" v-show="bBox.resize && !bBox.locked" @click.native="deleteBoundingBox(index)"/>
      </span>

      <span class="icon-resize" :style="{'margin-top': (parseFloat(boundingBoxesStyles[index].top.replace('px', ''))-74)+'px', 'margin-left': boundingBoxesStyles[index].left}" v-if="boundingBoxesStyles[index] != null">
        <q-icon name="keyboard arrow up" color="red" v-show="bBox.resize && !bBox.locked"/>
      </span>
      <span class="icon-resize" :style="{'margin-top': (parseFloat(boundingBoxesStyles[index].top.replace('px', ''))-72+parseFloat(boundingBoxesStyles[index].height.replace('px', ''))-12)+'px', 'margin-left': boundingBoxesStyles[index].left}" v-if="boundingBoxesStyles[index] != null">
        <q-icon name="keyboard arrow down" color="red" v-show="bBox.resize && !bBox.locked"/>
      </span>
      <span class="icon-resize" :style="{'margin-top': (parseFloat(boundingBoxesStyles[index].top.replace('px', ''))-74)+'px', 'margin-left': (parseFloat(boundingBoxesStyles[index].left.replace('px', ''))+parseFloat(boundingBoxesStyles[index].width.replace('px', ''))-15)+'px'}" v-if="boundingBoxesStyles[index] != null">
        <q-icon name="keyboard arrow up" color="red" v-show="bBox.resize && !bBox.locked"/>
      </span>
      <span class="icon-resize" :style="{'margin-top': (parseFloat(boundingBoxesStyles[index].top.replace('px', ''))-72+parseFloat(boundingBoxesStyles[index].height.replace('px', ''))-12)+'px', 'margin-left': (parseFloat(boundingBoxesStyles[index].left.replace('px', ''))+parseFloat(boundingBoxesStyles[index].width.replace('px', ''))-15)+'px'}" v-if="boundingBoxesStyles[index] != null">
        <q-icon name="keyboard arrow down" color="red" v-show="bBox.resize && !bBox.locked"/>
      </span>
    </div>

    <!-- connection lines -->
    <con-Line v-for="(lineCon, index) in linesCon" :key="'linesCon-'+index"
              :line1="lineCon.line1" :line2="lineCon.line2" class="movable"
              :style="linesConStyles[index]" v-if="toggleLinesCon && lineCon.delete != true">
    </con-Line>

    <!-- Setting knobs -->
    <v-touch @swipedown="disconnectComp" @tap="disconnectComp" :tap-options="{taps: 2}"
          @panend="moveFinal"
          :class="{transparent: transparentActive['settingKnobs' + index], hidden: hideAllToggle}"
             v-for="(settingKnob, index) in settingKnobs"
             :key="'settingKnob-'+index"
             :ref="'settingKnobsTouch'+index">
      <knob-setting v-bind="settingKnob"
                    :ref="'settingKnobs'+index"
                    :id="'settingKnobs-'+index"
                    :disable="settingKnob.disable"
                    v-touch-pan.prevent="demoMove"
                    :style="settingKnobsStyles[index]"
                    @turned="knobTurned(index,$event)"
                    class="movable"
                    >
      </knob-setting>
    </v-touch>

    <!-- action chips -->
    <v-touch @swiperight="disconnectComp"
             @tap="disconnectComp" :tap-options="{taps: 2}"
             @panend="moveFinal"
            :class="{transparent: transparentActive['chipsAction' + index], hidden: hideAllToggle}"
             v-for="(chipAction, index) in chipsAction"
             :key="'chipAction-'+index"
             :ref="'chipsActionTouch'+index" class="touch">
      <action-chip v-bind="chipAction"
                   :id="'chipsAction-'+index"
                   :ref="'chipsAction'+index"
                   v-touch-pan.prevent="demoMove"
                   :style="chipsActionStyles[index]"
                   @visibleToggle="chipsActionToggle(index, 'visibility',...arguments)"
                   @disableChip="chipsActionDisable(index,...arguments)"
                   @addbbox="addSegmentBox(index,...arguments)"
                   class="movable"
                   >
      </action-chip>
    </v-touch>

    <!-- action copies -->
    <v-touch @swiperight="disconnectComp"
             @tap="disconnectComp" :tap-options="{taps: 2}"
             @panend="moveFinal"
            :class="{transparent: transparentActive['actionCopies' + index], hidden: hideAllToggle}"
             v-for="(actionCopy, index) in actionCopies"
             :key="'actionCopy-'+index"
             :ref="'actionCopiesTouch'+index" class="touch">
      <copy-action v-bind="actionCopy"
                   :id="'actionCopies-'+index"
                   :ref="'actionCopies'+index"
                   v-touch-pan.prevent="demoMove"

                   :style="actionCopiesStyles[index]"
                   class="movable"
                   >
      </copy-action>
    </v-touch>

    <!-- Action flows @pan="moveN" -->
    <v-touch  @swiperight="disconnectComp"
             @tap="disconnectComp" :tap-options="{taps: 2}"
             @panend="moveFinal"
            :class="{transparent: transparentActive['actionFlows' + index], hidden: hideAllToggle, 'transparent': actionFlow.dimmed}"
             v-for="(actionFlow, index) in actionFlows"
             :key="'actionFlow-'+index"
             :ref="'actionFlowsTouch'+index">
      <flow-action v-bind="actionFlow"
                   :id="'actionFlows-'+index"
                   :ref="'actionFlows'+index"
                   :style="actionFlowsStyles[index]"
                   @updated="flowActionUpdated(index, $event)"
                   @changed="flowActionChanged(index, $event)"
                   v-touch-pan="demoMove"
                   class="movable"
                   >
      </flow-action>
    </v-touch>

    <!-- Writer Identification -->
    <v-touch @swiperight="disconnectComp"
             @tap="disconnectComp" :tap-options="{taps: 2}"
             @panend="moveFinal"
            :class="{transparent: transparentActive['identifyWriters' + index], hidden: hideAllToggle}"
             v-for="(identifyWriter, index) in identifyWriters"
             :key="'identifyWriter-'+index"
             :ref="'identifyWritersTouch'+index">
      <image-input-action v-bind="identifyWriter"
                   :id="'identifyWriters-'+index"
                   :ref="'identifyWriters'+index"
                   v-touch-pan.prevent="demoMove"
                   :style="identifyWritersStyles[index]"
                   @select_image="updateSelectImageMode(index, 'identifyWriters', ...arguments)"
                   @item_active="identifyWritersProcess(index, ...arguments)"
                   class="movable"
                   >
      </image-input-action>
    </v-touch>

    <!-- Template Matching -->
    <v-touch @swiperight="disconnectComp"
             @tap="disconnectComp" :tap-options="{taps: 2}"
             @panend="moveFinal"
            :class="{transparent: transparentActive['matchTemplates' + index], hidden: hideAllToggle}"
             v-for="(matchTemplate, index) in matchTemplates"
             :key="'matchTemplate-'+index"
             :ref="'matchTemplatesTouch'+index">
      <image-input-action v-bind="matchTemplate"
                   :id="'matchTemplates-'+index"
                   :ref="'matchTemplates'+index"
                   v-touch-pan.prevent="demoMove"

                   :style="matchTemplatesStyles[index]"
                   @select_image="updateSelectImageMode(index, 'matchTemplates', ...arguments)"
                   @item_active="matchTemplatesProcess(index, ...arguments)"
                   class="movable"
                   >
      </image-input-action>
    </v-touch>

    <!-- Text boxes -->
    <v-touch
             v-for="(boxText, index) in boxesText"
             :key="'boxText-'+index"
            :class="{transparent: transparentActive['boxesText' + index], hidden: hideAllToggle}"
             :ref="'boxesTextTouch'+index">
      <text-box v-bind="boxText"
                   :id="'boxesText-'+index"
                   :ref="'boxesText'+index"
                   :style="boxesTextStyles[index]"
                   class="movable"
                   >
      </text-box>
    </v-touch>

    <layer3d v-show="layer3dShow"> </layer3d>
    <flip-book v-show="flipbookShow"></flip-book>

    <div v-for="(imageM, index) in imagesM" :key="'imageMRect' + index" v-if="typeof imageM['selectRect'] !=='undefined'">
      <div :id="'div' + index"
        :style= "{'left': imageM.selectRect[0] + 'px',
        'top': imageM.selectRect[1] + 'px',
        'width': imageM.selectRect[2] + 'px',
        'height': imageM.selectRect[3] + 'px',
        'border': '1px solid red', 'position': 'absolute', 'filter': 'blur(0.5px)'}">
      </div>
    </div>

    <div v-for="(imageM, index) in collectionBooks" :key="'imageMRect' + index" v-if="typeof imageM['selectRect'] !=='undefined'">
      <div :id="'div' + index"
        :style= "{'left': imageM.selectRect[0] + 'px',
        'top': imageM.selectRect[1] + 'px',
        'width': imageM.selectRect[2] + 'px',
        'height': imageM.selectRect[3] + 'px',
        'border': '1px solid red', 'position': 'absolute', 'filter': 'blur(0.5px)'}">
      </div>
    </div>

  </q-page-container>

  <!-- <carbon-copy :style="{left: '200px', top: '300px', height: '400px', width: '400px', position: 'absolute', 'z-index': 200}"> </carbon-copy> -->
  <!-- Creating a pseduomanuscript with bits and pieces from everything else -->

  <q-layout-drawer side="left" v-model="showLeft" class="bg-positive">

    <b>Activity Log </b>
    <hr/>
    <log-entry v-for="(log,index) in logs" :key="'entryLog' + index" v-bind="log" class="q-ma-md"
     @delete="deleteLog(index)" @rerun="rerunLog(index)" v-if="log !== null"> </log-entry>
  </q-layout-drawer>

  <q-layout-drawer side="right" v-model="showRight" class="shadow-1">
      <q-collapsible icon="flash on" label="Binarization">
        <span class="row" v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key" v-if="['OpenCV Binarization','Otsu Binarization', 'Sauvola Binarization', 'Kraken Binarization', 'Ocropus Binarization'].includes(key)">
        <span class="col-10">
        <v-touch @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}">
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer" widthk="200">
         </flow-chip>
        </v-touch>
        </span>
        <span class="col-2">
          <q-btn flat icon="info" @click="infoBox(key)" size="md"></q-btn>
        </span>
       </span>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Other Image Enhancements">
        <v-touch v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key"  @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['Sharpen Enhancement', 'Histogram Enhancement', 'Grayification', 'Image Inversion', 'Histogram Eq Color'].includes(key)">
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer">
         </flow-chip>
       </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Noise">
        <v-touch v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key"  @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['NonLocal Denoising Gray', 'NonLocal Denoising Color', 'Add Random Noise'].includes(key)">
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer">
         </flow-chip>
       </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Filters">
        <v-touch v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key"  @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['Blur', 'Guassian Blur', 'Median Blur', 'Bilateral Filter'].includes(key)">
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer">
         </flow-chip>
       </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Feature Detection">
        <v-touch v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key"  @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['Multi Scale Interest Point Detection', 'Canny', 'ORB keypoints', 'Good Features to Track'].includes(key)"> <!-- add SIFT here later and other menans of features -->
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer">
         </flow-chip>
       </v-touch>
     </q-collapsible>
      <q-collapsible icon="flash on" label="Morphology">
        <v-touch v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key"  @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['Skeletonize', 'Medial Axis', 'Thin', 'Hough Line', 'Hough Line Prob'].includes(key)"> <!-- add SIFT here later and other menans of features -->
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer">
         </flow-chip>
       </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Layout Analysis">
        <v-touch v-for="key in Object.keys(chipsActionAvailable)" :key="'chipAction-' + key" @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['segmentLine','segmentChar', 'segmentHist', 'segmentKraken'].includes(key)">
          <action-chip :action="key" :id="'chipsAction_' + key" class="stationary action-chip-drawer">
          </action-chip>
        </v-touch>
        <v-touch v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key"  @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['Ocropus Page Segmentation', 'Seam Carving Text Line Extraction', 'Wavelength Seam Carving', 'TopBase Lines', 'MidInter Lines', 'All Lines'].includes(key)"> <!-- add SIFT here later and other menans of features -->
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer">
         </flow-chip>
       </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Propagate Actions">
        <v-touch v-for="key in Object.keys(actionCopiesAvailable)" :key="'actionCopies-' + key" @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}">
          <flow-chip :text="key" :id="'actionCopies_' + key" colorbg="brown" class="stationary action-chip-drawer"
            icon="copy files">
          </flow-chip>
        </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Countours">
        <v-touch v-for="key in Object.keys(actionFlowsAvailable)" :key="'actionFlow-' + key"  @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['Contour', 'Skeletonize'].includes(key)"> <!-- add SIFT here later and other menans of features -->
         <flow-chip :text="key" :id="'actionFlows_' + key" class="stationary action-chip-drawer">
         </flow-chip>
       </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Spotting">
        <v-touch v-for="key in Object.keys(matchTemplatesAvailable)" :key="'matchTemplates-' + key" @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}">
          <flow-chip :text="key" :id="'matchTemplates_' + key" class="stationary action-chip-drawer"
            icon="find_in_page">
          </flow-chip>
        </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Writer Identification">
        <v-touch v-for="key in Object.keys(identifyWritersAvailable)" :key="'identifyWriters-' + key" @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}">
          <flow-chip :text="key" :id="'identifyWriters_' + key" class="stationary action-chip-drawer"
           icon="fingerprint">
          </flow-chip>
        </v-touch>
      </q-collapsible>
      <q-collapsible icon="flash on" label="Transcription">
        <v-touch v-for="key in Object.keys(chipsActionAvailable)" :key="'chipAction-' + key" @pan="attachDrawItems" @tap="attachDrawItemsClick" :tap-options="{taps: 2}"
         v-if="['textEntry', 'textGoogle'].includes(key)">
          <action-chip :action="key" :id="'chipsAction_' + key" class="stationary action-chip-drawer">
          </action-chip>
        </v-touch>
      </q-collapsible>
  </q-layout-drawer>

  <!-- view settings that don't permanents affect the manuscript -->
  <!-- They get attached to the bottom -->
  <q-layout-footer>
    <q-toolbar color="dark">

      <q-icon flat name="settings brightness" size="50px" color="orange">
          <q-tooltip> Image View Settings </q-tooltip>
        </q-icon>

      <v-touch @pan="attachDrawItems" @tap="attachDrawItemsClickY" :tap-options="{taps: 2}">
        <q-btn flat round id="settingKnobs_brightness" class="stationary" icon="brightness low" size="lg">
          <q-tooltip> Brightness </q-tooltip>
        </q-btn>
      </v-touch>

      <v-touch @pan="attachDrawItems" @tap="attachDrawItemsClickY" :tap-options="{taps: 2}">
        <q-btn flat round large id="settingKnobs_contrast" class="stationary" icon="brightness_medium" size="lg">
          <q-tooltip> Contrast </q-tooltip>
        </q-btn>
      </v-touch>

      <v-touch @pan="attachDrawItems" @tap="attachDrawItemsClickY" :tap-options="{taps: 2}">
        <q-btn flat round large id="settingKnobs_grayscale" class="stationary" icon="format_color_fill" size="lg">
          <q-tooltip> Greyscale </q-tooltip>
        </q-btn>
      </v-touch>

      <v-touch @pan="attachDrawItems" @tap="attachDrawItemsClickY" :tap-options="{taps: 2}">
        <q-btn flat round large id="settingKnobs_invert" class="stationary" icon="invert_colors" size="lg">
          <q-tooltip> Invert Colors </q-tooltip>
        </q-btn>
      </v-touch>

      <v-touch @pan="attachDrawItems" id="opacity" @tap="attachDrawItemsClickY" :tap-options="{taps: 2}">
        <q-btn flat round large id="settingKnobs_opacity" class="stationary" icon="opacity" size="lg">
          <q-tooltip> Opacity </q-tooltip>
        </q-btn>
      </v-touch>

      <v-touch @pan="attachDrawItems" @tap="attachDrawItemsClickY" :tap-options="{taps: 2}">
        <q-btn flat round large id="settingKnobs_hue-rotate" class="stationary" icon="color lens" size="lg">
          <q-tooltip> Hue Rotate </q-tooltip>
        </q-btn>
      </v-touch>

    </q-toolbar>

  </q-layout-footer>

</q-layout>

</template>

<script>
import {Dialog, Notify, ActionSheet, QToolbar, QChip, QKnob, QSpinnerGears, QInnerLoading, QTooltip, QLayout, QLayoutDrawer, QCollapsible, QList, QLayoutHeader, QLayoutFooter, QPageContainer} from 'quasar'
import 'jimp/browser/lib/jimp'
import MImage from '../components/MImage.vue'
import Ruler from '../components/Ruler.vue'
import Protractor from '../components/Protractor.vue'
import BoundingBox from '../components/BoundingBox.vue'
import MImageClip from '../components/MImageClip.vue'
import conLine from '../components/conLine.vue'
import CarbonCopy from '../components/CarbonCopy.vue'
import KnobSetting from '../components/KnobSetting.vue'
import ActionChip from '../components/ActionChip.vue'
import FlowAction from '../components/FlowAction.vue'
import FlowChip from '../components/FlowChip.vue'
import TextBox from '../components/TextBox.vue'
import Layer3d from '../components/Layer3d.vue'
import FlipBook from '../components/FlipBook.vue'
import BookCollection from '../components/BookCollection.vue'
import LogEntry from '../components/LogEntry.vue'
import ImageInputAction from '../components/ImageInputAction.vue'
import CopyAction from '../components/CopyAction.vue'
import BoundingBoxIcons from '../components/BoundingBoxIcons.vue'

export default {
  components: {
    QToolbar,
    BoundingBoxIcons,
    MImage,
    Ruler,
    Protractor,
    BoundingBox,
    MImageClip,
    conLine,
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
    QLayoutDrawer,
    QLayoutFooter,
    QLayoutHeader,
    QCollapsible,
    QPageContainer,
    QList,
    FlowChip,
    TextBox,
    Layer3d,
    FlipBook,
    BookCollection,
    ImageInputAction,
    LogEntry,
    CopyAction
  },
  plugins: [Notify, ActionSheet, Dialog],
  data () {
    return {
      deleteIconSize: '75px',
      selectRectKey: 'selection',
      showScaleTilt: false,
      hideAllToggle: false,
      demoval: [{vin: 200}, {raj: 300}],
      deleteActive: false,
      transparentActive: {},
      layer3dShow: false,
      flipbookShow: false,
      selectImageMode: false,
      hiddenRect: false,
      showHeader: true,
      selectRect: false,
      showDiva: true,
      showOthers: true,
      showRight: true,
      showLeft: false,
      showFoote: true,
      loadingdata: false,
      showIcons: true,
      imagesM: [],
      attachingElements: ['imagesM', 'imagesMCrop', 'rulers', 'protractors', 'collectionBooks'],
      attachedElements: ['settingKnobs', 'chipsAction', 'actionFlows', 'boxesText', 'identifyWriters', 'matchTemplates', 'actionCopies'],
      loading: true,
      // x1 y1 x2 y2
      imagesMCrop: [],
      collectionBooks: [],
      // Change passing expicit colors
      // The component shoudl pass active/inactive etc and the local veu file shold
      actionFlowsAvailable: {
        'OpenCV Binarization': {
          controls: [
            {
              value: 0,
              min: 0,
              max: 4,
              property: 'type',
              textOptions: ['THRESH_BINARY', 'THRESH_BINARY_INV', 'THRESH_TRUNC', 'THRESH_TOZERO', 'THRESH_TOZERO_INV']
            },
            {
              value: 130,
              min: 0,
              max: 255,
              property: 'threshold'
            }
          ]
        },
        'Hough Line': {
          controls: [
            {
              value: 200,
              min: 0,
              max: 400,
              property: 'threshold'
            }
          ]
        },
        'Hough Line Prob': {
          controls: [
            {
              value: 200,
              min: 0,
              max: 400,
              property: 'threshold'
            },
            {
              value: 100,
              min: 0,
              max: 1000,
              property: 'min_length'
            },
            {
              value: 10,
              min: 0,
              max: 100,
              property: 'max_gap'
            }
          ]
        },
        'Canny': {
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
            },
            {
              value: 3,
              min: 1,
              max: 20,
              property: 'aperture_size'
            }
          ]
        },
        'Blur': {
          controls: [
            {
              value: 5,
              min: 0,
              max: 30,
              property: 'kernelX'
            },
            {
              value: 5,
              min: 0,
              max: 30,
              property: 'kernelY'
            }
          ]
        },
        'Guassian Blur': {
          controls: [
            {
              value: 5,
              min: 0,
              max: 30,
              property: 'kernelX'
            },
            {
              value: 5,
              min: 0,
              max: 30,
              property: 'kernelY'
            }
          ]
        },
        'Median Blur': {
          controls: [
            {
              value: 5,
              min: 0,
              max: 30,
              property: 'kernel'
            }
          ]
        },
        'Skeletonize': {
        },
        'Thin': {
        },
        'Bilateral Filter': {
          controls: [
            {
              value: 5,
              min: 0,
              max: 50,
              property: 'kernel'
            },
            {
              value: 5,
              min: 0,
              max: 200,
              property: 'sigma'
            }
          ]
        },
        'TopBase Lines': {
          controls: [
            {
              value: 30,
              min: 0,
              max: 400,
              property: 'scale'
            },
            {
              value: 0.5,
              min: 0,
              max: 2,
              step: 0.05,
              property: 'theta'
            }
          ]
        },
        'MidInter Lines': {
          controls: [
            {
              value: 30,
              min: 0,
              max: 400,
              property: 'scale'
            },
            {
              value: 0.5,
              min: 0,
              max: 2,
              step: 0.05,
              property: 'theta'
            }
          ]
        },
        'All Lines': {
          controls: [
            {
              value: 30,
              min: 0,
              max: 400,
              property: 'scale'
            },
            {
              value: 0.5,
              min: 0,
              max: 2,
              step: 0.05,
              property: 'theta'
            }
          ]
        },
        'Good Features to Track': {
          controls: [
            {
              value: 5,
              min: 0,
              max: 50,
              property: 'kernel'
            },
            {
              value: 5,
              min: 0,
              max: 200,
              property: 'sigma'
            }
          ]
        },
        'Histogram Eq Color': {},
        'Contour': {},
        'ORB keypoints': {},
        'Medial Axis': {},
        'NonLocal Denoising Gray': {
          controls: [
            {
              value: 10,
              min: 0,
              max: 50,
              property: 'filter_strength'
            },
            {
              value: 7,
              min: 0,
              max: 50,
              property: 'template'
            },
            {
              value: 21,
              min: 0,
              max: 100,
              property: 'search'
            }
          ]
        },
        'NonLocal Denoising Color': {
          controls: [
            {
              value: 10,
              min: 0,
              max: 50,
              property: 'filter_strength'
            },
            {
              value: 10,
              min: 0,
              max: 50,
              property: 'filter_strength_color'
            },
            {
              value: 7,
              min: 0,
              max: 50,
              property: 'template'
            },
            {
              value: 21,
              min: 0,
              max: 100,
              property: 'search'
            }
          ]
        },
        'Add Random Noise': {
          controls:
          [
            {
              value: 0,
              min: 0,
              max: 6,
              property: 'type',
              textOptions: ['gaussian', 'localvar', 'poisson', 'salt', 'pepper', 's&p', 'speckle']
            },
            {
              value: 0,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'mean',
              dependant: ['type', 'gaussian']
            },
            {
              value: 0,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'mean',
              dependant: ['type', 'speckle']
            },
            {
              value: 0.01,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'var',
              dependant: ['type', 'gaussian']
            },
            {
              value: 0.01,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'var',
              dependant: ['type', 'speckle']
            },
            {
              value: 0.05,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'amount',
              dependant: ['type', 'salt']
            },
            {
              value: 0.05,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'amount',
              dependant: ['type', 'pepper']
            },
            {
              value: 0.05,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'amount',
              dependant: ['type', 's&p']
            },
            {
              value: 0.5,
              min: 0,
              max: 1,
              step: 0.05,
              property: 'salt_vs_pepper',
              dependant: ['type', 's&p']
            }
          ]
        }
      },
      actionFlows: [],
      // Rewrite this to be generic
      chipsActionAvailable: {
        'segmentLine': {},
        'segmentChar': {},
        'textEntry': {},
        'textGoogle': {},
        'segmentHist': {
          'diva': 'Histogram Text Line Segmentation'
        },
        'segmentKraken': {
          'diva': 'Kraken Pagesegmentation'
        }
      },
      actionCopiesAvailable: {
        'copy': {},
        'compile': {}
      },
      actionCopies: [],
      chipsAction: [],
      settingKnobs: [],
      copiesCarbon: [],
      boxesText: [],
      linesCon: [],
      rulers: [],
      logs: [],
      identifyWritersAvailable: {
        'NBNN': {
          active: false,
          processing: 'NBNN',
          progress: false,
          activeItem: false,
          results: '',
          type: 'identifyWriters',
          controls: [
            {
              value: 0,
              min: 0,
              max: 1,
              property: 'type',
              textOptions: ['SIFT', 'FAST']
            },
            {
              value: 100,
              min: 0,
              max: 100,
              property: 'keypoints',
              dependant: ['type', 'FAST']
            },
            {
              value: 10,
              min: 0,
              max: 360,
              property: 'rotation',
              dependant: ['type', 'SIFT']
            }
          ],
          connectImages: [
            {
              iconShow: true,
              url: '',
              type: ''
            }
          ]
        }
      },
      identifyWriters: [],
      matchTemplatesAvailable: {
        'Word Spot.': {
          active: false,
          progress: false,
          activeItem: false,
          results: '',
          type: 'matchTemplates',
          controls: [
            {
              value: 0,
              min: 0,
              max: 1,
              property: 'method',
              textOptions: ['Corr.', 'SIFT']
            },
            {
              value: 0.5,
              min: 0,
              max: 1,
              step: 0.0125,
              property: 'threshold'
            }
          ],
          connectImages: [
            {
              iconShow: true,
              url: '',
              type: ''
            }
          ]
        }
      },
      descriptions: {
        'OpenCV Binarization': 'It converts image black and white, thereby removing any background noise and make the foreground prominent. Uses OpenCV for this process and provides two parameters than be tuned to get the desired binarized image.',
        'Otsu Binarization': 'It converts image black and white, thereby removing any background noise and make the foreground prominent. Provides optimal binarization automatically without any parameters.'
      },
      matchTemplates: [],
      // armAngles: [top, bottom]
      protractors: [],
      // coordinates: [left, top, width, height]
      boundingBoxes: [],
      toggleLinesCon: true,
      apiCall: this.$axios.create({
        baseURL: 'http://localhost:5000/amap/api',
        timeout: 15000000
      }),
      diva: this.$axios.create({
        baseURL: 'http://divaservices.unifr.ch/api/v2/',
        timeout: 60000
      })
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
      // console.log('called')
      return this.componentStyles('chipsAction')
    },
    settingKnobsStyles: function () {
      return this.componentStyles('settingKnobs')
    },
    identifyWritersStyles: function () {
      return this.componentStyles('identifyWriters')
    },
    matchTemplatesStyles: function () {
      return this.componentStyles('matchTemplates')
    },
    boxesTextStyles: function () {
      return this.componentStyles('boxesText')
    },
    actionCopiesStyles: function () {
      return this.componentStyles('actionCopies')
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
            transform: 'rotate(' + imageM.tilt + 'deg)',
            display: typeof imageM['delete'] === 'undefined' ? 'visible' : 'none'
          }
        )
      }
      return style
    },
    imagesMStylesDerived: function () {
      var style = []
      for (var i = 0; i < this.imagesM.length; i++) {
        var imageM = this.imagesM[i]
        style.push(
          {
            left: imageM.coord[0] + imageM.delCoord[0] + 'px',
            top: imageM.coord[1] + imageM.delCoord[1] - 50 + 'px',
            width: imageM.width + 'px',
            transform: 'rotate(' + imageM.tilt + 'deg)',
            display: typeof imageM['delete'] === 'undefined' ? 'visible' : 'none'
          }
        )
      }
      return style
    },
    collectionBooksStyles: function () {
      var style = []
      for (var i = 0; i < this.collectionBooks.length; i++) {
        var collectionBook = this.collectionBooks[i]
        style.push(
          {
            left: collectionBook.coord[0] + collectionBook.delCoord[0] + 'px',
            top: collectionBook.coord[1] + collectionBook.delCoord[1] + 'px',
            width: collectionBook.width + 'px',
            transform: 'rotate(' + collectionBook.tilt + 'deg)',
            display: typeof collectionBook['delete'] === 'undefined' ? 'visible' : 'none'
          }
        )
      }
      return style
    },
    collectionBooksStylesDerived: function () {
      var style = []
      for (var i = 0; i < this.collectionBooks.length; i++) {
        var collectionBook = this.collectionBooks[i]
        style.push(
          {
            left: collectionBook.coord[0] + collectionBook.delCoord[0] + 'px',
            top: collectionBook.coord[1] + collectionBook.delCoord[1] - 50 + 'px',
            width: collectionBook.width + 'px',
            transform: 'rotate(' + collectionBook.tilt + 'deg)',
            display: typeof collectionBook['delete'] === 'undefined' ? 'visible' : 'none'
          }
        )
      }
      return style
    },
    // I don't this anymore
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
            transform: 'rotate(' + ruler.tilt + 'deg)',
            display: typeof ruler['delete'] === 'undefined' ? 'visible' : 'none'
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
            top: protractor.coord[1] + protractor.delCoord[1] + 'px',
            display: typeof protractor['delete'] === 'undefined' ? 'visible' : 'none'
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
        var bBoxLeft
        var bBoxTop
        var bBoxWidth
        var bBoxHeight
        // console.log('Updating')

        if (bBox !== null && bBox.visibility) {
          // console.log('Displaying bounding boxes')
          var imageM = this[bBox.refComp][bBox.refIndex]

          // console.log('Scale of BB is' + imageM.scale)

          // console.log(imageM.scale)
          bBoxLeft = imageM.coord[0] + imageM.delCoord[0] +
                     (bBox.coord[0] / imageM.scale)
          bBoxTop = imageM.coord[1] + imageM.delCoord[1] +
                     (bBox.coord[1] / imageM.scale)
          bBoxWidth = bBox.coord[2] / imageM.scale
          bBoxHeight = bBox.coord[3] / imageM.scale

          bBox['actualCoord'] = [bBoxLeft, bBoxTop, bBoxWidth, bBoxHeight]

          // console.log(imageM)

          style.push(
            {
              left: bBoxLeft + 'px',
              top: bBoxTop + 'px',
              width: bBoxWidth + 'px',
              height: bBoxHeight + 'px',
              transform: 'rotate(' + imageM.tilt + 'deg)',
              'z-index': 201
            })
        } else {
          style.push(null)
        }
      }
      return style
    },
    // make it generic
    linesConStyles: function () {
      var style = []
      // console.log('updating connecting lines')

      console.log('We are here trying to style lines')

      console.log(this.linesCon)

      for (var i = 0; i < this.linesCon.length; i++) {
        var lineCon = this.linesCon[i]
        // var comp1 = this[lineCon.comp1][lineCon.index1]
        // var comp2 = this[lineCon.comp2][lineCon.index2]

        var boundingBoxesExist = this[lineCon.refComp1][lineCon.refIndex1] !== null &&
          this[lineCon.refComp2][lineCon.refIndex2] !== null

        var imagesExist = typeof this.imagesM[lineCon.refIndex2]['delete'] === 'undefined'
        console.log(imagesExist)
        console.log(boundingBoxesExist)
        console.log(this.boundingBoxes[lineCon.refIndex1].visibility)

        console.log(this[lineCon.refComp2][lineCon.refIndex2])

        // console.log('Trying to add lines')
        // console.log(lineCon)

        if (boundingBoxesExist && this.boundingBoxes[lineCon.refIndex1].visibility && imagesExist) {
          // console.log('creating lines')
          // console.log(lineCon)
          var x1 = parseFloat(this.boundingBoxesStyles[lineCon.refIndex1].left.replace('px'))
          var y1 = parseFloat(this.boundingBoxesStyles[lineCon.refIndex1].top.replace('px')) + parseFloat(this.boundingBoxesStyles[lineCon.refIndex1].height.replace('px'))

          console.log(x1)
          console.log(y1)

          var x2 = this[lineCon.refComp2][lineCon.refIndex2].coord[0] + this[lineCon.refComp2][lineCon.refIndex2].delCoord[0]
          var y2 = this[lineCon.refComp2][lineCon.refIndex2].coord[1] + this[lineCon.refComp2][lineCon.refIndex2].delCoord[1]

          console.log(x2)
          console.log(y2)

          lineCon.line1 = [x1, y1, x2, y2]

          // console.log(lineCon.line1)

          style.push({
            left: (x1 + 1) + 'px',
            top: (y1 - 2) + 'px'
          })
        } else {
          lineCon.delete = true
          style.push({})
        }
      }
      return style
    }
  },
  mounted: function () {
    this.getDivaList()
  },
  updated: function () {
    // update this whenever you change somethign in imageM
    this.loadingdata = false
    // console.log('Making this false')
    // console.log(this.loadingdata)

    var scaleElements = ['imagesM', 'collectionBooks']

    for (var i = 0; i < scaleElements.length; i++) {
      var elements = scaleElements[i]
      for (var j = 0; j < this[elements].length; j++) {
        // Find a better solution that below
        var imageM
        if (elements === 'imagesM') {
          imageM = this.$refs[elements + j][0].$el.childNodes[1].childNodes[0].childNodes[0].childNodes[0]
        } else if (elements === 'collectionBooks') {
          imageM = this.$refs[elements + j][0].$el.childNodes[1].childNodes[0].childNodes[1].childNodes[0].childNodes[0].childNodes[0]
        }
        this[elements][j]['widthN'] = imageM.naturalWidth
        this[elements][j]['heightN'] = imageM.naturalHeight
        var scale = imageM.naturalWidth / this[elements][j].width
        this[elements][j].scale = scale

        // console.log('The scale is ' + scale)
      }
      this.$set(this, elements, this[elements])
    }
  },
  methods: {
    // http://divaservices.unifr.ch/api/v2/imageprocessing/multiscaleinterestpointdetection/1
    // implement this. add option to read output that has visualization as true
    // think about what to do with methods that return json (points, bounding boxes, polygons)
    // Think about writnig methods for that
    // Cross check with all the methods of diva services and make sure most of them are supported
    // Write mail to marcel about the highlight parameters
    // fix the width button of the chip: function () {}
    displayScaleTilt: function () {

    },
    demoMove: function (event) {
      event['deltaX'] = event.delta.x
      event['deltaY'] = event.delta.y
      event['target'] = event.evt.target
      event['center'] = {}
      event['center']['x'] = 2
      event['center']['y'] = 1
      var node = this.getMovableElement(event)
      console.log(event.isFinal)

      event['isFinal'] = true

      console.log(typeof node)

      if (typeof node !== 'undefined') {
        this['currentMoving'] = node
      } else {
        node = this['currentMoving']
        event['target'] = node
      }

      var elements = node.id.split('-')[0]
      var index = parseInt(node.id.split('-')[1])

      if (typeof this[elements][index]['disablepan'] === 'undefined' || !this[elements][index]['disablepan']) {
        this.moveN(event)
      }
    },
    infoBox: function (methodtype) {
      this.$q.dialog({
        title: methodtype,
        message: this.descriptions[methodtype],
        position: 'right',
        ok: false
      })
    },
    hideAll: function () {
      // var dhis = this
      this.hideAllToggle = !this.hideAllToggle
    },
    updateActivePage: function (index, event) {
      this.collectionBooks[index].activePage = event

      console.log('updating for active page')
      console.log(event)

      this.hideNonActiveBoundingBoxes(index, event)
    },
    hideNonActiveBoundingBoxes: function (index, event) {
      // hide other boundingBoxes
      for (var i = 0; i < this.boundingBoxes.length; i++) {
        var bBox = this.boundingBoxes[i]

        if (bBox !== null && bBox.refComp === 'collectionBooks' && parseInt(bBox.refIndex) === parseInt(index)) {
          var bBoxPage = bBox.type.split('-')[1]
          console.log(bBox.type)
          if (parseInt(bBoxPage) === parseInt(event)) {
            bBox.visibility = true
            console.log('setting visible')
          } else {
            bBox.visibility = false
            console.log('hiding')
          }
          this.$set(this.boundingBoxes, i, bBox)
        }
      }
    },
    detachPage: function (index, event) {
      this.imagesM.push({
        coord: [0, 80],
        delCoord: [0, 0],
        width: 200,
        tilt: 0,
        scale: 0,
        urlOrig: event,
        url: event,
        textBack: 'Detached Page',
        visibility: true,
        showOriginal: false
      })
      // console.log('Detaching page')
    },
    sleep: function (ms) {
      return new Promise(resolve => setTimeout(resolve, ms))
    },
    demovalfn: function () {
    },
    deleteLog: function (index) {
      // console.log('Trying delete logs')
      this.$set(this.logs, index, null)
    },
    rerunLog: function (index) {
      var refComp = this.logs[index].refComp
      var refIndex = this.logs[index].refIndex
      var actionFlowInit = this.getConnectedEl1toEl2(refComp, refIndex, 'actionFlows')

      var error = false

      if (actionFlowInit !== false) {
        var index2 = actionFlowInit

        while (index2 !== false) {
          // console.log('Inside changing parameters')
          // console.log(this.logs[index].parameters)
          // console.log(this.actionFlows[index2].parameters)
          this.logs[index].parameters.forEach(function (block) {
            var props = block[Object.keys(block)]

            // If the recorded parameters and the action flow doesn't match don't run ayting
            if (this.actionFlows[index2].processing !== Object.keys(block)[0]) {
              // console.log(this.actionFlows[index2].processing)
              // console.log(Object.keys(block)[0])
              // console.log(this.actionFlows[index2])

              this.actionFlows[index2].error = true
              this.actionFlows[index2].preview = false

              this.$set(this.actionFlows, index2, this.actionFlows[index2])

              // console.log(this.actionFlows[index2])

              // index2 = false
              // console.log('The processing blocks do not match')
              error = true
            } else {
              for (var prop in props) {
                // console.log(prop)
                // console.log(props[prop])
                // console.log(this.actionFlows[index2].parameters[prop])
                this.actionFlows[index2].parameters[prop].value = props[prop]
              }
              // this.actionFlows[index2].controls[i].value = parameters[prop]
            }
            index2 = this.getConnectedEl1toEl2('actionFlows', index2, 'actionFlows')
            // console.log('Connected Element found here323432')
            // console.log(index2)
          }.bind(this))
        }
      }
      // console.log('I am here doing things')
      if (!error) {
        this.flowActionProcess(actionFlowInit)
      }
    },
    addSegmentBox: function (index, event) {
      if (event) {
        this['selectRectKey'] = this.chipsAction[index].action + index
      } else {
        this['selectRectKey'] = 'selection'
      }
    },
    hideBoundingBox: function (index) {
      this.boundingBoxes[index].resize = !this.boundingBoxes[index].resize

      this.$set(this.boundingBoxes, index, this.boundingBoxes[index])
    },
    deleteBoundingBox: function (index) {
      this.$set(this.boundingBoxes, index, null)
    },
    dimElements: function (elements, index, dimming) {
      for (var i = 0; i < this.attachedElements.length; i++) {
        var elementsType = this.attachedElements[i]
        for (var j = 0; j < this[elementsType].length; j++) {
          var attachedElement = this[elementsType][j]
          if (typeof attachedElement !== 'undefined' && attachedElement.refComp === elements && attachedElement.refIndex === index) {
            this[elementsType][j]['dimmed'] = dimming
            this.$set(this[elementsType], j, this[elementsType][j])

            this.dimElements(elementsType, j, dimming)
          }
        }
      }
    },
    showOriginalImagesM: function (elements, index, event) {
      var imageM = this[elements][index]

      if (event) {
        imageM['showOriginal'] = true

        this.dimElements(elements, index, true)
      } else {
        imageM['showOriginal'] = false

        this.dimElements(elements, index, false)
      }

      this.$set(this[elements], index, imageM)

      console.log('Trying to implement showing original image')
    },
    showOriginalCollectionBooks: function (elements, index, event) {
      var imageM = this[elements][index]

      if (event) {
        imageM['showOriginal'] = true

        this.dimElements(elements, index, true)
      } else {
        imageM['showOriginal'] = false

        this.dimElements(elements, index, false)
      }

      this.$set(this[elements], index, imageM)
    },
    hideBoundingBoxes: function (elements, index, event) {
      // console.log('These are the bounding boxes')
      // console.log(this.boundingBoxes)
      for (var i = 0; i < this.boundingBoxes.length; i++) {
        var bBox = this.boundingBoxes[i]

        if (bBox.refComp === elements && parseInt(bBox.refIndex) === parseInt(index)) {
          // console.log('inside')
          bBox.visibility = !event
          this.$set(this.boundingBoxes, i, bBox)
        }
      }
    },
    boundBoxResizeUL: function (index, event) {
      // console.log('resize event')

      // console.log('Direction of movement ' + event.offsetDirection)
      // console.log(event.offsetDirection)

      // console.log(this.boundingBoxes[index].actualCoord[1])
      // console.log(event.center.y)

      var diffHeight = event.center.y - this.boundingBoxes[index].actualCoord[1]
      var diffWidth = event.center.x - this.boundingBoxes[index].actualCoord[0]

      // console.log(diffHeight)

      if (this.boundingBoxes[index].resize) {
        if (event.offsetDirection === 8 || event.offsetDirection === 16) {
          if (diffHeight > 40) {
            this.boundingBoxes[index].coord[3] += event.deltaY / 4
          } else {
            this.boundingBoxes[index].coord[1] += event.deltaY / 4
            this.boundingBoxes[index].coord[3] -= event.deltaY / 4
          }
        }

        if (event.offsetDirection === 2 || event.offsetDirection === 4) {
          if (diffWidth > 40) {
            this.boundingBoxes[index].coord[2] += event.deltaX / 4
          } else {
            this.boundingBoxes[index].coord[0] += event.deltaX / 4
            this.boundingBoxes[index].coord[2] -= event.deltaX / 4
          }
        }
      }

      // console.log(this.boundingBoxes[index])

      this.$set(this.boundingBoxes, index, this.boundingBoxes[index])
      // console.log(index)
      // console.log(event)
    },
    updateSelectImageMode: function (index, elements, event) {
      this.selectImageMode = true
      this['selectImage'] = []
      this['selectImage']['elements'] = elements
      this['selectImage']['identify'] = index
      this['selectImage']['selection'] = event
    },
    selectRectangle: function (index, event) {
      this.selectRect = !this.selectRect
    },
    saveData: function () {
      const data = JSON.stringify(this._data)
      const blob = new Blob([data], {type: 'application/json'})
      const e = document.createEvent('MouseEvents')
      const a = document.createElement('a')
      a.download = 'test.json'
      a.href = window.URL.createObjectURL(blob)
      a.dataset.downloadurl = ['text/json', a.download, a.href].join(':')
      e.initEvent('click', true, false, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null)
      a.dispatchEvent(e)
    },
    loadLocalSave: async function () {
      var files = this.$refs.localSave.files

      var content = await this.readFileText(files[0])
      // console.log(content)

      var loadedData = JSON.parse(content)

      for (var prop in loadedData) {
        this[prop] = loadedData[prop]
      }

      this.loadingdata = true

      // console.log('Making this true')
      // console.log(this.loadingdata)

      // console.log(this)
    },
    copyElements: function (elements, index) {
      console.log('here trying to copy')

      var element = this[elements][index]

      var newElement = JSON.parse(JSON.stringify(element))
      newElement.coord = [0, 80]
      newElement.delCoord = [0, 0]
      newElement.showOriginal = false
      newElement.urlOrig = newElement.url

      this[elements].push(newElement)

      console.log(this[elements])
    },
    copyPage: function (index, url) {
      this.imagesM.push({
        coord: [0, 80],
        delCoord: [0, 0],
        width: this.collectionBooks[index].width,
        tilt: this.collectionBooks[index].tilt,
        scale: this.collectionBooks[index].scale,
        urlOrig: url,
        url: url,
        showOriginal: false,
        visibility: true,
        textBack: ''
      })
    },
    imagesMClick: function (index, event) {
      if (this.selectImageMode) {
        var identifyConnentImg = this[this.selectImage.elements][this.selectImage.identify].connectImages[this.selectImage.selection]

        if (identifyConnentImg.url === '') {
          this[this.selectImage.elements][this.selectImage.identify].connectImages.push({
            iconShow: true,
            url: '',
            type: ''
          })
        }

        identifyConnentImg.url = this.imagesM[index].url
        identifyConnentImg.iconShow = false
        identifyConnentImg.type = 'imagesM'

        this.selectImageMode = false

        this.$set(this[this.selectImage.elements], this.selectImage.identify, this[this.selectImage.elements][this.selectImage.identify])
      }
    },
    collectionBooksClick: function (index, event) {
      if (this.selectImageMode) {
        var identifyConnentImg = this[this.selectImage.elements][this.selectImage.identify].connectImages[this.selectImage.selection]

        if (identifyConnentImg.url === '') {
          this[this.selectImage.elements][this.selectImage.identify].connectImages.push({
            iconShow: true,
            url: '',
            type: ''
          })
        }

        identifyConnentImg.url = this.collectionBooks[index].pages[0]
        identifyConnentImg['pages'] = this.collectionBooks[index].pages
        identifyConnentImg.iconShow = false
        identifyConnentImg.type = 'collectionBooks'

        this.selectImageMode = false

        this.$set(this[this.selectImage.elements], this.selectImage.identify, this[this.selectImage.elements][this.selectImage.identify])
      }
    },
    rect: function (arg) {
      // console.log(arg)
    },
    rectCalc: function (x1, y1, x2, y2) {
      var x3 = Math.min(x1, x2)
      var x4 = Math.max(x1, x2)
      var y3 = Math.min(y1, y2)
      var y4 = Math.max(y1, y2)

      var left = x3
      var top = y3
      var width = x4 - x3
      var height = y4 - y3

      return [left, top, width, height]
    },
    rectStart: function (event) {
      // console.log('rect start')
      var node = this.getMovableElement(event)

      if (typeof node !== 'undefined' && typeof node.id !== 'undefined') {
        var elements = node.id.split('-')[0]
        var index = parseInt(node.id.split('-')[1])

        if (this.selectRect) {
          this[elements][index]['selectRect'] = []
          this[elements][index]['x1'] = event.center.x
          this[elements][index]['y1'] = event.center.y
          this[elements][index]['selectRect'] = this.rectCalc(this[elements][index]['x1'], this[elements][index]['y1'], this[elements][index]['x1'], this[elements][index]['y1'])

          this.$set(this[elements], index, this[elements][index])
        }
      }
    },
    rectMove: function (event) {
      var node = this.getMovableElement(event)

      if (typeof node !== 'undefined' && typeof node.id !== 'undefined') {
        var index = parseInt(node.id.split('-')[1])
        var elements = node.id.split('-')[0]

        if (this.selectRect) {
          this[elements][index]['x2'] = event.center.x
          this[elements][index]['y2'] = event.center.y

          this[elements][index]['selectRect'] = this.rectCalc(this[elements][index]['x1'], this[elements][index]['y1'],
            this[elements][index]['x2'], this[elements][index]['y2'])

          this.$set(this[elements], index, this[elements][index])
        }
      }
    },
    rectEnd: function (event) {
      var node = this.getMovableElement(event)
      if (typeof node !== 'undefined' && typeof node.id !== 'undefined') {
        var index = node.id.split('-')[1]
        var elements = node.id.split('-')[0]

        if (this.selectRect) {
          var imageM = this[elements][index]
          var scale = imageM.scale
          var rect = imageM.selectRect

          rect[0] -= imageM.coord[0] + imageM.delCoord[0]
          rect[1] -= imageM.coord[1] + imageM.delCoord[1]

          rect = rect.map(e => e * scale)

          if (elements === 'collectionBooks') {
            console.log('The active key is ' + this[elements][index].activePage)
            this.selectRectKey = 'selection-' + this[elements][index].activePage
          }

          this.boundingBoxes.push(
            {
              refComp: elements,
              refIndex: parseInt(index),
              type: this.selectRectKey,
              coord: rect,
              visibility: true,
              resize: false,
              locked: false
            })

          delete this[elements][index].selectRect
          this.$set(this[elements], index, this[elements][index])
        }
        // for deleting images
        this.deleteItems(elements, index)
      }
    },
    deleteItems: function (elements, index) {
      if (this.detectCollisionIcons(elements, index, 'delete') && this.deleteActive) {
        this[elements][index]['delete'] = true
        this.$set(this[elements], index, this[elements][index])

        this.deleteIconSize = '75px'
        this.transparentActive[elements + index] = false

        console.log('deleting items')

        if (elements === 'imagesM') {
          this.attachedElements.forEach(function (element) {
            this[element].forEach(function (item) {
              if (item !== null && item.refComp === 'imagesM' && item.refIndex === parseInt(index)) {
                item.delete = true
              }
            })
          }.bind(this))

          this.boundingBoxes.forEach(function (item) {
            if (item !== null && item.refComp === 'imagesM' && item.refIndex === parseInt(index)) {
              item.visibility = false
            }
          })
        }
      }
    },
    moveFinal: function (event) {
      try {
        var node = this.getMovableElement(event)
        var index = node.id.split('-')[1]
        var elements = node.id.split('-')[0]
      } catch (e) {
        console.log(e)
      }

      this.deleteItems(elements, index)
    },
    fixElements: function (elements, index, event) {
      this[elements][index]['movement'] = event

      // console.log('The movement is ' + event)
    },
    getDivaList: async function (event) {
      var result = await this.getListGet('http://divaservices.unifr.ch/api/v2/')
      var irrelevantMethods = ['ICDAR2017 HisDocLayoutComp Baseline Evaluation', 'ICDAR2017 HisDocLayoutComp Layout Evaluation', 'ICDAR2017 HisDocLayoutComp Line Evaluation',
        'Artificial Noising', 'ocropus recognize', 'Ocropus Training', 'Graph transformation', 'Image to graph']
      for (var i = 0; i < result.data.length; i++) {
        if (!irrelevantMethods.includes(result.data[i].name)) { // relvantMethods.includes(result.data[i].name)
          var methodResult = await this.getListGet(result.data[i].url)
          // Todo the first parameter cannot be a file and it can be somewhere else
          if (methodResult.data.input.length === 2 &&
              typeof methodResult.data.input[0].file['name'] !== 'undefined') {
            this.actionFlowsAvailable[result.data[i].name] = {
              service: 'diva',
              serviceUrl: result.data[i].url
            }
          } else if (methodResult.data.input.length > 2) {
            var flowOptions = []
            for (var j = 0; j < methodResult.data.input.length; j++) {
              // console.log(result.data[i].name)
              var option = methodResult.data.input[j]
              var type = Object.keys(option)[0]
              if (type === 'number') {
                flowOptions.push({
                  value: typeof option.number.options.default !== 'undefined' ? option.number.options.default : 1,
                  min: typeof option.number.options.min !== 'undefined' ? option.number.options.min : 0,
                  max: typeof option.number.options.max !== 'undefined' ? option.number.options.max : 100,
                  step: typeof option.number.options.steps !== 'undefined' ? option.number.options.steps : 1,
                  property: option.number.name
                })
              } else if (type === 'select') {
                flowOptions.push({
                  value: option.select.options.default,
                  min: 0,
                  max: option.select.options.values.length - 1,
                  property: option.select.name,
                  textOptions: option.select.options.values
                })
              }
            }
            this.actionFlowsAvailable[result.data[i].name] = {
              service: 'diva',
              serviceUrl: result.data[i].url,
              controls: flowOptions
            }
          }
        }
      }
      // console.log(this.actionFlowsAvailable)
    },
    getListGet: function (url) {
      return new Promise(resolve => {
        this.$axios.get(url, {})
          .then(function (response) {
            resolve(response)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
    },
    getResultPost: function (url, data = {}) {
      return new Promise(resolve => {
        this.$axios.post(url, data)
          .then(function (response) {
            resolve(response)
          })
          .catch(function (error) {
            console.log(error)
          })
      })
    },
    attachDrawItemsClickY: function (event) {
      event.center.y = event.center.y - 200

      this.attachDrawItems(event)
    },
    attachDrawItemsClick: function (event) {
      event.center.x = event.center.x - 400

      this.attachDrawItems(event)
    },
    // rewrite this to be modular
    attachDrawItems: function (event) {
      // console.log(event)
      var node = this.getMovableElement(event, 'stationary')
      var type = node.id.split('_')[0]
      var item = node.id.split('_')[1]
      var key = ''
      // console.log('here1')
      // console.log(type + ' ' + item)
      // console.log(type)
      // console.log(item)
      // console.log('here2')
      if (typeof this[type][item + 'new'] === 'undefined') {
        this[type][item + 'new'] = {}

        this[type][item + 'new']['coord'] = [event.center.x, event.center.y]
        this[type][item + 'new']['delCoord'] = [event.deltaX, event.deltaY]
        this[type][item + 'new']['delete'] = false
        this[type][item + 'new']['visibility'] = true
        this[type][item + 'new']['dimmed'] = false

        if (type === 'settingKnobs') {
          this[type][item + 'new']['property'] = item
          this[type][item + 'new']['active'] = false
          this[type][item + 'new']['disable'] = true
          this[type][item + 'new']['tilt'] = 0

          if (item === 'brightness') {
            this[type][item + 'new']['initValue'] = 100
            this[type][item + 'new']['min'] = 0
            this[type][item + 'new']['max'] = 400
            this[type][item + 'new']['name'] = 'brightness_low'
          } else if (item === 'contrast') {
            this[type][item + 'new']['initValue'] = 100
            this[type][item + 'new']['min'] = 0
            this[type][item + 'new']['max'] = 400
            this[type][item + 'new']['name'] = 'brightness_medium'
          } else if (item === 'grayscale') {
            this[type][item + 'new']['initValue'] = 50
            this[type][item + 'new']['min'] = 0
            this[type][item + 'new']['max'] = 100
            this[type][item + 'new']['name'] = 'format_color_fill'
          } else if (item === 'invert') {
            this[type][item + 'new']['initValue'] = 50
            this[type][item + 'new']['min'] = 0
            this[type][item + 'new']['max'] = 100
            this[type][item + 'new']['name'] = 'invert_colors'
          } else if (item === 'opacity') {
            this[type][item + 'new']['initValue'] = 50
            this[type][item + 'new']['min'] = 0
            this[type][item + 'new']['max'] = 100
            this[type][item + 'new']['name'] = 'opacity'
          } else if (item === 'hue-rotate') {
            this[type][item + 'new']['initValue'] = 0
            this[type][item + 'new']['min'] = 0
            this[type][item + 'new']['max'] = 360
            this[type][item + 'new']['name'] = 'color_lens'
          }
        } else if (type === 'chipsAction') {
          this[type][item + 'new']['action'] = item
          this[type][item + 'new']['active'] = false
          this[type][item + 'new']['loading'] = false
          this[type][item + 'new']['tilt'] = 0
          this[type][item + 'new']['visibleIcons'] = true

          // console.log(this[type + 'Available'][item])

          for (key in this[type + 'Available'][item]) {
            // console.log('copying ' + key + ' of ' + item)
            this[type][item + 'new'][key] = this[type + 'Available'][item][key]
          }
          // console.log('Here I am')
          // console.log(this[type][item + 'new'])
        } else if (type === 'actionCopies') {
          // console.log('I am here for this 333')
          this[type][item + 'new']['action'] = item
          this[type][item + 'new']['progress'] = false

          for (key in this[type + 'Available'][item]) {
            this[type][item + 'new'][key] = this[type + 'Available'][item][key]
          }
        } else if (['actionFlows', 'identifyWriters', 'matchTemplates'].includes(type)) {
          this[type][item + 'new']['active'] = false
          this[type][item + 'new']['preview'] = false
          this[type][item + 'new']['progress'] = false
          this[type][item + 'new']['active'] = false
          this[type][item + 'new']['previewUrl'] = ''
          this[type][item + 'new']['processing'] = item
          this[type][item + 'new']['controls'] = []
          this[type][item + 'new']['tilt'] = 0

          // console.log(type + 'Available')

          for (key in this[type + 'Available'][item]) {
            console.log('copying ' + key + ' of ' + item)
            if (key !== 'controls' && key !== 'connectImages') {
              this[type][item + 'new'][key] = this[type + 'Available'][item][key]
            } else {
              this[type][item + 'new'][key] = JSON.parse(JSON.stringify(this[type + 'Available'][item][key]))
            }
          }
        }
        this[type].push(this[type][item + 'new'])
      } else {
        // fix this. You cannot move two things simultaneously
        this[type][item + 'new'].delCoord = [event.deltaX, event.deltaY]

        // Check for collission and attach things
        // add collision detection here

        if (event.isFinal) {
          this[type][item + 'new'].coord[0] += event.deltaX
          this[type][item + 'new'].coord[1] += event.deltaY

          this[type][item + 'new'].delCoord = [0, 0]

          delete this[type][item + 'new']
        }
      }
    },
    componentStyles: function (elements) {
      var style = []
      for (var i = 0; i < this[elements].length; i++) {
        var element = this[elements][i]
        if (typeof element.tilt === 'undefined') {
          element['tilt'] = 0
        }

        var visibility = element.visibility

        if (element.delete) {
          visibility = false
        }

        // console.log('the visibility is ' + visibility)

        // console.log('Inside Component Style')
        // console.log(typeof element['delete'])
        // console.log(typeof element['delete'] === 'undefined' ? 'visible' : 'none')

        style.push(
          {
            left: element.coord[0] + element.delCoord[0] + 'px',
            top: element.coord[1] + element.delCoord[1] + 'px',
            transform: 'rotate(' + element.tilt + 'deg)',
            display: visibility ? 'visible' : 'none'
          }
        )
      }

      // console.log(style)

      return style
    },
    getMovableElement: function (event, type = 'movable') {
      try {
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
      } catch (e) {
        console.log(e)
      }
    },
    addLocalImageM: function () {
      // console.log('hereeeee')
      // console.log('File uploading clicked')
      this.$refs.localUpload.click()
      // console.log('here trying to add 3333')
    },
    loadData: function () {
      // console.log('hereeeee')
      this.$refs.localSave.click()
    },
    readFile: function (url) {
      return new Promise(resolve => {
        var reader = new FileReader()
        reader.onload = function () {
          resolve(reader.result)
        }
        reader.readAsDataURL(url)
      })
    },
    readFileText: function (url) {
      return new Promise(resolve => {
        var reader = new FileReader()
        reader.onload = function () {
          resolve(reader.result)
        }
        reader.readAsText(url)
      })
    },
    uploadLocalImageM: async function () {
      // console.log('here trying to add')
      var files = this.$refs.localUpload.files

      // console.log('The files are')
      // console.log(this.$refs.localUpload.files)

      if (files.length === 1) {
        var content = await this.readFile(files[0])
        this.imagesM.push({
          coord: [100, 200],
          delCoord: [0, 0],
          width: 400,
          tilt: 0,
          scale: 0,
          urlOrig: content,
          url: content,
          showOriginal: false,
          visibility: true,
          textBack: files[0].name + ' ' + files[0].type
        })
      } else {
        var pagesContent = []
        var comments = []
        for (var i = 0; i < files.length; i++) {
          pagesContent.push(await this.readFile(files[i]))
          comments.push(files[i].name + ' ' + files[i].type)
        }
        this.collectionBooks.push({
          coord: [0, 80],
          delCoord: [0, 0],
          width: 400,
          tilt: 0,
          pages: pagesContent,
          pagesOrig: pagesContent,
          activePage: 0,
          movement: true,
          comments: comments,
          previewURL: ''
        })
      }
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
      try {
        var obj1 = this.$refs[object + objectIndex][0].$el
        var rect1 = {x: obj1.offsetLeft, y: obj1.offsetTop, width: obj1.offsetWidth, height: obj1.offsetHeight}
        // console.log(object + ' ' + objectTypes)
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
      } catch (e) {
        console.log(e)
        return false
      }
    },
    flowActionChanged: function (index, parameters) {
      // console.log(this.actionFlows)

      var actionFlow = this.actionFlows[index]
      actionFlow['parameters'] = parameters.parameters
      actionFlow['loopExists'] = parameters.loopExists
      actionFlow['loopActive'] = parameters.loopActive
    },
    flowActionUpdated: async function (index, parameters) {
      // console.log('Flow Action ' + index + ' updated')

      // console.log('Flow actionupdated')

      // console.log(this.actionFlows)

      var actionFlow = this.actionFlows[index]
      actionFlow['parameters'] = parameters.parameters
      actionFlow['loopExists'] = parameters.loopExists

      // If loop exists make it loop from the beginning instead of just from the middle

      // console.log('LoopExists')
      // console.log(actionFlow['loopExists'])

      var imageMCon = this.getConnectedImageM(index)
      var actionFlowInit = this.getConnectedEl1toEl2('imagesM', imageMCon, 'actionFlows')

      var bookCollectionsCon = this.getConnectedCollectionBooks(index)

      if (imageMCon !== false && !this.loadingdata) {
        // console.log('I ma here 12345677')
        if (actionFlow.loopExists) {
          await this.flowActionProcess(actionFlowInit, [], actionFlow['loopExists'])
        } else {
          // await this.flowActionProcess(actionFlowInit, [], actionFlow['loopExists'])
          await this.flowActionProcess(index, [], actionFlow['loopExists'])
        }
      } else if (bookCollectionsCon !== false) {
        await this.flowActionProcess(index, [], actionFlow['loopExists'])
      }
    },
    encodeImageDiva: function (imgURL) {
      var postBody = {}
      // If the image is local, send the base64 versin of the image
      // else send the URL to DIVA
      if (imgURL.indexOf('base64') !== -1) {
        postBody = {
          'type': 'base64',
          'value': imgURL.split(',')[1],
          'name': 'vinodh.jpg'
        }
      } else {
        var UrlParts = imgURL.split('/')
        postBody = {
          'type': 'url',
          'value': imgURL,
          'name': UrlParts[UrlParts.length - 1].split('.')[0],
          'extension': UrlParts[UrlParts.length - 1].split('.')[1]
        }
      }
      return {'files': [postBody]}
    },
    getDivaProcessResults: async function (imgURL, URL, parameters) {
      console.log('uploading image')

      // Upload image to Diva
      var response = await this.dataPost('/collections', this.encodeImageDiva(imgURL), 'diva')
      var collection = response.data.collection

      console.log('Uploaded to ' + collection)

      var imageDivaURL = imgURL.indexOf('base64') !== -1 ? collection + '/vinodh.jpg' : collection + '/' + imgURL.split('/')[imgURL.split('/').length - 1]
      // console.log(imageDivaURL)

      // console.log(parameters)
      console.log(imageDivaURL)

      // Send the uploaded image to Diva for further processing
      response = await this.dataPost(URL, {
        'parameters': parameters,
        'data': [{'inputImage': imageDivaURL}]
      }, '$axios')

      var result

      console.log('The results are this')
      console.log(response)

      if (response !== 'error') {
        console.log('There result link is here ' + response.data.results[0].resultLink)
        result = await this.getResult(response.data.results[0].resultLink)
      } else {
        result = response
        console.log('There is an error in retrieving results')
      }

      // Delete uploaded image after posting
      this.diva.delete('/collections/' + imageDivaURL)
        .then(function (response) {
          console.log('File Deleted')
        })
        .catch(function (error) {
          console.log('File deletion error')
          console.log(error)
        })

      return new Promise(resolve => { resolve(result) })
    },
    getFlowProcessResults: async function (imgURL, actionFlow, parameters) {
      var resultURL = ''
      var response = ''

      if (actionFlow.service === 'diva') {
        var result = await this.getDivaProcessResults(imgURL, actionFlow.serviceUrl, parameters)

        // console.log('Result Received')
        // console.log(result)

        if (result !== 'error') {
          // Find the result image and update the link
          for (var i = 0; i < result.output.length; i++) {
            if (typeof result.output[i]['file'] !== 'undefined' &&
                result.output[i].file.options.visualization) {
              resultURL = result.output[i].file.url
            }
          }
        } else {
          resultURL = result
        }
      } else {
        response = await this.dataPost('/processing', {
          processing: actionFlow.processing,
          url: imgURL,
          parameters: JSON.stringify(parameters)
        }, 'apiCall')

        // console.log('Waiting for results')
        // console.log('3 Results Received')
        if (response !== 'error') {
          resultURL = response.data.results
        } else {
          resultURL = response
        }
      }

      return resultURL
    },
    getFlowProcessUpdateOthers: async function (index, imagesMCon, prevParameters = [], loopExists) {
      // search for selected components
      var actionFlowsCon = this.getConnectedEl1toEl2('actionFlows', index, 'actionFlows')
      var actionChipsCon = this.getConnectedEl1toEl2('actionFlows', index, 'chipsAction')

      console.log('Calling here' + actionFlowsCon)

      // update the related components
      if (actionFlowsCon !== false) {
        // console.log('Found actionFlows connected ' + actionFlowsCon + loopExists)
        // console.log(this.actionFlows[actionFlowsCon])
        await this.flowActionProcess(actionFlowsCon, prevParameters, loopExists)
      }

      if (actionChipsCon !== false) {
        // console.log('Found actionship connected ' + actionChipsCon)
        this.chipsAction[actionChipsCon].active = true
        this.chipsAction[actionChipsCon].loading = true
        this.boundingBoxesToggle(this.chipsAction[actionChipsCon].action + actionChipsCon, 'deletion')
        await this.actionChipAction(imagesMCon, actionChipsCon)
      }
    },
    identifyWritersProcess: async function (index, event) {
      var idW = this.identifyWriters[index]
      // console.log(idW)
      if (typeof idW['refComp'] !== 'undefined' && idW.refComp !== '') {
        // console.log('Doing Writer Identifaction')

        idW.progress = true
        idW.active = true

        if (idW.refComp === 'actionFlows') {
          var imageCon = this.getConnectedImageM(idW.refIndex)

          if (imageCon !== false) {
            event['unknown'] = {'type': 'imagesM', 'url': this['imagesM'][imageCon].url}
          }

          var booksCon = this.getConnectedCollectionBooks(idW.refIndex)

          if (booksCon !== false) {
            event['unknown'] = {'type': 'collectionBooks', 'pages': this['collectionBooks'][booksCon].pages}
          }
        } else if (idW.refComp === 'imagesM') {
          event['unknown'] = {'type': idW.refComp, 'url': this[idW.refComp][idW.refIndex].url}
        } else if (idW.refComp === 'collectionBooks') {
          console.log('The thing is connected to the collectionbooks')
          event['unknown'] = {'type': idW.refComp, 'pages': this[idW.refComp][idW.refIndex].pages}
        }

        var response = await this.dataPost('/writerid', {
          processing: 'NPNN',
          parameters: JSON.stringify(event)
        }, 'apiCall')

        var resultURL = response.data.results

        this.identifyWriters[index].results = resultURL

        this.$set(this.identifyWriters, index, this.identifyWriters[index])

        idW.progress = false
        idW.active = false
      }
    },
    matchTemplatesProcess: async function (index, event) {
      var mT = this.matchTemplates[index]
      // console.log(mT)

      var key = 'template' + index

      this.boundingBoxesToggle(key, 'deletion')

      if (typeof mT['refComp'] !== 'undefined' && mT.refComp !== '') {
        // console.log('Doing Template Matching')

        mT.progress = true
        mT.active = true
        var urlImg = ''
        var urlImgs = ''
        var imageRef = ''
        var type = ''
        var boxes = []

        if (mT.refComp === 'imagesM') {
          urlImg = this[mT.refComp][mT.refIndex].urlOrig

          imageRef = mT.refIndex
          type = 'imagesM'
        } else if (mT.refComp === 'actionFlows') {
          urlImg = this[mT.refComp][mT.refIndex].previewUrl

          imageRef = this.getConnectedImageM(mT.refIndex)
          type = 'imagesM'

          if (imageRef === false) {
            imageRef = this.getConnectedCollectionBooks(mT.refIndex)
            urlImgs = this['collectionBooks'][imageRef].pages
            type = 'collectionBooks'
          }
        } else if (mT.refComp === 'collectionBooks') {
          console.log('setting url')
          urlImgs = this[mT.refComp][mT.refIndex].pages
          console.log(urlImg)
          imageRef = mT.refIndex
          type = 'collectionBooks'
        }

        // Adding to logs

        // console.log('The parameters for matching are::')
        // console.log(event)

        var api = '/template'

        if (event.method === 'Corr.') {
          api = '/template'
        } else {
          api = '/keyword'
        }

        if (type === 'imagesM') {
          event['page'] = {'type': mT.refComp, 'url': urlImg}

          var useCachedResults = typeof this.matchTemplates[index]['prevParametersKnown'] !== 'undefined' && typeof this.matchTemplates[index]['prevParametersPage'] !== 'undefined' && event.method === 'SIFT' && this.matchTemplates[index].prevParametersKnown === JSON.stringify(event.known) && this.matchTemplates[index].prevParametersPage === JSON.stringify(event.page) && typeof this.matchTemplates[index]['cachedResults'] !== 'undefined'

          boxes = []

          if (!useCachedResults) {
            var response = await this.dataPost(api, {
              processing: 'template_matching',
              parameters: JSON.stringify(event)
            }, 'apiCall')

            boxes = response.data.boxes
          } else {
            console.log('using cached results for SIFT')
            boxes = this.matchTemplates[index]['cachedResults']
          }

          if (event.method === 'SIFT') {
            this.matchTemplates[index]['prevParametersKnown'] = JSON.stringify(event.known)
            this.matchTemplates[index]['prevParametersPage'] = JSON.stringify(event.page)
            this.matchTemplates[index]['cachedResults'] = boxes
          }

          this.addBoundingBoxesTemplates(index, boxes, event, imageRef, key, 'imagesM')
        }

        if (type === 'collectionBooks') {
          var resultPages = []
          for (var i = 0; i < urlImgs.length; i++) {
            urlImg = urlImgs[i]
            event['page'] = {'type': mT.refComp, 'url': urlImg}

            var useCachedResults2 = typeof this.matchTemplates[index]['prevParametersKnown'] !== 'undefined' && typeof this.matchTemplates[index]['prevParametersPage'] !== 'undefined' && event.method === 'SIFT' && this.matchTemplates[index].prevParametersKnown === JSON.stringify(event.known) && this.matchTemplates[index].prevParametersPage === JSON.stringify(event.page) && typeof this.matchTemplates[index]['cachedResults'] !== 'undefined'

            boxes = []

            if (!useCachedResults2) {
              var response2 = await this.dataPost(api, {
                processing: 'template_matching',
                parameters: JSON.stringify(event)
              }, 'apiCall')

              boxes = response2.data.boxes
            } else {
              console.log('using cached results for SIFT')
              boxes = this.matchTemplates[index]['cachedResults']
            }

            if (event.method === 'SIFT') {
              this.matchTemplates[index]['prevParametersKnown'] = JSON.stringify(event.known)
              this.matchTemplates[index]['prevParametersPage'] = JSON.stringify(event.page)
              this.matchTemplates[index]['cachedResults'] = boxes
            }

            resultPages.push(this.addBoundingBoxesTemplates(index, boxes, event, imageRef, key + '-' + i, 'collectionBooks'))
          }

          for (var j = 1; j < urlImgs.length; j++) {
            resultPages[0] = resultPages[0].map(function (num, idx) {
              return num + resultPages[j][idx]
            })
          }

          this.matchTemplates[index].results = resultPages[0]
        }

        // this.matchTemplates[index].results = results

        this.hideNonActiveBoundingBoxes(index, this.collectionBooks[index].activePage)

        mT.progress = false
        mT.active = false
      }
    },
    addBoundingBoxesTemplates: function (index, boxes, event, imageRef, key, refComp) {
      var color = ['green', 'orange', 'darkgreen', 'darkorange', 'purple', 'pink']

      var results = []

      for (var j = 0; j < boxes.length; j++) {
        var countBox = 0
        var tempColor = color[j]
        for (var i = 0; i < boxes[j].length; i++) {
          if ((event.method === 'SIFT' && boxes[j][i][4] >= event.threshold) ||
            event.method === 'Corr.') {
            countBox += 1
            this.boundingBoxes.push(
              {
                refComp: refComp,
                refIndex: imageRef,
                type: key,
                coord: boxes[j][i],
                color: tempColor,
                visibility: true,
                resize: false,
                locked: false
              }
            )
          }
        }
        results.push(countBox)
      }

      this.matchTemplates[index].results = results

      return results
    },
    // Processing Action Flows
    flowActionProcess: async function (index, prevParameters = [], loopExists = false) {
      var actionFlow = this.actionFlows[index]
      var imgURL = ''

      // console.log('Loop exists within ' + loopExists)
      actionFlow['error'] = false

      var collBookCon = this.getConnectedCollectionBooks(index)

      if (actionFlow.refComp === 'collectionBooks' || (actionFlow.refComp === 'actionFlows' && collBookCon !== false)) {
        var collectionBook = this.collectionBooks[collBookCon]

        var pages = []

        for (var i = 0; i < collectionBook.pages.length; i++) {
          actionFlow.preview = false
          actionFlow.progress = true
          actionFlow.active = true

          if (actionFlow.refComp === 'actionFlows') {
            imgURL = this.actionFlows[actionFlow.refIndex].previewPages[i]
          } else {
            imgURL = collectionBook.pagesOrig[i]
          }

          // console.log('The parametes are ')
          // console.log(actionFlow.parameters)

          var parameters = {}

          for (var prop in actionFlow.parameters) {
            parameters[prop] = actionFlow.parameters[prop].value
          }

          // console.log(parameters)

          let resultURL = await this.getFlowProcessResults(imgURL, actionFlow, parameters)

          pages[i] = resultURL
          actionFlow.previewUrl = resultURL

          // mark as completed
          actionFlow.preview = true
          actionFlow.progress = false

          // console.log('connected to books' + ' iteration ' + i)
          // console.log('after propagation')
          // console.log(collectionBook.previewURL)
          if (collectionBook.previewURL !== '') {
            pages[i] = collectionBook.previewURL
          }
        }
        collectionBook.previewURL = ''
        collectionBook.pages = pages
        collectionBook.comments = []

        actionFlow.previewPages = pages

        console.log('We are here trying to debug')

        this.$set(this.collectionBooks, actionFlow.refIndex, collectionBook)

        await this.getFlowProcessUpdateOthers(index, collBookCon, [], false)

        return
      }

      // Process only if the connected components are ImagesM and actionFlows
      if (actionFlow.refComp === 'imagesM' || actionFlow.refComp === 'actionFlows') {
        // Changing the status of the actionflows
        actionFlow.preview = false
        actionFlow.progress = true
        actionFlow.active = true

        var imageM = this[actionFlow.refComp][actionFlow.refIndex] /// This can mean anything not just ImageM.
        let imgURL = actionFlow.refComp === 'imagesM' ? imageM.urlOrig : imageM.previewUrl // get the image URL

        if (actionFlow.refComp === 'imagesM' && loopExists) {
          imageM.url = imageM.urlOrig
          // console.log('The first step of the processing chain')

          this.collectionBooks.push({
            coord: [0, 80],
            delCoord: [0, 0],
            width: 200,
            tilt: 0,
            pages: [],
            pagesOrig: [],
            activePage: 0,
            movement: true,
            previewURL: '',
            comments: []
          })
        }

        var valuesList = []

        // console.log('The action Flow is ')
        // console.log(JSON.stringify(actionFlow))

        if (typeof actionFlow['parameters'] === 'undefined') {
          // console.log(JSON.stringify(actionFlow))
          // console.log('Method has no parameters')
          // actionFlow.parameters = {}
        }

        var properties = Object.keys(actionFlow.parameters)
        var indexP = 0

        // console.log('Looping Begin' + JSON.stringify(actionFlow.parameters))

        for (var property in actionFlow.parameters) {
          // console.log(property)
          // console.log('The properties are ')
          // console.log(actionFlow.parameters[property])
          var values = []
          if (typeof actionFlow.parameters[property].loop === 'undefined') {
            values.push(actionFlow.parameters[property])
          } else if (actionFlow.parameters[property].loop === false) {
            // console.log(actionFlow.parameters[property].value)
            values.push(actionFlow.parameters[property].value)
          } else if (!loopExists) {
            values.push(actionFlow.parameters[property].value)
          } else {
            let loopVar = actionFlow.parameters[property].loop
            for (let i = loopVar[0]; i <= loopVar[1]; i = i + loopVar[2]) {
              // console.log(actionFlow.controls[indexP])
              // console.log('I am here')
              values.push(i)
            }
          }
          indexP = indexP + 1
          valuesList.push(values)
        }

        const flatten = (arr) => [].concat.apply([], arr)

        const product = (...sets) =>
          sets.reduce((acc, set) =>
            flatten(acc.map(x => set.map(y => [ ...x, y ]))),
          [[]])

        var parameterMatric = product(...valuesList)

        // console.log('The overall parameter space')
        // console.log(parameterMatric)

        // console.log('The list of parameters are')
        // console.log(valuesList)

        // What about things with no parameters :-/

        for (let i = 0; i < parameterMatric.length; i++) {
          actionFlow.preview = false
          actionFlow.progress = true
          actionFlow.active = true

          var pars = {}
          for (let j = 0; j < properties.length; j++) {
            if (typeof parameterMatric[i][j] !== 'string') {
              // console.log('I am here 1')
              actionFlow.controls[j].value = parameterMatric[i][j]
              // this.$set(this.actionFlows, index, actionFlow)
              // this.$set(this, 'actionFlows', this.actionFlows)
            }
            if (typeof actionFlow.controls[j].textOptions === 'undefined' ||
              typeof parameterMatric[i][j] === 'string') {
              if (typeof parameterMatric[i][j] === 'string') {
                actionFlow.controls[j].value = actionFlow.controls[j].textOptions.indexOf(parameterMatric[i][j])
              }

              pars[properties[j]] = parameterMatric[i][j]
            } else {
              // console.log('Text Options')
              pars[properties[j]] = actionFlow.controls[j].textOptions[parameterMatric[i][j]]
              actionFlow.controls[j].value = parameterMatric[i][j]
            }
            // console.log(this.actionFlows[index])
            // console.log(this.actionFlows[index])
          }

          // actionFlow.parameters = pars

          // console.log('parmeters')
          // console.log(pars)

          let resultURL = await this.getFlowProcessResults(imgURL, actionFlow, pars)

          if (resultURL !== 'error') {
            // upload image URL in the respective components
            var imagesMCon = this.getConnectedImageM(index)

            // console.log('Conected')
            // console.log(this.getConnectedEl1toEl2('actionFlows', index, 'actionFlows'))

            if (prevParameters.length === 0 && actionFlow.refComp === 'actionFlows') {
              // console.log('This is the starting of the process in the middle')
              prevParameters = this.getPreviousParameters('actionFlows', index)
              // console.log(prevParameters)
            }

            let lastParameters = []
            if (prevParameters.length > 0) {
              lastParameters = lastParameters.concat(prevParameters)
            }

            lastParameters.push({ [actionFlow.processing]: pars })

            if (imagesMCon !== false &&
              !this.getConnectedEl1toEl2('actionFlows', index, 'actionFlows')) {
              if (!loopExists) {
                let currentdate = new Date()
                let timestamp = currentdate.getDate() + '/' +
                  (currentdate.getMonth() + 1) + '/' + currentdate.getFullYear() +
                  ' @ ' + currentdate.getHours() + ':' + currentdate.getMinutes() +
                  ':' + currentdate.getSeconds()

                let log = {}

                log['input'] = this['imagesM'][imagesMCon].urlOrig
                log['refComp'] = 'imagesM'
                log['refIndex'] = imagesMCon
                log['output'] = resultURL
                log['parameters'] = lastParameters
                log['timestamp'] = timestamp

                this['imagesM'][imagesMCon].url = resultURL

                this.logs.push(log)
              }
              // console.log(actionFlow)
              // console.log('Adding pages' + i)
              if (loopExists) {
                // console.log('The parameter history is')
                // console.log(JSON.stringify(lastParameters))

                let currentdate = new Date()
                let timestamp = currentdate.getDate() + '/' +
                  (currentdate.getMonth() + 1) + '/' + currentdate.getFullYear() +
                  ' @ ' + currentdate.getHours() + ':' + currentdate.getMinutes() +
                  ':' + currentdate.getSeconds()

                let log = {}

                log['input'] = this['imagesM'][imagesMCon].url
                log['refComp'] = 'imagesM'
                log['refIndex'] = imagesMCon
                log['output'] = resultURL
                log['parameters'] = lastParameters
                log['timestamp'] = timestamp
                this.logs.push(log)

                console.log('Trying to crreat books collection')

                this.collectionBooks[this.collectionBooks.length - 1].pages.unshift(resultURL)
                this.collectionBooks[this.collectionBooks.length - 1].pagesOrig.unshift(resultURL)

                this.collectionBooks[this.collectionBooks.length - 1].comments.unshift(this.parsePars(lastParameters))

                console.log(this.collectionBooks)
              }
              // console.log(resultURL)
            }

            var collectionBooksCon = this.getConnectedCollectionBooks(index)
            // console.log('The connected book are ' + collectionBooksCon)
            if (collectionBooksCon !== false) {
              this.collectionBooks[collectionBooksCon].previewURL = resultURL
            }

            actionFlow.previewUrl = resultURL

            // console.log('5 image has beeen updated')

            // mark as completed
            actionFlow.preview = true
            actionFlow.progress = false

            this.getFlowProcessUpdateOthers(index, imagesMCon, lastParameters, loopExists)
          } else {
            actionFlow.preview = false
            actionFlow.progress = false
            actionFlow['error'] = true
          }
        }
      }
    },
    parsePars: function (parameters) {
      var parametersExpanded = ''
      for (var i = 0; i < parameters.length; i++) {
        var par = parameters[i]
        if (par === 0) {

        }
        for (var proc in par) {
          parametersExpanded += proc + ': \n'

          for (var prop in par[proc]) {
            parametersExpanded += '\t' + prop + ' ' + par[proc][prop] + '\n'
          }
          parametersExpanded += '\n\n'
        }
      }

      return parametersExpanded
    },
    // upload images and stuff to APIs
    dataPost: function (url, data, type) {
      // console.log('1 here in divapost')
      // console.log('2 Waiting for Results')
      return new Promise(resolve => {
        this[type].post(url, data)
          .then(function (response) {
            resolve(response)
          })
          .catch(function (error) {
            console.log(error)
            resolve('error')
          })
      })
    },
    // Get the result from DIVA once it has been processed
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
            } else {
              setTimeout(function () {
                resolve(dhis.getResult(url))
              }, 1000)
            }
          })
      })
    },
    logParameters: function (elements, index) {
      var pars = {}
      var parameters = this.actionFlows[index].parameters
      // console.log('loggin parameters')
      for (var prop in parameters) {
        pars[prop] = parameters[prop].value
      }
      return pars
    },
    getPreviousParameters: function (elements, index, pars = []) {
      if (elements === 'actionFlows') {
        if (this.actionFlows[index].refComp === 'imagesM') {
          pars.unshift({ [this.actionFlows[index].processing]: this.logParameters('actionFlows', index) })
          pars.pop()
          return pars
        } else if (this.actionFlows[index].refComp === 'actionFlows') {
          pars.unshift({ [this.actionFlows[index].processing]: this.logParameters('actionFlows', index) })
          return this.getPreviousParameters('actionFlows', this.actionFlows[index].refIndex, pars)
        }
      }
    },
    // get El2 element connected to El1
    getConnectedEl1toEl2: function (El1, index, El2) {
      for (var i = 0; i < this[El2].length; i++) {
        /* // console.log(this[El2][i])
        // console.log(this[El2][i].refComp !== 'undefined')
        // console.log(this[El2][i].refComp === El1)
        // console.log(this[El2][i].refIndex + typeof this[El2][i].refIndex)
        // console.log(index + typeof index)
        // console.log(this[El2][i].refIndex === index) */
        if (typeof this[El2][i].refComp !== 'undefined' &&
          this[El2][i].refComp === El1 &&
          this[El2][i].refIndex === index) {
          return i
        }
      }
      return false
    },
    getConnectedImageM: function (index) {
      if (this.actionFlows[index].refComp === 'imagesM') {
        return this.actionFlows[index].refIndex
      } else if (this.actionFlows[index].refComp === 'actionFlows') {
        return this.getConnectedImageM(this.actionFlows[index].refIndex)
      }
      return false
    },
    getConnectedCollectionBooks: function (index) {
      if (this.actionFlows[index].refComp === 'collectionBooks') {
        return this.actionFlows[index].refIndex
      } else if (this.actionFlows[index].refComp === 'actionFlows') {
        return this.getConnectedCollectionBooks(this.actionFlows[index].refIndex)
      }
      return false
    },
    moveN: function (event) {
      var node = this.getMovableElement(event)
      if (typeof node !== 'undefined' && typeof node.id !== 'undefined') {
        var elements = node.id.split('-')[0]
        var index = node.id.split('-')[1]

        if (elements === 'protractors') {
          this.moveProtractor(node, event)
        } else {
          if (!this.selectRect &&
            (this[elements][index].movement || typeof this[elements][index].movement === 'undefined')) {
            this.moveGeneric(node, event)
          }
        }
      }
    },
    detectCollisionIcons: function (object, objectIndex, type) {
      try {
        var obj1 = this.$refs[object + objectIndex][0].$el
        var rect1 = {x: obj1.offsetLeft, y: obj1.offsetTop, width: obj1.offsetWidth, height: obj1.offsetHeight}
        // console.log(rect1)
        // console.log(this.$refs[type + '-icon'])

        // console.log(object + ' ' + objectTypes)
        var obj2 = this.$refs[type + '-icon'].$el
        var rect2 = {x: obj2.offsetLeft, y: obj2.offsetTop, width: obj2.offsetWidth, height: obj2.offsetHeight}
        // console.log(rect1)
        // console.log(rect2)

        if (rect1.x < rect2.x + rect2.width &&
           rect1.x + rect1.width > rect2.x &&
           rect1.y < rect2.y + rect2.height &&
           rect1.height + rect1.y > rect2.y) {
          return true
        }
        return false
      } catch (e) {
        console.log(e)
        return false
      }
    },
    moveGeneric: function (node, event) {
      var pinchCheck = typeof this.pinchTime === 'undefined' ||
                       Date.now() - this.pinchTime > 300
      var rotateCheck = typeof this.rotateTime === 'undefined' ||
                        Date.now() - this.rotateTime > 300

      var elements = node.id.split('-')[0]
      var index = parseInt(node.id.split('-')[1])

      this.deleteIconSize = '75px'
      this.transparentActive[elements + index] = false

      // console.log('Trying to move and delete')

      if (pinchCheck && rotateCheck) {
        if (![].includes(elements)) {
          if (this.detectCollisionIcons(elements, index, 'delete') && this.deleteActive) {
            // this[elements][index]['delete'] = true
            // this.$set(this[elements], index, this[elements][index])

            this.deleteIconSize = '150px'
            this.transparentActive[elements + index] = true

            // console.log(this[elements][index])
          }
        }

        // console.log('moving here22')

        if (this.attachedElements.includes(elements)) {
          // console.log('checking collision of ' + elements)

          // For elements getting attaching to other elements

          var collide = this.detectCollision(elements, index, 'imagesM')

          if (collide !== false) {
            if (typeof this[elements][parseInt(index)].refIndex === 'undefined' ||
                this[elements][parseInt(index)].refIndex === '') { // to prevent reattaching already attached elements
              this.attachedElementsFix('imagesM', collide, elements, index, event)
            }
          }

          collide = this.detectCollision(elements, index, 'collectionBooks')

          if (collide !== false) {
            console.log('collision detected. attaching ' + elements)
            if (typeof this[elements][parseInt(index)].refIndex === 'undefined' ||
                this[elements][parseInt(index)].refIndex === '') { // to prevent reattaching already attached elements
              this.attachedElementsFix('collectionBooks', collide, elements, index, event)
            }
          }

          collide = this.detectCollision(elements, index, 'actionFlows')

          if (collide !== false) {
            // console.log('collision detected')
            if (typeof this[elements][parseInt(index)].refIndex === 'undefined' ||
                this[elements][parseInt(index)].refIndex === '') { // to prevent reattaching already attached elements
              // console.log(typeof this.actionFlows[collide].refIndex !== 'undefined')
              // console.log(this.actionFlows[collide].refIndex === parseInt(index))
              // console.log(this.actionFlows[collide].refComp === elements)
              // to prevent circular refernce
              if (typeof this.actionFlows[collide].refIndex !== 'undefined' && this.actionFlows[collide].refIndex === parseInt(index) &&
                  this.actionFlows[collide].refComp === elements) {
                // console.log('inifinte loop')
              } else {
                this.attachedElementsFix('actionFlows', collide, elements, index, event)
              }
            }
          }
        }

        collide = this.detectCollision(elements, index, 'matchTemplates')

        if (collide !== false && (elements !== 'imagesM' && elements !== 'collectionBooks' && elements !== 'actionCopies')) {
          // console.log('collision detected')
          // console.log(elements)
          this[elements][index].coord[0] += 20
        }

        if (collide !== false && elements === 'actionCopies') {
          // console.log('attached actioncopies to chipsaction')
          this.attachedElementsFix('matchTemplates', collide, elements, index, event)
        }

        collide = this.detectCollision(elements, index, 'identifyWriters')

        if (collide !== false && !['imagesM', 'actionFlows', 'collectionBooks'].includes(elements)) {
          console.log('collision detected')
          this[elements][index].coord[0] += 20
        }

        collide = this.detectCollision(elements, index, 'chipsAction')

        if (collide !== false && elements === 'actionFlows') {
          // console.log('collision detected')
          this[elements][index].coord[0] += 20
        }

        if (collide !== false && elements === 'actionCopies') {
          // console.log('attached actioncopies to chipsaction')
          this.attachedElementsFix('chipsAction', collide, elements, index, event)
        }

        if (['imagesM', 'actionFlows', 'collectionBooks', 'identifyWriters', 'matchTemplates', 'chipsAction'].includes(elements)) {
          this.positionImagesAttach(elements, parseInt(index), event, 'move')
        }

        this.moveComponent(elements, index, event)
      }
    },
    attachedElementsFix: function (nonMoving, nonMovingIndex, moving, movingIndex, event) {
      // this[moving][movingIndex].coord[0] += this[moving][movingIndex].delCoord[0]
      // this[moving][movingIndex].coord[1] += this[moving][movingIndex].delCoord[1]

      // this[moving][movingIndex].delCoord[0] = 0
      // this[moving][movingIndex].delCoord[1] = 0

      var previousConnected = false

      for (var i = 0; i < this.attachedElements.length; i++) {
        if (nonMoving === 'imagesM' &&
            this.getConnectedEl1toEl2(nonMoving, nonMovingIndex, this.attachedElements[i]) !== false &&
            this.attachedElements[i] !== 'settingKnobs') {
          previousConnected = true
          this[moving][movingIndex].coord[0] += 20
          // console.log('A previous connection exists')
        }
      }

      if (!previousConnected || moving === 'settingKnobs') {
        this[moving][movingIndex]['refComp'] = nonMoving
        // console.log('here22')
        this.$refs[moving + 'Touch' + movingIndex][0].disable('pan')
        this[moving][movingIndex]['disablepan'] = true
        // console.log('here33')

        this[moving][movingIndex]['refIndex'] = parseInt(nonMovingIndex)
        event.isFinal = true

        if (moving === 'settingKnobs') {
          this.settingKnobs[movingIndex].active = true
          this.settingKnobs[movingIndex].disable = false
        } else if (moving === 'actionCopies') {
          this.actionCopies[movingIndex].progress = true
          this.$set(this.actionCopies, movingIndex, this.actionCopies[movingIndex])
          this.repeatAction(this.actionCopies[movingIndex])
          this.actionCopies[movingIndex].progress = false
        } else if (moving === 'chipsAction') {
          if (this.chipsAction[movingIndex].refComp === 'imagesM') {
            this.chipsAction[movingIndex].active = true
            this.chipsAction[movingIndex].loading = true
            this.chipsAction[movingIndex]['imageRef'] = nonMovingIndex
            this.actionChipAction(nonMovingIndex, movingIndex)
          } else if (this.chipsAction[movingIndex].refComp === 'actionFlows' &&
              this.actionFlows[nonMovingIndex].previewUrl !== '') {
            this.chipsAction[movingIndex].active = true
            this.chipsAction[movingIndex].loading = true

            var imagesMCon = this.getConnectedImageM(nonMovingIndex)
            if (imagesMCon !== false) {
              this.chipsAction[movingIndex]['imageRef'] = imagesMCon
              this.actionChipAction(imagesMCon, movingIndex)
            }

            var collectionBooksCon = this.getConnectedCollectionBooks(movingIndex)
            if (collectionBooksCon !== false) {
              this.chipsAction[movingIndex]['imageRef'] = collectionBooksCon
              this.actionChipAction(collectionBooksCon, movingIndex, 'collectionBooks')
            }
          } else if (this.chipsAction[movingIndex].refComp === 'collectionBooks') {
            this.chipsAction[movingIndex].active = true
            this.chipsAction[movingIndex].loading = true
            this.chipsAction[movingIndex]['booksRef'] = nonMovingIndex
            this.actionChipAction(nonMovingIndex, movingIndex, 'collectionBooks')
            console.log('We are here trying to implement this feature')
          }
        } else if (moving === 'actionFlows') {
          if (nonMoving === 'imagesM' ||
              nonMoving === 'collectionBooks' ||
             (nonMoving === 'actionFlows' &&
              this.actionFlows[nonMovingIndex].previewUrl !== '')) {
            if (!this.actionFlows[movingIndex].loopActive) {
              this.actionFlows[movingIndex].active = true
              this.flowActionProcess(movingIndex)
            }
          }
        }
      }
      // console.log(this.actionFlows)
    },
    // Repositioning all things attached to the main ImageM elemeent
    positionImagesAttach: function (elements, index, event, type, category = 'start') {
      // Move the knobs associted with the image as well
      // console.log('moving everything')
      for (var i = 0; i < this.attachedElements.length; i++) {
        var elementsType = this.attachedElements[i]
        // console.log('moving type ' + elementsType)
        // console.log(elementsType)
        for (var j = 0; j < this[elementsType].length; j++) {
          var attachedElement = this[elementsType][j]
          // console.log('attached element')
          // console.log(attachedElement)
          if (attachedElement.refComp === elements && attachedElement.refIndex === index) {
            // console.log('moving ' + elementsType + ' ' + j + 'attached to' + elements + ' ' + index)
            if (type === 'move') {
              // console.log('moving....' + elementsType)
              this.moveComponent(elementsType, j, event)
              this.positionImagesAttach(elementsType, j, event, type)
            } else if (type === 'scale') {
              if (category === 'start') {
                attachedElement['oldCoord'] = attachedElement.coord.slice(0)
              }

              var oldCoord = attachedElement.coord.slice(0)

              this.scaleComponent(elementsType, j, event)

              var eventScale = {}

              eventScale['center'] = {}
              eventScale['center']['x'] = 0.001
              eventScale['center']['y'] = 0.001
              eventScale['deltaX'] = attachedElement.coord[0] - oldCoord[0]
              eventScale['deltaY'] = attachedElement.coord[1] - oldCoord[1]
              eventScale['isFinal'] = true
              // console.log('eventScale')
              // console.log(eventScale)
              this.positionImagesAttach(elementsType, j, eventScale, 'move')
            } else if (type === 'rotate') {
              attachedElement['oldCoord'] = attachedElement.coord.slice(0)
              this.rotateComponent(elementsType, j, event)
              this.positionImagesAttach(elementsType, j, event, type)
            }
          }
        }
      }
    },
    // Rotate the invidivudal attached components
    // Event has the differental rotation in degrees
    rotateComponent: function (elements, index, event) {
      // console.log('Trying to rotate Component')
      // console.log(this[elements][index])
      this[elements][index].tilt -= event

      // console.log('Total tilt ' + this[elements][index].tilt)

      // console.log('I am rotating through ' + event + ' degrees')

      event = -event * (Math.PI / 180)

      // console.log('I am rotating through ' + event + ' radians')

      var oldCoord = this[elements][index].coord.slice(0)

      // console.log(this[elements][index])
      // console.log(oldCoord)

      var imageRef = this[elements][index].refIndex

      var imageM = this.imagesM[imageRef]
      // var imageHTML = this.$refs['imagesM' + imageRef][0].$el.firstChild
      var width = imageM.width
      // var height = (imageHTML.naturalHeight / imageM.scale)
      var height = (imageM.heightN / imageM.scale)

      var rx = imageM.coord[0] + (width / 2)
      var ry = imageM.coord[1] + (height / 2)

      // console.log('centre of rotation' + rx + ' ' + ry)

      this[elements][index].coord[0] = (oldCoord[0] - rx) * Math.cos(event) - (oldCoord[1] - ry) * Math.sin(event) + rx
      this[elements][index].coord[1] = (oldCoord[1] - ry) * Math.cos(event) + (oldCoord[0] - rx) * Math.sin(event) + ry

      // console.log('Old Coordinates')
      // console.log(oldCoord)
      // console.log('New Coordinates')
      // console.log(this[elements][index].coord)

      this.$set(this[elements], index, this[elements][index])

      // and also translate the elements
    },
    scaleComponent: function (elements, index, event) {
      // event here is just the scale factor
      // http://studylib.net/doc/5892312/scaling-relative-to-a-fixed-point-using-matrix-using-the
      // Use the top, left coordinates of the image as the fixed point
      // https://books.google.de/books?id=Ng5Qa15MZ84C&pg=PA79&lpg=PA79&dq=2d+scaling+relative&source=bl&ots=LPmgxlB-i4&sig=6hgo-0DuOJSWRk4wLuswn4MQcGw&hl=en&sa=X&ved=0ahUKEwiMnJy18oXaAhVNr6QKHXnsC3YQ6AEINjAB#v=onepage&q=2d%20scaling%20relative&f=false

      // console.log('scaling component')

      this[elements][index].coord[0] = event.scale * this[elements][index].oldCoord[0] + event.left * (1 - event.scale)

      if (elements !== 'boxesText') {
        // all other cases
        this[elements][index].coord[1] = event.scale * this[elements][index].oldCoord[1] + event.top * (1 - event.scale)
      } else {
        // if it's boxexTest
        var imageMRef = this.boxesText[index].refIndex
        var imageM = this.imagesM[imageMRef]
        var imageHTML = this.$refs['imagesM' + imageMRef][0].$el
        var height = imageHTML.naturalHeight / imageM.scale

        this[elements][index].oldCoord[1] = event.scale * this[elements][index].oldCoord[1] + event.top * (1 - event.scale) +
                                          ((this[elements][index].height + 47) * event.scale) - height - 47
        this[elements][index].height = height
        this[elements][index].width = imageM.width
      }

      this.$set(this[elements], index, this[elements][index])
    },
    moveComponent: function (elements, index, event) {
      // The extra condition here and the if condition below is to prevent objects from flying away after disocnnection
      // for some reason, after disocnnectiong (with a double click), a continous motions resets the center to 0,0
      if (event.center.x !== 0 && event.center.y !== 0) {
        this[elements][index].delCoord[0] = event.deltaX
        this[elements][index].delCoord[1] = event.deltaY

        this.$set(this[elements], index, this[elements][index])
        // console.log('updating not zero')
      }

      if (event.isFinal && event.center.x !== 0 && event.center.y !== 0) {
        // console.log(event.deltaX)
        // console.log(event.deltaY)

        console.log('Finalizing the move')

        this[elements][index].coord[0] += event.deltaX
        this[elements][index].coord[1] += event.deltaY

        this[elements][index].delCoord = [0, 0]

        this.$set(this[elements], index, this[elements][index])
        // console.log('updating not zero 2')
      }
    },
    moveProtractor: function (node, event) {
      if (event.target.className.indexOf('arm') !== -1) {
        this.moveProtractorArm(node, event)
      } else {
        this.moveGeneric(node, event)
      }
    },
    moveProtractorArm: function (node, event) {
      // console.log('Arms')
      // console.log(event.target.className)

      var index = node.id.split('-')[1]

      if (event.additionalEvent === 'pandown' ||
          event.additionalEvent === 'panright') {
        if (event.target.className.indexOf('top') !== -1) {
          this.protractors[index].armAngles[0] += 1
        } else {
          this.protractors[index].armAngles[1] += 1
        }
      } else if (event.additionalEvent === 'panup' ||
        event.additionalEvent === 'panleft') {
        if (event.target.className.indexOf('top') !== -1) {
          this.protractors[index].armAngles[0] -= 1
        } else {
          this.protractors[index].armAngles[1] -= 1
        }
      }
      this.$set(this.protractors, index, this.protractors[index])
    },
    scaleN: function (category, event) {
      var node = this.getMovableElement(event)

      // console.log('Pinch movement ' + category)

      this.scaleGeneric(node, event, category)
    },
    zoomClick: function (elements, index, type) {
      console.log('We are here')
      if (type === 'in') {
        this[elements][index].width = this[elements][index].width * 1.05
        this[elements][index].scale = this[elements][index].scale * 1.05
      }
      if (type === 'out') {
        this[elements][index].width = this[elements][index].width * 0.95
        this[elements][index].scale = this[elements][index].scale * 0.95
      }
      var category = ''
      var eventScale = {}
      eventScale['scale'] = event.scale
      eventScale['top'] = this[elements][index].coord[1]
      eventScale['left'] = this[elements][index].coord[0]
      this.positionImagesAttach(elements, parseInt(index), eventScale, 'scale', category)
      this.$set(this[elements], index, this[elements][index])
    },
    scaleGeneric: function (node, event, category) {
      var rotateCheck = typeof this.rotateTime === 'undefined' ||
                        Date.now() - this.rotateTime > 300

      // rotateCheck = true

      if (rotateCheck) {
        var elements = node.id.split('-')[0]
        var index = node.id.split('-')[1]

        if (category === 'start') {
          this[elements][index]['initScale'] = this[elements][index].scale
          this[elements][index]['initWidth'] = this[elements][index].width
          event.scale = 1
        }

        // console.log('Scaled! ' + event.scale)
        // console.log(event)

        // console.log(event.velcocity)

        // scale slowly if it's a ruler
        /* (elements === 'rulers') {
          scaleFactor = 1
        } */

        this[elements][index].width = this[elements][index]['initWidth'] * event.scale
        // console.log('New Width ' + this[elements][index]['initWidth'] * event.scale)

        if (elements === 'imagesM' || elements === 'collectionBooks') {
          // var imageM = this.$refs[elements + index][0].$el
          // var scale = imageM.naturalWidth / this[elements][index].width
          // console.log('calc ' + scale)
          // console.log('mult ' + this[elements][index].scale / scaleFactor)
          this[elements][index].scale = this[elements][index]['initScale'] / event.scale
          // make this work for all connection components
          // fix rotating
          // then fix imagecrop
          var eventScale = {}
          eventScale['scale'] = event.scale
          eventScale['top'] = this[elements][index].coord[1]
          eventScale['left'] = this[elements][index].coord[0]
          this.positionImagesAttach(elements, parseInt(index), eventScale, 'scale', category)
        }

        this.$set(this[elements], index, this[elements][index])

        this.pinchTime = Date.now()
      }
    },
    rotateN: function (event) {
      var node = this.getMovableElement(event)

      this.rotateGeneric(node, event)
    },
    rotateClick: function (elements, index, direction) {
      if (direction === 'right') {
        this[elements][index].tilt += 5
      }
      if (direction === 'left') {
        this[elements][index].tilt -= 5
      }

      this.$set(this[elements], index, this[elements][index])
      this.positionImagesAttach(elements, parseInt(index), this[elements][index].actRotation, 'rotate')
    },
    rotateGeneric: function (node, event) {
      var elements = node.id.split('-')[0]
      var index = node.id.split('-')[1]

      var rotate = false
      if (event.velocity === 0) {
        this[elements][index]['initRotation'] = event.rotation
        this[elements][index]['initDistance'] = event.distance
      } else {
        this[elements][index]['actRotation'] = this[elements][index].initRotation - event.rotation
        this[elements][index]['actDistance'] = Math.abs(this[elements][index].initDistance - event.distance)
        // console.log('Rot Difference ' + this[elements][index]['actRotation'])
        // console.log('Rot Distance ' + this[elements][index]['actDistance'])
        this[elements][index].initRotation = event.rotation
        rotate = true
      }
      if (rotate && Math.abs(this[elements][index].actRotation < 10)) {
        this[elements][index].tilt -= this[elements][index].actRotation
        this.$set(this[elements], index, this[elements][index])
        this.positionImagesAttach(elements, parseInt(index), this[elements][index].actRotation, 'rotate')
        // console.log('rotated!')
        this.rotateTime = Date.now()
      }
    },
    disconnectComp: function (event) {
      var node = this.getMovableElement(event)
      this.disconnectComponent(node, event)
    },
    disconnectComponent: function (node, event, completeDiscon = true) {
      var elements = node.id.split('-')[0]
      var index = node.id.split('-')[1]

      if (this[elements][index].refComp !== '' &&
          typeof this[elements][index].refComp !== 'undefined') {
        this.disconnectCompGeneric(node, event, completeDiscon)

        this.attachedElements.forEach(function (element) {
          var i = 0

          this[element].forEach(function (item) {
            if (item.refComp === elements && item.refIndex === parseInt(index)) {
              // console.log('disconnecting connected components ' + elements + i)
              var node = {}
              node['id'] = element + '-' + i
              this.disconnectComponent(node, '', false)
            }

            i += 1
          }.bind(this))
        }.bind(this))
      }
    },
    disconnectCompGeneric: function (node, event, completeDiscon = true) {
      var elements = node.id.split('-')[0]
      var index = node.id.split('-')[1]

      // console.log('disonnecting ' + elements + ' ' + index)

      this[elements][index].active = false
      this.$refs[elements + 'Touch' + index][0].enable('pan')
      this[elements][index]['disablepan'] = false

      // This must be propagated over the chain.
      if (elements === 'settingKnobs') {
        this[elements][index].disable = true
        this[elements][index].coord[1] += 40
      } else if (elements === 'chipsAction') {
        this[elements][index].coord[0] += 40
        this.boundingBoxesToggle(this[elements][index].action + index, 'deletion')
      } else if (elements === 'identifyWriters' || elements === 'matchTemplates') {
        /** this[elements][index].connectImages = [
          {
            iconShow: true,
            url: '',
            type: ''
          }
        ] **/
        this[elements][index].results = []
        this[elements][index].coord[0] += 40

        if (elements === 'matchTemplates') {
          var key = 'template' + index
          this.boundingBoxesToggle(key, 'deletion')
          // bounding box disoconnection for collection books
        }
      } else if (elements === 'actionFlows') {
        this[elements][index].coord[0] += 40
        this[elements][index].preview = false
        this[elements][index].previewUrl = ''
        this[elements][index]['error'] = false
        this[elements][index]['dimmed'] = false

        if (this.actionFlows[index].refComp === 'imagesM') {
          // update the image to the original URL
          this.imagesM[this.actionFlows[index].refIndex].url = this.imagesM[this.actionFlows[index].refIndex].urlOrig
        } else if (this.actionFlows[index].refComp === 'actionFlows') {
          // Update the image to the previous connect component
          var imageMCon = this.getConnectedImageM(index)
          try {
            this.imagesM[imageMCon].url = this.actionFlows[this.actionFlows[index].refIndex].previewUrl
          } catch (err) {
            // console.log(err)
          }

          var collectionBooksCon = this.getConnectedCollectionBooks(index)
          try {
            this.collectionBooks[collectionBooksCon].pages = this.actionFlows[this.actionFlows[index].refIndex].previewPages
          } catch (err) {
            // console.log(err)
          }
        } else if (this.actionFlows[index].refComp === 'collectionBooks') {
          this.collectionBooks[this.actionFlows[index].refIndex].pages = this.collectionBooks[this.actionFlows[index].refIndex].pagesOrig
        }
      } else {
        this[elements][index].coord[0] += 40
      }

      if (completeDiscon) {
        this[elements][index].refComp = ''
        this[elements][index].refIndex = ''
      }

      this.$set(this[elements], index, this[elements][index])
    },
    swipeKnob: function (event) {
      // console.log(event)
    },
    // Fix this for flowchips, actioships with preprocessing and books
    repeatAction: async function (actionCopy) {
      var imagesMCon
      var rootComp
      console.log('I am here for copying')
      console.log(actionCopy)

      // console.log(actionCopy.progress)
      if (actionCopy.refComp === 'imagesM') {
        rootComp = 'imagesM'
        imagesMCon = actionCopy.refIndex
      } else if (actionCopy.refComp === 'collectionBooks') {
        rootComp = 'collectionBooks'
        imagesMCon = actionCopy.refIndex
      } else if (actionCopy.refComp === 'chipsAction') {
        imagesMCon = this.chipsAction[actionCopy.refIndex].imageRef
        // console.log(imagesMCon + 'connected to imagesM')
      } else if (actionCopy.refComp === 'actionFlows') {
        imagesMCon = this.getConnectedImageM(actionCopy.refIndex)
        rootComp = 'imagesM'
        if (imagesMCon === false) {
          imagesMCon = this.getConnectedCollectionBooks(actionCopy.refIndex)
          rootComp = 'collectionBooks'
        }
      } else if (actionCopy.refComp === 'matchTemplates') {
        if (this.matchTemplates[actionCopy.refIndex].refComp === 'imagesM') {
          rootComp = 'imagesM'
          imagesMCon = actionCopy.refIndex
        } else if (this.matchTemplates[actionCopy.refIndex].refComp === 'collectionBooks') {
          rootComp = 'collectionBooks'
          imagesMCon = actionCopy.refIndex
        } else if (this.matchTemplates[actionCopy.refIndex].refComp === 'actionFlows') {
          imagesMCon = this.getConnectedImageM(actionCopy.refIndex)
          rootComp = 'imagesM'
          if (imagesMCon === false) {
            imagesMCon = this.getConnectedCollectionBooks(actionCopy.refIndex)
            rootComp = 'collectionBooks'
          }
        }
      }

      var prevHeight = 0
      console.log(rootComp)

      if (actionCopy.action === 'compile') {
        this.collectionBooks.push({
          coord: [0, 80],
          delCoord: [0, 0],
          width: 200,
          tilt: 0,
          pages: [],
          pagesOrig: [],
          activePage: 0,
          movement: true,
          previewURL: '',
          comments: []
        })
      }

      for (var i = 0; i < this.boundingBoxes.length; i++) {
        var bBox = this.boundingBoxes[i]

        var condition = bBox !== null && bBox.refComp === rootComp && parseInt(bBox.refIndex) === parseInt(imagesMCon)

        if (rootComp === 'collectionBooks') {
          var collectionBook = this.collectionBooks[imagesMCon]
          condition = condition && (parseInt(bBox.type.split('-')[1]) === parseInt(collectionBook.activePage))
        }

        if (condition) {
          var imageM

          if (rootComp === 'imagesM') {
            imageM = this.imagesM[imagesMCon]
          } else if (rootComp === 'collectionBooks') {
            imageM = {}
            imageM['url'] = this.collectionBooks[imagesMCon].pages[this.collectionBooks[imagesMCon].activePage]
            imageM['coord'] = collectionBook.coord
            imageM['scale'] = collectionBook.scale
            imageM['tilt'] = collectionBook.tilt
          }

          var cropWidth, x, y

          cropWidth = bBox.coord[2] / imageM.scale
          x = imageM.coord[0] - cropWidth - 20
          y = imageM.coord[1] + prevHeight
          prevHeight = prevHeight + (bBox.coord[3] / imageM.scale) + 20

          // console.log(x + ' ' + y + ' ' + prevHeight)

          if (actionCopy.action === 'copy') {
            actionCopy.progress = true
            this.copyImage(imageM, bBox, i, x, y, rootComp)
          } else if (actionCopy.action === 'compile') {
            this.linesCon.push({
              refComp1: 'boundingBoxes',
              refIndex1: i,
              refComp2: 'collectionBooks',
              refIndex2: this.collectionBooks.length - 1,
              delete: false
            })
            var src = await this.cropImage(imageM, bBox, rootComp)
            this.collectionBooks[this.collectionBooks.length - 1].pages.push(src)
            this.collectionBooks[this.collectionBooks.length - 1].pagesOrig.push(src)
          }
        }
      }
      // actionCopy.progress = false
    },
    cropImage: function (imageM, bBox, type = 'imagesM') {
      return new Promise(resolve => {
        var jimpSrc = imageM.url

        if (jimpSrc.indexOf('http://') === -1) {
          jimpSrc = Buffer.from(jimpSrc.replace(/^data:image\/\w+;base64,/, ''), 'base64').buffer
        }

        window.Jimp.read(jimpSrc).then(function (imgSrc) {
          imgSrc.crop(bBox.coord[0], bBox.coord[1], bBox.coord[2], bBox.coord[3])

          imgSrc.getBase64(window.Jimp.AUTO, function (err, src) {
            resolve(src)
            if (err) {
              // console.log(err)
            }
          })
        })
          .catch(function (err) {
            console.error(err)
          })
      })
    },
    copyImageSelected: function (event) {
      var index = event.target.id.split('-')[1]

      var bBox = this.boundingBoxes[index]
      bBox.locked = true

      var imageM, cropWidth, x, y

      if (bBox.refComp === 'imagesM') {
        imageM = this[bBox.refComp][bBox.refIndex]

        cropWidth = bBox.coord[2] / imageM.scale

        x = imageM.coord[0] - cropWidth - 20
        y = imageM.coord[1]

        this.copyImage(imageM, bBox, index, x, y)
      }

      if (bBox.refComp === 'collectionBooks') {
        var collectionBook = this[bBox.refComp][bBox.refIndex]

        cropWidth = bBox.coord[2] / collectionBook.scale

        x = collectionBook.coord[0] - cropWidth - 20
        y = collectionBook.coord[1]

        console.log(collectionBook)

        imageM = {}
        imageM['scale'] = collectionBook.scale
        imageM['url'] = collectionBook.pages[collectionBook.activePage]

        this.copyImage(imageM, bBox, index, x, y)
      }
    },
    copyImage: function (imageM, bBox, index, x, y, type = 'imagesM') {
      var jimpSrc = imageM.showOriginal ? imageM.urlOrig : imageM.url

      console.log('here for copying')

      // ## Copy from URL :: This is not yet implemented
      if (jimpSrc.indexOf('http://') === -1) {
        jimpSrc = Buffer.from(jimpSrc.replace(/^data:image\/\w+;base64,/, ''), 'base64').buffer
      }

      // var cropUrl = ''

      var dhis = this

      window.Jimp.read(jimpSrc).then(function (imgSrc) {
        imgSrc.crop(bBox.coord[0], bBox.coord[1], bBox.coord[2], bBox.coord[3])

        imgSrc.getBase64(window.Jimp.AUTO, function (err, src) {
          // console.log('crop')

          var cropWidth = bBox.coord[2] / imageM.scale

          var newImage = {
            coord: [x, y],
            delCoord: [0, 0],
            width: cropWidth < 100 ? 100 : cropWidth,
            tilt: imageM.tilt,
            scale: 0,
            urlOrig: src,
            url: src,
            showOriginal: false,
            visibility: true,
            backText: ''
          }

          dhis.imagesM.push(newImage)

          dhis.linesCon.push({
            refComp1: 'boundingBoxes',
            refIndex1: index,
            refComp2: 'imagesM',
            refIndex2: dhis.imagesM.length - 1,
            delete: false
          })

          if (err) {
            // console.log(err)
          }
        })
      })
        .catch(function (err) {
          console.error(err)
        })

      // console.log('crop2')
      // console.log(cropUrl)

      // Copy image attributes to make sure the copied part is independent of changes in the original image
      /* var newImageMCrop = {
        coord: [0, 580],
        delCoord: [0, 0],
        width: imageM.width,
        tilt: imageM.tilt,
        scale: imageM.scale,
        url: cropUrl,
        clipCoord: bBox.coord.slice()
      }

      this.imagesMCrop.push(newImageMCrop) */

      /* Notify.create({
        html: 'Section copied',
        icon: 'content_copy',
        timeout: 2500,
        detail: 'copied'
      }) */
    },
    onCtxOpen: function (locals) {
      this.CtxRef = locals.ref
    },
    actionChipAction: async function (imageRef, index, elements = 'imagesM') {
      var actionChip = this.chipsAction[index]
      if (actionChip.action === 'segmentHist') {
        await this.segmentImagesM(imageRef, index, 'diva', elements)
      } else if (actionChip.action === 'segmentKraken') {
        await this.segmentImagesM(imageRef, index, 'diva', elements)
      } else if (actionChip.action.indexOf('segment') !== -1) {
        await this.segmentImagesM(imageRef, index, 'tesseract', elements)
      } else if (actionChip.action === 'textEntry') {
        await this.textEntryCreate(imageRef, index)
      } else if (actionChip.action === 'textGoogle') {
        await this.textEntryOCRCreate(imageRef, index)
      }
    },
    textEntryOCRCreate: async function (imageRef, actionChip) {
      // console.log()
      var data = {
        'requests': [
          {
            'image': {
              'content': this.imagesM[imageRef].url.split(',')[1]
            },
            'features': [
              {
                'type': 'DOCUMENT_TEXT_DETECTION'
              }
            ]
          }
        ]
      }

      // console.log(data)

      // console.log('Sending Results')
      var result = await this.getResultPost('https://vision.googleapis.com/v1/images:annotate?key=', data)
      // console.log('Got the results back')
      var text = result.data.responses[0].fullTextAnnotation.text

      this.chipsAction[actionChip].loading = false
      var imageM = this.imagesM[imageRef]
      // var imageHTML = this.$refs['imagesM' + imageRef][0].$el.firstChild
      var width = (imageM.widthN / imageM.scale)
      var height = (imageM.heightN / imageM.scale)

      this.boxesText.push({
        coord: [imageM.coord[0] - width - 47, imageM.coord[1]],
        delCoord: [0, 0],
        refComp: 'imagesM',
        refIndex: imageRef,
        width: imageM.width,
        text: text,
        'height': height,
        visibility: true,
        disability: false
      })
      // console.log(this.boxesText[0])
    },
    textEntryCreate: function (imageRef, actionChip) {
      this.chipsAction[actionChip].loading = false
      var imageM = this.imagesM[imageRef]
      // var imageHTML = this.$refs['imagesM' + imageRef][0].$el.firstChild
      var height = (imageM.heightN / imageM.scale)
      this.boxesText.push({
        coord: [imageM.coord[0], imageM.coord[1] - height - 47],
        delCoord: [0, 0],
        refComp: 'imagesM',
        refIndex: imageRef,
        width: imageM.width,
        'height': height,
        text: '',
        visibility: true,
        disability: false
      })
      // console.log(this.boxesText[0])
    },
    segmentImagesM: async function (imageRef, index, type = 'tesseract', elements = 'imagesM') {
      var response = ''
      var boxes = []
      var i = 0
      var j, box, value, actionFlow, results, json, pointList

      var segmentMode = {
        segmentBlock: 0,
        segmenetPara: 1,
        segmentLine: 2,
        segmentWord: 3,
        segmentChar: 4
      }

      var actionChip = this.chipsAction[index]

      if (elements === 'imagesM') {
        if (type === 'tesseract') {
          // console.log('tesseract type')
          response = await this.dataPost('/segment/tesseract', {
            mode: segmentMode[actionChip.action],
            url: this.imagesM[imageRef].url
          }, 'apiCall')

          boxes = response.data.boxes
        } else if (type === 'diva') {
          // console.log('Here in Diva segmentation')
          actionFlow = this.actionFlowsAvailable[actionChip.diva]
          results = await this.getDivaProcessResults(this.imagesM[imageRef].url, actionFlow.serviceUrl, actionFlow.parameters)
          // console.log(results)
          json = await this.getListGet(results.output[0].file.url)
          pointList = json.data

          // console.log(actionChip.action)

          if (actionChip.action === 'segmentHist') {
            for (i = 0; i < pointList.length; i++) {
              value = pointList[i].array.values
              box = [value[0][0], value[0][1], value[1][0] - value[0][0], value[2][1] - value[1][1]]
              boxes.push(box)
            }
          } else if (actionChip.action === 'segmentKraken') {
            pointList = pointList.boxes
            for (i = 0; i < pointList.length; i++) {
              for (j = 0; j < pointList[i].length; j++) {
                // console.log(pointList[i][j])
                // push(pointList[i][j][1])
              }
            }
          }
        }
        // Adding bounding boxes to the image
        // Fix this: What if the image had more than one type of actions in different workflows
        for (i = 0; i < boxes.length; i++) {
          this.boundingBoxes.push(
            {
              refComp: 'imagesM',
              refIndex: imageRef,
              type: actionChip.action + index,
              coord: boxes[i],
              visibility: true,
              resize: false,
              locked: false
            }
          )
        }
      } else if (elements === 'collectionBooks') {
        var urlImgs = this['collectionBooks'][imageRef].pages

        for (var k = 0; k < urlImgs.length; k++) {
          if (type === 'tesseract') {
            // console.log('tesseract type')

            response = await this.dataPost('/segment/tesseract', {
              mode: segmentMode[actionChip.action],
              url: urlImgs[k]
            }, 'apiCall')

            boxes = response.data.boxes
          } else if (type === 'diva') {
            // console.log('Here in Diva segmentation')
            actionFlow = this.actionFlowsAvailable[actionChip.diva]
            results = await this.getDivaProcessResults(urlImgs[i], actionFlow.serviceUrl, actionFlow.parameters)
            // console.log(results)
            json = await this.getListGet(results.output[0].file.url)
            pointList = json.data

            // console.log(actionChip.action)

            if (actionChip.action === 'segmentHist') {
              for (i = 0; i < pointList.length; i++) {
                value = pointList[i].array.values
                box = [value[0][0], value[0][1], value[1][0] - value[0][0], value[2][1] - value[1][1]]
                boxes.push(box)
              }
            } else if (actionChip.action === 'segmentKraken') {
              pointList = pointList.boxes
              for (i = 0; i < pointList.length; i++) {
                for (j = 0; j < pointList[i].length; j++) {
                  // console.log(pointList[i][j])
                  // push(pointList[i][j][1])
                }
              }
            }
          }
          // Adding bounding boxes to the image
          // Fix this: What if the image had more than one type of actions in different workflows
          for (i = 0; i < boxes.length; i++) {
            this.boundingBoxes.push(
              {
                refComp: 'collectionBooks',
                refIndex: imageRef,
                type: actionChip.action + index + '-' + k,
                coord: boxes[i],
                visibility: true,
                resize: false,
                locked: false
              }
            )
          }
          this.hideNonActiveBoundingBoxes(imageRef, this.collectionBooks[imageRef].activePage)
        }
      }
      // console.log(this.boundingBoxes)
      actionChip.loading = false
      // console.log('boundingBoxes added')
    },

    knobTurned: function (index, event) {
      // console.log('knob turned')
      this.settingKnobs[index].value = event
      this.$set(this.settingKnobs, index, this.settingKnobs[index])
      this.settingKnobs[index].initValue = event
    },
    clearBoundingBoxes: function () {
      this.boundingBoxes = []
    },
    chipsActionDisable: function (index, disability) {
      var chipAction = this.chipsAction[index]

      if (chipAction.action === 'textEntry') {
        var indexBT = this.getConnectedEl1toEl2('imagesM', chipAction.refIndex, 'boxesText')
        this.boxesText[indexBT].disability = disability
        var bt = this.$refs['boxesText' + indexBT][0]

        if (disability) {
          if (bt.model !== '') {
            this.boxesText[indexBT].coord[1] += 50
          } else {
            // console.log('here')
            this.boxesText[indexBT].coord[1] += 50
          }
        } else {
          if (bt.model !== '') {
            this.boxesText[indexBT].coord[1] -= 50
          } else {
            // console.log('here')
            this.boxesText[indexBT].coord[1] -= 50
          }
        }

        this.$set(this.boxesText, indexBT, this.boxesText[indexBT])
      }
    },
    chipsActionToggle: function (index, action, visibility) {
      var chipAction = this.chipsAction[index]

      if (chipAction.action.indexOf('segment') !== -1) {
        this.boundingBoxesToggle(chipAction.action + index, action)
      } else if (chipAction.action === 'textEntry') {
        // console.log('Ref Index is ' + chipAction.refIndex)
        var indexBT = this.getConnectedEl1toEl2('imagesM', chipAction.refIndex, 'boxesText')
        // console.log('Connection Found ' + indexBT)
        this.boxesText[indexBT].visibility = visibility
        // console.log(this.boxesText[indexBT].visibility)
      }
    },
    boundingBoxesToggle: function (key, action, flexible = false) {
      // console.log('Deleting old values')
      for (var i = 0; i < this.boundingBoxes.length; i++) {
        var bBox = this.boundingBoxes[i]
        if (bBox !== null && bBox.type.split('-')[0] === key) {
          if (action === 'visibility') {
            bBox.visibility = !bBox.visibility
          } else if (action === 'deletion') {
            this.boundingBoxes[i] = null
          }
        }
      }
      this.$set(this, 'boundingBoxes', this.boundingBoxes)
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

.icon-resize {
  display: inline-block;
  padding: 0px;
  position: absolute;
}

.action-chip-drawer {
  margin-bottom: 5px;
}

.delete {
  position: fixed;
  bottom: 75px;
  right: 300px;

}

.transparent {
  opacity: 0.2;
}
</style>
