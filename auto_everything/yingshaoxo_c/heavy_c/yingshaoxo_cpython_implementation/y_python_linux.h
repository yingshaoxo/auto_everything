#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

/*
Run a bash command and return the result as a string.
*/
char *ypython_run_command(const char *bash_command_line)
{
    FILE *FileOpen;
    FileOpen = _ypython_execute_shell_command_as_a_subprocess_pipe_stream(bash_command_line, "r");

    char *all_lines = _ypython_get_infinate_length_text(FileOpen);
    _ypython_close_subprocess_pipe_stream(FileOpen);

    return (char *)ypython_string_strip(all_lines);
}

/*
Run a bash command and wait for it to get finished, it won't return anything.
*/
void ypython_run(const char *bash_command_line)
{
    FILE *FileOpen;
    FileOpen = _ypython_execute_shell_command_as_a_subprocess_pipe_stream(bash_command_line, "r");

    while (!_ypython_return_end_of_file_indicator_for_a_STREAM(FileOpen))
    {
        char *a_line = _ypython_get_infinate_length_text_line(FileOpen);
        printf("%s", a_line);
    }

    _ypython_close_subprocess_pipe_stream(FileOpen);
}

void ypython_clear_screen() {
    /*
    ypython_run("clear");
    fflush(stdout);
    return;
    */

    for (int i=0; i < 100; i=i+1) {
        printf("\n");
    }

    /*
    //char *tty_path = "/dev/pts/2";
    char *tty_path = ypython_run_command("tty");

    FILE* the_tty_file;
    the_tty_file = fopen(tty_path, "w+");

    for (int i=0; i < 10000; i=i+1) {
        //fprintf(the_tty_file, "%s %s %s", "Welcome", "to", "GeeksforGeeks");
        putc((unsigned char)32, the_tty_file);
    }

    for (int i=0; i < 10000; i=i+1) {
        putc((unsigned char)8, the_tty_file);
    }

    fclose(the_tty_file);
    */

    /*
    putc('\x1b', stdout);
    putc('[', stdout);
    putc('2', stdout);
    putc('J', stdout);
    fflush(stdout);
    return;
    */

}

bool ypython_disk_exists(char *path) {
    struct stat temp_data;

    int exists = stat(path, &temp_data);
    if (exists == 0) {
        return true;
    }

    return false;
}

bool ypython_disk_is_folder(char *path) {
    struct stat temp_data;

    int exists = stat(path, &temp_data);
    if (exists == 0 && S_ISDIR(temp_data.st_mode)) {
        return true;
    }

    return false;
}
