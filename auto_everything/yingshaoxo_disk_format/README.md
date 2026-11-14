## goal
the disk can get load to memory as bytes object.
the disk can also be in disk, operate without using memory.


## main framework

### file_list at the beginning:

```
yingshaoxo_file_list_start\n
last_available_seek_bytes_position:512000
folder_or_file | file_name | file_size_in_bytes | update_time | seek_bytes_position1 | seek_bytes_position2 | file_size_in_chars | page_number_location | \r\n
1|/novel.txt|200|2029-01-11-09-10-60|0|26|25|0|\r\n
1|/music.wav|4194304|2029-01-11-09-11-60|303|365|524288|0|\r\n
0|/root/a_folder_name|0|2029-01-11-09-12-60|0|0|0|0|\r\n
#|/root/this_is_a_deleted_file_because_it_starts_with_#||519999|2029-01-11-09-13-60|0|0|0|0|\r\n
...
yingshaoxo_file_list_end\r\n
```

> replace every '|' in those part into url_version of '|': '%7c'. for example, "file_name=yingshao|xo.bmp" should become "file_name=yingshaoxo%7cxo.bmp".

> file_name byte length should be less or equal to 255. in other words, char number <= 255.

### file_content later is:
```
start,start.start?start:\n(this is where the seek_bytes_location1 start)
name:/novel.txt\n
size:200\n
time:2029-01-11-09-10-6\n
content:(this is where the seek_bytes_location2 start)\n
end?end.end,end.\r\n\n

start,start.start?start:\n(this is where the seek_bytes_location1 start)
name:/music.wav\n
size:4194304\n
time:2029-01-11-09-11-6\n
content:(this is where the seek_bytes_location2 start)\n
end?end.end,end.\r\n\n
```

### save data process
1.change file_list data for rename, move, delete, add, edit
2.when you delete, you replace the first character into #
3.when you change content, if new content is smaller than original, you replace old content. if new content is bigger than original, you add new one at bottom.
4.when you change content, you first send new change size, then send real data.
5.when you add data, if you found deleted file in file_list that bigger than the one you add, you can reuse its container for saving new data.
