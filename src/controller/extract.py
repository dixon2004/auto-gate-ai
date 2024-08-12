from src.utils.log import write_log
import numpy as np
import easyocr
import cv2
import re


class TextExtraction:

    def __init__(self) -> None:
        """
        Initialize the EasyOCR reader.
        """
        self.reader = easyocr.Reader(['en'])


    def crop_bounding_box(self, image: np.ndarray, label: dict) -> np.ndarray:
        """
        Crop the bounding box from the image using the coordinates provided in the label.

        Args:
            image (np.ndarray): The image to crop the bounding box from.
            label (dict): The label containing the bounding box coordinates.

        Returns:
            np.ndarray: The cropped image.
        """
        try:
            if isinstance(image, str):
                image = cv2.imread(image)
            
            if image is None:
                raise FileNotFoundError(f"Image not found at {image}")

            x_min = label.get("x1")
            y_min = label.get("y1")
            x_max = label.get("x2")
            y_max = label.get("y2")
            
            if None in [x_min, y_min, x_max, y_max]:
                raise ValueError("Bounding box coordinates are incomplete")
            
            cropped_image = image[y_min:y_max, x_min:x_max]
            
            if cropped_image.size == 0:
                raise ValueError("Cropped image is empty. Check the bounding box coordinates.")
            
            return cropped_image
        
        except Exception as e:
            write_log("error", f"[TextExtraction] Failed to crop bounding box: {e}")


    def resize_image(self, image: np.ndarray, scale_factor: float) -> np.ndarray:
        """
        Resize the image by a given scale factor.

        Agrs:
            image (np.ndarray): The image to resize.
            scale_factor (float): The factor to resize the image by.

        Returns:
            np.ndarray: The resized image.
        """
        try:
            return cv2.resize(image, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        except Exception as e:
            write_log("error", f"[TextExtraction] Failed to resize image: {e}")


    def convert_to_grayscale(self, image: np.ndarray) -> np.ndarray:
        """
        Convert the image to grayscale.
        
        Args:
            image (np.ndarray): The image to convert.

        Returns:
            np.ndarray: The grayscale image.
        """
        try:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        except Exception as e:
            write_log("error", f"[TextExtraction] Failed to convert image to grayscale: {e}")


    def denoise_image(self, image: np.ndarray) -> np.ndarray:
        """
        Apply Gaussian blur to denoise the image.

        Args:
            image (np.ndarray): The image to denoise.

        Returns:
            np.ndarray: The denoised image. 
        """
        try:
            return cv2.GaussianBlur(image, (5, 5), 0)
        except Exception as e:
            write_log("error", f"[TextExtraction] Failed to denoise image: {e}")


    def format_car_plate(self, number: str) -> str:
        """
        Extract the car plate number from the text and format it.

        Args:
            number (str): The extracted text.

        Returns:
            str: The formatted car plate number.
        """
        try:
            pattern = r'\b[A-Z]{1,3}\s?\d{1,4}\s?[A-Z]?\b'
            matches = re.findall(pattern, number)
            if not matches:
                return None
            
            return matches[0].strip().replace(" ", "")
        
        except Exception as e:
            write_log("error", f"[TextExtraction] Failed to format car plate: {e}")


    def get_car_plate(self, image: str, label: dict) -> str:
        """
        Extract the car plate number from the image.

        Args:
            image (str): The path to the image.
            label (dict): The label containing the bounding box coordinates.

        Returns:
            str: The extracted car plate number.
        """
        try:
            cropped_image = self.crop_bounding_box(image, label)

            # Resize the image by a factor of 2x
            resized_image = self.resize_image(cropped_image, 2)

            # Convert to grayscale
            grayscale_image = self.convert_to_grayscale(resized_image)

            # Denoise the image
            denoised_image = self.denoise_image(grayscale_image)
            
            # Extract text using EasyOCR
            easyocr_results = self.reader.readtext(denoised_image)
            extracted_text = [result[1] for result in easyocr_results if result[2] > 0.25]
            
            if not extracted_text:
                return None

            combined_text = ' '.join(extracted_text)
            car_plate = self.format_car_plate(combined_text)
            
            return car_plate
        
        except Exception as e:
            write_log("error", f"[TextExtraction] Failed to extract car plate: {e}")
    