import sys
arguments_length = len(sys.argv)
if arguments_length != 2:
    print("You should run this script with the target url service address: python3 a_window.py 'http://localhost:7777' '600x800'")
    target_url = "http://localhost:7777"
else:
    target_url = sys.argv[1]
if not target_url.endswith("/"):
    target_url = target_url + "/"
if arguments_length >= 3:
    size_string = sys.argv[2]
    if "x" not in size_string:
        height = 600
        width = 800
    else:
        height, width = size_string.split("x")
        height, width = int(height), int(width)
else:
    height = 600
    width = 800

from auto_everything.http_ import Yingshaoxo_Http_Client
yingshaoxo_http_client = Yingshaoxo_Http_Client()

from auto_everything.image import Image
a_image = Image()

from multiprocessing import Queue, Process
from threading import Thread
from time import sleep, time
input_data_queue = Queue(1)
stop_signal_queue = Queue(1)

import ctypes

# Load the X11 library
x11 = ctypes.CDLL("libX11.so.6")

x11.XInitThreads()

# Create a display
display = x11.XOpenDisplay(None)

# Get screen
screen = x11.XDefaultScreen(display)

# Get root window
#root_window = x11.XDefaultRootWindow(display)
root_window = x11.XRootWindow(display, screen)

# Create a window
window = x11.XCreateSimpleWindow(display, root_window, 0, 0, width, height, 0, 0, 0)

# Select events to listen for
#XSelectInput(main_display, main_window, KeyPressMask | KeyReleaseMask | PointerMotionMask | ButtonPressMask | ButtonReleaseMask);
x11.XSelectInput(display, window, ctypes.c_uint(79))

# Map the window
x11.XMapWindow(display, window)

x11.XFlush(display)

class XWindowAttributes(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int),
                ("width", ctypes.c_int),
                ("height", ctypes.c_int),
                ("border_width", ctypes.c_int),
                ("depth", ctypes.c_int),
                ("visual", ctypes.c_void_p),
                ("root", ctypes.c_ulong),
                ("class", ctypes.c_int),
                ("bit_gravity", ctypes.c_int),
                ("win_gravity", ctypes.c_int),
                ("backing_store", ctypes.c_int),
                ("backing_planes", ctypes.c_ulong),
                ("backing_pixel", ctypes.c_ulong),
                ("save_under", ctypes.c_int),
                ("colormap", ctypes.c_ulong),
                ("map_installed", ctypes.c_int),
                ("map_state", ctypes.c_int),
                ("all_event_masks", ctypes.c_long),
                ("your_event_mask", ctypes.c_long),
                ("do_not_propagate_mask", ctypes.c_long)]

def get_window_height_and_width():
  attributes = XWindowAttributes()
  x11.XGetWindowAttributes(display, window, ctypes.byref(attributes))
  return int(attributes.height), int(attributes.width)

class XEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_ulong),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
        ("root", ctypes.c_ulong),
        ("subwindow", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("x_root", ctypes.c_int),
        ("y_root", ctypes.c_int),
        ("state", ctypes.c_uint),
        ("keycode", ctypes.c_uint),
        ("same_screen", ctypes.c_int),
    ]

class XKeyPressedEvent(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_int),
        ("serial", ctypes.c_long),
        ("send_event", ctypes.c_int),
        ("display", ctypes.c_void_p),
        ("window", ctypes.c_ulong),
        ("root", ctypes.c_ulong),
        ("subwindow", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("x", ctypes.c_int),
        ("y", ctypes.c_int),
        ("x_root", ctypes.c_int),
        ("y_root", ctypes.c_int),
        ("state", ctypes.c_int),
        ("keycode", ctypes.c_int),
        ("same_screen", ctypes.c_int),
    ]

KeyPress = 2
KeyRelease = 3
MotionNotify = 6
ButtonPress = 4

def draw_pixel(x, y, red, green, blue):
    gc = x11.XCreateGC(display, window, 0, 0)
    pixel_color = (blue << 16) + (green << 8) + red
    x11.XSetForeground(display, gc, pixel_color)
    x11.XDrawPoint(display, window, gc, x, y)
    x11.XFreeGC(display, gc)

#def draw_image(a_image):
#    a_image = a_image.copy()
#    a_image.resize(height, width)
#
#    gc = x11.XCreateGC(display, window, 0, 0)
#    for y in range(height):
#        for x in range(width):
#            r,g,b,a = a_image.raw_data[y][x]
#            b,g,r,a = r,g,b,a
#            if a != 255:
#                continue
#            pixel_color = (b << 16) + (g << 8) + r
#            x11.XSetForeground(display, gc, pixel_color)
#            x11.XDrawPoint(display, window, gc, x, y)
#    #x11.XFreeGC(display, gc)
#    #x11.XFlush(display)

