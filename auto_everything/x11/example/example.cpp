//sudo gcc example.cpp -lstdc++ -lX11 -lXmu -o example && ./example
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <X11/Xlib.h>
#include <X11/Xatom.h>
#include <errno.h>
 
 
Window *winlist (Display *disp, unsigned long *len);
char *winame (Display *disp, Window win); 
 
int main(int argc, char *argv[]) {
    int i;
    unsigned long len;
    Display *disp = XOpenDisplay(NULL);
    Window *list;
    char *name;
 
    if (!disp) {
        puts("no display!");
        return -1;
    }
 
    list = (Window*)winlist(disp,&len);
 
    for (i=0;i<(int)len;i++) {
        name = winame(disp,list[i]);
        printf("-->%s<--\n",name);
        free(name);
    }
 
    XFree(list);
 
    XCloseDisplay(disp);
    return 0;
}
 
 
Window *winlist (Display *disp, unsigned long *len) {
    Atom prop = XInternAtom(disp,"_NET_CLIENT_LIST",False), type;
    int form;
    unsigned long remain;
    unsigned char *list;
 
    errno = 0;
    if (XGetWindowProperty(disp,XDefaultRootWindow(disp),prop,0,1024,False,XA_WINDOW,
                &type,&form,len,&remain,&list) != Success) {
        perror("winlist() -- GetWinProp");
        return 0;
    }
     
    return (Window*)list;
}
 
 
char *winame (Display *disp, Window win) {
    Atom prop = XInternAtom(disp,"WM_NAME",False), type;
    int form;
    unsigned long remain, len;
    unsigned char *list;
 
    errno = 0;
    if (XGetWindowProperty(disp,win,prop,0,1024,False,XA_STRING,
                &type,&form,&len,&remain,&list) != Success) {
        perror("winlist() -- GetWinProp");
        return NULL;
    }
 
    return (char*)list;
}
