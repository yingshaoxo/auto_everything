<script setup lang="ts">

import {
  withDefaults,
  defineProps,
  defineEmits,
  onMounted,
  onUnmounted,
  computed,
  reactive,
  unref,
  ref
} from 'vue'

interface Props {
  display?: boolean
  // applicationId: string
  // approveOpinion: string
}

const props = withDefaults(defineProps<Props>(), {
  display: false
})

const emit = defineEmits(['theV'])

const dialogReference = ref(null)

const dict = reactive({
  theVModel: computed({
    get: () => props.display,
    set: (newVal) => {
      //@ts-expect-error
      emit('update:display', newVal)
    },
  }),
  tempData: {
    lastFinalAuditSignature: "",
    lastFinalAuditCeNumber: ""
  },
  form: {
    finalAuditSignature: '',
    finalAuditCeNumber: ''
  },
  rules: {
    finalAuditSignature: [
      { required: true, message: '请输入签名', trigger: 'change' },
      {
        validator: (rule: any, value: any, callback: any): boolean => {
          return value.length <= 250
        },
        trigger: ['change'],
        message: '字符数超过250',
      },
    ],
    finalAuditCeNumber: [
      { required: true, message: '请输入中央编号', trigger: 'change' },
      {
        validator: (rule: any, value: any, callback: any): boolean => {
          return value.length <= 15
        },
        trigger: ['change'],
        message: '字符数超过15',
      },
    ]
  },
  functions: {
    checkIfTheInputIsValid: (): boolean => {
      if ((!dict.form.finalAuditSignature) || (!dict.form.finalAuditCeNumber)) {
        return false
      }

      if (dict.form.finalAuditCeNumber.length > 15) {
        return false
      }
      if (dict.form.finalAuditSignature.length > 250) {
        return false
      }

      return true
    },
  }
})

onMounted(() => {
})

onUnmounted(() => {
})

const log = (...args: any[]) => {
  console.log('FinalAgree', ...args)
}
</script>

<template>
  <el-dialog
    ref="dialogReference"
    v-model="dict.theVModel"
    title="Warning"
    width="380px"
    @close="() => {
      dict.theVModel = false
    }"
    :destroy-on-close="true"
  >
    <template #title>
      确定同意？
      <br />
      <br />
      <span class="description">同意后，将会提交柜台进行开户。作为最后批核人，请您填写以下信息：</span>
    </template>

    <el-form
      :label-position="'left'"
      label-width="100px"
      :model="dict.form"
      :rules="dict.rules"
      style="max-width: 460px"
    >
      <el-form-item class="myRow1" label="签名:" prop="finalAuditSignature">
        <el-input v-model="dict.form.finalAuditSignature" placeholder="请输入负责人员中/英文姓名"></el-input>
        <div v-if="dict.tempData.lastFinalAuditSignature" class="previousSuggestion">some text</div>
      </el-form-item>

      <el-form-item class="myRow2" label="中央编号:" prop="finalAuditCeNumber">
        <el-input v-model="dict.form.finalAuditCeNumber" placeholder="请输入SFC C.E. Number"></el-input>
        <div v-if="dict.tempData.lastFinalAuditCeNumber" class="previousSuggestion">some text</div>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dict.theVModel = false">取消</el-button>
        <el-button
          :disabled="
            !dict.functions.checkIfTheInputIsValid()
          "
          type="primary"
          @click="dict.theVModel = false"
        >确定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.description {
  letter-spacing: normal;
  text-align: left;
  font-family: "PingFangSC-Regular", "PingFang SC", sans-serif;
  font-weight: 400;
  font-style: normal;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.427450980392157);
  line-height: 22px;
  word-wrap: break-word;
  text-transform: none;
  text-rendering: optimizeLegibility;
  -webkit-font-feature-settings: "kern";
  font-kerning: normal;
}

.previousSuggestion {
  margin-left: 0;
  margin-top: 5px;

  font-size: 13px;
  letter-spacing: normal;
  text-align: center;
  line-height: normal;
  text-transform: none;
  color: #ffffff;
  border-width: 0px;
  width: 158px;
  height: 24px;
  background: inherit;
  background-color: rgba(170, 170, 170, 1);
  border: none;
  border-radius: 5px;
  box-shadow: none;
  font-family: "PingFangSC-Regular", "PingFang SC", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.myRow1 {
  margin-bottom: 30px;
}

.myRow2 {
  margin-top: 30px;
}
</style>
