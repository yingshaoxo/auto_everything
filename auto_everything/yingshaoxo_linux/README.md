# yingshaoxo_linux_standards

Here, I just want to talk about how to make a free linux by following some standards that yingshaoxo feels OK with.

You can definately copy the newest linux kernel and use it, but it has license, and the newest may not as good as the old one. The old one has more freedom and more stability.

My standards based on MIT license, but the more accurate license is: "Do whatever you want with it, I don't care."


## From what users could see

### 1. Text based command line interface
In linux, there has a principle: "If you can do things with pure text, don't do it with graphic. Because your typing speed is as fast as your thinking speed".

### 2. User has the highest Root permission
In real free linux system, the user always have the highest permission. That is to say, the user can modifying any file in that system. The user can even delete the whole old system and flash (or install) their own new system by doing file copy and paste. Everything is transparent for that user. The user can see and control anything that is running in that system. And user can run any software without limitations.

### 3. Leave user with more freedom as possible
In linux system, the system will always power the user. For example, whenever the hardware has some outside interface, linux will let the user has full control over those outside devices. For example, USB devices, Outside microcontroller pins, speakers, microphones, mouse, keyboard, LED/LCD screen, CPU frequency, Network lines, so on and on.

### 4. Offline Usable
In linux, we do not ask our user to connect network to use the system. We don't want to spy on our users. So we basacally have everything inside, you can use those tools without network. For example, the system will have a programming language compiler or intepreter, then the user can write and compile and run their own software as many as they want.

### 5. Less and Core software
A less than 5MB c compiler and python interpreter is necessary. For other software, unless they can become a loop, self_independent, otherwise, we do not include. What is a self_independent loop? HTTP browser client and HTTP server are two ends software, they must be together. Music MIDI making software and music MIDI player must be together, otherwise, we do not include music player.


## From tech side

### 1. command line interface
Control big led screen is hard, but control a small ASCII char printer and a simple keyboard is easy.

### 2. root permission
Just give the user full permisson on files and folders. And can run any binary software.

### 3. ourside device freedom
Just let the user be able to control the outside device input and output data stream. So that they may write their own hardware driver software. For example, show pictures by using framebuffer pixels rgba array.

### 4. offline usage
Make sure all core function is offline usable. And make sure the programming language compiler is fully staticlly compiled and can be used in offline. Normally it is a staticlly compiled gcc and python. You just have to make sure the programming language support local file import without network.

### 5. small system
To reduce the system size, you can only have a compiler and python, then load any other tools as source code. You do the compile in the installation time. So the final system size is "compiler_size + command_line_tools_source_code size".

### 6. backward compatibility
New system must allow old software to run. Otherwise, no new system should get released. New programming language compiler must be able to compile old code, otherwise, no new compiler should get released. New script interpreter such as python must be able to run old script, otherwise, we give up new version of python. For example, if python3 can't run python2 code, we will not include python3, and will always use python2.

### 7. network implementation
The user can use pins to connect their own network devices. (pins are micro_controller pins) There are so many network method. Free to do whatever you like, wire or wireless, one line or two line or 4 lines, nobody cares. As for IP/HTTP proxy implementation, just make sure the proxy can be customized to change 'source_ip to target_ip', change 'source_ip:port to another_ip:different_port'. The IP here can be a HTTP address. All in all, since you have handled a package to another person to process, that package should be fully change_able for that person.


## From hardware side

The hardware is composed by two part: the host x86 cpu and two micro_controllers. The host x86 computer handles the system level computation, the micro_controllers receive or send data between system and outside devices. For example, the system sends user interface graph to micro_controller_1, so the micro_controller_1 can display that picture to the LED panel. Another example is, micro_controller_2 receive pin callback signal as keyboard input, it sends data to the host x86 system. Third example is micro_controller_2 can expose pins to users, the host x86 system can crontrol those pins, let a pin be high or low, 5 voltage or 0 voltage, and micro_controller_2 can also sends pin anolog or digital value back. So the host x86 system can directly receive voltage anolog signal from microphone to record sound, and directly output voltage to control a speaker to make sound,  

