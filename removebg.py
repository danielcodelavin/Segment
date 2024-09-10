from rembg import remove
from PIL import Image
import io
def remove_background(input: str, save_output: bool = True):
    imgpath = input
    input_path = imgpath

    with open(input_path, 'rb') as i:



        input = i.read()
        output = remove(input)
        pil_image = Image.open(io.BytesIO(output))
        return pil_image


if __name__ == '__main__':
    remove_background('onceler.jpeg')
