<template>
  <div class="search">
    <a href="/">
      <img src="/search_logo.png" class="search-logo" alt="mef"/>
    </a>
    <div style="display: flex;flex-direction: row;margin-top: 2.5rem">
      <input class="search-box" v-model="keyword" placeholder="搜你想搜" @keyup="search"/>
      <div class="search-button" @click="clickSearch">搜索</div>
    </div>
  </div>
</template>

<script lang="ts" setup>

import {ref} from "vue";
import {useRouter} from "vue-router";

const keyword = ref('')
const router = useRouter()

const search = (e: KeyboardEvent) => {
  if (e.keyCode !== 13) {
    return
  }
  console.log('关键字', keyword.value)
  router.push({name: 'search', query: {keyword: keyword.value}})
}

const clickSearch = () => {
  console.log('关键字', keyword.value)
  router.push({name: 'search', query: {keyword: keyword.value}})
}
</script>

<style scoped lang="scss">

.search {
  display: flex;
  flex-direction: column;
  flex-wrap: nowrap;
  align-items: center;
  //justify-content: center;
  height: 75vh;
  padding-top: 25vh;
  background-color: #ffffff;

  .search-logo {
    height: 6rem;
    object-fit: scale-down;
  }


  .search-box {
    //width: 28vw;
    width: 30rem;
    //height: 1rem;
    border-top: 2px solid #e1e1e1;
    border-bottom: 2px solid #e1e1e1;
    border-left: 2px solid #e1e1e1;
    border-right: none;
    border-radius: 10px 0 0 10px;
    padding: 12px;
    font-size: 1rem;
    height: calc(41px - 24px);

    &:focus {
      outline: none;
      border-color: #409EFF;
    }

  }

  .search-button {
    border-radius: 0 10px 10px 0;
    padding: 12px;
    background-color: #409EFF;
    color: #ffffff;
    text-align: center;
    width: 50px;
    height: calc(45px - 24px);
    line-height: calc(45px - 24px);
    cursor: pointer;
    user-select: none;
    font-size: 1rem;

    &:hover {
      //font-weight: bold;
      background-color: #3786d9;
    }


  }

}
</style>