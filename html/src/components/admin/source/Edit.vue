<template>
  <div>
    <source-header btn-text="返回主页" :btn-action="backIndex" :title="(editOrCreate==='edit'?'编辑':'创建')+'数据源'"/>
    <el-row class="editor">
      <el-col :span="10" class="side-left">
        <el-scrollbar view-style="overflow-x:hidden" class="side-left-scroll">
          <el-form label-width="110px" label-position="left">
            <el-form-item label="资源名称">
              <el-input v-model="source.sourceName" placeholder="资源的名称"></el-input>
            </el-form-item>
            <el-form-item label="资源类型">
              <el-select v-model="source.sourceType" :disabled="editOrCreate==='edit'">
                <el-option label="maccms" value="maccms"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="资源ID">
              <el-input v-model="source.sourceId" placeholder="资源ID，保存后不可修改"
                        :disabled="editOrCreate==='edit'"></el-input>
            </el-form-item>
            <el-form-item label="是否启用">
              <el-switch v-model="source.sourceEnable"/>
            </el-form-item>
            <el-form-item label="优先级">
              <el-input v-model="source.sourcePriority" placeholder="资源的优先级，数字越小优先级越高"></el-input>
            </el-form-item>
            <el-form-item label="资源主页">
              <el-input v-model="source.sourceHomePage" placeholder="主页的地址"></el-input>
            </el-form-item>
            <!--            <el-form-item label="请求方式">-->
            <!--              <el-select v-model="source.requestMethod">-->
            <!--                <el-option label="GET" value="GET"></el-option>-->
            <!--                <el-option label="POST" value="POST"></el-option>-->
            <!--              </el-select>-->
            <!--            </el-form-item>-->
            <!--            <el-form-item label="请求编码">-->
            <!--              <el-select v-model="source.requestCharset" placeholder="请求时的编码，形如UTF-8、GB2312、GBK">-->
            <!--                <el-option label="UTF-8" value="UTF-8"></el-option>-->
            <!--                <el-option label="GBK" value="GBK"></el-option>-->
            <!--                <el-option label="GB2312" value="GB2312"></el-option>-->
            <!--              </el-select>-->
            <!--            </el-form-item>-->
            <el-form-item label="网页编码">
              <el-select v-model="source.responseCharset" placeholder="网页响应的编码，形如UTF-8、GB2312、GBK">
                <el-option label="UTF-8" value="UTF-8"></el-option>
                <el-option label="GBK" value="GBK"></el-option>
                <el-option label="GB2312" value="GB2312"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="全局请求头">
              <div v-for="(item,index) in requestHeader" class="header-item">
                <el-row :gutter="10">
                  <el-col :span="7">
                    <el-input v-model="item[0]" placeholder="键名"
                              @change="headerValueChanged('requestHeader',index)"></el-input>
                  </el-col>
                  <el-col :span="0.5">=</el-col>
                  <el-col :span="10">
                    <el-input v-model="item[1]" placeholder="键值"
                              @change="headerValueChanged('requestHeader',index)"></el-input>
                  </el-col>
                  <el-col :span="2.5">
                    <el-button type="danger" :icon="Delete"
                               @click="deleteHeaderItem('requestHeader',index,requestHeader)" plain/>
                  </el-col>
                  <el-col :span="2.5">
                    <el-button type="primary" :icon="Plus" @click="createHeaderItem(requestHeader)" plain
                               v-if="requestHeader.length===index+1"/>
                  </el-col>
                </el-row>
              </div>

            </el-form-item>
            <el-form-item label="搜索方式">
              <el-select v-model="source.searchMethod" style="">
                <el-option label="GET" value="GET"></el-option>
                <el-option label="POST" value="POST"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="搜索地址">
              <el-input v-model="source.searchUrl" placeholder="搜索资源的地址，以{keyword}代替关键字"></el-input>
            </el-form-item>

            <el-form-item label="搜索请求头">
              <div v-for="(item,index) in searchHeader" class="header-item">
                <el-row :gutter="10">
                  <el-col :span="7">
                    <el-input v-model="item[0]" placeholder="键名"
                              @change="headerValueChanged('searchHeader',index)"></el-input>
                  </el-col>
                  <el-col :span="0.5">=</el-col>
                  <el-col :span="10">
                    <el-input v-model="item[1]" placeholder="键值"
                              @change="headerValueChanged('searchHeader',index)"></el-input>
                  </el-col>
                  <el-col :span="2.5">
                    <el-button type="danger" :icon="Delete" @click="deleteHeaderItem('searchHeader',index,searchHeader)"
                               plain/>
                  </el-col>
                  <el-col :span="2.5">
                    <el-button type="primary" :icon="Plus" @click="createHeaderItem(searchHeader)" plain
                               v-if="searchHeader.length===index+1"/>
                  </el-col>
                </el-row>
              </div>
            </el-form-item>
            <el-form-item label="搜索请求参数" v-if="source.searchMethod==='POST'">
              <el-input v-model="source.searchParams" placeholder="POST请求时的参数，以key=value&key1=value1填写"
                        type="textarea"
                        :autosize="{minRows: 1, maxRows: 3}"></el-input>
            </el-form-item>
            <el-form-item label="搜索是否验证">
              <el-switch v-model="source.searchVerify"/>
            </el-form-item>
            <el-form-item label="验证码地址" v-if="source.searchVerify">
              <el-input v-model="source.searchVerifyUrl" placeholder="验证码图片的地址"></el-input>
            </el-form-item>
            <el-form-item label="验证提交地址" v-if="source.searchVerify">
              <el-input v-model="source.searchVerifySubmitUrl" placeholder="提交验证码的地址，{verifyCode}代替验证码"></el-input>
            </el-form-item>
            <el-form-item label="搜索结果列表">
              <el-input v-model="source.searchResultList" placeholder="搜索结果的每一项的规则"></el-input>
            </el-form-item>
            <el-form-item label="结果每项标题">
              <el-input v-model="source.searchResultItemTitle" placeholder="每项的标题规则"></el-input>
            </el-form-item>
            <el-form-item label="结果每项链接">
              <el-input v-model="source.searchResultItemUrl" placeholder="每项的链接规则"></el-input>
            </el-form-item>
            <el-form-item label="结果每项图片">
              <el-input v-model="source.searchResultItemImage" placeholder="每项的图片规则"></el-input>
            </el-form-item>
            <el-form-item label="结果每项状态">
              <el-input v-model="source.searchResultItemStatus" placeholder="每项的状态规则，是否完结"></el-input>
            </el-form-item>
            <el-form-item label="结果每项评分">
              <el-input v-model="source.searchResultItemRating" placeholder="每项的评分规则"></el-input>
            </el-form-item>
            <el-form-item label="详情页标题">
              <el-input v-model="source.detailPageTitle" placeholder="响应页面的标题规则"></el-input>
            </el-form-item>
            <el-form-item label="详情页图片">
              <el-input v-model="source.detailPageImage" placeholder="响应页面的图片规则"></el-input>
            </el-form-item>
            <el-form-item label="详情页描述">
              <el-input v-model="source.detailPageDescription" placeholder="响应页面的描述规则"></el-input>
            </el-form-item>
            <el-form-item label="详情页线路列表">
              <el-input v-model="source.detailPageLineList" placeholder="响应页面各线路的每一项的规则"></el-input>
            </el-form-item>
            <el-form-item label="详情页线路名称">
              <el-input v-model="source.detailPageLineName" placeholder="响应页面各线路名称的每一项的规则"></el-input>
            </el-form-item>
            <el-form-item label="详情页剧集列表">
              <el-input v-model="source.detailPageEpisodeList" placeholder="可选，如果剧集不在线路元素下，需要填写"></el-input>
            </el-form-item>
            <el-form-item label="详情页剧集每项">
              <el-input v-model="source.detailPageEpisodeItem" placeholder="剧集每一项的规则"></el-input>
            </el-form-item>
            <el-form-item label="剧集每项标题">
              <el-input v-model="source.detailPageEpisodeItemTitle" placeholder="剧集每项标题的规则"></el-input>
            </el-form-item>
            <el-form-item label="剧集每项链接">
              <el-input v-model="source.detailPageEpisodeItemUrl" placeholder="剧集每项链接的规则"></el-input>
            </el-form-item>
            <el-form-item label="播放页标题">
              <el-input v-model="source.playPageTitle" placeholder="播放页的标题规则"></el-input>
            </el-form-item>
            <el-form-item label="播放页线路名称">
              <el-input v-model="source.playPageLineName" placeholder="播放页线路名称规则"></el-input>
            </el-form-item>
            <el-form-item label="播放页线路配置">
              <el-input v-model="source.playPageLineConfig" placeholder="播放页线路配置规则"></el-input>
            </el-form-item>
            <el-form-item label="播放器配置地址">
              <el-input v-model="source.playPagePlayerConfigUrl" placeholder="播放器配置地址，{lineName}代替线路"></el-input>
            </el-form-item>
            <el-form-item label="播放器地址">
              <el-input v-model="source.playPagePlayerUrl" placeholder="从播放器配置地址中读取播放器地址规则"></el-input>
            </el-form-item>
          </el-form>
        </el-scrollbar>
        <div class="editor-btn">
          <div style="float: right">
            <!--            <el-button type="primary" @click="verifySource" :loading="verifyLoading">验 证</el-button>-->
            <el-button type="primary" @click="saveSource">保 存</el-button>
          </div>
        </div>
      </el-col>
      <el-col :span="14" class="side-right">
        <el-input v-model="searchKeyword" placeholder="请输入搜索关键字">
          <template #append>
            <el-button :icon="Search" @click="testSearch"/>
          </template>
        </el-input>
        <div style="margin-top: 10px">
          <div class="ret-result-title">返回结果：</div>
          <div class="ret-result-json">
            <el-scrollbar>
              <json-viewer :value="testSearchResult" :expand-depth='3' copyable sort expanded></json-viewer>
            </el-scrollbar>
          </div>
        </div>
        <div class="ret-result-table">
          <el-table :data="testSearchResultTable" height="100%">
            <el-table-column label="图片" width="100" fixed>
              <template #default="scope">
                <el-image style="width: 50px; height: 60px" :src="scope.row.image" fit="scale-down"/>
              </template>
            </el-table-column>
            <el-table-column prop="title" label="名称" width=""/>
            <el-table-column prop="status" label="状态" width=""/>
            <el-table-column prop="rating" label="评分" width=""/>
            <el-table-column prop="url" label="链接" width="80">
              <template #default="scope">
                <el-button type="text" @click="openUrl(scope.row.url)">打开</el-button>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="80">
              <template #default="scope">
                <el-button type="text" @click="testDetail(scope.row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-col>
    </el-row>
    <el-drawer v-model="showDetail" :close-on-click-modal="false">

      <div style="display: flex;padding: 10px 0">
        <el-image :src="testDetailResult.data.image" fit="scale-down" style="width: 120px;border-radius: 5px"/>
        <div style
                 ="margin-left: 10px;padding: 10px;font-size: 14px;color:var(--el-text-color-regular);width:calc(100% - 120px)">
          <div style="font-size: 16px;margin-bottom: 10px;overflow-x: hidden;font-weight: bold">
            {{ testDetailResult.data.title }}
          </div>
          <div style="max-lines: 4;">{{ testDetailResult.data.description }}</div>
        </div>
      </div>
      <div>
        <el-tabs>
          <el-tab-pane :label="name" v-for="(item,name) in testDetailResult.data.lineList">
            <div style="display: flex;flex-wrap: wrap;justify-content: flex-start;flex-direction: row;">
              <el-button v-for="subItem in item" plain style="margin: 0 10px 10px 0" @click="testPlay(subItem.url)">
                {{ subItem.title }}
              </el-button>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
      <json-viewer :value="testDetailResult" :expand-depth='2' copyable boxed sort expanded :show-double-quotes="true"/>

    </el-drawer>
    <el-dialog v-model="showPlayDialog" :title="testPlayResult.title+' - '+testPlayResult.lineName"
               :close-on-click-modal="false" top="4vh" :destroy-on-close="true" width="60%">
      <iframe border="0" :src="testPlayResult.playerUrl" class="player-dialog"
              marginwidth="0" framespacing="0" marginheight="0" frameborder="0"
              scrolling="no" vspale="0" allowfullscreen="allowfullscreen" mozallowfullscreen="mozallowfullscreen"
              msallowfullscreen="msallowfullscreen" oallowfullscreen="oallowfullscreen"
              webkitallowfullscreen="webkitallowfullscreen" noresize=""></iframe>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>

