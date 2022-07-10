from PIL import Image


def save_img(image_obj, save_name):
    im = Image.fromarray(image_obj)
    im.save(save_name)
