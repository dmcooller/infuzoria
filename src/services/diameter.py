import cv2
import numpy as np


def find_microscope_ocular_diameter(image_path: str) -> tuple[int, tuple[int, int]] | None:
    """Find the diameter (px) of the ocular lens in a microscope image.

    Args:
        image_path (str): The path to the image.

    Returns:
        tuple[int, tuple[int, int]] | None: The diameter of the ocular lens and the coordinates of the circle's center, or None if no circle is found.
    """
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (9, 9), 2)

    circles = cv2.HoughCircles(
        blurred_image, cv2.HOUGH_GRADIENT, dp=1, minDist=400, param1=200, param2=30, minRadius=1000, maxRadius=0
    )

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            # circle outline
            center = (i[0], i[1])
            radius = i[2]
            diameter = radius * 2
            return diameter, center
    return None
