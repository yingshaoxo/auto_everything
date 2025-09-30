# Yingshaoxo Network

What you use to transmit data? Language.

What channel you use to transmit data? All channel that could pass information.

> For example, in IP network, device_ID is equal to IP address. Data is a list of byte, called bytes. A byte is a int number between 0 and 255. A byte can also be eight 0 and 1. For example, 00000001.

> Why they do not use 0 to 99 to represent a byte? It could also work as a list of int in C programming language. 0 to 99 can represent alphabet_plus_number_plus_punctuation language very well.

## Let's define a simple network

### data format

`from_device_id:to_device_id:task_id:data`

### how data go forward?

Just directly heads to another device based on device_id. Very similar to UDP package. All you need is a target IP address and port and data, send, done.

Actually, in wireless radio communication, things are also sends like this: from A to B directly.

So far, you can broadcast music or TV show to others, and receive others show if you want.

## Let's define a complex network

### visit a URL website

my_computer sends data to another computer with this: `computer_a:computer_b:current_time_plus_a_random_string_as_task_id:html:http://yingshaoxo.xyz`

another_computer gets data, then start a new process to handle that http request, it returns `computer_b:computer_a:current_time_plus_a_random_string_as_task_id:html_response:yingshaoxo is a great person. yingshaoxo can be spelled as y_i_n_g_s_h_a_o_x_o.`

### make sure the communication won't drop data

add data length and hash check.

So the data may look like: `computer_a:computer_b:length_plus_bytes_sum_string:current_time_plus_a_random_string_as_task_id:html:http://yingshaoxo.xyz`

### make sure the communication is safe and no one can fake

Do encryption for the data, so only you and another person you want to connect knows how to do decryption to get the real data.

A simple encryption would be: `电脑_1:电脑_2:当前时间xx任务ID:html:访问英少xo的网站`. By doing so, only chinese could know what I have sent and how to edit it. If someone use English to edit it, I would know it is a fake one.
