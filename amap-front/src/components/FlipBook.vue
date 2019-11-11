<template>
  <div>
  <br/><br/><br/><br/><br/>

  <div id="flipbook">
    <div class="hard"> <img src="https://upload.wikimedia.org/wikipedia/commons/5/5f/Armenian_manuscript_cover%2C_Mashtots%2C_9th_century._Italy%2C_St._Ghazar%2C_Mekhitarians_old_manuscripts_library%2C_Ms._457.jpg"/> </div>
    <div > <img src="../statics/1L.jpg" /> </div>
    <div > <img src="../statics/1R.jpg" /> </div>
    <div > <img src="../statics/3L.jpg" /> </div>
    <div > <img src="../statics/3R.jpg" /> </div>
    <div > <img src="../statics/4L.jpg" /> </div>
    <div > <img src="../statics/4R.jpg" /> </div>
    <div > <img src="../statics/5L.jpg" /> </div>
    <div > <img src="../statics/5R.jpg" /> </div>
    <div class="hard"> <img src="https://upload.wikimedia.org/wikipedia/commons/5/5f/Armenian_manuscript_cover%2C_Mashtots%2C_9th_century._Italy%2C_St._Ghazar%2C_Mekhitarians_old_manuscripts_library%2C_Ms._457.jpg"/> </div>
  </div>

  </div>
</template>
<script>
var $script = require('scriptjs')
export default {
  // name: 'ComponentName',
  data () {
    return {}
  },
  mounted: function () {
    $script('https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js', function () {
      $script('https://cdn.jsdelivr.net/turn.js/3/turn.js', function () {
        window.$('#flipbook').turn({
          width: 600,
          height: 500,
          autoCenter: true
        })
      })
    })
  }
}
</script>

<style scoped>
#flipbook{
  background: white;
}
img {
  width: 300px;
  height: 500px;
}
</style>
