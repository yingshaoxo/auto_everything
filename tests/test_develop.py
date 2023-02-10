from auto_everything.develop import GRPC

grpc_ = GRPC()

def test_generate_key_string_map_from_protocols():
    # grpc_.generate_key_string_map_from_protocols(
    #     "rust", 
    #     "/Users/yingshaoxo/CS/we_love_party/party_protocols/protocols", 
    #     "/Users/yingshaoxo/CS/we_love_party/rust_internal_api_system/src/grpc_key_string_maps")

    # grpc_.generate_key_string_map_from_protocols(
    #     "kotlin", 
    #     "/Users/yingshaoxo/CS/we_love_party/party_protocols/protocols", 
    #     "/Users/yingshaoxo/CS/we_love_party/java_free_map_backend_system/app/src/main/kotlin/grpc_key_string_maps")

    grpc_.generate_key_string_map_from_protocols(
        "python", 
        "/Users/yingshaoxo/CS/we_love_party/party_protocols/protocols", 
        "/Users/yingshaoxo/CS/we_love_party/python_chat_with_friends_system/src/grpc_key_string_maps")