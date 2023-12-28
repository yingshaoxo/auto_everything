import cv2
import numpy as np
from auto_everything.gui_operator import AndroidGUI
from pprint import pprint

scrcpy_window_name, project_name = "pixel", "test"
androidGUI = AndroidGUI(scrcpy_window_name, project_name)


while(True):
    image, results = androidGUI.find_all("money", visual=True)

    for r in results:
        androidGUI.click(r)

    # Display the resulting frame
    cv2.imshow('frame', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
