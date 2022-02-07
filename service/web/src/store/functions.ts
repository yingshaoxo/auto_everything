import { ElLoading, ElMessage } from "element-plus"
import { BuildPropType } from "element-plus/es/utils/props"
import { pageIdentity, globalDict } from "/@/store/memory"

import { router } from "/@/store/router"

import * as projectRequests from "/@/requests/projects"

const functions = {
    basic: {
        jsonToObj(json: string) {
            return JSON.parse(json)
        },
        objToJson(obj: any) {
            return JSON.stringify(obj)
        },
        log: (msg: any) => {
            console.log(msg)
        },
        print: (msg: string, type: BuildPropType<StringConstructor, "success" | "info" | "warning" | "error", unknown> | undefined = 'success') => {
            ElMessage({
                message: msg,
                type: type,
            })
        },
        openALink: (url: string) => {
            window.open(url)
        },
        loadingStart: () => {
            globalDict.loadingInstance = ElLoading.service({
                lock: false,
                fullscreen: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)',
            }) as any
        },
        loadingEnd: () => {
            const instance = globalDict.loadingInstance as any
            instance.close()
        }
    },
    pages: {
        switchPage: (page: string, query?: any) => {
            globalDict.pageSelected = page
            if (query) {
                router.push({ path: globalDict.pageSelected, query })
            } else {
                router.push(page)
            }
        },
        getQueryValueByKey: (query: any, key: string) => {
            if (query && query[key]) {
                if (Array.isArray(query[key])) {
                    return query[key][0]
                } else {
                    return query[key]
                }
            }
            return null
        }
    },
    requests: {
        projectRequests,
    }
}

export default functions 