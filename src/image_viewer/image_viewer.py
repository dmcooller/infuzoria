import math

from PySide6.QtCore import QPointF, Qt
from PySide6.QtGui import (
    QAction,
    QColor,
    QContextMenuEvent,
    QFont,
    QImage,
    QKeyEvent,
    QKeySequence,
    QMouseEvent,
    QPainter,
    QPen,
    QPixmap,
)
from PySide6.QtWidgets import (
    QGraphicsPixmapItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QMenu,
    QMessageBox,
)

from services.image_service import crop_image, find_microscope_ocular_diameter
from ui.design import Ui_MainWindow
from utils import extract_zoom_from_filename, try_float


class ImageViewer(QGraphicsView):
    def __init__(self, mainWindow: Ui_MainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.setDragMode(QGraphicsView.NoDrag)
        self._isPanning: bool = False
        self._panStartX: int = 0
        self._panStartY: int = 0
        self._spacePressed: bool = False
        self._pov_mode: bool = False

        # Field of view (FOV) drawing
        self._is_fov_drawing = False
        self._fov_start_point = None
        self._fov_end_point = None

        # Keep track of points, lines, distances, and distance texts
        self.points: list = []
        self.lines: list = []
        self.distances: list = []
        self.distanceTexts: list = []
        self.fovCircle = None

        self.totalDistance = 0  # Sum of all distances

        # Default colors and sizes
        self.pointColor = QColor("red")
        self.lineColor = QColor("green")
        self.textColor = QColor("black")
        self.pointSize: int = 11
        self.lineHeight: int = 7
        self.textSize: int = 12

        self.undoStack: list = []
        self.redoStack: list = []

        self.pixmap_item = None  # Image item

        # Actions
        self.undoAction = self._createUndoAction()
        self.redoAction = self._createRedoAction()
        self.clearAllAction = self._createClearAllAction()
        self.clearDrawAction = self._createClearDrawAction()

    def contextMenuEvent(self, event: QContextMenuEvent):
        context_menu = QMenu(self)
        context_menu.addAction(self.clearDrawAction)
        context_menu.addAction(self.clearAllAction)
        context_menu.addSeparator()
        context_menu.addAction(self.undoAction)
        context_menu.addAction(self.redoAction)

        _ = context_menu.exec(event.globalPos())

    def _createClearAllAction(self) -> QAction:
        a = QAction("Clear All", self)
        a.triggered.connect(lambda: self._clear(remove_image=True, remove_circle=True))
        return a

    def _createClearDrawAction(self) -> QAction:
        a = QAction("Clear Drawing", self)
        a.triggered.connect(lambda: self.clearDrawing())
        return a

    def _createUndoAction(self) -> QAction:
        a = QAction("Undo", self)
        # Undo twice to remove last point and line
        a.triggered.connect(self.undoTwice)
        return a

    def _createRedoAction(self) -> QAction:
        a = QAction("Redo", self)
        # Redo twice to add back last point and line
        a.triggered.connect(self.redoTwice)
        return a

    def wheelEvent(self, event):
        factor = 1.1
        if event.angleDelta().y() < 0:
            factor = 0.9
        self.scale(factor, factor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # Pan image if space bar is pressed
            if self._spacePressed:
                self._isPanning = True
                self._panStartX = event.x()
                self._panStartY = event.y()
                self.setCursor(Qt.ClosedHandCursor)
                event.accept()
            # Add point if left click
            else:
                if not self.pixmap_item:
                    raise ValueError("Please load an image first.")
                if not self._pov_mode:
                    try:
                        _ = self._validateFov_Fields()
                    except ValueError as e:
                        QMessageBox.warning(self, "Error", str(e))
                        return
                else:
                    if not len(self.points) % 2:
                        # if self._pov_mode then clear the scene every two points
                        self._clear(remove_circle=True)
                        self._fov_start_point = self.mapToScene(event.pos())
                        self._is_fov_drawing = True
                        self.setMouseTracking(True)
                    else:
                        self._is_fov_drawing = False
                        self.setMouseTracking(False)

                pos = self.mapToScene(event.pos())
                self._addPoint(pos)
                super().mousePressEvent(event)

    def _validateFov_Fields(self) -> tuple[float, float]:
        fov_px = try_float(self.mainWindow.lineEditFovPx.text())
        fov_um = try_float(self.mainWindow.lineEditFovUm.text())
        if not fov_px or fov_px <= 0:
            raise ValueError("Field of view in pixels must be a positive number.")
        if not fov_um or fov_um <= 0:
            raise ValueError("Field of view in micrometers must be a positive number.")
        return fov_px, fov_um

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._is_fov_drawing:
            self._fov_end_point = self.mapToScene(event.pos())
            self._draw_fov()
        if self._isPanning:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self._panStartX))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self._panStartY))
            self._panStartX = event.x()
            self._panStartY = event.y()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton and self._isPanning:
            self._isPanning = False
            self.setCursor(Qt.CrossCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self._spacePressed = True
            event.accept()
        elif event.key() == Qt.Key_Escape:
            if self._pov_mode:
                self._clear(remove_circle=True)
        else:
            super().keyPressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Space:
            self._spacePressed = False
            event.accept()
        else:
            super().keyReleaseEvent(event)

    def setPovMode(self, pov_mode: bool):
        self._pov_mode = pov_mode
        if not pov_mode:
            self._clear(remove_image=False)
            self.mainWindow.statusbar.showMessage("POV mode disabled")
        else:
            self.mainWindow.statusbar.showMessage("POV mode enabled")

    def setNewImage(self, image_path: str):
        self._clear(remove_image=True)
        self.pixmap_item = QGraphicsPixmapItem(QPixmap(image_path))
        self.scene.addItem(self.pixmap_item)
        self.setScene(self.scene)
        self.fitInView(self.pixmap_item, Qt.KeepAspectRatio)
        self._imgAutoHelpers()
        self._tryAutoSetZoomFromFileName(image_path)
        self.setFocus()
        self.mainWindow.statusbar.showMessage(f"Image loaded: {image_path}")

    def _addPoint(self, pos):
        if not self._spacePressed:
            # Create a circle to represent the point
            pointItem = self.scene.addEllipse(
                pos.x() - self.pointSize / 2,
                pos.y() - self.pointSize / 2,
                self.pointSize,
                self.pointSize,
                QPen(self.pointColor),
                self.pointColor,
            )
            self.points.append(pointItem)
            if len(self.points) > 1:
                # Draw line and calculate distance if it's not the first point
                self._drawLineAndCalculateDistance()
            # Record this action
            self.undoStack.append(("point", pointItem))

    def _drawLineAndCalculateDistance(self):
        lastPoint = self.points[-1].rect().center()
        secondLastPoint = self.points[-2].rect().center()
        lineItem = self.scene.addLine(
            lastPoint.x(),
            lastPoint.y(),
            secondLastPoint.x(),
            secondLastPoint.y(),
            QPen(self.lineColor, self.lineHeight),
        )
        self.lines.append(lineItem)

        # Calculate distance between the two points in micrometers
        if self._pov_mode:
            # For POV mode, calculate distance in pixels
            distance = self._calcDistancePx(lastPoint, secondLastPoint)
            self._setlineEditFovPxText(distance)
            self._drawFovCircle(lastPoint.x() - distance / 2, lastPoint.y(), distance)
        else:
            # For normal mode, calculate distance in micrometers
            distance = self._calcDistanceUm(lastPoint, secondLastPoint)
            # Update total distance in the UI
            self._setTotalDistance(self.totalDistance + distance)
        self.distances.append(distance)

        distanceText = self._drawDistanceText(distance, lastPoint, secondLastPoint)

        # Record this action with all elements that needed to be removed for undo
        self.undoStack.append(("line", lineItem, distanceText, distance))

    def _drawDistanceText(self, distance: float, lastPoint: QPointF, secondLastPoint: QPointF) -> QGraphicsTextItem:
        """Draw text showing the distance between two points."""

        distanceText = QGraphicsTextItem(f"{distance:.2f}")

        font = QFont()
        font.setPointSize(self.textSize)
        distanceText.setFont(font)
        distanceText.setDefaultTextColor(self.textColor)

        midPoint = QPointF((lastPoint.x() + secondLastPoint.x()) / 2, (lastPoint.y() + secondLastPoint.y()) / 2)
        # center distance text based on text width
        midPoint.setX(midPoint.x() - distanceText.boundingRect().width() / 2)
        distanceText.setPos(midPoint)

        self.scene.addItem(distanceText)
        self.distanceTexts.append(distanceText)

        return distanceText

    def undo(self):
        if self.undoStack:
            if self._pov_mode:
                self._clear(remove_circle=True)
            else:
                action = self.undoStack.pop()
                if action[0] == "point":
                    # Undo add point
                    self.scene.removeItem(action[1])
                    self.points.remove(action[1])
                elif action[0] == "line":
                    # Undo draw line
                    self.scene.removeItem(action[1])  # Remove line
                    self.scene.removeItem(action[2])  # Remove distance text
                    self.lines.remove(action[1])
                    self.distanceTexts.remove(action[2])
                    self.distances.remove(action[3])
                    self._setTotalDistance(self.totalDistance - action[3])
                self.redoStack.append(action)

    def undoTwice(self):
        """Undo twice to remove last point and line."""
        self.undo()
        self.undo()

    def redo(self):
        if self.redoStack:
            action = self.redoStack.pop()
            if action[0] == "point":
                # Redo add point
                self.scene.addItem(action[1])
                self.points.append(action[1])
            elif action[0] == "line":
                # Redo draw line
                self.scene.addItem(action[1])  # Add line
                self.scene.addItem(action[2])  # Add distance text
                self.lines.append(action[1])
                self.distanceTexts.append(action[2])
                self.distances.append(action[3])
                if not self._pov_mode:
                    self._setTotalDistance(self.totalDistance + action[3])
            self.undoStack.append(action)

    def redoTwice(self):
        """Redo twice to add back last point and line."""
        self.redo()
        self.redo()

    def saveImageWithAnnotations(self, savePath: str):
        # Temporarily remove items not to be saved if necessary
        self.scene.removeItem(self.fovCircle)
        if not self.mainWindow.checkBoxSavePoints.isChecked():
            for point in self.points:
                self.scene.removeItem(point)
        if not self.mainWindow.checkBoxSaveLines.isChecked():
            for line in self.lines:
                self.scene.removeItem(line)
        if not self.mainWindow.checkBoxSaveDistance.isChecked():
            for distanceText in self.distanceTexts:
                self.scene.removeItem(distanceText)

        # Render scene to QPixmap and save
        img = QImage(self.scene.sceneRect().size().toSize(), QImage.Format_ARGB32)
        img.fill(Qt.white)
        painter = QPainter(img)
        self.scene.render(painter)
        painter.end()

        img.save(savePath)

        # Add back items removed for saving
        self.scene.addItem(self.fovCircle)
        if not self.mainWindow.checkBoxSavePoints.isChecked():
            for point in self.points:
                self.scene.addItem(point)
        if not self.mainWindow.checkBoxSaveLines.isChecked():
            for line in self.lines:
                self.scene.addItem(line)
        if not self.mainWindow.checkBoxSaveDistance.isChecked():
            for distanceText in self.distanceTexts:
                self.scene.addItem(distanceText)

    def clearDrawing(self):
        self._clear(remove_image=False)

    def _clear(self, remove_image: bool = False, remove_circle: bool = False):
        if remove_circle and self.fovCircle:
            self._removeFovCircle()
        if remove_image:
            self.pixmap_item = None
            self.scene.clear()
        else:
            for point in self.points:
                self.scene.removeItem(point)
            for line in self.lines:
                self.scene.removeItem(line)
            for distanceText in self.distanceTexts:
                self.scene.removeItem(distanceText)
        self._fov_start_point = None
        self._fov_end_point = None
        self.points.clear()
        self.lines.clear()
        self.distances.clear()
        self.distanceTexts.clear()
        self._setTotalDistance()
        self.undoStack.clear()
        self.redoStack.clear()

    def _imgAutoHelpers(self):
        """Automatically set FOV (px) and crop image if enabled."""
        if (
            self.mainWindow.checkBoxAutoFovPx.isChecked() or self.mainWindow.checkBoxAutoCrop.isChecked()
        ) and not self._pov_mode:
            if not self.pixmap_item:
                QMessageBox.warning(self, "Error", "Please load an image first.")
            try:
                result = find_microscope_ocular_diameter(self.pixmap_item.pixmap())
                if result:
                    diameter, (x, y) = result
                    crop_x, crop_y = 0, 0
                    if self.mainWindow.checkBoxAutoCrop.isChecked():
                        crop_x, crop_y = self._tryAutoCrop(x, y, diameter)
                    if self.mainWindow.checkBoxAutoFovPx.isChecked():
                        self._tryAutoSetFovPx(diameter, x - crop_x, y - crop_y)
                else:
                    self._setlineEditFovPxText()
                    QMessageBox.information(
                        self,
                        "Info",
                        "Could not find FOV (px) automatically. You can set it manually.",
                    )
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _draw_fov(self):
        # Remove last line and circle if they exist
        if self.lines:
            self.scene.removeItem(self.lines[-1])
            self.lines.pop()
        if self.fovCircle:
            self._removeFovCircle()
        if self.distanceTexts:
            self.scene.removeItem(self.distanceTexts[-1])
            self.distanceTexts.pop()

        # Draw line and circle based on the last two points
        if self._fov_start_point and self._fov_end_point:
            lastPoint = self._fov_end_point
            secondLastPoint = self._fov_start_point
            lineItem = self.scene.addLine(
                lastPoint.x(),
                lastPoint.y(),
                secondLastPoint.x(),
                secondLastPoint.y(),
                QPen(self.lineColor, self.lineHeight),
            )
            self.lines.append(lineItem)

            distance = self._calcDistancePx(lastPoint, secondLastPoint)
            self._setlineEditFovPxText(distance)
            self._drawFovCircle(lastPoint.x() - distance / 2, lastPoint.y(), distance)
            _ = self._drawDistanceText(distance, lastPoint, secondLastPoint)

    def _tryAutoSetFovPx(self, diameter: float = 0, x: int = 0, y: int = 0):
        """Set field of view in pixels and draw circle."""
        self._setlineEditFovPxText(diameter)
        self._drawFovCircle(x, y, diameter)

    def _tryAutoCrop(self, x: int, y: int, diameter: float):
        """Crop image around the ocular lens."""
        cropImage, crop_x, crop_y = crop_image(self.pixmap_item.pixmap(), QPointF(x, y), diameter)

        # Remove previous image and add new cropped image
        self.scene.removeItem(self.pixmap_item)
        self.pixmap_item = QGraphicsPixmapItem(cropImage)
        self.scene.addItem(self.pixmap_item)

        return crop_x, crop_y

    def _calcDistanceUm(self, point1: QPointF, point2: QPointF) -> float:
        """Calculate distance between two points in micrometers (μm)."""
        fov_um = float(self.mainWindow.lineEditFovUm.text())
        if not fov_um or fov_um <= 0:
            raise ValueError("Field of view in micrometers must be a positive number.")
        fov_px = float(self.mainWindow.lineEditFovPx.text())
        if not fov_px or fov_px <= 0:
            raise ValueError("Field of view in pixels must be a positive number.")
        distance_px = self._calcDistancePx(point1, point2)
        return distance_px / fov_px * fov_um

    def _calcDistancePx(self, point1: QPointF, point2: QPointF) -> float:
        """Calculate distance between two points in pixels."""
        return math.hypot(point1.x() - point2.x(), point1.y() - point2.y())

    def _setTotalDistance(self, distance: float = 0):
        distance = max(0, distance)
        self.totalDistance = distance
        self.mainWindow.lineEditTotalDistance.setText(f"{distance:.2f}")

    def _setlineEditFovPxText(self, distance: float = 0):
        self.mainWindow.lineEditFovPx.setText(f"{distance:.2f}")

    def _drawFovCircle(self, x: int, y: int, diameter: float):
        self._removeFovCircle()

        circle = self.scene.addEllipse(
            x - diameter / 2,
            y - diameter / 2,
            diameter,
            diameter,
            # Use the same line color and height as the lines
            QPen(self.lineColor, self.lineHeight),
        )
        self.fovCircle = circle

    def _tryAutoSetZoomFromFileName(self, filename: str):
        zoom = extract_zoom_from_filename(filename)
        if zoom:
            index = self.mainWindow.comboBoxDeviceZoom.findText(zoom)
            if index != -1:
                self.mainWindow.comboBoxDeviceZoom.setCurrentIndex(index)

    def _removeFovCircle(self):
        try:
            self.scene.removeItem(self.fovCircle)
        except Exception:
            pass
        finally:
            self.fovCircle = None