import SourceHeader from "../../common/SourceHeader.vue";
import {onMounted, reactive, ref, watch} from "vue";
import {Delete, Plus, Search} from "@element-plus/icons-vue";
import Api from "../../../api";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";


const router = useRouter()
const searchKeyword = ref('行尸走肉')
const verifyLoading = ref(false)
const showDetail = ref(false)
const editOrCreate = ref('edit')
const showPlayDialog = ref(false)

const source: { [k: string]: any } = reactive({
  "sourceId": "",
  "sourceName": "",
  "sourceEnable": false,
  "sourcePriority": 0,
  "sourceHomePage": "",
  "sourceType": "maccms",
  "requestMethod": "GET",
  "requestCharset": "UTF-8",
  "responseCharset": "UTF-8",
  "requestHeader": {},
  "searchUrl": "",
  "searchMethod": "GET",
  "searchHeader": {},
  "searchParams": "",
  "searchVerify": false,
  "searchVerifyUrl": "",
  "searchVerifySubmitUrl": "",
  "searchResultList": "",
  "searchResultItemTitle": "",
  "searchResultItemUrl": "",
  "searchResultItemImage": "",
  "searchResultItemStatus": "",
  "searchResultItemRating": "",
  "detailPageTitle": "",
  "detailPageImage": "",
  "detailPageDescription": "",
  "detailPageLineList": "",
  "detailPageLineName": "",
  "detailPageEpisodeList": "",
  "detailPageEpisodeItem": "",
  "detailPageEpisodeItemTitle": "",
  "detailPageEpisodeItemUrl": "",
  "playPageTitle": "",
  "playPageLineName": "",
  "playPageLineConfig": "",
  "playPagePlayerConfigUrl": "",
  "playPagePlayerUrl": ""
})
const requestHeader = reactive([['', '']])
const searchHeader = reactive([['', '']])
const testSearchResult = reactive({})
const testSearchResultTable: any[] = reactive([])
const testDetailResult = reactive({})
const testPlayResult = reactive({})
const message = ElMessage


