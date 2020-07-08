#include <pybind11/pybind11.h>
namespace py = pybind11; // pip3 install pybind11

#include <stdlib.h>
#include <stdio.h>
#include <locale.h>

#include <X11/Xlib.h>           // `apt-get install libx11-dev`
#include <X11/Xmu/WinUtil.h>    // `apt-get install libxmu-dev`

Bool xerror = False;

Display* open_display(){
  printf("connecting X server ... ");
  Display* d = XOpenDisplay(NULL);
  if(d == NULL){
    printf("fail\n");
    exit(1);
  }else{
    printf("success\n");
  }
  return d;
}

int handle_error(Display* display, XErrorEvent* error){
  printf("ERROR: X11 error\n");
  xerror = True;
  return 1;
}

Window get_focus_window(Display* d){
  Window w;
  int revert_to;
  printf("getting input focus window ... ");
  XGetInputFocus(d, &w, &revert_to); // see man
  if(xerror){
    printf("fail\n");
    exit(1);
  }else if(w == None){
    printf("no focus window\n");
    exit(1);
  }else{
    printf("success (window: %d)\n", (int)w);
  }

  return w;
}

// get the top window.
// a top window have the following specifications.
//  * the start window is contained the descendent windows.
//  * the parent window is the root window.
Window get_top_window(Display* d, Window start){
  Window w = start;
  Window parent = start;
  Window root = None;
  Window *children;
  unsigned int nchildren;
  Status s;

  printf("getting top window ... \n");
  while (parent != root) {
    w = parent;
    s = XQueryTree(d, w, &root, &parent, &children, &nchildren); // see man

    if (s)
      XFree(children);

    if(xerror){
      printf("fail\n");
      exit(1);
    }

    printf("  get parent (window: %d)\n", (int)w);
  }

  printf("success (window: %d)\n", (int)w);

  return w;
}

// search a named window (that has a WM_STATE prop)
// on the descendent windows of the argment Window.
Window get_named_window(Display* d, Window start){
  Window w;
  printf("getting named window ... ");
  w = XmuClientWindow(d, start); // see man
  if(w == start)
    printf("fail\n");
  printf("success (window: %d)\n", (int) w);
  return w;
}

// (XFetchName cannot get a name with multi-byte chars)
void print_window_name(Display* d, Window w){
  XTextProperty prop;
  Status s;

  printf("window name:\n");

  s = XGetWMName(d, w, &prop); // see man
  if(!xerror && s){
    int count = 0, result;
    char **list = NULL;
    result = XmbTextPropertyToTextList(d, &prop, &list, &count); // see man
    if(result == Success){
      printf("\t%s\n", list[0]);
    }else{
      printf("ERROR: XmbTextPropertyToTextList\n");
    }
  }else{
    printf("ERROR: XGetWMName\n");
  }
}

void print_window_class(Display* d, Window w){
  Status s;
  XClassHint* c_class;

  printf("application: \n");

  c_class = XAllocClassHint(); // see man
  if(xerror){
    printf("ERROR: XAllocClassHint\n");
  }

  s = XGetClassHint(d, w, c_class); // see man
  if(xerror || s){
    printf("\tname: %s\n\tclass: %s\n", c_class->res_name, c_class->res_class);
  }else{
    printf("ERROR: XGetClassHint\n");
  }
}

void print_window_info(Display* d, Window w){
  printf("--\n");
  print_window_name(d, w);
  print_window_class(d, w);
}

void a_cpp_function() {
  Display* d;
  Window w;

  // for XmbTextPropertyToTextList
  setlocale(LC_ALL, ""); // see man locale

  d = open_display();
  XSetErrorHandler(handle_error);

  // get active window
  w = get_focus_window(d);
  w = get_top_window(d, w);
  w = get_named_window(d, w);

  print_window_info(d, w);
}

PYBIND11_MODULE(myx11, m) {
    m.doc() = "pybind11 example plugin"; // Optional module docstring
    m.def("a_cpp_function", &a_cpp_function, "A function that multiplies two numbers");
}
