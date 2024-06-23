# yingshaoxo_linux_standards

Here, I just want to talk about how to make a free linux by following some standards that yingshaoxo feels OK with.

You can definately copy the newest linux kernel and use it, but it has license, and the newest may not as good as the old one. The old one has more freedom and more stability.

My standards based on MIT license, but the more accurate license is: "Do whatever you want with it, I don't care."


## From what users could see

### 1. Text based command line interface
In linux, there has a principle: "If you can do things with pure text, don't do it with graphic. Because your typing speed is as fast as your thinking speed".

### 2. User has the highest Root permission
In real free linux system, the user always have the highest permission. That is to say, the user can modifying any file in that system. The user can even delete the whole old system and flash (or install) their own new system by doing file copy and paste. Everything is transparent for that user. The user can see and control anything that is running in that system.

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


## From hardware side

The hardware is composed by two part: the host x86 cpu and two micro_controllers. The host x86 computer handles the system level computation, the micro_controllers receive or send data between system and outside devices. For example, the system sends user interface graph to micro_controller_1, so the micro_controller_1 can display that picture to the LED panel. Another example is, micro_controller_2 receive pin callback signal as keyboard input, it sends data to the host x86 system. Third example is micro_controller_2 can expose pins to users, the host x86 system can crontrol those pins, let a pin be high or low, 5 voltage or 0 voltage, and micro_controller_2 can also sends pin anolog or digital value back. So the host x86 system can directly receive voltage anolog signal from microphone to record sound, and directly output voltage to control a speaker to make sound,  

In the first level, we will let the micro_controller_2 has 40 pins, 20 are digital pins, 20 are anolog pins, users can use it with freedom. The micro_controller system can tatolly replace the complex USB system.

The data transfer protocol is simple. in micro_controller and host side, pin_A for signal_timer, it will generate time signal, it will loop 0 and 1 forever, when you detect voltage change, you have to take a sample data in other data pin to get other pin data. It helps synchronize signal transmition. pin_B is a line for host to micro_controller single way data pipe, in that line, data will only go from host to micro_controller. It only have 0 and 1 two status. pin_C is a line for micro_controller to host single way data pipe, in that line, data will only go from micro_controller to host, it has 0 and 1 two status.

The data format is simple: pure ascii bytes stream. For example: "pin33 1; pin35 0; pin26 1" or "pin12 3.7; pin17 1.5; pin8 4.9". If there has no data change, we transfer new line "\n". In micro_controller, if host did not change old pin status, it keeps the last status.

All micro_controller pins will get exposed in the right side of our computer. the left side will keep 2 old USB_A interface, audio input and output interface (3.5mm headphone jack), Ethernet cable line interface, CD or DVD interface if have space.

As for the system boot mechanism, we will hard code a small disk as boot disk, it supports bios/MBR partition. We will suggest usesrs to put their data into another disk, so that disk can be greater than 2TB.
