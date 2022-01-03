import functions from '/@/store/functions'

export interface Project {
    id: number
    title: string
    status: number
    completed: boolean
    input: string
    output: any
}

export const getProjects = async (): Promise<Project[]> => {
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    const result = await fetch("http://localhost:8001/projects/")
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

    const result = await fetch("http://localhost:8001/create_project/", requestOptions)
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

    const result = await fetch("http://localhost:8001/delete_project/", requestOptions)
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

    await fetch(`http://localhost:8001/upload_file?projectID=${projectId}`, requestOptions)
}


export const startTheProcessOfAProject = async (id: number): Promise<any> => {
    const obj = {
        project_id: id,
        job: "speedupSilence"
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

    const result = await fetch("http://localhost:8001/start_process_for_a_project/", requestOptions)
    return functions.basic.jsonToObj(await result.text())
}