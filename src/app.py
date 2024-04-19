import os
import sys

from PySide6 import QtWidgets
from PySide6.QtGui import QColor, QDoubleValidator, QScreen
from PySide6.QtWidgets import QApplication, QColorDialog, QFileDialog, QMessageBox

from devices import Devices
from image_viewer.image_viewer import ImageViewer
from settings import settings
from ui.design import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.settings = settings

        self.setGeometry(0, 0, self.settings.g_window_width, self.settings.g_window_height)

        center = QScreen.availableGeometry(QApplication.primaryScreen()).center()
        geo = self.frameGeometry()
        geo.moveCenter(center)
        self.move(geo.topLeft())

        self.imageViewer = ImageViewer(self)
        self.setupImageViewer()

        self.devices = self.loadDevices()

        self.pBtnSaveImg.clicked.connect(self.saveImage)
        self.pBtnLoadImg.clicked.connect(self.loadImage)
        self.pBtnChgLineColor.clicked.connect(self.changeLineColor)
        self.pBtnChgPointColor.clicked.connect(self.changePointColor)
        self.pBtnChgTextColor.clicked.connect(self.changeTextColor)
        self.sBoxLineHeight.valueChanged.connect(self.changeLineHeight)
        self.sBoxPointSize.valueChanged.connect(self.changePointSize)
        self.sBoxTextSize.valueChanged.connect(self.changeTextSize)
        self.toolBtnSetFovPx.setCheckable(True)
        self.toolBtnSetFovPx.clicked.connect(lambda: self.imageViewer.setPovMode(self.toolBtnSetFovPx.isChecked()))
        if self.devices:
            self.comboBoxDeviceModel.currentIndexChanged.connect(self.deviceModelChanged)
            self.comboBoxDeviceZoom.currentIndexChanged.connect(self.devices.updateFovUmValue)

        doubleValidator = QDoubleValidator(0.0, float("inf"), 2)
        self.lineEditFovPx.setValidator(doubleValidator)
        self.lineEditFovUm.setValidator(doubleValidator)

        self.setUiValues()

    def setupImageViewer(self):
        # Find the placeholder widget to add the ImageViewer to
        placeholder = self.findChild(QtWidgets.QWidget, "graphicsViewPlaceholder")
        layout = QtWidgets.QVBoxLayout(placeholder)
        layout.addWidget(self.imageViewer)

    def saveImage(self):
        savePath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", os.getenv("HOME"), "JPEG Files (*.jpg);;PNG Files (*.png)"
        )
        if savePath:
            self.imageViewer.saveImageWithAnnotations(savePath)

    def loadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(
            self, "Open Image", self.settings.g_last_path, "Images (*.png *.xpm *.jpg)"
        )
        if filePath:
            self.imageViewer.setNewImage(filePath)
            self.settings.g_last_path = os.path.dirname(filePath)

    def changeLineColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color_hex = color.name()
            self.imageViewer.lineColor = QColor(color_hex)
            self.settings.iw_line_color = color_hex

    def changePointColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color_hex = color.name()
            self.imageViewer.pointColor = QColor(color_hex)
            self.settings.iw_point_color = color_hex

    def changeTextColor(self):
        color = QColorDialog.getColor()
        if color.isValid():
            color_hex = color.name()
            self.imageViewer.textColor = QColor(color_hex)
            self.settings.iw_text_color = color_hex

    def changeTextSize(self, value):
        self.imageViewer.textSize = value
        self.settings.iw_text_size = value

    def changeLineHeight(self, value):
        self.imageViewer.lineHeight = value
        self.settings.iw_line_height = value

    def changePointSize(self, value):
        self.imageViewer.pointSize = value
        self.settings.iw_point_size = value

    def closeEvent(self, event):
        self.updateWindowSettings()
        self.settings.save_all()
        event.accept()

    def updateWindowSettings(self):
        self.settings.g_window_height = self.height()
        self.settings.g_window_width = self.width()

    def setUiValues(self):
        self.sBoxLineHeight.setValue(self.settings.iw_line_height)
        self.sBoxPointSize.setValue(self.settings.iw_point_size)
        self.sBoxTextSize.setValue(self.settings.iw_text_size)
        self.imageViewer.lineColor = QColor(self.settings.iw_line_color)
        self.imageViewer.pointColor = QColor(self.settings.iw_point_color)
        self.imageViewer.textColor = QColor(self.settings.iw_text_color)
        self.checkBoxSavePoints.setChecked(self.settings.iw_save_points)
        self.checkBoxSaveLines.setChecked(self.settings.iw_save_lines)
        self.checkBoxSaveDistance.setChecked(self.settings.iw_save_distance)
        self.checkBoxAutoFovPx.setChecked(self.settings.iw_auto_diameter)
        self.checkBoxAutoCrop.setChecked(self.settings.iw_auto_crop)

    def loadDevices(self) -> Devices | None:
        lastDevice = self.settings.devices_last_device
        try:
            return Devices(self, lastDevice=lastDevice)
        except FileNotFoundError:
            QMessageBox.warning(
                self, "Error", "Failed to load file devices.ini. You can specify FOV (μm) manually.", QMessageBox.Ok
            )
            return None

    def deviceModelChanged(self):
        self.devices.updateZoomOptions()
        self.settings.devices_last_device = self.comboBoxDeviceModel.currentText()


app = QtWidgets.QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()
