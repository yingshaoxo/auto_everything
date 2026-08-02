# Docs for 8MB memory micropython based phone project

"OpenSmart_LCD 2.4inch 320x240" uses 2 line tx+rx for touch and display. It is OK. (Don't buy opensmart 3.5inch lcd, it is hard to use, they are not using spi or uart protocol. And has no protocol docs.)

ili9341 use 8 lines 2 SPI for touch and display. esp32 only have two spi port, esp32 do not have sd card slot. Which means esp32 are shit. Because if you use esp32 touch screen and display, you won't have access to SD card.

But **pyboard** always has SD card support.

> SPI supports multiple devices using same `sck, mosi, miso` pin, but `cs` pin has to be different for each device.

## About memory
It seems like only 8MB memory micropython board "yd_esp32_s3_n16r8_8ram16flash" can handle this project. 

"pywifi_esp32p_8M_ram" is also fine in this case. (MicroPython v1.22.1 on 2024-01-05)

Other boards, such as 'pi pico' will fail on loading font. Even if the font is less than 10kb. (But I managed to fix this problem by slowing down the process speed and use less memory.)

## critical bugs

even comments in code will increase memory, and you can not use garbage.collect() to reduce the memory usage. after you import a module, you can not use del module to reduce memory usage.

it is like when you open a software, it takes more than 10mb plus memory, but when you close that software or application, the memory usage will not go down. so if you open and close some apps multiple times, the device simply go to died because memory is full.

> maybe you can try 'from machine import soft_reset; soft_reset();', but what is the point? reboot can solve all memory bugs?

```
2026: 我突然发现所有的micropython固件系统，都有一个bug，它连注释都算做内存占用，都要新增内存占用，并且用garbage.collect()都消除不了这种内存占用。代码注入执行越多，越容易内存耗尽而死机。

它是连代码本身也会增加内存消耗。"import xxx; del xxx;"并不会清除内存占用。

这个bug截止2026年，有7、8年了，都没有人发现。

> 据说是因为里面有个特别傻逼的qstr符号表，会把所有遇到的代码文本都永久性存储下来，删都删不掉，直接把内存撑爆，除非machine.soft_reset()。

> 这个bug最明显的功效是，假设你搞了个命令行终端程序，动态执行不同的py小程序，慢慢的设备就内存爆炸死机了。或者用户不停的打开并关闭很多界面app，每次打开一个应用程序，内存增加几十MB，关掉后内存也清除不了，然后手机就死机了。

> 比较明显的一个例子是这两行代码，运行一次内存少一点，特别是你在前面增加一个超长注释: from gc import mem_free, collect; print("Has memory of", mem_free()/1024, "KB.");
```

## Some words
```
mosi: master output, slave input; master send data, slave receive data.
miso: master input, slave output; master receive data, slave send data.
master means the main micro_controller, slave means the outside device that uses SPI protocol, here, it is SD card module or screen module.
```


## ili9341 led screen
```
VCC(vcc, 3.3v)
GND(ground)
CS(chip selection)
RESET
DC(data or command)
SDI(serial data input to lcd, mosi)
SCK/CLK(source clock)
LED(back light, 3.3v on normally, but some needs 0v)
SDO(serial data output from lcd, miso)

T_CLK(touch clock signal)
T_CS(touch chip selection)
T_DIN(serial data input to lcd, touch mosi)
T_DO(serial data output from lcd, touch miso)
T_IRQ(interrupt pin)
```

## ili9488 led screen. Do not recommend for using, because the communication is difficult and unstable for different product you buy
The seller only provides stm32 example, which is not good.

I tried a ili9488 github micropython library, it is not working, nothing got display.

It means even for a product have the same name "ili9488", they use different driver board, some of them has backdoor code or have seted a password, you can't init your screen because of that. (有些人戏称这种生产者为“加密狗”)

```
VDD(vcc, 3.3v)
GND(ground)
CS(chip selection)
RST(reset)
D/C
SDI(serial data input to lcd, mosi)
SCK/CLK(source clock)
BL(screen back light)
SDO(serial data output from lcd, miso)

TCK(clock signal)
TCS(chip selection)
TDI(serial data input to lcd, touch mosi)
TDO(serial data output from lcd, touch miso)
PEN(interrupt pin when pen touch down)
```
