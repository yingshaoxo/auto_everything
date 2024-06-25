"""
# How to backup data and sync data in a safe way? -- made by yingshaoxo


Suppose you have 3 disk, 1MB disk, 10GB disk, 1TB disk.

In 1MB disk, you only save folder tree, there has no files in each folder.

In 10GB disk, it has all folder from 1MB disk, and for some folder, it got some files in those folder, but only pure text file. Each file is less than 10MB.

In 1TB disk, it has all folders and files from 10GB disk, but it got more files, more types of file, some file even bigger than 100MB.

For all 3 disks, they all have a txt file at top, that txt file contains all folder and files tree information of 1TB disk.

To sync those disks, all you have to do is use `rsync` to copy all files and folder from 1MB to 10GB, then do the same thing from 10GB to 1TB.

But for file deletion, you only do the deletion at your level disk, you do not have permission to delete file in smaller size disk.
"""
