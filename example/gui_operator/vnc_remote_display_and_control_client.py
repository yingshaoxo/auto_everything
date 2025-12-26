#!/usr/bin/env python3
# qemu-system-i386 -cdrom xp.iso -enable-kvm -m 1024 -smp 2 -vga std -vnc :1 -display none
"""
author: gemini and yingshaoxo

Full VNC Client with Tkinter UI for Graphics Rendering and Stateful Input.

Key Features:
1. Persistent connection.
2. Stateful Mouse Input (Absolute Coordinates).
3. Keyboard Input (X Keysyms).
4. Asynchronous Framebuffer Update Request/Handling (Raw Encoding).
5. Pixel rendering to Tkinter Canvas.
"""

import socket
import struct
import time
import io
import sys

import zlib
import tkinter as tk
from PIL import Image, ImageTk

keyboard_key_list = [
    ('BackSpace', 65288),
    ('Tab', 65289),
    ('Return', 65293),
    ('Pause', 65299),
    ('Scroll_Lock', 65300),
    ('Escape', 65307),
    ('Delete', 65535),
    ('Insert', 65379),
    ('Menu', 65383),
    ('Home', 65360),
    ('Left', 65361),
    ('Up', 65362),
    ('Right', 65363),
    ('Down', 65364),
    ('Page_Up', 65365),
    ('Page_Down', 65366),
    ('End', 65367),
    ('F1', 65470),
    ('F2', 65471),
    ('F3', 65472),
    ('F4', 65473),
    ('F5', 65474),
    ('F6', 65475),
    ('F7', 65476),
    ('F8', 65477),
    ('F9', 65478),
    ('F10', 65479),
    ('F11', 65480),
    ('F12', 65481),
    ('Shift_L', 65505),
    ('Shift_R', 65506),
    ('Control_L', 65507),
    ('Control_R', 65508),
    ('Caps_Lock', 65509),
    ('Alt_L', 65513),
    ('Alt_R', 65514),
    ('Num_Lock', 65407),
    ('KP_Enter', 65421),
    ('KP_Multiply', 65450),
    ('KP_Add', 65451),
    ('KP_Subtract', 65453),
    ('KP_Decimal', 65454),
    ('KP_Divide', 65455),
    ('KP_0', 65456),
    ('KP_1', 65457),
    ('KP_2', 65458),
    ('KP_3', 65459),
    ('KP_4', 65460),
    ('KP_5', 65461),
    ('KP_6', 65462),
    ('KP_7', 65463),
    ('KP_8', 65464),
    ('KP_9', 65465),
    ('KP_Equal', 65469),
    ('A', 65),
    ('B', 66),
    ('C', 67),
    ('D', 68),
    ('E', 69),
    ('F', 70),
    ('G', 71),
    ('H', 72),
    ('I', 73),
    ('J', 74),
    ('K', 75),
    ('L', 76),
    ('M', 77),
    ('N', 78),
    ('O', 79),
    ('P', 80),
    ('Q', 81),
    ('R', 82),
    ('S', 83),
    ('T', 84),
    ('U', 85),
    ('V', 86),
    ('W', 87),
    ('X', 88),
    ('Y', 89),
    ('Z', 90),
    ('a', 97),
    ('b', 98),
    ('c', 99),
    ('d', 100),
    ('e', 101),
    ('f', 102),
    ('g', 103),
    ('h', 104),
    ('i', 105),
    ('j', 106),
    ('k', 107),
    ('l', 108),
    ('m', 109),
    ('n', 110),
    ('o', 111),
    ('p', 112),
    ('q', 113),
    ('r', 114),
    ('s', 115),
    ('t', 116),
    ('u', 117),
    ('v', 118),
    ('w', 119),
    ('x', 120),
    ('y', 121),
    ('z', 122),
    ('0', 48),
    ('1', 49),
    ('2', 50),
    ('3', 51),
    ('4', 52),
    ('5', 53),
    ('6', 54),
    ('7', 55),
    ('8', 56),
    ('9', 57),
    ('space', 32),
    ('exclam', 33),
    ('quotedbl', 34),
    ('numbersign', 35),
    ('dollar', 36),
    ('percent', 37),
    ('ampersand', 38),
    ('apostrophe', 39),
    ('parenleft', 40),
    ('parenright', 41),
    ('asterisk', 42),
    ('plus', 43),
    ('comma', 44),
    ('minus', 45),
    ('period', 46),
    ('slash', 47),
    ('colon', 58),
    ('semicolon', 59),
    ('less', 60),
    ('equal', 61),
    ('greater', 62),
    ('question', 63),
    ('at', 64),
    ('bracketleft', 91),
    ('backslash', 92),
    ('bracketright', 93),
    ('asciicircum', 94),
    ('underscore', 95),
    ('grave', 96),
    ('braceleft', 123),
    ('bar', 124),
    ('braceright', 125),
    ('asciitilde', 126),
    ('PrintScreen', 65377),
    ('Sys_Req', 65378),
    ('Super_L', 65515),
    ('Super_R', 65516),
]
keyboard_key_code_dict = {}
for one in keyboard_key_list:
    keyboard_key_code_dict[one[0]] = one[1]

