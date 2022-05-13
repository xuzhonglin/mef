<template>

</template>

<script lang="ts">

export default {

  name: "SourceDetail",
  props: {
    source: {
      type: Object,
      required: true
    },
    url: {
      type: String,
      required: true
    }
  },
  setup(props: any, ctx: any) {
    return {
      props,
      ctx
    }
  }
};


</script>

<style scoped lang="scss">

</style>