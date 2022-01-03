<script setup lang="ts">
import { computed, onBeforeMount, reactive } from 'vue';
import { getProjects, Project } from '/@/requests/projects';
import UploadWidget from '../components/UploadWidget.vue';
import functions from '../store/functions';
import { Edit, Share, Delete, Search, Upload } from '@element-plus/icons-vue'

const dict = reactive({
    tempData: {
        showAddingDialog: false,
        showUploadingDialog: false,
    },
    data: {
        projects: [] as Project[],
    },
    forms: {
        addingProject: {
            title: '',
        },
        uploadingFile: {
            projectId: '',
            file: null as File | null,
        }
    },
    rules:
    {
        addingProject: {
            title: [
                { required: true, message: 'Please enter project name', trigger: 'blur' },
            ],
        },
        uploadingFile: {}
    },
    functions:
    {
        uploadProjectListView: async () => {
            const projects = await getProjects();
            dict.data.projects = projects;
        },
        onAddingProjectButtonConfirm: async () => {
            const result = await functions.requests.projectRequests.createProject(dict.forms.addingProject.title);

            console.log(result)

            dict.tempData.showAddingDialog = false;

            await dict.functions.uploadProjectListView();
        },
        onUploadingFileButtonConfirm: async () => {
            const result = await functions.requests.projectRequests.uploadFile(dict.forms.uploadingFile.projectId, dict.forms.uploadingFile.file);

            console.log(dict.forms.uploadingFile)

            dict.tempData.showUploadingDialog = false;

            await dict.functions.uploadProjectListView();
        },
        handleTheProcessButtonClick: async (projectId: number, input: any) => {
            if (!input) {
                functions.basic.print('Please upload a file first!', 'error');
            } else {
                await functions.requests.projectRequests.startTheProcessOfAProject(projectId);
                functions.basic.print('The process has been started!', 'success');
                setTimeout(async () => {
                    await dict.functions.uploadProjectListView();
                }, 5000);
            }
        },
    }
})

onBeforeMount(async () => {
    await dict.functions.uploadProjectListView();
});


</script>

<template>
    <el-card class="box-card">
        <template #header>
            <div class="card-header">
                <span>Projects</span>
                <el-button
                    class="button"
                    type="primary"
                    @click="dict.tempData.showAddingDialog = true"
                >Add a new project</el-button>
            </div>
        </template>
        <el-table
            :data="dict.data.projects"
            style="width: 100%"
            :border="true"
            :fit="true"
            :stripe="true"
        >
            <el-table-column fixed prop="id" label="ID" width="60" :align="'center'" />
            <el-table-column prop="title" label="Title" width="220" :align="'center'" />
            <el-table-column prop="input" label="Input" :align="'center'">
                <template v-slot:default="scope">
                    <div v-if="scope.row.input">{{ scope.row.input }}</div>
                    <template v-if="!scope.row.input">
                        <el-button
                            type="success"
                            plain
                            @click="() => {
                                dict.forms.uploadingFile.projectId = scope.row.id
                                dict.tempData.showUploadingDialog = true
                            }"
                        >
                            Upload
                            <el-icon class="el-icon--right">
                                <Upload />
                            </el-icon>
                        </el-button>
                    </template>
                </template>
            </el-table-column>
            <el-table-column prop="output" label="Output" :align="'center'" />
            <el-table-column prop="status" label="Status" width="100" :align="'center'" />
            <el-table-column fixed="right" label="Operations" width="120" :align="'center'">
                <template #default="scope">
                    <div class="operationBox">
                        <el-button
                            type="primary"
                            plain
                            size="small"
                            @click.prevent
                            @click="dict.functions.handleTheProcessButtonClick(scope.row.id, scope.row.input)"
                        >Process</el-button>
                        <el-button
                            style="opacity: 0.8;"
                            type="default"
                            plain
                            size="small"
                            @click.prevent
                            @click="async () => {
                                functions.basic.loadingStart();
                                await functions.requests.projectRequests.deleteAProject(scope.row.id)
                                await dict.functions.uploadProjectListView()
                                functions.basic.loadingEnd();
                            }"
                        >Remove</el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-card>

    <el-dialog
        v-model="dict.tempData.showAddingDialog"
        title="Add a new project"
        width="400px"
        center
    >
        <el-form
            ref="ruleFormRef"
            :model="dict.forms.addingProject"
            :rules="dict.rules.addingProject"
            status-icon
            label-width="100px"
            class="demo-ruleForm"
        >
            <el-form-item label="Project Title" prop="title">
                <el-input
                    :style="{ width: 80 }"
                    v-model="dict.forms.addingProject.title"
                    type="text"
                    autocomplete="off"
                ></el-input>
            </el-form-item>
        </el-form>

        <template #footer>
            <span class="dialog-footer">
                <el-button @click="dict.tempData.showAddingDialog = false">Cancel</el-button>
                <el-button
                    type="primary"
                    @click="dict.functions.onAddingProjectButtonConfirm"
                >Confirm</el-button>
            </span>
        </template>
    </el-dialog>

    <el-dialog
        v-model="dict.tempData.showUploadingDialog"
        title="Upload a file"
        width="500px"
        center
    >
        <el-form
            label-position="top"
            :model="dict.forms.uploadingFile"
            :rules="dict.rules.uploadingFile"
        >
            <el-form-item label="Project ID" prop>
                <el-input
                    :style="{ width: 80 }"
                    v-model="dict.forms.uploadingFile.projectId"
                    type="text"
                    autocomplete="off"
                    :disabled="true"
                ></el-input>
            </el-form-item>
            <el-form-item label="File" prop>
                <div class="Center FullSize">
                    <UploadWidget v-model:file="dict.forms.uploadingFile.file"></UploadWidget>
                </div>
            </el-form-item>
        </el-form>

        <template #footer>
            <span class="dialog-footer">
                <el-button @click="dict.tempData.showUploadingDialog = false">Cancel</el-button>
                <el-button
                    type="primary"
                    @click="dict.functions.onUploadingFileButtonConfirm"
                >Confirm</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<style lang="scss">
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.box-card {
    @include _fullSize;
}

.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.text {
    font-size: 14px;
}

.item {
    margin-bottom: 18px;
}

.box-card {
    @include _fullSize;
}

.operationBox {
    .el-button + .el-button {
        margin-left: 0px;
    }

    display: flex;
    flex-direction: column;
    align-items: center;
    align-content: center;
    justify-content: space-between;
    justify-items: stretch;
    height: 60px;
    margin-block: 5px;
}
</style>