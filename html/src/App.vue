<script setup lang="ts">
</script>

<template>
  <router-view v-slot="{ Component, route }">
    <transition>
      <keep-alive>
        <component :is="Component"/>
      </keep-alive>
    </transition>
  </router-view>
</template>

<style>

body {
  margin: 0;
  padding: 0;
  background-color: #f6f6f6;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
  'Microsoft YaHei', '微软雅黑', Arial, sans-serif;;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
