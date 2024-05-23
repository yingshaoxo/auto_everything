from auto_everything.additional.image_type_and_shape_detector.get_image_size import get_image_size as _get_image_size
from auto_everything.additional.image_type_and_shape_detector.get_image_size import get_image_metadata as _get_image_metadata

def get_image_type(file_path):
    return _get_image_metadata(file_path).type.lower()

def get_image_shape(file_path):
    width, height = _get_image_size(file_path)
    return height, width
