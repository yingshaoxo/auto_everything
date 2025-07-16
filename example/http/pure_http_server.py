import socket

def handle_request(request_type, url, url_key_and_value_dict, raw_data):
    if request_type == "GET" and (url == "/" or url.startswith("/?")):
        return "html", """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <!--[if !IE]>-->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!--<![endif]-->
    <title>Chat</title>
    <style type="text/css">
        #input_container {
            display:flex;
            flex-direction:row;
            justify-content:start;
            align-items:center;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div id="chat-container">
        <div id="chat-header">
            <h1>Chat with <a href="http://ask.ai-tools-online.xyz/chat_page" target="_blank" style="color: #4682B4; text-decoration: none;">yingshaoxo</a></h1>
        </div>
        <div id="chat-history"></div>
        <div id="input_container">
            <textarea id="message_input" cols="40" rows="3"></textarea>
            <input style="margin-left: 15px; padding: 2px; padding-left: 10px; padding-right: 10px; height: 60px;" type="button" id="send-button" value="Send" onclick="window.sendMessage()" />
        </div>

        <form action="/new_message?" method="post">
            <div style="display: flex; flex-direction: row; width: 100%; margin-top: 20px;">
                <div>
                    <textarea id="a_textarea" type="text" name="text" style="height: 30px; width: 400px;"></textarea>
                </div>
                <div style="margin-top: 5px; display: flex; flex-direction: row;">
                    <input type="submit" value="Form Submit It" style="margin-left: 15px; padding: 2px; padding-left: 10px; padding-right: 10px;" />
                </div>
            </div>
        </form>
    </div>

    <script type="text/javascript">
    //<![CDATA[
    window.sendMessage = function() {
        var input = document.getElementById('message_input');
        var message = input.value;
        if (!message) return;

        addMessage(message, true);
        input.value = '';

        var xhr;
        try {
            xhr = new ActiveXObject("Microsoft.XMLHTTP");
        } catch(e) {
            try {
                xhr = new XMLHttpRequest();
            } catch(e) {
                alert("Your browser does not support AJAX!");
                return false;
            }
        }

        // Using a separate function for the callback to avoid scope issues in IE6
        function handleResponse() {
            if (xhr.readyState == 4) {
                if (xhr.status == 200) {
                    addMessage(xhr.responseText, false);
                }
            }
        }
        xhr.onreadystatechange = handleResponse;

        try {
            var url = "/chat?message=" + escape(message);
            xhr.open("GET", url, true);
            xhr.send(null);  // IE6 requires null parameter
        } catch(e) {
            alert("Error sending message");
            return false;
        }
    };

    function addMessage(text, isUser) {
        try {
            var chatHistory = document.getElementById('chat-history');
            var messageDiv = document.createElement('div');

            messageDiv.className = 'message';
            messageDiv.className += isUser ? ' user-message' : ' ai-message';

            var lines = text.split('\\n');
            for (var i = 0; i < lines.length; i++) {
                if (i > 0) {
                    var br = document.createElement('br');
                    messageDiv.appendChild(br);
                }
                var textNode = document.createTextNode(lines[i] || ' ');
                messageDiv.appendChild(textNode);
            }

            chatHistory.appendChild(messageDiv);

            // Add clearfix div after each message
            var clearfix = document.createElement('div');
            clearfix.className = 'clearfix';
            chatHistory.appendChild(clearfix);

            // Scroll to bottom
            var scrollHeight = chatHistory.scrollHeight;
            if (scrollHeight) {
                chatHistory.scrollTop = scrollHeight;
            }
        } catch(e) {
            alert("Error adding message");
        }
    }

    // Simple cross-browser event handler
    document.getElementById('message_input').onkeypress = function(e) {
        e = e || window.event;
        var keyCode = e.keyCode || e.which;
        return true;
    };
    //]]>
    </script>
</body>
</html>
"""
    elif url.startswith("/chat?"):
        message = url_key_and_value_dict.get("message", "")
        return "text", "server response: " + message
    elif url.startswith("/new_message?"):
        message = url_key_and_value_dict.get("text", "")
        return "text", "it is a form post message: " + message + "\n" + "But it will not show in web page later (Because I am lazy for implementing the functionality)."
    else:
        return "text", 'Hello, welcome to AI chat.'

def url_decode(encoded_string):
    result = ""
    i = 0
    while i < len(encoded_string):
        if encoded_string[i] == '+':
            result += ' '
            i += 1
        elif encoded_string[i] == '%':
            try:
                hex_code = encoded_string[i + 1:i + 3]
                char = chr(int(hex_code, 16))
                result += char
                i += 3
            except (ValueError, IndexError):
                result += encoded_string[i]
                i += 1
        else:
            result += encoded_string[i]
            i += 1
    return result

def parse_url(request):
    request_type = request.strip().split(" ")[0]
    if not request_type == "GET" and not request_type == "POST":
        return request_type, "", {}, ""
    else:
        url = request.split(" ")[1]
        url_dict = {}
        key_value_text_list = []
        raw_data = ""
        if request_type == "GET":
            url_dict = {}
            if "?" in url:
                key_value_text_list = url.split("?")[1].split("&")
        elif request_type == "POST":
            raw_string = request.split("\r\n\r\n")[1].strip()
            key_value_text_list = raw_string.split("&")
            raw_data = raw_string

        for key_and_value_text in key_value_text_list:
            splits = key_and_value_text.split("=")
            if len(splits) == 2:
                key, value = splits
                url_dict[key] = url_decode(value)

        return request_type, url, url_dict, raw_data

def work_function(port_in_number=8899):
    print("Starting AI chat server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', port_in_number))
    server_socket.listen(100)
    print("Chat server ready.\n")
    print("http://127.0.0.1:" + str(port_in_number))

    while True:
        try:
            client_socket, addr = server_socket.accept()
            request = client_socket.recv(20480).decode('utf-8')
            request_type, url, url_key_and_value_dict, raw_data = parse_url(request)

            return_type, return_value = handle_request(request_type, url, url_key_and_value_dict, raw_data)

            response = 'HTTP/1.1 200 OK\n'
            if return_type == "html":
                response += "Content-Type: text/html\n\n"
                response += return_value
            elif return_type == "text":
                response += "\n" + return_value

            client_socket.sendall(response.encode('utf-8'))
            client_socket.close()
        except Exception as e:
            print(e)

if __name__ == '__main__':
    work_function(9999)
