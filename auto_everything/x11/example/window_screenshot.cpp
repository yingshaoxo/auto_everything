//https://gist.github.com/richard-to/10017943
//https://github.com/richard-to/wolf3d-ai/blob/master/src/core/x11_controller.cpp
//
//https://linuxize.com/post/how-to-install-opencv-on-ubuntu-18-04/
//sudo gcc window_screenshot.cpp -lstdc++ `pkg-config --cflags --libs opencv4` -lX11 -lXmu -o example && ./example
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/Xatom.h>

using namespace cv;
using namespace std;

#define ACTIVE_WINDOWS "_NET_CLIENT_LIST"

#define WINDOW_TITLE "Screenshot"
#define WINDOW_DOXBOX "x11"


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

int main(int argc, char *argv[])
{
    Display *display = XOpenDisplay(NULL);
    Window rootWindow = RootWindow(display, DefaultScreen(display));    
    Window DOSBoxWindow;

    // working
    get_all_windows(display, DOSBoxWindow);
    XWindowAttributes DOSBoxWindowAttributes;
    XGetWindowAttributes(display, DOSBoxWindow, &DOSBoxWindowAttributes);
  
    int height = DOSBoxWindowAttributes.height;
    int width = DOSBoxWindowAttributes.width;

    namedWindow(WINDOW_TITLE, WINDOW_AUTOSIZE);    
    
    Mat frame = Mat::zeros(height, width, CV_8UC3);
    Vec3b frameRGB;

    XColor colors;
    XImage *image;
    
    unsigned long red_mask;
    unsigned long green_mask;
    unsigned long blue_mask;
    
    while (true) {
        image = XGetImage(
            display, DOSBoxWindow, 0, 0, width, height, AllPlanes, ZPixmap);

        red_mask = image->red_mask;
        green_mask = image->green_mask;
        blue_mask = image->blue_mask;

        for (int i = 0; i < height; ++i) {
            for (int j = 0; j < width; ++j) {
                colors.pixel = XGetPixel(image, j, i);
               
                // TODO(richard-to): Figure out why red and blue are swapped
                frameRGB = frame.at<Vec3b>(i, j);            
                frameRGB.val[0] = colors.pixel & blue_mask;
                frameRGB.val[1] = (colors.pixel & green_mask) >> 8;
                frameRGB.val[2] = (colors.pixel & red_mask) >> 16;       
                frame.at<Vec3b>(i, j) = frameRGB;
            }
        }
        
        XFree(image);

        imshow(WINDOW_TITLE, frame);
        
        if (waitKey(10) >= 0) {
            break;
        }
    }
}
