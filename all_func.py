import torchvision.transforms as transforms
from PIL import Image
import numpy as np
from skimage.feature import hog
import cv2


class HOGFeatureExtractor:
    def _init_(self, orientations=9, pixels_per_cell=(8, 8), cells_per_block=(2, 2)):
        self.orientations = orientations
        self.pixels_per_cell = pixels_per_cell
        self.cells_per_block = cells_per_block
    
    def extract_features(self, image):

        image = image/255
        # Compute HOG features and visualization
        features, hog_image = hog(image, orientations=self.orientations, 
                                    pixels_per_cell=self.pixels_per_cell,
                                    cells_per_block=self.cells_per_block, 
                                    visualize=True, transform_sqrt=True)
    
        return np.array(features), np.array(hog_image)

    def prepare_data(self, image):
        features, hog_image = self.extract_features(image)
        # Normalize features
        features = np.array(features)
        return features, hog_image

def resize_images(image):
    """
    Resize a list of images to 125x94 pixels with 3 channels using PyTorch.
    
    Args:
    - images (list): List of images to resize.
    
    Returns:
    - resized_images (list): List of resized images as PyTorch tensors.
    """
    # Define the transformation
    transform = transforms.Compose([
        transforms.Resize((125, 94), interpolation=Image.BILINEAR),
        transforms.ToTensor(),
    ])
    
    image_pil = Image.fromarray(np.uint8(image))
    resized_image = transform(image_pil)
    return resized_image

def convert_to_grayscale(image):
    # Convert to grayscale
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
