# Docs for micropython

OpenSmart_LCD uses 2 line tx+rx for touch and display. It is OK.

ili9341 use 8 lines 2 SPI for touch and display. esp32 only have two spi port, esp32 do not have sd card slot. Which means esp32 are shit. Because if you use esp32 touch screen and display, you won't have access to SD card.

But **pyboard** always has SD card support.

> SPI supports multiple devices using same `sck, mosi, miso` pin, but `cs` pin has to be different for each device.
