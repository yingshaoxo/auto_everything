"""
How to sync data in 3 disk storage?

1. You have diskA, diskB, and diskC. diskC should have biggest storage.
2. You compare diskA, diskB and diskC, find common things in 3 disk. find different parts in 3 disk.
3. You manually choose what folder or file in diskA need to get saved. A software will remember that.
4. You manually choose what folder or file in diskB need to get saved. This time it would be easier for you because software remembers some choice you did last time.
5. You copy everything need to get saved from diskA and diskB to diskC.
6. You delete unwanted difference data in diskC.
7. You re-manage diskC data.
8. You copy diskC data into diskA and diskB directly by overwrite everything.
"""

from auto_everything.disk import Disk
disk = Disk()
from auto_everything.terminal import Terminal_User_Interface
terminal_user_interface = Terminal_User_Interface()

result = terminal_user_interface.selection_box(text="Please select one:", selections=["a", "b"])
print(result)

