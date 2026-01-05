# made by doubao ai
from machine import Pin, SoftSPI
import time

# -------------------------- Configuration Parameters --------------------------
# DG25Q128CSIG Command Set
CMD_READ_ID = 0x9F        # Read manufacturer and device ID
CMD_READ = 0x03           # Standard data read
CMD_PAGE_PROGRAM = 0x02   # Page program (write data, 256 bytes per page)
CMD_SECTOR_ERASE = 0x20   # Sector erase (4KB bytes)
CMD_WRITE_ENABLE = 0x06   # Write enable (must be called before write/erase)
CMD_WRITE_DISABLE = 0x04  # Write disable
CMD_READ_STATUS1 = 0x05   # Read status register 1 (check busy state)

# DG25Q128CSIG Capacity Parameters
PAGE_SIZE = 256           # 256 bytes per page
SECTOR_SIZE = 4096        # 4096 bytes (4KB) per sector
DEVICE_SIZE = 16 * 1024 * 1024  # Total capacity 16MB (128M-bit)
CS_PIN = 13               # Chip select pin

# -------------------------- DG25Q128 Class Definition --------------------------
class DG25Q128_Flash_Storage:
    def __init__(self):
        # Initialize SoftSPI with specified parameters
        self.spi = SoftSPI(
            baudrate=9600,
            polarity=1,
            phase=0,
            sck=Pin(10),
            mosi=Pin(11),
            miso=Pin(12)
        )

        # Initialize chip select pin (push-pull output, default high level)
        self.cs = Pin(CS_PIN, Pin.OUT, value=1)

        # Verify Flash connection
        self.manufacturer_id, self.device_id = self.read_id()
        manu_id_hex = "0x{:02X}".format(self.manufacturer_id)
        dev_id_hex = "0x{:04X}".format(self.device_id)
        print("Manufacturer ID: {}".format(manu_id_hex))
        print("Device ID: {}".format(dev_id_hex))

        # Check if DG25Q128CSIG is detected
        if self.manufacturer_id != 0xC8 or (self.device_id & 0xFFFF) != 0x4018:
            print("Warning: DG25Q128CSIG Flash not detected! Please check wiring.")
        else:
            print("DG25Q128CSIG initialized successfully!")

    # -------------------------- Basic Operation Functions --------------------------
    def _cs_low(self):
        """Pull CS pin low to start communication"""
        self.cs.value(0)
        time.sleep_us(1)  # Short delay for signal stability

    def _cs_high(self):
        """Pull CS pin high to end communication"""
        time.sleep_us(1)
        self.cs.value(1)

    def write_enable(self):
        """Write enable: Must be called before write/erase operations"""
        self._cs_low()
        self.spi.write(bytearray([CMD_WRITE_ENABLE]))
        self._cs_high()
        time.sleep_us(10)  # Wait for command to take effect

    def write_disable(self):
        """Write disable: Prevent accidental operations after write/erase"""
        self._cs_low()
        self.spi.write(bytearray([CMD_WRITE_DISABLE]))
        self._cs_high()
        time.sleep_us(10)

    def is_busy(self):
        """Check if Flash is busy (Bit 0 of status register 1 = 1 means busy)"""
        self._cs_low()
        self.spi.write(bytearray([CMD_READ_STATUS1]))
        status = self.spi.read(1)[0]
        self._cs_high()
        return (status & 0x01) == 0x01  # Return True if busy, False if idle

    def wait_idle(self):
        """Wait until Flash is idle (blocking when busy)"""
        while self.is_busy():
            time.sleep_us(100)

    # -------------------------- Core Function Functions --------------------------
    def read_id(self):
        """Read manufacturer ID and device ID to verify Flash connection"""
        self._cs_low()
        # Send read ID command and read 3 bytes (1 byte manu ID + 2 bytes device ID)
        self.spi.write(bytearray([CMD_READ_ID]))
        id_data = self.spi.read(3)
        self._cs_high()
        manufacturer_id = id_data[0]
        device_id = (id_data[1] << 8) | id_data[2]
        return manufacturer_id, device_id

    def _read_data(self, addr, length):
        """
        Internal data read function
        :param addr: Start address (3 bytes, 0 ~ 0xFFFFFF)
        :param length: Data length to read
        :return: Read byte array
        """
        if addr + length > DEVICE_SIZE:
            raise ValueError("Read address out of Flash capacity range")

        self.wait_idle()  # Wait for Flash to be idle
        self._cs_low()

        # Send read command + 3-byte address (big-endian, high byte first)
        cmd = bytearray([CMD_READ])
        cmd.append((addr >> 16) & 0xFF)
        cmd.append((addr >> 8) & 0xFF)
        cmd.append(addr & 0xFF)
        self.spi.write(cmd)

        # Read specified length of data
        data = self.spi.read(length)
        self._cs_high()
        return data

    def _sector_erase(self, addr):
        """
        Internal sector erase function (4KB)
        :param addr: Sector start address (must be 4096-byte aligned)
        """
        if addr % SECTOR_SIZE != 0:
            raise ValueError("Sector erase address must be 4096-byte aligned")
        if addr >= DEVICE_SIZE:
            raise ValueError("Erase address out of Flash capacity range")

        self.write_enable()  # First enable write
        self.wait_idle()     # Wait for idle
        self._cs_low()

        # Send sector erase command + 3-byte address
        cmd = bytearray([CMD_SECTOR_ERASE])
        cmd.append((addr >> 16) & 0xFF)
        cmd.append((addr >> 8) & 0xFF)
        cmd.append(addr & 0xFF)
        self.spi.write(cmd)

        self._cs_high()
        self.wait_idle()     # Wait for erase completion
        self.write_disable() # Disable write after erase

    def _page_program(self, addr, data):
        """
        Internal page program function
        :param addr: Start address (0 ~ 0xFFFFFF)
        :param data: Byte array to write (length <= 256)
        """
        if len(data) > PAGE_SIZE:
            raise ValueError("Single write data length cannot exceed 256 bytes")
        if addr + len(data) > DEVICE_SIZE:
            raise ValueError("Write address out of Flash capacity range")

        # Check if cross page (prevent write failure)
        page_start = addr & 0xFFFFFF00  # Page start address (256-byte aligned)
        page_end = page_start + PAGE_SIZE
        if addr + len(data) > page_end:
            raise ValueError("Write data cannot cross pages, please split and write")

        self.write_enable()  # First enable write
        self.wait_idle()     # Wait for idle
        self._cs_low()

        # Send page program command + 3-byte address
        cmd = bytearray([CMD_PAGE_PROGRAM])
        cmd.append((addr >> 16) & 0xFF)
        cmd.append((addr >> 8) & 0xFF)
        cmd.append(addr & 0xFF)
        self.spi.write(cmd)

        # Write data
        self.spi.write(bytearray(data))
        self._cs_high()
        self.wait_idle()     # Wait for write completion
        self.write_disable() # Disable write after write

    # -------------------------- High Level Public Functions --------------------------
    def write_bytes(self, address, bytes_data, length):
        """
        High level function: Write specified length of bytes to target address
        :param address: Target start address (0 ~ 0xFFFFFF)
        :param bytes_data: Byte array to be written
        :param length: Length of data to write (must match actual valid data length)
        """
        # Truncate data to specified length
        write_data = bytes_data[:length]
        current_addr = address

        # Calculate total bytes to write
        remaining_bytes = length

        while remaining_bytes > 0:
            # Calculate sector address for current position (erase first)
            sector_addr = current_addr & 0xFFFFF000  # 4KB aligned
            self._sector_erase(sector_addr)

            # Calculate bytes to write in current page
            page_offset = current_addr % PAGE_SIZE
            write_bytes_in_page = min(PAGE_SIZE - page_offset, remaining_bytes)

            # Write data to current page
            self._page_program(current_addr, write_data[:write_bytes_in_page])

            # Update variables for next iteration
            current_addr += write_bytes_in_page
            write_data = write_data[write_bytes_in_page:]
            remaining_bytes -= write_bytes_in_page

    def read_bytes(self, address, length):
        """
        High level function: Read specified length of bytes from target address
        :param address: Target start address (0 ~ 0xFFFFFF)
        :param length: Length of data to read
        :return: Read byte array
        """
        return self._read_data(address, length)

def test_dg25q128_function():
    # Initialize DG25Q128
    flash = DG25Q128_Flash_Storage()

    # Test parameters
    test_addr = 0x000000

    # test last time saved data
    read_data = flash.read_bytes(test_addr, 19)
    print("\n\nlast saved data: {}".format(read_data))

    # Save new data by using the following code
    test_data = b"Hello, DG25Q128CSIG! This is MicroPython Test."
    test_length = len(test_data)

    # Print test info
    print("Data to write: {}".format(test_data))
    print("Data length: {} bytes".format(test_length))

    try:
        # Write data using high level function
        print("Writing data...")
        flash.write_bytes(test_addr, test_data, test_length)

        # Read data using high level function
        print("Reading data...")
        read_data = flash.read_bytes(test_addr, test_length)
        print("Read data: {}".format(read_data))

        # Verify data
        if read_data == test_data[:test_length]:
            print("Data write & read verification successful!")
        else:
            print("Data write & read verification failed!")
    except Exception as e:
        print("Test error: {}".format(e))


if __name__ == "__main__":
    pass

