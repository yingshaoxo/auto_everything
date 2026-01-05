# DG25Q128_flash_storage

## pin map

### english
there has a circle dot, consider it as left_top.

1    8
2    7
3    6
4    5

1: CS, chip selection, 0v to enable this chip
2: SO(MISO), data signal output, this storage chip send data to others
3: WP, writing protection, 0v to stop writing, 3v to allow writing (the better way is cut the power of this chip)
4: VSS, ground, 0v

8: VCC, 3v power
7: HOLD/RESET, hold or reset input, 0v to pause communication, 3v to continue communication
6: SCLK, outside Serial Clock
5: SI(MOSI), data signal input, others send data to this storage chip

### chinese

DG25Q128CSIG 引脚	功能说明	推荐 Pico 引脚	备注

CS/SS (Pin 1)	片选信号（低电平有效）	GP5	可自定义其他 GPIO
MISO (Pin 2)	主机收 / 从机发数据	GP4	数据读取 Flash
WP (Pin 3)	写保护（低电平写保护）	GP8	高电平解除写保护
GND (Pin 4)	接地	GND	共地保证通信稳定

VCC (Pin 8)	电源（3.3V）	3.3V	不可接 5V，避免烧毁
HOLD (Pin 7)	暂停通信（低电平有效）	GP9	高电平正常通信
SCK (Pin 6)	SPI 时钟信号	GP6	SPI 主机提供时钟
MOSI (Pin 5)	主机发 / 从机收数据	GP7	数据写入 Flash

注：WP 和 HOLD 引脚若不需要使用，可直接接 3.3V 上拉，无需占用 Pico GPIO（对应代码中可省略相关配置）。

### line connect guide
Just connect [8, 3, 7] to 3V, connect [4] to 0v, connect [1,6,5,2] to [0v_enable_pin, sck,mosi,miso].

You might notice, this flash storage chip has pin design problem, it should put the [1,6,5,2] into one side, while [3,8,7,4] in another side. so that we can just put its pin into micro_controller pin hole. and connect [8,3,7] as one pin.

### code guide
```
1. write the micropython program
2. do not use WP_PIN,HOLD_PIN. connect them to 3.3v directly
3. use softSPI with 9600, SoftSPI(baudrate=9600, polarity=1, phase=0, sck=Pin(10), mosi=Pin(11), miso=Pin(12)), chip_selection_pin=13
4. do not use f format, use "".format()
5. make sure in the end, there has 2 high level function: write_bytes(address, bytes_data, length) and read_bytes(address, length)
6. use english as comment language
```

## final note
yingshaoxo:

I would suggest use SD/TF card, because it can save 1GB data.

So that you can listen some music.

But all those storage device that you buy has limited life. The data will lose after 6 months of no power.

Create by yourself.
