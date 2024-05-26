# yingshaoxo_linux_standards

Here, I just want to talk about how to make a free linux by following some standards that yingshaoxo feels OK with.

You can definately copy the newest linux kernel and use it, but it has license, and the newest may not as good as the old one. The old one has more freedom and more stability.

My standards based on MIT license, but the more accurate license is: "Do whatever you want with it, I don't care."

## From what users could see

### 1. Text based command line interface
In linux, there has a principle: "If you can do things with pure text, don't do it with graphic. Because your typing speed is as fast as your thinking speed".

### 2. User has the highest Root permission
In real free linux system, the user always have the highest permission. That is to say, the user can modifying any file in that system. The user can even delete the whole old system and flash (or install) their own new system. Everything is transparent for that user. The user can see and control anything that is running in that system.

### 3. Leave user with more freedom as possible
In linux system, the system will always power the user. For example, whenever the hardware has some outside interface, linux will let the user has full control over those outside devices. For example, USB devices, Outside microcontroller pins, speakers, microphones, mouse, keyboard, LED screen, CPU frequency, Network lines, so on and on.

### 4. Offline Usable
In linux, we do not ask our user to connect network to use the system. We don't want to spy on our users. So we basacally have everything inside, you can use those tools without network. For example, the system will have a programming language compiler or intepreter, then the user can write and compile and run their own software as many as they want.

## From tech side

### 1. command line interface
Control big led screen is hard, but control a small ASCII char printer and a simple keyboard is easy.

### 2. root permission
Just give the user full permisson on files and folders.

### 3. ourside device freedom
Just let the user be able to control the outside device input and output data stream. So that they may write their own hardware driver software.

### 4. offline usage
Make sure all core function is offline usable. And make sure the programming language compiler is fully staticlly compiled and can be used in offline. Normally it is a staticlly compiled gcc and python. You just have to make sure the programming language support local file import without network.

### 5. small system
To reduce the system size, you can only have a compiler and python, then load any other tools as source code. You do the compile in the installation time. So the final system size is "compiler_size + command_line_tools_source_code size".
