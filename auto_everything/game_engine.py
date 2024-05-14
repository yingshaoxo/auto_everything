# In development...

from auto_everything.image import Image

class Raw_3D_Object():
    """
    How to use data to represent a 3D model? Think about people shape to 3d model by using a 3d shape scanner:
        We have a person stand in center, then there has a distance_detector points to that person, and do a rotate around that person. The distance_detector can be a camera or ultrasonic_distance_detector. The detector will go round to make a circle, and the center of that circle have the person stand. And for each time, the distance_detector will go up for 0.1mm length. So in the end, you will get a distance list or points list that represents the person shape.
        If you think that list of data in polar coordinate system, you can have each points angle and line distance, so that you can get a list of 3D point in real xyz coordinates, for example, [z, y, x].
        And as you know, you can't get all points, but some points to represent a human shape. Just think about drawing a line, you got some broken points, you have to connect those points togather to get a continues line that is considered the real line. Between 1 and 2, there could have infinite float numbers, so you can only choose some broken points.
        For the 3D model, it is the same, you have to use around mean value to represent those plane that did not get scanned at the first place. So you will get a 3D model that have every points includeing those you calculated based on around points.
        Those points you scanned for a 3D model can be the data that saved in disk to represent the model, but it is too big when you just want to save a cube.
        When you save a cube, you just need to save a side length, and tell the render it is a cube. It only takes less than 100 characters to represent this cube, in other words, a cube model in disk will only take less than 1KB storage.
        So how to make the 3d format a perfect one for saving all kinds of shapes with low storage cost?
        1. You first specify all kinds of shape that could get represented with special shape, for example, cube, sphere.
        2. Then you specify lines, planes.
        3. After those special shapes, you rendering raw points list, points that from 3d scanner. Those points can form a unusual plane.
        All in all, just like SVG image format, use small math description words to represent shape first, then use raw points to represents unusual things later.

    To a extreme compression level of 3D model, you can simply use natural language to represent a shape, for example: "I want a cube that has side length of 3cm" or "A ball that center point is (0,0,0), radius is 1 meter".
    What kind of thing you can't use natural language to represent in this world?
    """
    pass

class Three_Dimension_Object():
    """
    This should be a class that similar to image.py Image class.
    But this class will mainly focus on handling 3D object.
    For example, import an 3d object, resize a 3d object, rotate a 3d object, move a 3d object
    But all operations will only change some propertys, string, int, float, bool, not the object shape data
    """
    def __init__(self, object_file_path):
        self.type = "3d_object"
        # you should find a way to import a 3d object from path
        self.raw_object = None

class Two_Dimension_Object():
    """
    This should be a class that wraps image.py Image class.
    This class will handle more behavior in 3D world.
    For example, resize a 3d object, rotate a 3d object, move a 3d object
    But all operations will only change some propertys, string, int, float, bool, not the image raw data
    It can reuse the Three_Dimension_Object class codes
    """
    def __init__(self, image):
        self.type = "2d_object"
        self.raw_image = image

class Camera():
    """
    Camera is also a 3d object, but it is not visible to users in final rendering image.
    You can only rotate, move a camera.
    """
    def __init__(self, id_string):
        self.type = "camera"
        self.id_string = id_string

    def render(self, scene_object):
        """
        The render function will loop 'two_dimension_objects' and 'three_dimension_objects' in scene_object, then render an image that represent what this camera sees according to those propertys in those 3d objects. For example how big they are, how far they are away from this camera, what kind of angle they are in, how they should look like under the light.
        """
        return Image()

class Light():
    """
    Light is also a 3d object, but it is not visible to users in final rendering image.
    You can only rotate, move a Light, change a light brightness.
    You should make the simplest light to gain performence.
    A simple shadow would be enough.
    """
    def __init__(self):
        self.type = "light"

class Scene():
    """
    For this class, it can take Two_Dimension_Object, or Three_Dimension_Object class
    You can think the Scene as a 3D world that uses x,y,z axis. All objects that can be put into this 3D world.
    This world can have multiple camera object, you can use scene.a_camera.render() function to get a 2D image object, that's what the camera sees.
    """
    def __init__(self):
        self.two_dimension_objects = {}
        self.three_dimension_objects = {}

    def add_a_2d_object(self, name, an_object):
        """
        name: str
        an_object: Two_Dimension_Object
        """
        self.two_dimension_objects[name] = an_object

    def add_a_3d_object(self, name, an_object):
        """
        name: str
        an_object: Three_Dimension_Object

        Camera, Light is also a 3d object.
        """
        self.three_dimension_objects[name] = an_object
