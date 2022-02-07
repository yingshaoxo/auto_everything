from py_backend.store.globalVariables import GlobalStore

globalStore = GlobalStore()


def getFilePathByProjectID(projectID: int) -> str:
    return globalStore.tempFolder + "/" + str(projectID) + ".mp4"
