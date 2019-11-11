<template>
<div>
    <img :src="url"/>
</div>
</template>

<script>
export default {
  props: ['url'],
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>

<style scoped>
img {
  width: 100%;
}
</style>
