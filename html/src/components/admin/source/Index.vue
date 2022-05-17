<template>
  <div>
    <source-header btn-text="新建配置" :btn-action="createSource" title="数据源列表" sec-btn-text="导入配置"
                   :sec-btn-action="importSource"/>
    <div class="list-view">
      <el-table :data="tableSource" stripe style="width: 100%">
        <el-table-column prop="sourceName" label="资源名称" width=""/>
        <el-table-column prop="sourceId" label="资源ID" width=""/>
        <el-table-column prop="sourceType" label="资源类型" width=""/>
        <el-table-column prop="sourceHomePage" label="资源主页" width=""/>
        <el-table-column prop="requestMethod" label="请求方式" width=""/>
        <el-table-column prop="responseCharset" label="字符编码" width=""/>
        <el-table-column prop="sourcePriority" label="优先级" width="">
          <template #default="scope">
            <el-tag size="small">{{ scope.row.sourcePriority }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="sourceEnable" label="是否启用" width="">
          <template #default="scope">
            <el-tag :type="scope.row.sourceEnable?'success':'danger'" size="small">
              {{ scope.row.sourceEnable ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="100">
          <template #default="scope">
            <el-button type="text" size="small" @click="viewSource(scope.row)">查看</el-button>
            <el-button type="text" size="small" @click="editSource(scope.row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog v-model="showJsonView" title="预览" top="10vh">
      <json-viewer :value="jsonData" :expand-depth='2' copyable boxed sort expanded :show-double-quotes="true"/>
    </el-dialog>

    <el-dialog v-model="showImportDialog" title="导入数据源" top="10vh">
      <el-input
          v-model="importData"
          :rows="16"
          type="textarea"
          placeholder="请粘贴json格式的数据源配置"
      />
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="showImportDialog = false">取消</el-button>
        <el-button type="primary" @click="saveImport" :loading="importSubmitLoading">提交</el-button
        >
      </span>
      </template>
    </el-dialog>

  </div>
</template>

<script lang="ts" setup>

import SourceHeader from "../../common/SourceHeader.vue";
import Api from "../../../api";
import {onMounted, ref} from "vue";
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus/es";

const tableSource = ref([]);
const showJsonView = ref(false);
const showImportDialog = ref(false);
const importSubmitLoading = ref(false);
const jsonData = ref({});
const importData = ref("");
const router = useRouter();
const message = ElMessage


const getSourceList = async () => {
  const res = await Api.getSourceList();
  tableSource.value = res.data;
};

const editSource = (row: any) => {
  router.push({name: 'adminSourceEdit', query: {id: row.sourceId}});
};

const createSource = () => {
  router.push({name: 'adminSourceEdit'});
}

const importSource = () => {
  showImportDialog.value = true;
}

const saveImport = async () => {
  importSubmitLoading.value = true;
  let importDataJson = null;
  try {
    importDataJson = JSON.parse(importData.value);
  } catch (e) {
    importSubmitLoading.value = false;
    message.error("数据源配置格式错误，请检查是否为json格式");
    return
  }
  const res = await Api.importSource(importDataJson);
  importSubmitLoading.value = false;
  if (res.data && res.data === true) {
    message.success('导入成功，1秒后刷新列表')
    showImportDialog.value = false;
    setTimeout(() => {
      getSourceList();
    }, 1000);
  } else {
    message.error('导入失败: ' + res.data)
  }
}

const viewSource = (row: any) => {
  console.log(row);
  showJsonView.value = true;
  jsonData.value = row;
};

onMounted(() => {
      getSourceList();
    }
);
</script>

<style scoped>


.list-view {
  margin: 1.5rem;
  padding: 1rem;
  background-color: #ffffff;
  height: calc(100vh - 3rem - 2 * 2.5rem);
  border-radius: 5px;
}
</style>