from auto_everything.camera import FakeCamera
import pornstar

def my_handler(frame):
    frame = pornstar.effect_of_whitening(frame)
    #frame = pornstar.stylize_background_and_human_body(
    #        frame,
    #        [pornstar.effect_of_pure_white],
    #        [pornstar.effect_of_whitening]
    #    )
    fakecam.next(frame, rgb=True)
    return frame

# create fake camera
fakecam = FakeCamera()

# keep running
pornstar.process_camera(0, my_handler, show=False)
