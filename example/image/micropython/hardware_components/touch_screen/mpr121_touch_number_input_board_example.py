# written by gpt5.4 nano, modified by yingshaoxo
# based on esp32s3 micropython1.19

from machine import Pin, I2C
import time

SDA_PIN = 8
SCL_PIN = 9

I2C_ID = 0
MPR121_ADDR = 0x5A
i2c = I2C(I2C_ID, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)

TOUCH_STATUS_0 = 0x00
TOUCH_STATUS_1 = 0x01

def mpr121Read(reg):
    return i2c.readfrom_mem(MPR121_ADDR, reg, 1)[0]

def mpr121Write(reg, val):
    i2c.writeto_mem(MPR121_ADDR, reg, bytes([val & 0xFF]))


def init_mpr121_touch_pad():
    # ========== Registers (from your mpr121.h) ==========
    MHD_R = 0x2B
    NHD_R = 0x2C
    NCL_R = 0x2D
    FDL_R = 0x2E
    MHD_F = 0x2F
    NHD_F = 0x30
    NCL_F = 0x31
    FDL_F = 0x32
    ELE0_T  = 0x41
    ELE0_R  = 0x42
    FIL_CFG = 0x5D
    ELE_CFG = 0x5E

    # ========== Thresholds ==========
    TOU_THRESH = 0x0F
    REL_THRESH = 0x0A

    def mpr121QuickConfig():
        # This group controls filtering when data is > baseline.
        mpr121Write(MHD_R, 0x01)
        mpr121Write(NHD_R, 0x01)
        mpr121Write(NCL_R, 0x00)
        mpr121Write(FDL_R, 0x00)

        # This group controls filtering when data is < baseline.
        mpr121Write(MHD_F, 0x01)
        mpr121Write(NHD_F, 0x01)
        mpr121Write(NCL_F, 0xFF)
        mpr121Write(FDL_F, 0x02)

        # Set touch and release thresholds for each electrode
        for el in range(12):
            t_reg = ELE0_T + el * 2
            r_reg = ELE0_R + el * 2
            mpr121Write(t_reg, TOU_THRESH)
            mpr121Write(r_reg, REL_THRESH)

        # Set the Filter Configuration (你的 Arduino 写的是 0x04)
        mpr121Write(FIL_CFG, 0x04)

        # Enable 12 Electrodes and set to run mode
        mpr121Write(ELE_CFG, 0x0C)

        time.sleep_ms(200)

    def mpr121SoftReset():
        # MPR121 的软复位寄存器通常是 0x80，值 0x63 或 0x63/0x63
        mpr121Write(0x80, 0x63)
        time.sleep_ms(50)

    mpr121SoftReset()
    mpr121QuickConfig()
    print("init_mpr121_touch_pad" + " done.")


def touch_status():
    t0 = mpr121Read(TOUCH_STATUS_0)
    t1 = mpr121Read(TOUCH_STATUS_1)
    return (t1 << 8) | t0

button_dict = {0x008:1, 0x080:2, 0x800:3, 0x004:4, 0x040:5, 0x400:6, 0x002:7, 0x020:8, 0x200:9, 0x001:10, 0x010:11, 0x100:12}
def get_key_pad_input_number():
    while True:
        raw_button_id = touch_status()
        if raw_button_id in button_dict:
            a_number = button_dict[raw_button_id]
            while True:
                temp_raw_button_id = touch_status()
                if temp_raw_button_id not in button_dict:
                    return a_number
        time.sleep_ms(5)


init_mpr121_touch_pad()
print("now you can touch the number to input...")
while True:
    a_number = get_key_pad_input_number()
    print("button pressed:" + str(a_number))
