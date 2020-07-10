//https://gist.github.com/richard-to/10017943
//https://github.com/richard-to/wolf3d-ai/blob/master/src/core/x11_controller.cpp
//
//
//https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
//sudo gcc window_send_event.cpp -lstdc++ -lX11 -lXmu -o example && ./example
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <unistd.h>
#include <vector>

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xatom.h>
#include <X11/keysym.h>

using namespace std;

#define ACTIVE_WINDOWS "_NET_CLIENT_LIST"

#define WINDOW_TITLE "Wolf3d Screenshot"
#define WINDOW_DOXBOX "Pixel"

string get_window_detail_name2(Display *display, Window &window) {
    string name;

    Status status;
    char *windowName;
    status = XFetchName(display, window, &windowName);
    if (status >= Success && windowName != NULL) {
        printf("\t* %s\n", windowName);
        name = windowName;
    }

    return name;
}

vector<string> get_all_windows(Display *display, Window &window) {
  vector<string> string_list;

  Atom property_name = XInternAtom(display, "_NET_CLIENT_LIST", False);
  Atom actual_type_return;
  int actual_format_return;
  unsigned long number_of_items;
  unsigned long number_of_bytes_left;
  unsigned char *data_return;

  int status = XGetWindowProperty(display, XDefaultRootWindow(display), property_name, 0, 1024, False, XA_WINDOW, &actual_type_return, &actual_format_return, &number_of_items, &number_of_bytes_left, &data_return);

  if (status == Success)
  {
    Window *list = (Window *)data_return;

    if (number_of_items)
    {
      for (unsigned long i = 0; i < number_of_items; i++)
      {
        //string name = get_window_class_name(display, list[i]);
        //string name = get_window_detail_name(display, list[i]);
        string name = get_window_detail_name2(display, list[i]);
        if (!name.empty()) {
            string_list.push_back(name);
            if (name.find(WINDOW_DOXBOX) != string::npos) {
                printf("found it\n");
                window = list[i];
            }
        }
      }
      XFree(data_return);
    }
  }
  else
  {
    printf("failed to get window property");
  }

  return string_list;
}

void millisleep(int ms)
{
    usleep(ms * 1000);
}

//http://csweb.cs.wfu.edu/~torgerse/Kokua/Irix_6.5.21_doc_cd/usr/share/Insight/library/SGI_bookshelves/SGI_Developer/books/XLib_PG/sgi_html/ch09.html#:~:text=The%20keycode%20member%20of%20XKeyEvent,key%20is%20pressed%20or%20released.
int main(int argc, char *argv[])
{
    Display *display = XOpenDisplay(NULL);
    Window rootWindow = RootWindow(display, DefaultScreen(display));    
    Window DOSBoxWindow;

    get_all_windows(display, DOSBoxWindow);
    XWindowAttributes DOSBoxWindowAttributes;
    XGetWindowAttributes(display, DOSBoxWindow, &DOSBoxWindowAttributes);

    XKeyEvent event;
    event.display = display;
    event.send_event = False;
    event.window = DOSBoxWindow;
    event.root = rootWindow;
    event.time = CurrentTime;
    event.same_screen = True;
    event.keycode = XKeysymToKeycode(display, XK_3);
    event.type = KeyPress;      
    XSendEvent(display, DOSBoxWindow, True, KeyPressMask, (XEvent *)&event);
    XFlush(display);

    millisleep(100);

    event.type = KeyRelease;      
    XSendEvent(display, DOSBoxWindow, True, KeyReleaseMask, (XEvent *)&event);
    XFlush(display);
}
