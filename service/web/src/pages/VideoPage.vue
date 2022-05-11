<script setup lang="ts">
import { computed, onBeforeMount, onMounted, reactive } from 'vue';
import { getProjects, Project } from '/@/requests/projects';
import UploadWidget from '/@/components/UploadWidget.vue';
import functions from '/@/store/functions';
import { Edit, Share, Delete, Search, Upload } from '@element-plus/icons-vue'
import * as memory from '/@/store/memory';

const dict = reactive({
    tempData: {
        showAddingDialog: false,
        showUploadingDialog: false,
        showStartProcessDialog: false,
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
        },
        startProcess: {
            projectId: '',
            jobType: memory.globalDict.consts.jobType.removeSilence as unknown as typeof memory.globalDict.consts.jobType,
        },
    },
    rules:
    {
        addingProject: {
            title: [
                { required: true, message: 'Please enter project name', trigger: 'blur' },
            ],
        },
        uploadingFile: {},
        startProcess: {
            jobType:
                [
                    { required: true, message: 'Please select a function', trigger: 'blur' },
                ],
        },
    },
    functions:
    {
        formatTheStatusCodeToString: (statusCode: number) => {
            switch (statusCode) {
                case -1:
                    return 'Failed';
                case 0:
                    return 'Waiting';
                case 1:
                    return 'Processing';
                case 2:
                    return 'Finished';
                default:
                    return 'Unknown';
            }
        },
        uploadProjectListView: async () => {
            const projects = await getProjects();
            projects?.reverse();
            dict.data.projects = projects;
        },
        onAddingProjectButtonConfirm: async () => {
            functions.basic.loadingStart();

            const result = await functions.requests.projectRequests.createProject(dict.forms.addingProject.title);

            console.log(result)

            dict.tempData.showAddingDialog = false;

            await dict.functions.uploadProjectListView();

            functions.basic.loadingEnd();
        },
        onUploadingFileButtonConfirm: async () => {
            functions.basic.loadingStart();

            const result = await functions.requests.projectRequests.uploadFile(dict.forms.uploadingFile.projectId, dict.forms.uploadingFile.file);

            console.log(dict.forms.uploadingFile)

            dict.tempData.showUploadingDialog = false;

            await dict.functions.uploadProjectListView();

            functions.basic.loadingEnd();
        },
        onStartProcessButtonConfirm: async () => {
            functions.basic.loadingStart();
            await functions.requests.projectRequests.startTheProcessOfAProject(Number(dict.forms.startProcess.projectId), dict.forms.startProcess.jobType);
            functions.basic.loadingEnd();

            dict.tempData.showStartProcessDialog = false;

            functions.basic.print('The process has been started!', 'success');
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
                <el-button class="button" type="primary" @click="dict.tempData.showAddingDialog = true">Add a new
                    project</el-button>
            </div>
        </template>
        <el-table :data="dict.data.projects" style="width: 100%" :border="true" :fit="true" :stripe="true">
            <el-table-column fixed prop="id" label="ID" width="60" :align="'center'" />
            <el-table-column prop="title" label="Title" width="220" :align="'center'" />
            <el-table-column prop="input" label="Input" :align="'center'">
                <template v-slot:default="scope">
                    <div v-if="scope.row.input">
                        <el-popover placement="top" trigger="hover">
                            <template v-slot:reference>
                                <div>{{ scope.row?.input }}</div>
                            </template>
                            <template v-slot:default>
                                <div class="inputLinkPopups">
                                    <el-button type="primary" @click="() => {
                                        let path = functions.requests.projectRequests.getStreamPath(scope.row?.input);
                                        functions.pages.switchPage(memory.pageIdentity.videoPlayGround, {
                                            projectId: scope.row?.id,
                                            videoURL: path,
                                        } as memory.VideoPlayGroundPageRouteQueryTypeDefinition);
                                    }">Play around</el-button>
                                    <el-button type="success" plain @click="() => {
                                        let path = functions.requests.projectRequests.getDownloadPath(scope.row?.input);
                                        functions.basic.openALink(path)
                                    }">Download</el-button>
                                </div>
                            </template>
                        </el-popover>
                    </div>
                    <template v-if="!scope.row.input">
                        <el-button type="success" plain @click="() => {
                            dict.forms.uploadingFile.projectId = scope.row.id
                            dict.tempData.showUploadingDialog = true
                        }">
                            Upload
                            <el-icon class="el-icon--right">
                                <Upload />
                            </el-icon>
                        </el-button>
                    </template>
                </template>
            </el-table-column>
            <el-table-column prop="output" label="Output" :align="'center'">
                <template v-slot:default="scope">
                    <el-popover placement="top" trigger="hover">
                        <template v-slot:reference>
                            <div v-show="scope.row.output" class="outputLink">{{ scope.row?.output }}</div>
                        </template>
                        <template v-slot:default>
                            <div class="Center">
                                <el-button type="success" plain @click="() => {
                                    let path = functions.requests.projectRequests.getDownloadPath(scope.row?.output);
                                    functions.basic.openALink(path)
                                }">Download</el-button>
                            </div>
                        </template>
                    </el-popover>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="Status" width="100" :align="'center'">
                <template v-slot:default="scope">
                    <div>{{ dict.functions.formatTheStatusCodeToString(scope.row.status) }}</div>
                </template>
            </el-table-column>
            <el-table-column fixed="right" label="Operations" width="120" :align="'center'">
                <template #default="scope">
                    <div class="operationBox">
                        <el-button type="primary" plain size="small" @click.prevent @click="() => {
                            if (scope.row.input) {
                                dict.forms.startProcess.projectId = scope.row.id
                                dict.tempData.showStartProcessDialog = true
                            } else {
                                functions.basic.print('You need to upload a file first!', 'warning')
                            }
                        
                        }">Process</el-button>
                        <el-button style="opacity: 0.8;" type="default" plain size="small" @click.prevent @click="async () => {
                            functions.basic.loadingStart();
                            await functions.requests.projectRequests.deleteAProject(scope.row.id)
                            await dict.functions.uploadProjectListView()
                            functions.basic.loadingEnd();
                        }">Remove</el-button>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </el-card>

    <el-dialog v-model="dict.tempData.showAddingDialog" title="Add a new project" width="400px" center>
        <el-form ref="ruleFormRef" :model="dict.forms.addingProject" :rules="dict.rules.addingProject" status-icon
            label-width="100px" class="demo-ruleForm">
            <el-form-item label="Project Title" prop="title">
                <el-input :style="{ width: 80 }" v-model="dict.forms.addingProject.title" type="text"
                    autocomplete="off"></el-input>
            </el-form-item>
        </el-form>

        <template #footer>
            <span class="dialog-footer">
                <el-button @click="dict.tempData.showAddingDialog = false">Cancel</el-button>
                <el-button type="primary" @click="dict.functions.onAddingProjectButtonConfirm">Confirm</el-button>
            </span>
        </template>
    </el-dialog>

    <el-dialog v-model="dict.tempData.showUploadingDialog" title="Upload a file" width="500px" center>
        <el-form label-position="top" :model="dict.forms.uploadingFile" :rules="dict.rules.uploadingFile">
            <el-form-item label="Project ID" prop>
                <el-input :style="{ width: 80 }" v-model="dict.forms.uploadingFile.projectId" type="text"
                    autocomplete="off" :disabled="true"></el-input>
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
                <el-button type="primary" @click="dict.functions.onUploadingFileButtonConfirm">Confirm</el-button>
            </span>
        </template>
    </el-dialog>

    <el-dialog v-model="dict.tempData.showStartProcessDialog" title="Start the process" width="500px" center>
        <el-form label-position="top" :model="dict.forms.startProcess" :rules="dict.rules.startProcess">
            <el-form-item label="Project ID" prop>
                <el-input :style="{ width: 80 }" v-model="dict.forms.startProcess.projectId" type="text"
                    autocomplete="off" :disabled="true"></el-input>
            </el-form-item>
            <el-form-item label="Job Type" prop="jobType">
                <!-- <div class="Center FullSize">
                </div>-->
                <el-select class="m-2 FullSize" v-model="dict.forms.startProcess.jobType" placeholder="Select">
                    <el-option v-for="jobType in Object.values(memory.globalDict.consts.jobType)" :key="jobType"
                        :label="jobType" :value="jobType"></el-option>
                </el-select>
            </el-form-item>
        </el-form>

        <template #footer>
            <span class="dialog-footer">
                <el-button @click="dict.tempData.showStartProcessDialog = false">Cancel</el-button>
                <el-button type="primary" @click="dict.functions.onStartProcessButtonConfirm">Confirm</el-button>
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
    .el-button+.el-button {
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

.outputLink {
    background: #56cf38;
    background: -webkit-linear-gradient(to right, #56cf38 0%, #2e99cf 100%);
    background: -moz-linear-gradient(to right, #56cf38 0%, #2e99cf 100%);
    background: linear-gradient(to right, #56cf38 0%, #2e99cf 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.inputLinkPopups {
    display: flex;
    flex-direction: column;
    justify-content: center;
    justify-items: center;
    align-items: center;
    align-content: center;

    .el-button+.el-button {
        margin-left: 0px;
        margin-top: 15px;
    }
}
</style>