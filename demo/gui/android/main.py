from auto_everything.gui import AndroidGUI
from pprint import pprint

scrcpy_window_name, project_name = "pixel", "test"
androidGUI = AndroidGUI(scrcpy_window_name, project_name)

results = androidGUI.find_all("money")
pprint(results)
for result in results:
    androidGUI.click(result)
