// created by yingshaoxo at 2020-07-09 07:41.
//
// Feel free to use it.
// But please keep this comments here.
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11; // pip3 install pybind11

#include <cstdio>
#include <cstdlib>
#include <string>
#include <vector>
#include <chrono>
#include <thread>
#include <algorithm>
using namespace std;

/*
I read docs from :
https://www.student.cs.uwaterloo.ca/~cs349/f15/resources/X/xTutorialPart1.html
https://tronche.com/gui/x/xlib/window-information/XQueryTree.html
*/
#include <X11/Xlib.h> // `apt-get install libx11-dev`
#include <X11/Xatom.h>
#include <X11/Xmu/WinUtil.h> // `apt-get install libxmu-dev`
#include <X11/Xutil.h>

string get_window_class_name(Display *d, Window w)
{
    Status s;
    XClassHint *c_class;

    c_class = XAllocClassHint();
    s = XGetClassHint(d, w, c_class);
    if (s)
    {
        //printf("\t* name: %s\n\t* class: %s\n", c_class->res_name, c_class->res_class);
        string name = c_class->res_class;
        return name;
    }
    else
    {
        printf("ERROR: XGetClassHint\n");
        string name{};
        return name;
    }
}

string get_window_detail_name(Display *disp, Window win)
{
    Atom prop = XInternAtom(disp, "WM_NAME", False), type;
    int form;
    unsigned long remain, len;
    unsigned char *list;

    errno = 0;
    if (XGetWindowProperty(disp, win, prop, 0, 1024, False, XA_STRING,
                           &type, &form, &len, &remain, &list) != Success)
    {
        perror("winlist() -- GetWinProp");
    }

    char *name = (char *)list;
    //printf("\t* %s\n", name);
    string return_name = name;
    free(name);
    return return_name;
}

string get_window_detail_name2(Display *display, Window &window)
{
    string name;

    Status status;
    char *windowName;
    status = XFetchName(display, window, &windowName);
    if (status >= Success && windowName != NULL)
    {
        //printf("\t* %s\n", windowName);
        name = windowName;
    }

    free(windowName);
    return name;
}

