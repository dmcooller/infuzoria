import cv2
import numpy as np
from PySide6.QtCore import QPointF
from PySide6.QtGui import QImage, QPixmap


def find_microscope_ocular_diameter(image_source: str | QPixmap) -> tuple[int, tuple[int, int]] | None:
    """Find the diameter (px) of the ocular lens in a microscope image.

    Args:
        image_path (str): The path to the image.

    Returns:
        tuple[int, tuple[int, int]] | None: The diameter of the ocular lens and the coordinates of the circle's center, or None if no circle is found.
    """
    if isinstance(image_source, QPixmap):
        image = qimage_to_opencv(image_source.toImage())
    else:
        image = cv2.imread(image_source, cv2.IMREAD_COLOR)
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


def qimage_to_opencv(qimage: QPixmap):
    """Convert QImage to an OpenCV format."""
    qimage = qimage.convertToFormat(QImage.Format.Format_RGB32)
    width = qimage.width()
    height = qimage.height()
    ptr = qimage.bits()

    arr = np.array(ptr, copy=False).reshape((height, width, 4))  # QImage is stored as ARGB
    return cv2.cvtColor(arr, cv2.COLOR_BGRA2BGR)


def crop_image(image_source: QPixmap, center: QPointF, diameter: float, margin: int = 10) -> tuple[QPixmap, int, int]:
    if not image_source:
        raise ValueError("No image source provided.")
    image = image_source.toImage()
    radius = diameter / 2
    crop_x = max(0, int(center.x() - radius - margin))
    crop_y = max(0, int(center.y() - radius - margin))
    crop_width = min(image.width() - crop_x, int(diameter + 2 * margin))
    crop_height = min(image.height() - crop_y, int(diameter + 2 * margin))
    image = image.copy(crop_x, crop_y, crop_width, crop_height)
    return QPixmap.fromImage(image), crop_x, crop_y