const createHeaderItem = (obj: any) => {
  obj = obj || []
  obj.push(['', ''])
}

const deleteHeaderItem = (target: string, index: number, obj: any) => {
  obj = obj || []
  obj.splice(index, 1)
  let temp: { [k: string]: string } = {}
  for (let i = 0; i < obj.length; i++) {
    temp[obj[i][0]] = obj[i][1]
  }
  source[target] = temp
  if (obj.length === 0) {
    createHeaderItem(obj)
  }
  console.log(source)
}

const backIndex = () => {
  router.push({name: 'adminSourceList'})
}

const openUrl = (url: string) => {
  window.open(url)
}

const headerValueChanged = (target: string, index: number) => {
  if (target === 'requestHeader') {
    let key = requestHeader[index][0]
    let value = requestHeader[index][1]
    Object.assign(source['requestHeader'], {[key]: value})
  } else if (target === 'searchHeader') {
    let key = searchHeader[index][0]
    let value = searchHeader[index][1]
    Object.assign(source['searchHeader'], {[key]: value})
  }
  console.log(source)
}

const saveSource = async () => {
  if (editOrCreate.value === 'edit') {
    const res = await Api.saveSource(source)
    if (res.data && res.data === true) {
      message.success('保存成功')
    } else {
      message.error('保存失败: ' + res.data)
    }
  } else {
    const res = await Api.saveSource(source)
    if (res.data && res.data === true) {
      message.success('创建成功')
    } else {
      message.error('创建失败，请检查输入')
    }
  }
}


