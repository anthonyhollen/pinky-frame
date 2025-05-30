from PIL import Image
from inky.auto import auto

def display_image(image_path):
    inky_display = auto()
    inky_display.set_image(Image.open(image_path))
    inky_display.show()
