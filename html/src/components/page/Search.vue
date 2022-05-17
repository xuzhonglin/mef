<template>

  <div class="search-result">
    <div class="search-header">
      <a href="/">
        <img src="/search_logo.png" class="search-logo" alt="mef"/>
      </a>
      <input class="search-box" v-model="keyword" placeholder="搜你想搜" @keyup="doSearch"/>
      <div class="search-button" @click="clickSearch">搜索</div>
    </div>
    <el-tabs class="search-result-box" v-loading="resultLoading">
      <div style="height: 30vh;text-align: center;padding-top: 18vh" v-if="resultLoading">加载中...</div>

      <el-tab-pane :label="result.name" v-for="result in searchResult" v-else>
        <div class="search-result-content">
          <div v-if="result.result.length===0">暂无结果</div>
          <div v-for="item in result.result" class="content-item" v-else>
            <div class="content-cover" :style="{backgroundImage:`url(${getImage(item.image)})`,backgroundSize:'cover'}"
                 @click="goToDetail(result.id,item)">
              <div class="content-status">{{ item.status }}</div>
            </div>
            <div class="content-title">{{ item.title }}</div>
          </div>

        </div>
      </el-tab-pane>
    </el-tabs>
  </div>

</template>

<script lang="ts" setup>

import {useRouter} from "vue-router";
import {onMounted, ref} from "vue";
import {Base64} from "js-base64";
import Api from "../../api";

const router = useRouter();

const keyword: any = ref(router.currentRoute.value.query.keyword);
const searchResult: any = ref([]);
const resultLoading: any = ref(true);
const BASE_URL = import.meta.env.VITE_APP_BASE_URL

const search = async () => {
  resultLoading.value = true;
  let refresh = router.currentRoute.value.query.refresh;
  const response = await Api.search(keyword.value, refresh);
  let resultData = response.data;
  let hasResultData: any[] = []
  let noResultData: any[] = []

  for (let index in resultData) {
    if (resultData[index].result.length > 0) {
      hasResultData.push(resultData[index])
    } else {
      noResultData.push(resultData[index])
    }
  }
  searchResult.value = hasResultData.concat(noResultData)
  resultLoading.value = false;
}

const doSearch = (e: any) => {
  if (e.keyCode !== 13) {
    return
  }
  clickSearch()
}

const clickSearch = () => {
  router.push(`/search?keyword=${keyword.value}`)
  search()
}

const goToDetail = (id: any, item: any) => {
  let url = Base64.encode(item.url)
  sessionStorage.setItem(`DETAIL_${url}`, JSON.stringify(item))
  window.open(`/detail?id=${id}&url=${url}`, '_blank')
}

const getImage = (url: string) => {
  if (!url) {
    return ''
  }
  return `${BASE_URL}/proxy/image/${url}.img`
}

onMounted(() => {
  // console.log('mounted')
  // search()
})

search()

</script>

<style scoped lang="scss">

//#app {
//  background-color: #ffffff !important;
//}

.search-result {
  background-color: #ffffff;
  height: 100vh;
}

.search-header {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
  align-items: center;
  justify-content: flex-start;
  margin: 0 3rem;

  height: 7rem;
  //border-bottom: 1px solid var(--el-border-color);
  //margin-top: 10rem;

  .search-logo {
    height: 3rem;
    margin: auto 1rem auto 0;
    object-fit: scale-down;
  }

  .search-box {
    width: 25vw;
    //width: 35rem;
    //height: 1rem;
    border-top: 2px solid #e1e1e1;
    border-bottom: 2px solid #e1e1e1;
    border-left: 2px solid #e1e1e1;
    border-right: none;
    border-radius: 10px 0 0 10px;
    padding: 12px;
    font-size: 1rem;
    height: calc(36px - 24px);

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
    height: calc(40px - 24px);
    line-height: calc(40px - 24px);
    cursor: pointer;
    user-select: none;
    font-size: 1rem;

    &:hover {
      //font-weight: bold;
      background-color: #3786d9;
    }
  }
}

.search-result-box {

  margin: -1rem 12rem 0 12rem;
  //background-color: #fff;

  .search-result-content {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: flex-start;
    //padding: 0 3rem;
    margin-top: 10px;


    .content-item {
      width: 170px;
      //height: 280px;
      margin: 0 20px 20px 0;


      .content-cover {

        width: 170px;
        height: 260px;
        object-fit: cover;
        border-radius: 5px;
        position: relative;
        cursor: pointer;

        .content-status {
          font-size: 12px;
          color: #fff;
          padding: 5px;
          position: absolute;
          bottom: 0;
          right: 0;
        }
      }

      .content-title {
        font-size: 14px;
        color: var(--el-text-color);
        padding: 5px 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }


    }
  }
}


</style>