const testSearch = async () => {
  if (!searchKeyword.value || searchKeyword.value.length < 2) {
    message.error('搜索关键字不能少于2个字符')
    return
  }

  let payload = {
    "source": source,
    "keyword": searchKeyword.value
  }
  const res = await Api.testSourceSearch(payload)
  Object.assign(testSearchResult, res)
  testSearchResultTable.splice(0, testSearchResultTable.length, ...res.data.result)
  console.log(res)
}

const testDetail = async (row: any) => {
  const res = await Api.testSourceDetail({
    "source": source,
    "url": row.url
  })
  Object.assign(testDetailResult, res)
  showDetail.value = true
  console.log(res.data)
}

const testPlay = async (url: string) => {
  const res = await Api.testSourcePlay({
    "source": source,
    "url": url
  })

  Object.assign(testPlayResult, res.data)
  showPlayDialog.value = true
  console.log(res.data)
}

const getSource = async (sourceId: string) => {
  if (!sourceId || sourceId.length === 0) {
    editOrCreate.value = 'create'
    return
  }
  const res = await Api.getSingleSource(sourceId);
  if (res.data) {
    editOrCreate.value = 'edit'
    if (typeof res.data.requestHeader === 'string') {
      res.data.requestHeader = {}
    }
    if (typeof res.data.searchHeader === 'string') {
      res.data.searchHeader = {}
    }
    Object.assign(source, res.data)
    let tempRequestHeader = []
    let tempSearchHeader = []
    for (let key in res.data.requestHeader) {
      tempRequestHeader.push([key, res.data.requestHeader[key]])
    }
    for (let key in res.data.searchHeader) {
      tempSearchHeader.push([key, res.data.searchHeader[key]])
    }

    if (tempRequestHeader.length > 0) {
      requestHeader.splice(0, requestHeader.length, ...tempRequestHeader)
    }

    if (tempSearchHeader.length > 0) {
      searchHeader.splice(0, searchHeader.length, ...tempSearchHeader)
    }

    console.log(requestHeader, searchHeader)
  }
}

