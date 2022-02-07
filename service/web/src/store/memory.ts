import { ElLoading } from "element-plus";
import { reactive } from "vue";

export const pageIdentity = {
    homePage: "/",
    videoPage: '/video',
    videoPlayGround: '/video_playground',
}

export const globalDict = reactive({
    loadingInstance: null as unknown as typeof ElLoading,
    pageSelected: pageIdentity.homePage,
    consts: {
        jobType:
        {
            speedupSilence: "speedupSilence",
            removeSilence: "removeSilence",
        }
    }
})

export interface VideoPlayGroundPageRouteQueryTypeDefinition {
    projectId: string | string[],
    videoURL: string | string[],
}
