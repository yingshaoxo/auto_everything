import auto_everything.additional.pypng.png as png


def read_png_from_file(path):
    """
    return (height, width, raw_data)
    """
    reader = png.Reader(path)
    try:
        width, height, rows, info = reader.read()
    except Exception as e:
        print("The python bytearray has bug, it can't handle big file. You may need to read a smaller png file. For example, 800*600 image.")
        raise e

    rows = list(rows)

    data = []
    for row_index in range(0, height):
        source_data_row = rows[row_index]
        row = [None] * width
        for column_index in range(0, width):
            source_column_index = column_index * 4
            an_rgb_list = [None] * 4
            for i in range(4):
                 an_rgb_list[i] = source_data_row[source_column_index+i]
            row[column_index] = an_rgb_list
        data.append(row)

    return height, width, data


"""
    from auto_everything.image import Image
    image = Image()

    import auto_everything.additional.pypng.png as png
    reader = png.Reader(source_image_path)
    width, height, rows, info = reader.read()
    print(height, width)

    a_image = image.create_an_image(height, width)

    length_in_one_row = width * 4
    for row_index, row in enumerate(rows):
        step_index = 0
        index = 0
        while step_index < length_in_one_row:
            an_rgb_list = [None] * 4
            for i in range(4):
                 an_rgb_list[i] = row[step_index+i]
            a_image.raw_data[row_index][index] = an_rgb_list

            step_index += 4
            index += 1

    a_image.print(width=70)
"""


def save_png_to_file(image_object, path):
    if type(image_object) == list:
        data = image_object
        if type(image_object[0]) == list:
            data = []
            for each_line in image_object:
                each_line_data = []
                for grba in each_line:
                    for i in range(4):
                        each_line_data.append(grba[i])
                data.append(each_line_data)
    else:
        height, width = image_object.get_shape()
        data = [None] * height
        for row_index, each_line in enumerate(image_object.raw_data):
            each_line_data = [None] * width * 4
            for index, grba in enumerate(each_line):
                the_index = index * 4
                for i in range(4):
                    each_line_data[the_index+i] = grba[i]
            data[row_index] = each_line_data

    png.from_array(data, 'RGBA').save(path)


__all__ = [
    "png",
    "read_png_from_file",
    "save_png_to_file"
]
