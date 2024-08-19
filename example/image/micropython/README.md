# Docs for 8MB memory micropython based phone project

"OpenSmart_LCD 2.4inch 320x240" uses 2 line tx+rx for touch and display. It is OK. (Don't buy opensmart 3.5inch lcd, it is hard to use, they are not using spi or uart protocol. And has no protocol docs.)

ili9341 use 8 lines 2 SPI for touch and display. esp32 only have two spi port, esp32 do not have sd card slot. Which means esp32 are shit. Because if you use esp32 touch screen and display, you won't have access to SD card.

But **pyboard** always has SD card support.

> SPI supports multiple devices using same `sck, mosi, miso` pin, but `cs` pin has to be different for each device.

## About memory
It seems like only 8MB memory micropython board "yd_esp32_s3_n16r8_8ram16flash" can handle this project. 

"pywifi_esp32_8M_ram" or "esp32_wroom_32_8M_ram" is also fine in this case. (MicroPython v1.22.1 on 2024-01-05)

Other board like pi pico will fail on loading font. Even if the font is less than 10kb.

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
SDI(mosi)
SCK/CLK(source clock)
LED(back light, 3.3v on normally, but some needs 0v)
SDO(miso)

T_CLK(touch clock signal)
T_CS(touch chip selection)
T_DIN(touch mosi)
T_DO(touch miso)
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
SDI(mosi)
SCK/CLK(source clock)
BL(screen back light)
SDO(miso)

TCK(clock signal)
TCS(chip selection)
TDI(mosi)
TDO(miso)
PEN
```
