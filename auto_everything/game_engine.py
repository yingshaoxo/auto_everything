# In development...

from auto_everything.image import Image

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
