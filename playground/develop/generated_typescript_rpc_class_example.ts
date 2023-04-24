import * as test_protobuff_code_objects from './generated_typescript_protobuff_class_example'

export class Client_test_protobuff_code {
  /**
   * @param {string} _service_url is something like: "http://127.0.0.1:80" or "https://127.0.0.1"
   * @param {{ [key: string]: string }} _header  http headers, it's a dictionary, liek {'content-type', 'application/json'}
   * @param {Function} _error_handle_function will get called when http request got error, you need to give it a function like: (err: String) {print(err)}
   * @param {Function} _interceptor_function will get called for every response, you need to give it a function like: (data: dict[Any, Any]) {print(data)}
   */
    _service_url: string
    _header: { [key: string]: string } = {}
    _error_handle_function: (error: string) => void = (error: string) => {console.log(error)}
    _special_error_key: string = "__yingshaoxo's_error__"
    _interceptor_function: (data: any) => void = (data: any) => {console.log(data)}

    constructor(service_url: string, header?: { [key: string]: string }, error_handle_function?: (error: string) => void, interceptor_function?: (data: any) => void) {
        if (service_url.endsWith("/")) {
            service_url = service_url.slice(0, service_url.length-1);
        }
        try {
            if (location.protocol === 'https:') {
                if (service_url.startsWith("http:")) {
                    service_url = service_url.replace("http:", "https:")
                }
            } else if (location.protocol === 'http:') {
                if (service_url.startsWith("https:")) {
                    service_url = service_url.replace("https:", "http:")
                }
            }
        } catch (e) {
        }
        this._service_url = service_url
        
        if (header != null) {
            this._header = header
        }

        if (error_handle_function != null) {
            this._error_handle_function = error_handle_function
        }

        if (interceptor_function != null) {
            this._interceptor_function = interceptor_function
        }
    } 

    async _get_reponse_or_error_by_url_path_and_input(sub_url: string, input_dict: { [key: string]: any }): Promise<any> {
        let the_url = `${this._service_url}/test_protobuff_code/${sub_url}/`
        try {
            const response = await fetch(the_url, 
            {
                method: "POST",
                body: JSON.stringify(input_dict),
                headers: {
                    "Content-type": "application/json; charset=UTF-8",
                    ...this._header
                }
            });
            var json_response = await response.json()
            this._interceptor_function(json_response)
            return json_response
        } catch (e) {
            return {[this._special_error_key]: String(e)};
        }
    }

    async a_rpc_function(item: test_protobuff_code_objects.User, ignore_error?: boolean): Promise<test_protobuff_code_objects.User | null> {
        let result = await this._get_reponse_or_error_by_url_path_and_input("a_rpc_function", item.to_dict())
        if (Object.keys(result).includes(this._special_error_key)) {
            if ((ignore_error == null) || ((ignore_error != null) && (!ignore_error))) {
                this._error_handle_function(result[this._special_error_key])
            }
            return null
        } else {
            return new test_protobuff_code_objects.User().from_dict(result)
        }
    }
}

export default Client_test_protobuff_code

let client = new Client_test_protobuff_code("hhh", {dd: "2"}, )
let response = await client.a_rpc_function(new test_protobuff_code_objects.User())