// 监听页面大小变化
window.addEventListener("resize", () => {
  console.log("resize", window.innerHeight)
})

onMounted(() => {
  let source_id: any = router.currentRoute.value.query.id
  getSource(source_id)
})

watch(router.currentRoute, (newValue, oldValue) => {
  if (!newValue || newValue.name != 'adminSourceEdit') return
  let idTemp = newValue.id ? newValue.query.id : undefined
  if (!idTemp) return
  console.log('watch 已触发', idTemp)
  keyword.value = idTemp
  getSource(idTemp)
})
</script>

<style scoped lang="scss">

$editor-height: calc(100vh - 3rem - 3rem);
$side-left-height: calc(#{$editor-height} - 2rem);


.editor {
  margin: 1.5rem;
  padding: 1rem;
  height: $editor-height;
  background-color: #ffffff;
  border-radius: 5px;
  overflow: hidden;
}

.side-left {

  padding-right: 1rem;
  border-right: 1px dashed var(--el-border-color);
  height: $side-left-height;
}

.side-left-scroll {
  //overflow-x: hidden;
  height: calc(#{$side-left-height} - 42px);
}


.side-right {
  padding-left: 1rem;
  height: $side-left-height;
}

.header-item {
  width: 100%;

  &:not(:last-child) {
    margin-bottom: 10px;
  }
}

.editor-btn {
  height: 42rem;
  padding-top: 10px;
  border-top: 1px dashed var(--el-border-color);
}

.ret-result-title {
  font-size: 14px;
  color: var(--el-text-color-regular);
  margin-bottom: 10px;
}

.ret-result-json {
  border: 1px dashed var(--el-border-color);
  border-radius: 2px;
  height: 178px
}

.ret-result-table {
  height: calc(#{$side-left-height} - 32px - 210px - 10px);
  overflow: hidden;
}

.player-dialog {
  $player-width: 100vw;
  $player-padding: 40px;
  width: 100%;
  height: calc((#{$player-width * 0.6} - #{$player-padding}) / 16 * 9);
}


</style>