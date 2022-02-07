<script setup lang="ts">import { onBeforeMount, onMounted, reactive, ref, unref } from 'vue';
import { useRoute } from 'vue-router';
import functions from '../store/functions';
import * as memory from '/@/store/memory';

import Plyr from 'plyr';
import "plyr/dist/plyr.css";

import Chart from 'chart.js/auto';

const route = useRoute()

const audioGraphElement = ref(null)
const videoPlayerElement = ref(null)

interface OneSingleAudioSegmentType {
    type: number
    start: number
    end: number
}
type MySilenceDataType = OneSingleAudioSegmentType[]

const dict = reactive({
    objects: {
        videoPlayer: null as Plyr | null,
        audioChart: null as any,
    },
    tempData: {
        projectId: '',
        videoUrl: '',
        audioProgressRatio: 0,
        progressLeftStartPoint: 0,
        progressRightEndPoint: 0,
        targetDB: 21,
        silenceData: [] as MySilenceDataType,
        enableEffectHandler: false,
    },
    functions: {
        getAudioIndicatorLeftStyle: () => {
            // if (dict.tempData.progressRightEndPoint == 0) {
            //     return {
            //         left: `${dict.tempData.audioProgressRatio * 100}%`,
            //     }
            // } else {
            //     return {
            //         left: `${dict.tempData.progressLeftStartPoint + dict.tempData.audioProgressRatio * (dict.tempData.progressRightEndPoint - dict.tempData.progressLeftStartPoint)}px`
            //     }
            // }
            return {
                left: `${dict.tempData.progressLeftStartPoint + dict.tempData.audioProgressRatio * (dict.tempData.progressRightEndPoint - dict.tempData.progressLeftStartPoint)}px`
            }
        },
        pauseTheVideoAndPlayFromThePositionWhereTheAudioIndicatorIs: () => {
            if (dict.objects.videoPlayer) {
                dict.objects.videoPlayer!.pause()
                dict.objects.videoPlayer!.currentTime = dict.tempData.audioProgressRatio * (dict.objects.videoPlayer?.duration ?? 0)
                dict.objects.videoPlayer!.play()
            }
        },
        convertHMStoFloatSecond: (hms: string) => {
            if (!hms.includes(":")) {
                return parseFloat(hms);
            }
            const a = hms.split('.')[0].split(':')
            let result = (+a[0]) * 60 * 60 + (+a[1]) * 60 + (+a[2])
            if (hms.includes(".")) {
                const tailing = parseFloat("0." + hms.split('.')[1])
                return result + tailing
            } else {
                return result
            }
        },
        updateSilenceData: async (targetDB: number) => {
            const response = await functions.requests.projectRequests.getVideoSilenceDataByProjectID(dict.tempData.projectId, targetDB)

            if (response?.data) {
                // [[0, ['0:00:00', '0:00:00.255420']], [1, ['0:00:00.255420', '0:01:27.829478']]]
                //   {
                //   "type": 0,
                //   "start": 0.1,
                //   "end": 0.1
                //   }
                const data = response.data
                const myData: MySilenceDataType = data.map((item: any) => {
                    // time_duration = (datetime.datetime.strptime(part[1][1], '%H:%M:%S.%f') - datetime.datetime.strptime(part[1][0], '%H:%M:%S.%f')).seconds
                    return {
                        type: item[0],
                        start: dict.functions.convertHMStoFloatSecond(item[1][0]),
                        end: dict.functions.convertHMStoFloatSecond(item[1][1])
                    }
                })
                dict.tempData.silenceData = myData
                console.log(dict.tempData.silenceData)
            }
        },
        handleVideoTimeUpdate: () => {
            if (dict.tempData.enableEffectHandler === false) {
                return
            }

            if (dict.objects.videoPlayer) {
                const currentTime = dict.objects.videoPlayer?.currentTime
                if (currentTime) {
                    for (let i = 0; i < dict.tempData.silenceData.length; i++) {
                        const item = dict.tempData.silenceData[i]
                        if (item.start <= currentTime && currentTime <= item.end) {
                            let anotherI = i
                            while (anotherI < dict.tempData.silenceData.length - 1 && dict.tempData.silenceData[anotherI].type === 0) {
                                if (dict.tempData.silenceData[anotherI + 1].type === 1) {
                                    dict.objects.videoPlayer.currentTime = dict.tempData.silenceData[anotherI + 1].start
                                    break
                                }
                                anotherI++
                            }
                            break
                        }
                    }
                }
            }
        },
    }
})

