import pyfakewebcam
import cv2

from auto_everything.base import Terminal
t = Terminal(debug=True)


class FakeCamera():
    """
    This module based on `pyfakewebcam`.
    """

    def __init__(self, device: str = None, width: int = 640, height: int = 480):
        list_command = "v4l2-ctl --list-devices"
        list_devices = t.run_command(list_command)
        assert "not found" not in list_devices, f"{list_devices}\n\nv4l2-ctl not found, you may have to install it with 'sudo apt install v4l2loopback-utils'"
        assert "v4l2loopback" in list_devices, f"{list_devices}\n\nTo create a fake camera, you have to add a dummy device first by 'sudo modprobe v4l2loopback'"
        lines = list_devices.split("\n")
        the_device = None
        for index, line in enumerate(lines):
            if index < len(lines) - 1:
                if ("v4l2loopback" in line) and "/dev/video" in lines[index + 1]:
                    the_device = lines[index + 1].strip()
        if device == None:
            assert the_device != None, f"{list_devices}\n\ncan't auto find the dummy device, you may have to specify it manullay: FakeCamera('/dev/video*')"
            self.device = the_device
        else:
            self.device = device
        self.camera = pyfakewebcam.FakeWebcam(self.device, width, height)

    def next(self, frame, rgb=False):
        """
        Pipe new frame to the fake camera

        Parameters
        ----------
        frame: numpy representation of an image
            np.zeros((480,640,3), dtype=np.uint8)
        rgb: bool
            if you want to give me an rgb frame, you'll have to set this.
        """
        if rgb:
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        self.camera.schedule_frame(frame)

    def show(self):
        """
        Show the fake camera by using ffplay

        Parameters
        ----------
        """
        t.run(f"ffplay {self.device}")


if __name__ == "__main__":
    from pprint import pprint
    fakecam = FakeCamera()
