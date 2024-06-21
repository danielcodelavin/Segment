import segment_anything

class AnythingMask:
    def __init__(self, model_path, device, image_size):
        self.model = segment_anything.Segmentation(model_path=model_path, device=device, image_size=image_size)