In the first level, we will let the micro_controller_2 has 40 pins, 20 are digital pins, 20 are anolog pins, users can use it with freedom. The micro_controller system can tatolly replace the complex USB system.

The data transfer protocol is simple. in micro_controller and host side, pin_A for signal_timer, it will generate time signal, it will loop 0 and 1 forever, when you detect voltage change, you have to take a sample data in other data pin to get other pin data. It helps synchronize signal transmition. pin_B is a line for host to micro_controller single way data pipe, in that line, data will only go from host to micro_controller. It only have 0 and 1 two status. pin_C is a line for micro_controller to host single way data pipe, in that line, data will only go from micro_controller to host, it has 0 and 1 two status.

The data format is simple: pure ascii bytes stream. For example: "pin33 1; pin35 0; pin26 1" or "pin12 3.7; pin17 1.5; pin8 4.9". If there has no data change, we transfer new line "\n". In micro_controller, if host did not change old pin status, it keeps the last status.

All micro_controller pins will get exposed in the right side of our computer. the left side will keep 2 old USB_A interface, audio input and output interface (3.5mm headphone jack), Ethernet cable line interface, CD or DVD interface if have space.

As for the system boot mechanism, we will hard code a small disk as boot disk, it supports bios/MBR partition. We will suggest usesrs to put their data into another disk, so that disk can be greater than 2TB.

> How to let x86 CPU take less electricity power and has less heat? Lower the CPU frequency, or lower the speed of 'crystal oscillation frequency' in hardware level. If we make the calculation speed of x86 to '0.3' of normal PC CPU, we could simply use this kind of x86 CPU to anywhere, such as mobile phone. Mobile phone handles less pixel number than PC, so it does not need many computation resources.

As for wireless device, we use radio tech, which means send bytes data out in a broadcast way, anyone can receive it, encrypt data yourself, not hardware. Of cause we also have to receive that bytes data. The send and receive part can be done by using one module two pins, tx and rx, based on UART. But we also allow one pin to send data out, one pin to receive data as two modules without UART. We seperate channels by leading bytes, like "device_id + ',' + length + ',' + bytes_data". The frequency is normally in range of [300kHz, 433MHz, 2GHz]. We use an anolog pin to change sender/receiver frequency, for example, 5V means maximum_frequency, 0V means minimum_frequency, which normally cause no_data_sending.

### Solution 2

Sometimes, we can't built a x86 CPU or motherboard by ourselves, how do we do? We use something else. For example, if we have 6 micro_controller: micro_controller_A is for reading keyboard signal and convert it into ASCII code and send it to other microcontroller 30 times per second. micro_controller_B is for sending text or grapic pixels to LED screen to show information. micro_controller_C is for handling the keyboard ASCII 128 characters input and do some operations, then output some results to the screen. micro_controller_D is for disk or storage operations, it handles data saving and reading. micro_controller_E is for sending and receiving digital_and_analog pin value, it works as USB, but much more open, for example, you can use it to make your own recorder and speaker.

This is just an archetecture or framework, you can even use other small computing devices to finish the whole computer, for example, you can use 5 mobile devices to do the same thing.

> 'Electronic Ink Screen' could save power, better use it as screen. Because for terminal or shell operations, white and black screen is good enough. (Some people even created 7 color E_ink_screen.)

> Just think this: what if human network are a computer. You see, some people collect information, some people do decisions based on information, some people save experiment data and history as knowledge base, some poeple work as an interface to make friends with outside world, and they all are belonging to one group.


## From software side

Solve the following questions:

1. how to create python3.2 by using pure C from scratch?
2. how to create a c compiler that similar to gcc from scratch?
3. how to create a computer that could run a c compiler from scratch?
4. how to make a better c language that uses english full name for keywords?
5. how to use python3.2 to make every software you want?
