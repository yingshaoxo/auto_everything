from build.test_protobuff_code_objects import *


from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn


router = APIRouter()


class Service_test_protobuff_code:
    async def create_hello_request(self, item: hello_request) -> hello_request:
        return hello_request()


def init(service_instance: Any):
    @router.post("/create_hello_request/", tags=["test_protobuff_code"])
    async def create_hello_request(item: hello_request) -> hello_request:
        item = hello_request().from_dict(item.to_dict())
        return (await service_instance.create_hello_request(item)).to_dict()


def run(service_instance: Any, port: str):
    init(service_instance=service_instance)

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(
        router,
        prefix="/test_protobuff_code",
    )

    print(f"You can see the docs here: http://127.0.0.1:{port}/docs")
    uvicorn.run( #type: ignore
        app=app,
        host="0.0.0.0",
        port=int(port)
    ) 


if __name__ == "__main__":
    class NewService(Service_test_protobuff_code):
        async def create_hello_request(self, item: hello_request) -> hello_request:
            if (item.name != None):
                item.name += "---"
            return item
    service_instance = NewService()
    run(service_instance, port="6060")