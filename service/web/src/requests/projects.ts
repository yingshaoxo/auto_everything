import functions from '/@/store/functions'
import { globalDict } from '/@/store/memory';

export interface Project {
    id: number
    title: string
    status: number
    input: string
    output: any
}

const HOST = 'http://localhost:8765'

export const getProjects = async (): Promise<Project[]> => {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    const result = await fetch(HOST + "/projects/")
    return functions.basic.jsonToObj(await result.text())
}

export const createProject = async (title: string): Promise<Project> => {
    const obj = {
        title: title,
        status: 0,
        completed: false,
    }

    const raw = functions.basic.objToJson(obj)

    var requestOptions = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: raw,
        redirect: 'follow'
    } as any;

    const result = await fetch(HOST + "/create_project/", requestOptions)
    return functions.basic.jsonToObj(await result.text())
}

export const deleteAProject = async (id: number): Promise<any> => {
    const obj = {
        project_id: id,
    }

    const raw = functions.basic.objToJson(obj)

    var requestOptions = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: raw,
        redirect: 'follow'
    } as any;

    const result = await fetch(HOST + "/delete_project/", requestOptions)
    return functions.basic.jsonToObj(await result.text())
}


export const uploadFile = async (projectId: string, file: File | null): Promise<void> => {
    if (!file) {
        return
    }

    const formData = new FormData();
    formData.append('file', file);

    var requestOptions = {
        method: 'POST',
        body: formData,
        redirect: 'follow'
    } as any;

    await fetch(HOST + `/upload_file?projectID=${projectId}`, requestOptions)
}


export const getStreamPath = (outputPath: string): string => {
    return HOST + `/stream_file?filePath=${outputPath}`
}


export const getDownloadPath = (outputPath: string): string => {
    return HOST + `/download_file?filePath=${outputPath}`
}


export const startTheProcessOfAProject = async (id: number, job: typeof globalDict.consts.jobType): Promise<any> => {
    const obj = {
        project_id: id,
        job: job
    }

    const raw = functions.basic.objToJson(obj)

    var requestOptions = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: raw,
        redirect: 'follow'
    } as any;

    const result = await fetch(HOST + "/start_process_for_a_project/", requestOptions)
    return functions.basic.jsonToObj(await result.text())
}


export const getAudioVolumeDataByProjectID = async (projectId: number | string): Promise<any> => {
    const obj = {
    }

    const raw = functions.basic.objToJson(obj)

    var requestOptions = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: raw,
        redirect: 'follow'
    } as any;

    const result = await fetch(HOST + `/video/getAudioVolumeData?projectID=${projectId}`, requestOptions)
    return functions.basic.jsonToObj(await result.text())
}


export const getVideoSilenceDataByProjectID = async (projectId: number | string, targetDB: number): Promise<any> => {
    const obj = {
    }

    const raw = functions.basic.objToJson(obj)

    var requestOptions = {
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        method: 'POST',
        body: raw,
        redirect: 'follow'
    } as any;

    const result = await fetch(HOST + `/video/getSilenceData?projectID=${projectId}&targetDB=${targetDB}`, requestOptions)
    return functions.basic.jsonToObj(await result.text())
}