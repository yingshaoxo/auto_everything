<script lang="ts" setup>
import {
  Film,
  Document,
  Menu as IconMenu,
  Setting,
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { computed, defineComponent, nextTick, onMounted, reactive, ref } from 'vue'

import functions from './store/functions'
import { pageIdentity, globalDict } from "./store/memory"

import FinalAgree from './dialogs/FinalAgree/index.vue'

const dict = reactive({
  tempData: {
    showFinalAgreeDialog: false,
  },
}) as any
</script>

<template>
  <FinalAgree v-model:display="dict.tempData.showFinalAgreeDialog" />
  <!-- <button @click="dict.tempData.showFinalAgreeDialog = true">test button</button> -->

  <div class="topBar">
    <div @click="functions.pages.switchPage(pageIdentity.homePage)">Auto Everyting</div>
    <div @click="
      () => {
        functions.basic.openALink('https://github.com/yingshaoxo/auto_everything')
      }
    ">Github</div>
  </div>

  <el-row>
    <el-col :span="3">
      <el-menu default-active="1">
        <el-sub-menu index="1">
          <template #title>
            <el-icon>
              <Film />
            </el-icon>
            <span>Media Processor</span>
          </template>
          <el-menu-item index="1-1" @click="() => {
            functions.pages.switchPage(pageIdentity.videoPage)
          }">Video</el-menu-item>
          <!-- <el-menu-item
            index="1-2"
            @click="() => {
              functions.pages.switchPage(pageIdentity.speedupSilencePage)
            }"
          >Speed up Silence</el-menu-item>-->
        </el-sub-menu>
        <el-menu-item index="2" disabled>
          <el-icon>
            <icon-menu />
          </el-icon>
          <span>More to add ...</span>
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="21">
      <div class="boxContainer">
        <router-view></router-view>
      </div>
    </el-col>
  </el-row>
</template>

<style lang="scss">
body {
  padding: 0;
  margin: 0;
}

.topBar {
  height: 50px;
  background-color: #f5f5f5;

  div {
    margin-left: 25px;
    margin-right: 25px;
  }

  @include _center;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}

.boxContainer {
  @include _center;
  @include _fullSize;

  // margin-top: 30px;
}
</style>
