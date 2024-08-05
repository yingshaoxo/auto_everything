//sudo apt install libx11-dev
//gcc a_window.c -o window.run -lX11
//echo "We can't staticlly link x11?"
//
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <unistd.h>
#include <stdio.h>

int main()
{
    // create a window
    Display* main_display = XOpenDisplay(0);
    Window root_window = XDefaultRootWindow(main_display);

    int WindowX = 0;
    int WindowY = 0;
    int WindowWidth = 800;
    int WindowHeight = 600;
    int BorderWidth = 0;
    int WindowDepth = CopyFromParent;
    int WindowClass = CopyFromParent;
    Visual* WindowVisual = CopyFromParent;

    int AttributeValueMask = CWBackPixel | CWEventMask;
    XSetWindowAttributes WindowAttributes = {};
    WindowAttributes.background_pixel = 0xffffccaa;
    WindowAttributes.event_mask = StructureNotifyMask | KeyPressMask | KeyReleaseMask | ExposureMask;

    Window main_window = XCreateWindow(main_display, root_window, 
            WindowX, WindowY, WindowWidth, WindowHeight,
            BorderWidth, WindowDepth, WindowClass, WindowVisual,
            AttributeValueMask, &WindowAttributes);

    XMapWindow(main_display, main_window);

    // handle input callback function
    XSelectInput(main_display, main_window, KeyPressMask | KeyReleaseMask | PointerMotionMask | ButtonPressMask | ButtonReleaseMask);
    //printf("%ld", KeyPressMask | KeyReleaseMask | PointerMotionMask | ButtonPressMask | ButtonReleaseMask);
    //return 0;

    // handle pixel drawing
    GC graphic_collector = XCreateGC(main_display, main_window, 0, NULL);
    Colormap colormap = DefaultColormap(main_display, DefaultScreen(main_display));
    for (int i=0; i < 255; i++) {
        XColor color;
        color.red = 255*257; // 65535 is the max value
        color.green = i*257;
        color.blue = 0;
        color.flags = DoRed | DoGreen | DoBlue;
        XAllocColor(main_display, colormap, &color);
        //unsigned long pixel_color_variable = color.pixel;
        XSetForeground(main_display, graphic_collector, color.pixel);
        XDrawPoint(main_display, main_window, graphic_collector, i, i); // Draw a pixel at (x, y)
        XFreeColors(main_display, colormap, &color.pixel, 1, 0);
    }
    XFlush(main_display);

    XEvent general_event = {};
    int IsWindowOpen = 1;
    while(IsWindowOpen) {
        XNextEvent(main_display, &general_event);

        switch(general_event.type) {
            case KeyPress:
            {
                // There has bug with x11 system, it can't know how long you pressed a button
            } break;

            case KeyRelease:
            {
                XKeyPressedEvent *Event = (XKeyPressedEvent *)&general_event;
                if(Event->keycode == XKeysymToKeycode(main_display, XK_Escape))
                {
                    IsWindowOpen = 0;
                }
                else if(Event->keycode == XKeysymToKeycode(main_display, XK_Up))
                {
                    printf("up\n");
                }
                else if(Event->keycode == XKeysymToKeycode(main_display, XK_Down))
                {
                    printf("down\n");
                }
                else if(Event->keycode == XKeysymToKeycode(main_display, XK_Left))
                {
                    printf("left\n");
                }
                else if(Event->keycode == XKeysymToKeycode(main_display, XK_Right))
                {
                    printf("right\n");
                }
            } break;

            case MotionNotify:
            {
                int y = general_event.xmotion.y;
                int x = general_event.xmotion.x;
                printf("Mouse moved to (%d, %d)\n", y, x);
            } break;

            case ButtonPress:
            {
                if(general_event.xbutton.button == Button1) {
                    //printf("Left button clicked at (%i, %i)\n", general_event.xbutton.y_root, general_event.xbutton.x_root);
                    printf("Left button clicked at (%i, %i)\n", general_event.xbutton.y, general_event.xbutton.x);
                } else if(general_event.xbutton.button == Button3) {
                    //printf("Right button clicked at (%i, %i)\n", general_event.xbutton.y_root, general_event.xbutton.x_root);
                    printf("Right button clicked at (%i, %i)\n", general_event.xbutton.y, general_event.xbutton.x);
                }
            } break;

            default:
                break;
        }

        //sleep(1);
    }

    //XFreeColors(main_display, colormap, &pixel_color_variable, 1, 0);
    //XFreeGC(main_display, graphic_collector);
    //XCloseDisplay(main_display);
}
