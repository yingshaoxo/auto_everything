from build.test_protobuff_code_objects import *


from fastapi import APIRouter, FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os


class Service_test_protobuff_code:
    async def create_hello_request(self, headers: dict[str, str], item: hello_request) -> hello_request:
        return hello_request()


def init(service_instance: Any, router: Any):
    @router.post("/create_hello_request/", tags=["test_protobuff_code"])
    async def create_hello_request(request: Request, item: hello_request) -> hello_request:
        item = hello_request().from_dict(item.to_dict())
        headers = dict(request.headers.items())
        return (await service_instance.create_hello_request(headers, item)).to_dict()


def run(service_instance: Any, port: str, html_folder_path: str="", serve_html_under_which_url: str="/", only_return_app: bool = False):
    router = APIRouter()

    init(service_instance=service_instance, router=router)

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

    if (html_folder_path != ""):
        if os.path.exists(html_folder_path) and os.path.isdir(html_folder_path):
            app.mount(serve_html_under_which_url, StaticFiles(directory=html_folder_path, html = True), name="web")
            @app.get(serve_html_under_which_url, response_model=str)
            async def index_page():
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            @app.exception_handler(404) #type: ignore
            async def custom_404_handler(_, __):  #type: ignore
                return FileResponse(os.path.join(html_folder_path, 'index.html'))
            print(f"the website is running at: http://127.0.0.1:{port}/")
        else:
            print(f"Error: You should give me an absolute html_folder_path than {html_folder_path}")

    if only_return_app == True:
        return app

    print(f"You can see the docs here: http://127.0.0.1:{port}/docs")
    uvicorn.run( #type: ignore
        app=app,
        host="0.0.0.0",
        port=int(port)
    )


if __name__ == "__main__":
    class NewService(Service_test_protobuff_code):
        async def create_hello_request(self, headers: dict[str, str], item: hello_request) -> hello_request:
            if (item.name != None):
                item.name += "---"
            return item
    service_instance = NewService()
    run(service_instance, port="6060", html_folder_path="/Users/yingshaoxo/CS/it_has_alternatives/backend_service/backend_service/vue")
