# LCD (Liquid-crystal display)

There has many LCD in the market, i think the most useful one has following feature:
1. only need 2 line or 3 line to work. SPI protocol.
2. you can draw string or pixel by a single command: draw_string(y,x,text) and draw_pixel(y,x,(r,g,b)) and clear_screen(r,g,b).
3. you will not need to manually handle font, because it takes memory and storage and processing speed. (for some LCD in the market, if you set cpu speed to 1000 per second, it will not work)

## ST7920 12864 LCD (or DV12864KZK-1_v1)

you have to connect some point in the board to make it use 'serial mode'. it might be 'S' point. (or PSB pin set to 0, PSB means 'Parallel or Serial Binary')

Drive such LCD only need 3 lines: RS, RW, E.
RS: it is the chip_selection. or CS.
RW: serial_data. or MOSI/SDO/DO(data_output).
E: serial_clock. or SCK.

some code:
```
#include <Arduino.h>

// author: yingshaoxo

// ***************
// ****************
// SET LCD!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// ***************
// ****************
/* D9:E, D8:RW, D7:RS */
#define chip_select_1 digitalWrite(7, HIGH) //RS
#define chip_select_0 digitalWrite(7, LOW)
#define serial_data_input_1 digitalWrite(8, HIGH) //R/W
#define serial_data_input_0 digitalWrite(8, LOW)
#define serial_clock_1 digitalWrite(9, HIGH) //E
#define serial_clock_0 digitalWrite(9, LOW)

void send_byte(unsigned char eight_bits)
{
    unsigned int i;

    for (i = 0; i < 8; i++)
    {
        if ((eight_bits << i) & 0x80)
        {
            serial_data_input_1;
        }
        else
        {
            serial_data_input_0;
        }
        serial_clock_0;
        serial_clock_1;
    }
}

void write_command(unsigned char command)
{
    chip_select_1;

    send_byte(0xf8);
    send_byte(command & 0xf0);        
    send_byte((command << 4) & 0xf0);

    delay(1);
    chip_select_0;
}

void write_data(unsigned char character)
{
    chip_select_1;

    send_byte(0xfa);
    send_byte(character & 0xf0);        
    send_byte((character << 4) & 0xf0);

    delay(1);
    chip_select_0;
}

void print_string(unsigned int y, unsigned int x, char *a_string)
{
    // super quick
    unsigned char *string = a_string;
    switch (y)
    {
    case 0:
        write_command(0x80 + x);
        break;
    case 1:
        write_command(0x90 + x);
        break;
    case 2:
        write_command(0x88 + x);
        break;
    case 3:
        write_command(0x98 + x);
        break;
    default:
        break;
    }

    while (*string > 0)
    {
        write_data(*string);
        string++;
        delay(1);
    }
}

void clear_the_screen() {
    write_command(0x01);
    return;
}

// Global temp frame buffer array, 1024 bytes (64*128/8), initialized to all 0 to avoid stack overflow
unsigned char the_lcd_fixed_frame_buffer[1024] = {0}; 

void clear_graphic_screen() {
    //0x30  Basic instruction set
    //0x34  Extended instruction set
    //0x36  Graphic display on
    //0x38  Graphic display off

    // Clear our memory frame buffer first
    for (int i=0; i<1024; i++) {
        the_lcd_fixed_frame_buffer[i] = 0;
    }
    
    // Clear the real LCD screen
    write_command(0x34);
    for (uint8_t y_pair = 0; y_pair < 32; y_pair++) {
        for (uint8_t x_byte = 0; x_byte < 16; x_byte++) {
            write_command(0x80 + y_pair);
            write_command(0x80 + x_byte);
            write_data(0x00);
            write_data(0x00);
        }
    }
    write_command(0x36);
    write_command(0x30);
}

void draw_pixel(int y, int x, int value) {
    // Value can be 0 or 1, 1 means light up that point
    // Call update_graphic_screen() to do real update later
    
    // Coordinate validity check (LCD resolution: 128x64, x:0-127, y:0-63)
    if (x < 0 || x >= 128 || y < 0 || y >= 64) {
        return;
    }

    // 1. Calculate pixel position in frame buffer (fully aligned with reference code logic)
    unsigned char x_byte = x / 16;          // Horizontal direction: 16 pixels/word → 0~7
    unsigned char x_bit = x % 16;           // Bit offset within word: 0~15
    unsigned char y_byte = y / 32;          // 0=upper screen, 1=lower screen
    unsigned char y_bit = y % 32;           // Vertical line number: 0~31

    // 2. Calculate byte index in frame buffer
    // Frame buffer structure: [upper screen 32 lines × 8 words × 2 bytes] + [lower screen 32 lines × 8 words × 2 bytes]
    int base = y_byte * 32 * 16;            // Screen partition base address (upper=0, lower=32*16=512)
    int word_offset = y_bit * 16 + x_byte * 2; // Word offset within line
    int byte_index = base + word_offset;

    // 3. Determine to operate on high byte or low byte based on x_bit
    if (x_bit < 8) {
        // High byte (first 8 bits)
        if (value == 1) {
            the_lcd_fixed_frame_buffer[byte_index] |= (1 << (7 - x_bit));
        } else {
            the_lcd_fixed_frame_buffer[byte_index] &= ~(1 << (7 - x_bit));
        }
    } else {
        // Low byte (last 8 bits)
        if (value == 1) {
            the_lcd_fixed_frame_buffer[byte_index + 1] |= (1 << (15 - x_bit));
        } else {
            the_lcd_fixed_frame_buffer[byte_index + 1] &= ~(1 << (15 - x_bit));
        }
    }
}

void update_graphic_screen() {
    // Super slow: 2 seconds
    unsigned char *temp = the_lcd_fixed_frame_buffer;

    write_command(0x34);                 // Extended instruction set
    write_command(0x36);                 // Graphic display on

    // Upper screen (y=0~31)
    for (unsigned char y_bit = 0; y_bit < 32; y_bit++) {
        write_command(0x80 | y_bit);     // Vertical address
        write_command(0x80);             // Horizontal start address (upper screen)
        for (unsigned char x_byte = 0; x_byte < 8; x_byte++) {
            write_data(*temp++);         // High byte
            write_data(*temp++);         // Low byte
        }
    }

    // Lower screen (y=32~63)
    for (unsigned char y_bit = 0; y_bit < 32; y_bit++) {
        write_command(0x80 | y_bit);     // Vertical address
        write_command(0x88);             // Horizontal start address (lower screen)
        for (unsigned char x_byte = 0; x_byte < 8; x_byte++) {
            write_data(*temp++);         // High byte
            write_data(*temp++);         // Low byte
        }
    }

    write_command(0x30);                 // Switch back to basic instruction set
}

void draw_pixel_directly(int y, int x, int value) {
    // slow: 33ms for one point but 1 second for a char(16*8)
    if (x < 0 || x >= 128 || y < 0 || y >= 64) {
        return;
    }

    unsigned char x_byte = x / 16;
    unsigned char x_bit = x % 16;
    unsigned char y_screen = y / 32;
    unsigned char y_line = y % 32;

    int base = y_screen * 32 * 16;
    int word_offset = y_line * 16 + x_byte * 2;
    int byte_index = base + word_offset;
    unsigned char target_byte_high = the_lcd_fixed_frame_buffer[byte_index];
    unsigned char target_byte_low = the_lcd_fixed_frame_buffer[byte_index + 1];

    if (x_bit < 8) {
        if (value == 1) {
            target_byte_high |= (1 << (7 - x_bit));
        } else {
            target_byte_high &= ~(1 << (7 - x_bit));
        }
    } else {
        if (value == 1) {
            target_byte_low |= (1 << (15 - x_bit));
        } else {
            target_byte_low &= ~(1 << (15 - x_bit));
        }
    }
    the_lcd_fixed_frame_buffer[byte_index] = target_byte_high;
    the_lcd_fixed_frame_buffer[byte_index + 1] = target_byte_low;

    write_command(0x34);
    write_command(0x36);
    
    write_command(0x80 | y_line);
    write_command(0x80 + x_byte + (8 * y_screen));
    
    if (x_bit < 8) {
        write_data(target_byte_high);
        write_data(target_byte_low);
    } else {
        write_data(target_byte_high);
        write_data(target_byte_low);
    }
    
    write_command(0x30);
}

void set_LCD_pin_to_low() {
    digitalWrite(9, LOW);
    digitalWrite(8, LOW);
    digitalWrite(7, LOW);
}

void initialize_LCD()
{
    pinMode(9, OUTPUT);
    pinMode(8, OUTPUT);
    pinMode(7, OUTPUT);

    set_LCD_pin_to_low();

    delay(1000);

    write_command(0x30);
    delay(20);
    write_command(0x0c);
    delay(20);
    write_command(0x01);

    delay(200);
}

void setup() {
    initialize_LCD();

    clear_the_screen();
    clear_graphic_screen();

    print_string(0, 0, "Hi!");

    // show a small cube
    for (int y=28; y < 36; y++) {
        for (int x=60; x < 68; x++) {
            draw_pixel(y, x, 1);
        }
    }
    update_graphic_screen();

    draw_pixel_directly(22, 98, 1);
}

void loop() {
}
```
