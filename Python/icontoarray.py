from PIL import Image
import numpy as np
import sys

# Import color scheme
from ulib.graphics_library import (
    colors,
)  # Adjust if the dict is named differently
import ulib.graphics_library as gl


def to_array(image_path):
    """
    Converts an image to a numpy array.
    """
    with Image.open(image_path) as img:
        img = img.convert("RGB")
        return np.array(img)


def colors_to_gl_statements(image_array, color_scheme):
    gl_array = np.empty(image_array.shape[0:2], dtype=object)
    for x in range(image_array.shape[0]):
        for y in range(image_array.shape[1]):
            color = tuple(image_array[x, y])
            if color in color_scheme.values():
                color_name = [
                    name for name, value in color_scheme.items() if value == color
                ][0]
                gl_array[x, y] = f"gl.colors['{color_name}']"
            else:
                gl_array[x, y] = str(color)
    return gl_array


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python toarray.py <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]
    image_array = to_array(image_path)
    print(image_array.shape)
    print(image_array)

    # Print gl.colors statements for unique colors
    gl_array = colors_to_gl_statements(image_array, colors)
    gl_array = gl_array.T
    print("Converted array:")
    print(gl_array.shape)
    # Print each row without quotes around the strings
    print("np.array([")
    for row in gl_array:
        print("[" + ", ".join(str(item) for item in row) + "],")
    print("])")

    print("Done converting image to gl.colors statements.")
