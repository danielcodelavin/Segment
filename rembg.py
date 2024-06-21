from rembg import remove

def remove_background(input: str, save_output: bool = True):
    imgpath = input
    input_path = '/dataset/'+imgpath
    output_path = 'outputrmbg'+imgpath

    with open(input_path, 'rb') as i:
        with open(output_path, 'wb') as o:
            input = i.read()
            output = remove(input)
            if save_output:
                o.write(output)
            else :
                return output