def show_image_data(data, image_height, image_width):
    if data == None:
        return
    gc = x11.XCreateGC(display, window, 0, 0)
    visual = x11.XDefaultVisual(display, screen)
    image = x11.XCreateImage(
        display,
        visual,  # Use the same visual as your window
        24,  # Match the image depth with the window depth
        2, #x11.ZPixmap,
        0,
        ctypes.c_char_p(data),
        image_width,
        image_height,
        32,  # Assuming 32-bit depth
        0
    )
    x11.XSetForeground(display, gc, ((255 << 16) + (255 << 8) + 255))
    x11.XPutImage(display, window, gc, image, 0, 0, 0, 0, width, height)
    #x11.XFlush(display)
    #x11.XFreeImage(display, image)
    #x11.XFreeGC(display, gc)

def convert_image_to_image_data(a_image):
    try:
        #a_image = a_image.copy()
        #a_image = a_image.resize(height, width)

        data_list = []
        for row in a_image.raw_data:
            for pixel in row:
                r,g,b,a = pixel
                b,g,r,a = r,g,b,a
                data_list.append(r)
                data_list.append(g)
                data_list.append(b)
                data_list.append(a)
        data = bytes(data_list)
        return data
    except Exception as e:
        print(e)
        return None

def get_image_data():
    global a_image
    source_image_path = "/home/yingshaoxo/Downloads/water.png"
    a_image = a_image.read_image_from_file(source_image_path)
    return convert_image_to_image_data(a_image)

def get_image_data_from_http_service():
    global a_image

def get_input_data_loop(stop_signal_queue):
    window_height, window_width = height, width
    event = XEvent()
    running = True
    while stop_signal_queue.empty():
        ascii_code = None
        button_code = None
        point_y, point_x = None, None

        x11.XNextEvent(display, ctypes.pointer(event)) # this function will block until window got some input
        if event.type == KeyPress:
            # x11 has bug, you should ignore key press event
            #key_event = XKeyEvent.from_address(cytpes.addressof(event))
            #key_evnet = ctypes.cast(ctypes.byref(event), ctypes.POINTER(XKeyEvent))
            pass
        elif event.type == KeyRelease:
            print("press", event.keycode, "upper" if event.state==17 else "lower")
            if event.keycode == 9:
                # esc
                stop_signal_queue.put(True)
                return
            key_event = ctypes.cast(ctypes.byref(event), ctypes.POINTER(XKeyPressedEvent))
            buffer = ctypes.create_string_buffer(1)
            length = x11.XLookupString(key_event, buffer, 1, None, None)
            if length > 0 and len(buffer) > 0:
                ascii_code = buffer[0].decode("ascii")
                print("character:", ascii_code, "\n")

        elif event.type == MotionNotify:
            point_y, point_x = str(event.y), str(event.x)
            print("move", event.y, event.x)
            #draw_pixel(event.x, event.y, 255,0,255)
        elif event.type == ButtonPress:
            button_code = str(event.keycode)
            point_y, point_x = str(event.y), str(event.x)
            if event.keycode == 1:
                print("left click", event.y, event.x)
            elif event.keycode == 3:
                print("right click", event.y, event.x)

        # send keyboard input out
        if input_data_queue.empty():
            a_input_data = """
ascii_code={}
button_code={}
point_y={}
point_x={}
height={}
width={}
            """.format(ascii_code, button_code, point_y, point_x, window_height, window_width).strip()
            input_data_queue.put(a_input_data)

def send_input_data_to_http_service(input_data_queue):
    while True:
        try:
            a_string = input_data_queue.get()
            yingshaoxo_http_client.post(target_url+"handle_input", a_string)
        except Exception as e:
            print(e)

get_input_process = Thread(target=get_input_data_loop, args=(stop_signal_queue,))
get_input_process.start()

send_input_process = Process(target=send_input_data_to_http_service, args=(input_data_queue,))
send_input_process.start()

#global_image_data = bytes([0 for one in range(height*width*4)]) # not work, for unknown reason
global_image_data = get_image_data()
while stop_signal_queue.empty():
    try:
        start_time = time()
        response = yingshaoxo_http_client.post(target_url+"download_picture", "")
        if "," in response:
            # we got picture
            a_image = a_image.read_image_from_string(response)
            image_height, image_width = a_image.get_shape()
            global_image_data = convert_image_to_image_data(a_image)
            show_image_data(global_image_data, image_height, image_width)
            end_time = time()
            time_use_in_milliseconds = round((end_time - start_time)*1000)
            #print("time use in milliseconds:", time_use_in_milliseconds)
            print("fps:", round(1000/time_use_in_milliseconds))
            if time_use_in_milliseconds < 40:
                sleep((40-time_use_in_milliseconds)/1000)
    except Exception as e:
        print(e)

try:
    send_input_process.kill()
except Exception as e:
    print(e)

exit()
