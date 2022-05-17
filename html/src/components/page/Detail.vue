<template>
  <div>
    <source-header :title="title"></source-header>
    <div class="play-box">
      <el-container class="player" v-loading="playerLoading" :element-loading-text="playerLoadingText"
                    element-loading-background="rgba(122, 122, 122, 0.8)"
      >
        <iframe border="0" :src="curPlayUrl" width="100%" height="100%" id="playerIframe" :onload="playerLoaded"
                marginwidth="0" framespacing="0" marginheight="0" frameborder="0"
                scrolling="no" vspale="0" allowfullscreen="allowfullscreen" mozallowfullscreen="mozallowfullscreen"
                msallowfullscreen="msallowfullscreen" oallowfullscreen="oallowfullscreen"
                webkitallowfullscreen="webkitallowfullscreen" noresize=""></iframe>
      </el-container>
      <div class="line">
        <div class="title">
          <div>播放线路</div>
          <div v-if="altKeyPressed">启用刷新</div>
        </div>
        <el-tabs v-model="curPlayLine">
          <el-tab-pane :label="name" :name='name' v-for="(line,name) in detailData.lineList">
            <div class="line-box">
              <div v-for="(ep,index) in line" class="ep"
                   :class="(activeEp[0]===name && activeEp[1]===index)?'active':''"
                   @click="epChanged(name,index,ep)">
                {{ ep.title }}
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
    <!--    <div class="detail-box">-->
    <!--      <img :src="detailData.image" class="poster"/>-->
    <!--      <div class="info">-->
    <!--        <div class="title">{{ detailData.title }}</div>-->
    <!--        <div class="desc">{{ detailData.description }}</div>-->
    <!--      </div>-->
    <!--    </div>-->
    <div id="script"></div>

  </div>
</template>

<script lang="ts" setup>
import SourceHeader from "../common/SourceHeader.vue";
import {onMounted, reactive, ref} from "vue";
import {useRouter} from "vue-router";
import {Base64} from "js-base64";
import Api from "../../api";

const title = ref("资源详情");
const router = useRouter();

const sourceId: any = ref(router.currentRoute.value.query.id)
const detailUrl: any = ref(router.currentRoute.value.query.url)
const detailData = ref({})
const curPlayUrl = ref("")
const curPlayLine = ref('')
const activeEp = ref([0, -1])
const altKeyPressed = ref(false)
const playerLoading = ref(false)
const playerLoadingText = ref("加载中请耐心等待...")


const fetchDetail = async () => {
  if (!sourceId.value || !detailUrl.value) {
    console.log("sourceId or detailUrl is empty");
    return;
  }
  if (!Base64.isValid(detailUrl.value)) {
    console.log("invalid detail url");
    return;
  }
  let detailUrlTemp = Base64.decode(detailUrl.value);
  let refresh = router.currentRoute.value.query.refresh;
  let res = await Api.detail(sourceId.value, detailUrlTemp, refresh);
  curPlayLine.value = res.data.lineNames[0];
  detailData.value = res.data;
  title.value = res.data.title;
  setupEp()
}

const epChanged = (name: any, index: number, ep: any) => {
  playerLoading.value = true;
  let line = Base64.encode(name);
  router.push({
    path: '/detail',
    query: {
      id: sourceId.value,
      url: detailUrl.value,
      line: line,
      ep: index + 1
    }
  })
  activeEp.value = [name, index];
  let refresh = altKeyPressed.value;
  getPlay(sourceId.value, ep.url, refresh);
  title.value = title.value.split(' - ')[0] + ' - ' + ep.title;
  // setTimeout(() => {
  //   playerLoading.value = false;
  // }, 1000);
  playerLoading.value = false;
}

const getPlay = async (id: any, url: any, refresh: boolean = undefined) => {
  if (refresh) {
    // console.log("刷新 ALT+Click");
  }
  let res = await Api.play(id, url, refresh);
  curPlayUrl.value = res.data.playerUrl;
}

const setupEp = () => {
  let line = router.currentRoute.value.query.line;
  let epNo = router.currentRoute.value.query.ep;
  if (line && epNo) {
    curPlayLine.value = Base64.decode(line);
    activeEp.value = [curPlayLine.value, parseInt(epNo) - 1];
    epChanged(curPlayLine.value, parseInt(epNo) - 1, detailData.value.lineList[curPlayLine.value][epNo - 1]);
  }
}

const keyHold = (keyCode: number, upOrDown: string) => {
  if (keyCode != 18) return
  altKeyPressed.value = upOrDown === 'down'
  // console.log(altKeyPressed.value)
}

const playerLoaded = (e: any) => {
  console.log(e)
}


fetchDetail()

document.onkeydown = function (e) {
  keyHold(e.keyCode, 'down')
}
document.onkeyup = function (e) {
  keyHold(e.keyCode, 'up')
}


</script>

<style scoped lang="scss">

$player-width: 65vw;
$player-height: calc(#{$player-width} / 16 * 9);

.play-box {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  padding: 1.5rem 2rem;


  .player {

    width: $player-width;
    height: $player-height;
    background: #000;
  }

  .detail-box {
    width: calc(40% - (2 * 2rem) - 2rem);
    height: calc(#{$player-height} - 2rem);
    padding: 0 0 0 2rem;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    //white-space: nowrap;
    //text-overflow: ellipsis;

    .poster {
      width: 150px;
      height: 230px;
      object-fit: cover;
    }

    .info {
      margin-left: 20px;
      height: 230px;
      overflow: hidden;

      .title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 20px;
        height: 20px;
      }

      .desc {
        font-size: 1rem;
        height: 190px;
        overflow: hidden;
        text-overflow: ellipsis;
        //white-space: ;
      }
    }
  }

  .line {
    margin-left: 2rem;
    width: calc(100vw - #{$player-width} - (2 * 2rem) - 2rem);
    height: calc(#{$player-height} - 2rem);
    background-color: #ffffff;
    padding: 1rem 1.5rem;
    border: 1px solid #e8e8e8;
    border-radius: 5px;

    .title {
      height: 20px;
      width: 100%;
      display: flex;
      justify-content: space-between;
    }

    .line-box {
      display: flex;
      flex-direction: row;
      justify-content: flex-start;
      flex-wrap: wrap;
      //overflow-y: scroll;
      //height: calc(#{$player-height} - 20px - 55px);

      .ep {
        //width: 4rem;
        min-width: 4rem;
        height: 1.5rem;
        line-height: 1.5rem;
        font-size: 0.7rem;
        margin: 0 10px 10px 0;
        cursor: pointer;
        border: 1px solid #ccc;
        border-radius: 3px;
        text-align: center;
        padding: 1px 5px;

        //&.active {
        //  background: #ccc;
        //}

        &.active, &:hover {
          color: #fff;
          background: #409EFF;
          border: 1px solid #409EFF;
        }
      }
    }
  }
}
</style>