vector<string> get_all_windows(Display *display, vector<Window> &window_list)
{
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
        Window *temp_window_list = (Window *)data_return;
        if (number_of_items)
        {
            for (unsigned long i = 0; i < number_of_items; i++)
            {
                //string name = get_window_class_name(display, temp_window_list[i]);
                //string name = get_window_detail_name(display, temp_window_list[i]);
                string name = get_window_detail_name2(display, temp_window_list[i]);
                if (!name.empty())
                {
                    string_list.push_back(name);
                    window_list.push_back(temp_window_list[i]);
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

bool get_a_window_by_name(Display *display, const char window_name[], Window &window)
{
    string sub_name = window_name;
    vector<Window> window_list;
    vector<string> list_of_windows = get_all_windows(display, window_list);
    for (size_t i = 0; i < list_of_windows.size(); i++)
    {
        transform(list_of_windows[i].begin(), list_of_windows[i].end(), list_of_windows[i].begin(), ::tolower);
        transform(sub_name.begin(), sub_name.end(), sub_name.begin(), ::tolower);
        if (list_of_windows[i].find(sub_name) != string::npos)
        {
            window = window_list[i];
            return true;
        }
    }
    return false;
}

bool window_exists(const char window_name[])
{
    Display *display = XOpenDisplay(NULL);
    Window no_use_window{};
    return get_a_window_by_name(display, window_name, no_use_window);
}

tuple<int, int, vector<int>> c_capture_screen(Display *display, Window &window)
{
    XWindowAttributes DOSBoxWindowAttributes;
    XGetWindowAttributes(display, window, &DOSBoxWindowAttributes);

    int width = DOSBoxWindowAttributes.width;
    int height = DOSBoxWindowAttributes.height;

    XColor colors;
    XImage *image;

    image = XGetImage(
        display, window, 0, 0, width, height, AllPlanes, ZPixmap);

    unsigned long red_mask;
    unsigned long green_mask;
    unsigned long blue_mask;

    red_mask = image->red_mask;
    green_mask = image->green_mask;
    blue_mask = image->blue_mask;

    //printf("%d, %d\n", height, width);
    vector<int> final_array;

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            colors.pixel = XGetPixel(image, j, i);
            auto red = (colors.pixel & red_mask) >> 16;
            auto green = (colors.pixel & green_mask) >> 8;
            auto blue = colors.pixel & blue_mask;
            final_array.push_back(red);
            final_array.push_back(green);
            final_array.push_back(blue);
        }
    }

    tuple<int, int, vector<int>> final_result = make_tuple(width, height, final_array);

    XDestroyImage(image);
    return final_result;
}

//http://csweb.cs.wfu.edu/~torgerse/Kokua/Irix_6.5.21_doc_cd/usr/share/Insight/library/SGI_bookshelves/SGI_Developer/books/XLib_PG/sgi_html/ch09.html#:~:text=The%20keycode%20member%20of%20XKeyEvent,key%20is%20pressed%20or%20released.
//Only works for some software, like scrcpy
void c_press_a_key(Display *display, Window &rootWindow, Window &window, KeySym keycode, int duration)
{
    XKeyEvent event;
    event.type = KeyPress;
    event.display = display;
    event.send_event = False;
    event.window = window;
    event.root = rootWindow;
    event.time = CurrentTime;
    event.same_screen = False;
    event.keycode = XKeysymToKeycode(display, keycode);
    XSendEvent(display, window, True, KeyPressMask, (XEvent *)&event);
    XFlush(display);

    std::this_thread::sleep_for(std::chrono::milliseconds(duration));

    event.type = KeyRelease;
    XSendEvent(display, window, True, KeyReleaseMask, (XEvent *)&event);
    XFlush(display);
}


// not working, guys, sorry for this. I just couldn't undertand the fucking x11 logic about how they handle background mouse moving and clicking.
//void c_mouse_click(Display *display, Window &rootWindow, Window &target_window, int x, int y, int duration)
//{
//    XWarpPointer(display, None, target_window, 0, 0, 0, 0, x, y);
//    XFlush(display);
//    std::this_thread::sleep_for(std::chrono::milliseconds(1));
//
//    XEvent event;
//    memset(&event, 0, sizeof(event));
//    event.xbutton.button = Button1;
//    event.xbutton.same_screen = False;
//    event.xbutton.root = rootWindow;
//    event.xbutton.window = target_window;
//
//    /*
//    XEvent useless_event;
//    unsigned int mask_return;
//
//    XQueryPointer(display, target_window, &useless_event.xbutton.root, &useless_event.xbutton.window, &useless_event.xbutton.x_root, &useless_event.xbutton.y_root, &useless_event.xbutton.x, &useless_event.xbutton.y, &mask_return);
//    printf("x: %d, y: %d\n", useless_event.xbutton.x, useless_event.xbutton.y);
//    printf("root_x: %d, root_y: %d", useless_event.xbutton.x_root, useless_event.xbutton.y_root);
//    */
//    event.xbutton.x_root = 0;
//    event.xbutton.y_root = 0;
//    event.xbutton.x = x;
//    event.xbutton.y = y;
//    // Press
//    event.type = ButtonPress;
//    XSendEvent(display, target_window, True, ButtonPressMask, &event);
//    XFlush(display);
//    std::this_thread::sleep_for(std::chrono::milliseconds(duration));
//    // Release
//    event.type = ButtonRelease;
//    XSendEvent(display, target_window, True, ButtonReleaseMask, &event);
//    XFlush(display);
//}
//
//bool mouse_click(const char window_name[], int x, int y, int duration)
//{
//    // get root window
//    Display *display = XOpenDisplay(NULL);
//    Window rootWindow = RootWindow(display, DefaultScreen(display));
//    Window target_window;
//    if (get_a_window_by_name(display, window_name, target_window))
//    {
//        c_mouse_click(display, rootWindow, target_window, x, y, duration);
//        return true;
//    }
//    else
//    {
//        return false;
//    }
//    XCloseDisplay(display);
//}

vector<string> a_cpp_function()
{
    // get a display instance
    Display *display = XOpenDisplay(NULL);

    // get some information
    int screen_num;
    screen_num = DefaultScreen(display); // get default screen id

    int screen_width;
    int screen_height;
    screen_width = DisplayWidth(display, screen_num);
    screen_height = DisplayHeight(display, screen_num);
    printf("width: %d, height: %d\n", screen_width, screen_height);

    // get all window
    vector<Window> window_list;
    vector<string> window_list_name = get_all_windows(display, window_list);

    // get the window
    Window hi;
    printf("%d\n", get_a_window_by_name(display, "x11", hi));

    // capture screen
    c_capture_screen(display, hi);

    return window_list_name;
}


struct MyX11 {
    public:
        MyX11(){
            this->display = XOpenDisplay(NULL);
        }
        ~MyX11(){
            XCloseDisplay(this->display);
            //XFree(this->the_window);
        }
        tuple<int, int, vector<int>> capture_screen(const char window_name[])
        {
            if (get_a_window_by_name(this->display, window_name, this->the_window))
            {
                return c_capture_screen(display, this->the_window);
            }
            else
            {
                vector<int> none = {};
                return make_tuple(0, 0, none);
            }
        }
        bool press_a_key(const char window_name[])
        {
            Window rootWindow = RootWindow(this->display, DefaultScreen(this->display));
            Window target_window;
            if (get_a_window_by_name(this->display, window_name, target_window))
            {
                c_press_a_key(this->display, rootWindow, target_window, XK_y, 100);
                return true;
            }
            else
            {
                return false;
            }
        }
    private:
        Display *display;
        Window the_window;
};


PYBIND11_MODULE(myx11, m)
{
    m.doc() = "pybind11 example plugin"; // Optional module docstring
    //m.def("a_cpp_function", &a_cpp_function, "A function that multiplies two numbers");
    //m.def("window_exists", &window_exists, "check if a window exists by its name");
    py::class_<MyX11>(m, "MyX11")
    .def(py::init<>())
    .def("capture_screen", &MyX11::capture_screen)
    .def("press_a_key", &MyX11::press_a_key);
}

int main() {
    MyX11 myx11 = MyX11();
    int count = 0;
    while(count <= 30)
    {
        myx11.capture_screen("pixel");
        count++;
    }
}