# --- Configuration & Globals ---
HOST = '127.0.0.1'
PORT = 5901
TIMEOUT = 5.0
UPDATE_INTERVAL_MS = 100  # How often to check for VNC server updates

# Screen dimensions (will be updated after handshake)
the_screen_height = 768
the_screen_width = 1024

# --- RFB Message Types (Constants) ---
MSG_CLIENT_SET_PIXEL_FORMAT = 0
MSG_CLIENT_SET_ENCODINGS = 2
MSG_CLIENT_FRAMEBUFFER_UPDATE_REQUEST = 3
MSG_CLIENT_KEY_EVENT = 4
MSG_CLIENT_POINTER_EVENT = 5

MSG_SERVER_FRAMEBUFFER_UPDATE = 0
MSG_SERVER_BELL = 2
MSG_SERVER_SERVER_CUT_TEXT = 3

# RFB Encodings (Supported)
ENC_RAW = 0
ENC_ZLIB = 6
# We only support raw encoding for simplicity and reliability.

class VNCScreenshotClient:
    def __init__(self, host, port, canvas):
        self.host = host
        self.port = port
        self.canvas = canvas
        self.socket = None
        self.connected = False
        self.img = None # Stores the current ImageTk.PhotoImage

        # --- STATEFUL INPUT TRACKING ---
        self.current_mouse_x = 0
        self.current_mouse_y = 0
        self.current_button_mask = 0

        self.zlib_decompressor = zlib.decompressobj()

    # --- Communication Utilities ---

    def _read_exact(self, length):
        """Reads exactly 'length' bytes from the socket."""
        data = b''
        while len(data) < length:
            try:
                chunk = self.socket.recv(length - len(data))
            except socket.error as e:
                # Handle non-blocking errors (EAGAIN/EWOULDBLOCK) during update loop
                if e.errno in (11, 35):  # Common non-blocking error codes
                    return b''
                raise IOError(f"Socket read failed: {e}")
            if not chunk:
                raise EOFError("Connection closed unexpectedly.")
            data += chunk
        return data

    def _read_uint(self, byte_count):
        """Read unsigned integer of 'byte_count' bytes"""
        data = self._read_exact(byte_count)
        return int.from_bytes(data, byteorder='big')

    def _send_message(self, data):
        """Sends a complete message over the socket."""
        if isinstance(data, str):
            data = data.encode('latin-1')
        self.socket.sendall(data)

    # --- Connection and Protocol Setup ---

    def _vnc_handshake(self):
        """Performs VNC protocol handshake."""
        global the_screen_height, the_screen_width

        # 1. Read Version, Send 3.8
        self._read_exact(12)
        self._send_message(b"RFB 003.008\n")

        # 2. Security Negotiation (Select 1: None)
        self._read_exact(1) # num security types
        self._read_exact(1) # security type 1
        self._send_message(struct.pack('>B', 1))

        security_result = struct.unpack('>L', self._read_exact(4))[0]
        if security_result != 0: raise ConnectionError("Security selection failed.")

        # 3. ClientInit (Shared=1)
        self._send_message(struct.pack('>B', 1))

        # 4. ServerInit (Get screen info)
        header_raw = self._read_exact(20)
        width, height, _ = struct.unpack('>HH16s', header_raw)
        if width > the_screen_width:
            the_screen_width = width
        if height > the_screen_height:
            the_screen_height = height

        name_length = struct.unpack('>L', self._read_exact(4))[0]
        self._read_exact(name_length)
        print(f"FrameBuffer size: {width}x{height}")

        # 5. Set Client Pixel Format (32bpp RGBA, required for simple raw decoding)
        pixel_format_data = struct.pack('>BxxxBBBBHHHBBBxxx',
            MSG_CLIENT_SET_PIXEL_FORMAT, 32, 32, 1, 1,
            255, 255, 255,
            16, 8, 0  # rshift=16, gshift=8, bshift=0 (RGBA format)
        )
        self._send_message(pixel_format_data)

        # 6. Set Encoding (Only support Raw=0 for reliable pixel transfer)
        #set_encoding_data = struct.pack('>BxHl', MSG_CLIENT_SET_ENCODINGS, 1, ENC_RAW)
        set_encoding_data = struct.pack('>BxHl', MSG_CLIENT_SET_ENCODINGS, 1, ENC_ZLIB)
        self._send_message(set_encoding_data)

        # Set socket to non-blocking for continuous UI loop
        self.socket.setblocking(False)


    def connect(self):
        """Connect to VNC server and perform handshake"""
        if self.connected: return

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(TIMEOUT)
            self.socket.connect((self.host, self.port))

            # Protocol must be done blocking
            self.socket.settimeout(TIMEOUT)
            self._vnc_handshake()

            self.connected = True
            print("✓ VNC connection successful and non-blocking mode set.")

        except Exception as e:
            print(f"✗ VNC connection failed: {e}")
            self.disconnect()

    def disconnect(self):
        """Cleanly close the socket connection."""
        if self.socket:
            self.socket.close()
            self.socket = None
        self.connected = False
        print("✓ VNC connection closed.")

    # --- Graphics Rendering (The New Core Logic) ---

    def request_update(self, incremental=True):
        """Sends a Framebuffer Update Request to the server."""
        if not self.connected: return

        # Incremental (1): Request only regions that have changed
        # Non-incremental (0): Request the entire screen (useful for the first update)
        incremental_flag = 1 if incremental else 0

        # Format: Type (1), Incremental (1), X (2), Y (2), W (2), H (2) = 10 bytes
        request = struct.pack('>BBHHHH',
            MSG_CLIENT_FRAMEBUFFER_UPDATE_REQUEST,
            incremental_flag,
            0, 0,
            the_screen_width, the_screen_height
        )
        self._send_message(request)

    def _process_raw_data(self, x, y, width, height):
        """Process raw pixel data and convert to RGBA list format"""
        #print(f"Processing raw pixel data for {width}x{height} area")

        # Calculate pixel data size
        pixel_size = width * height * 4  # Assuming 32-bit RGBA

        # Read pixel data
        pixel_data = self._read_exact(pixel_size)
        if not pixel_data: return # In non-blocking mode, might read 0 bytes

        # Convert to nested RGBA list format
        image_data = []
        for row in range(height):
            row_data = []
            for col in range(width):
                pixel_offset = (row * width + col) * 4
                b = pixel_data[pixel_offset]
                g = pixel_data[pixel_offset + 1]
                r = pixel_data[pixel_offset + 2]
                a = pixel_data[pixel_offset + 3]
                row_data.append([r, g, b, 255])
            image_data.append(row_data)

        #print(f"✓ Screenshot captured successfully")
        #print(f"Image dimensions: {len(image_data)} rows x {len(image_data[0])} columns")

        return image_data

    def _process_zlib_data(self, x, y, width, height):
        """Process zlib compressed pixel data"""
        #print(f"Processing zlib compressed data for {width}x{height} area")

        # Read compressed data length
        data_length = self._read_uint(4)
        compressed_data = self._read_exact(data_length)

        try:
            # Decompress data
            decompressed = self.zlib_decompressor.decompress(compressed_data)
            #print(f"✓ Zlib data decompressed: {len(compressed_data)} -> {len(decompressed)} bytes")

            # Convert to nested RGBA list format
            image_data = []
            for row in range(height):
                row_data = []
                for col in range(width):
                    pixel_offset = (row * width + col) * 4
                    b = decompressed[pixel_offset]
                    g = decompressed[pixel_offset + 1]
                    r = decompressed[pixel_offset + 2]
                    a = decompressed[pixel_offset + 3]
                    row_data.append([r, g, b, 255])
                image_data.append(row_data)
            return image_data
        except zlib.error as e:
            print(f"✗ Zlib decompression failed: {e}")
            raise

    def _handle_image(self, image_data, x, y, w, h):
        """
        Processes Raw encoding pixel data (32bpp RGBA).
        Assumes pixel format is 32-bit (4 bytes per pixel).
        """
        #pixel_data = self._read_exact(w * h * 4)
        #if not pixel_data: return # In non-blocking mode, might read 0 bytes
        #img = Image.frombytes('RGBA', (w, h), pixel_data, 'raw', 'RGBA')
        if not image_data:
            return

        # Create a PIL Image object from the raw RGBA data
        #print(image_data[0][0])

        # If this is the first update, initialize the image on the canvas
        if self.img is None:
            # Initialize the canvas with the full blank image
            img = Image.new('RGBA', (the_screen_width, the_screen_height))
            img.putdata([tuple(pixel) for row in image_data for pixel in row])

            self.img = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=self.img, anchor='nw')
            self.canvas.current_pil_image = img
        else:
            img = Image.new('RGBA', (w, h))
            img.putdata([tuple(pixel) for row in image_data for pixel in row])

            if not hasattr(self.canvas, 'current_pil_image'):
                 # First update, store the image
                 self.canvas.current_pil_image = img
            else:
                 # Subsequent update, paste the new rectangle onto the existing full image
                 self.canvas.current_pil_image.paste(img, (x, y))

            # Update the Tkinter PhotoImage from the patched PIL Image
            self.img = ImageTk.PhotoImage(self.canvas.current_pil_image)
            self.canvas.itemconfig(self.canvas.find_all()[0], image=self.img)
            self.canvas.update_idletasks()

    def handle_server_message(self):
        """Checks socket for incoming messages and processes one if available."""
        if not self.connected or not self.socket: return

        try:
            # Read the first byte (message type) in non-blocking mode
            header = self._read_exact(1)
            if not header: return # No data available

            message_type = struct.unpack('>B', header)[0]

            if message_type == MSG_SERVER_FRAMEBUFFER_UPDATE:
                header_update = self._read_exact(3)
                if not header_update: return
                _, num_rects = struct.unpack('>BH', header_update)

                for _ in range(num_rects):
                    rect_header = self._read_exact(12)
                    if not rect_header: continue
                    x, y, w, h, encoding = struct.unpack('>HHHHl', rect_header)

                    if encoding == ENC_RAW:
                        #print(x, y, w, h)
                        image_data = self._process_raw_data(x, y, w, h)
                        self._handle_image(image_data, x, y, w, h)
                    elif encoding == ENC_ZLIB:
                        image_data = self._process_zlib_data(x, y, w, h)
                        self._handle_image(image_data, x, y, w, h)
                    else:
                        print(f"Warning: Received unsupported VNC encoding type: {encoding}")
                        # Skip remaining data for unsupported encoding (dangerous, but necessary for demo)
                        # We should ideally know the size and read it, but Raw is simpler.
                        pass

                # Request the next update immediately after processing
                self.request_update(incremental=True)

            elif message_type == MSG_SERVER_BELL:
                print("Server BELL received.")

            elif message_type == MSG_SERVER_SERVER_CUT_TEXT:
                # Handle Clipboard/Cut text
                length = struct.unpack('>L', self._read_exact(4))[0]
                self._read_exact(length) # Discard cut text for now

            else:
                print(f"Warning: Received unknown message type: {message_type}")
                # Dangerous: We must skip the rest of the message, but without size info, we can't.
                # In a real client, you'd need the protocol definition for all types.
                pass

        except (IOError, EOFError, struct.error) as e:
            print(f"Error handling server message: {e}")
            self.disconnect()

    # --- Input Event Sending (Retained and Enhanced) ---

    def calculate_button_mask(self, left=False, middle=False, right=False):
        """Calculates the VNC button mask."""
        mask = 0
        if left: mask |= 1
        if middle: mask |= 2
        if right: mask |= 4
        return mask

    def send_mouse_event(self, button_mask, x, y):
        """
        Sends a PointerEvent (Mouse move/click) with Absolute Coordinates.
        Uses stateful tracking.
        """
        if not self.connected: return

        x = max(0, min(x, the_screen_width - 1))
        y = max(0, min(y, the_screen_height - 1))

        # Check for state change
        if x == self.current_mouse_x and y == self.current_mouse_y and button_mask == self.current_button_mask:
            return

        self.current_mouse_x = x
        self.current_mouse_y = y
        self.current_button_mask = button_mask

        message = struct.pack('>BBHH',
            MSG_CLIENT_POINTER_EVENT,
            button_mask,
            x,
            y
        )
        self._send_message(message)

    def send_key_event(self, down, key):
        """
        Send keyboard event to server.
        """
        if not self.connected:
            raise ConnectionError("Not connected to VNC server")

        key_code = keyboard_key_code_dict.get(key)
        print(key, key_code)
        if key_code == None:
            return

        # Prepare key event
        message = struct.pack('>BBHl', MSG_CLIENT_KEY_EVENT, down, 0, key_code)
        self._send_message(message)

        action = "pressed" if down else "released"
        print(f"✓ Key {action}: {key} (code: {key_code})")

    # --- Utility Methods ---
    def get_initial_dimensions(self):
        """Returns the dimensions discovered during the handshake."""
        return the_screen_width, the_screen_height