onBeforeMount(async () => {
    let query = route.query as unknown as memory.VideoPlayGroundPageRouteQueryTypeDefinition

    const projectIdKey: keyof memory.VideoPlayGroundPageRouteQueryTypeDefinition = "projectId";
    dict.tempData.projectId = functions.pages.getQueryValueByKey(query, projectIdKey);

    const videoUrlKey: keyof memory.VideoPlayGroundPageRouteQueryTypeDefinition = "videoURL";
    dict.tempData.videoUrl = functions.pages.getQueryValueByKey(query, videoUrlKey);
});

onMounted(async () => {
    if (unref(videoPlayerElement) != null) {
        dict.objects.videoPlayer = new Plyr(unref(videoPlayerElement) as unknown as HTMLElement);
        // dict.objects.videoPlayer.muted = true;
        dict.objects.videoPlayer.on('timeupdate', () => {
            const duration = dict.objects.videoPlayer?.duration
            const currentTime = dict.objects.videoPlayer?.currentTime
            const progressRatio = (currentTime ?? 0) / (duration ?? 1)
            // console.log(progressRatio)
            dict.tempData.audioProgressRatio = progressRatio

            dict.functions.handleVideoTimeUpdate()
        });
        dict.objects.videoPlayer.source = {
            type: 'video',
            sources: [
                {
                    src: dict.tempData.videoUrl,
                    type: 'video/mp4',
                },
            ],
        };
    }

    if (unref(audioGraphElement) != null) {
        const response = await functions.requests.projectRequests.getAudioVolumeDataByProjectID(dict.tempData.projectId);
        console.log(response)

        dict.objects.audioChart = new Chart(unref(audioGraphElement) as unknown as HTMLCanvasElement, {
            type: 'line',
            data: {
                labels: Object.keys(response?.data).map((v: any) => String(v)),
                datasets: [{
                    label: 'Audio Volume Graph',
                    data: Object.values(response?.data),
                    borderColor: 'rgb(75, 192, 192)',
                    borderWidth: 1.5,
                    pointRadius: 0,
                }],
            },
            options: {
                maintainAspectRatio: false,
                scales: {
                    x: {
                    },
                    y: {
                        type: 'linear',
                        min: 0,
                        max: 1
                    }
                },
                events: ['click'],
                onClick: (e, activeEls) => {
                    // console.log(e)

                    const newElement = e as any;
                    const chartArea = newElement.chart.chartArea;
                    const { left, right } = chartArea
                    const { x } = newElement;

                    dict.tempData.progressLeftStartPoint = left
                    dict.tempData.progressRightEndPoint = right

                    const progressRatio = (x - left) / (right - left);
                    console.log(progressRatio)
                    dict.tempData.audioProgressRatio = progressRatio;

                    dict.functions.pauseTheVideoAndPlayFromThePositionWhereTheAudioIndicatorIs()
                }
            }

        });

        const chartArea = dict.objects.audioChart.chartArea;
        const { left, right } = chartArea

        dict.tempData.progressLeftStartPoint = left
        dict.tempData.progressRightEndPoint = right
    }

    await dict.functions.updateSilenceData(dict.tempData.targetDB)
})
</script>

<template>
    <el-card class="box-card">
        <template #header>
            <div class="card-header">
                <span>Video Playground</span>
            </div>
        </template>
        <!-- <div>{{ dict.tempData.projectId }}</div>
        <div>{{ dict.tempData.videoUrl }}</div>-->

        <el-row justify="center">
            <el-input-number
                v-model="dict.tempData.targetDB"
                :min="1"
                :max="60"
                @change="() => {
                    dict.functions.updateSilenceData(dict.tempData.targetDB)
                }"
            ></el-input-number>
        </el-row>
        <el-row justify="center">
            <el-button
                plain
                class="noSilenceButton"
                :type="dict.tempData.enableEffectHandler ? 'success' : 'info'"
                @click="dict.tempData.enableEffectHandler = !dict.tempData.enableEffectHandler"
            >No Silence Fileter Enabled</el-button>
        </el-row>
        <div class="audioGraphElementContainer">
            <canvas ref="audioGraphElement"></canvas>
            <div class="audioIndicator" :style="dict.functions.getAudioIndicatorLeftStyle()"></div>
        </div>
        <video ref="videoPlayerElement" class="videoStyle"></video>
    </el-card>
</template>

<style lang="scss" scoped>
.audioGraphElementContainer {
    height: 200px;
    position: relative;
}
.audioIndicator {
    position: absolute;
    width: 2px;
    height: 100%;
    border-radius: 20px;
    background-color: red;
    top: 0px;
}
.noSilenceButton {
    margin-top: 30px;
    margin-bottom: 30px;
}
</style>
