import ctypes

# Load the X11 library
x11 = ctypes.CDLL("libX11.so.6")

# Create a display
display = x11.XOpenDisplay(None)

# Create a window
width = 800
height = 600
window = x11.XCreateSimpleWindow(display, x11.XDefaultRootWindow(display), 0, 0, width, height, 0, 0, 0)

# Select events to listen for
#XSelectInput(main_display, main_window, KeyPressMask | KeyReleaseMask | PointerMotionMask | ButtonPressMask | ButtonReleaseMask);
x11.XSelectInput(display, window, ctypes.c_uint(79))

# Map the window
x11.XMapWindow(display, window)

x11.XFlush(display)

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

def draw_image(a_image):
    a_image = a_image.copy()
    a_image.resize(height, width)

    gc = x11.XCreateGC(display, window, 0, 0)
    for y in range(height):
        for x in range(width):
            r,g,b,a = a_image.raw_data[y][x]
            b,g,r,a = r,g,b,a
            if a != 255:
                continue
            pixel_color = (b << 16) + (g << 8) + r
            x11.XSetForeground(display, gc, pixel_color)
            x11.XDrawPoint(display, window, gc, x, y)
    x11.XFreeGC(display, gc)
    x11.XFlush(display)

def test():
    from auto_everything.image import Image
    image = Image()
    source_image_path = "/home/yingshaoxo/Downloads/water.png"
    a_image = image.read_image_from_file(source_image_path)
    draw_image(a_image)

event = XEvent()
while True:
    x11.XNextEvent(display, ctypes.pointer(event))
    if event.type == KeyPress:
        # x11 has bug, you should ignore key press event
        #key_event = XKeyEvent.from_address(cytpes.addressof(event))
        #key_evnet = ctypes.cast(ctypes.byref(event), ctypes.POINTER(XKeyEvent))
        pass
    elif event.type == KeyRelease:
        print("press", event.keycode)
        if event.keycode == 9:
            exit()
        if event.keycode == 46:
            test()
    elif event.type == MotionNotify:
        print("move", event.y, event.x)
        draw_pixel(event.x, event.y, 255,0,255)
    elif event.type == ButtonPress:
        if event.keycode == 1:
            print("left click", event.y, event.x)
        elif event.keycode == 3:
            print("right click", event.y, event.x)