class Point_Drawer(tk.Canvas):
    """Tkinter canvas to visualize the simulated framebuffer and handle events."""
    def __init__(self, master, height, width):
        super().__init__(master, height=height, width=width, bg='gray')
        self.pack()
        self.height = height
        self.width = width

    def center_window(self):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width // 2) - (self.width // 2)
        y = (screen_height // 2) - (self.height // 2)
        self.master.geometry(f'{self.width}x{self.height}+{x}+{y}')
        self.master.title(f"VNC Client {self.width}x{self.height}")

    def draw_cross(self, x, y, size=10, color="red"):
        """Draws a crosshair at the given coordinates (for input feedback)."""
        self.delete("cross")
        self.create_line(x - size, y, x + size, y, fill=color, tags="cross")
        self.create_line(x, y - size, x, y + size, fill=color, tags="cross")

def update_loop(client, root_window):
    """
    Main loop to poll for server updates and request new frames.
    Runs asynchronously using Tkinter's 'after'.
    """
    if client.connected:
        client.handle_server_message()

    # Schedule the next check
    root_window.after(UPDATE_INTERVAL_MS, update_loop, client, root_window)


if __name__ == '__main__':
    root_window = tk.Tk()

    # Step 1: Initialize client and attempt connection to get dimensions
    # We pass a temporary canvas size, which will be updated after handshake
    temp_canvas = Point_Drawer(root_window, the_screen_height, the_screen_width)
    client = VNCScreenshotClient(host=HOST, port=PORT, canvas=temp_canvas)

    client.connect()

    # Step 2: Use actual dimensions from VNC server handshake
    w, h = client.get_initial_dimensions()
    temp_canvas.destroy() # Destroy temp canvas

    # Create final canvas with correct dimensions
    point_drawer = Point_Drawer(root_window, h, w)
    point_drawer.center_window()
    client.canvas = point_drawer # Assign the correct canvas instance

    # --- Input Handlers ---

    def handle_mouse_move(event):
        """FIXED: Sends the actual absolute X and Y coordinates."""
        x = event.x
        y = event.y
        point_drawer.draw_cross(x, y, color="blue")
        client.send_mouse_event(client.current_button_mask, x, y) # Maintain current button state

    def handle_mouse_click(event):
        """Handles mouse button down and up for clicking."""
        x, y = event.x, event.y
        mask = client.calculate_button_mask(left=(event.num==1), right=(event.num==3))

        # Visualize click
        #point_drawer.draw_cross(x, y, color="red")

        # 1. Mouse Button Down
        client.send_mouse_event(mask, x, y)

        # 2. Schedule Mouse Button Up (to avoid blocking UI thread)
        def release_button():
            client.send_mouse_event(0, x, y) # Mask 0 = release all buttons
            #point_drawer.draw_cross(x, y, color="blue") # Revert crosshair color

        root_window.after(50, release_button) # Wait 50ms then release

    def handle_key_down(event):
        key_name = event.keysym
        key_code = key_name
        if key_code:
            client.send_key_event(1, key_code) # Down

    def handle_key_up(event):
        key_name = event.keysym
        key_code = key_name
        if key_code:
            client.send_key_event(0, key_code) # Up

    # --- Bind Events ---
    point_drawer.bind('<Motion>', handle_mouse_move)
    point_drawer.bind('<ButtonPress>', handle_mouse_click)
    #point_drawer.bind('<ButtonRelease>', handle_mouse_click_up)
    # Bind keyboard events to the root window to capture them easily
    root_window.bind('<KeyPress>', handle_key_down)
    root_window.bind('<KeyRelease>', handle_key_up)

    # Step 3: Start the Update Loop and Initial Request
    if client.connected:
        client.request_update(incremental=False) # Request full frame initially
        update_loop(client, root_window)

    try:
        root_window.mainloop()
    except tk.TclError:
        # Happens if the window is closed forcefully
        pass
    finally:
        client.disconnect()
        sys.exit(0)
