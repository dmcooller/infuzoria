import os
from configparser import ConfigParser

from ui.design import Ui_MainWindow


class Devices:
    def __init__(self, mainWindow: Ui_MainWindow, configPath: str = "devices.ini", lastDevice: str = ""):
        self.mainWindow = mainWindow
        self.config = None
        self.readConfig(configPath)
        self.populateDeviceModelComboBox(lastDevice)
        self.updateZoomOptions()
        self.updateFovUmValue()

    def readConfig(self, configPath):
        if not os.path.exists(configPath):
            raise FileNotFoundError(f"Config file {configPath} not found.")
        self.config = ConfigParser()
        self.config.read(configPath)

    def populateDeviceModelComboBox(self, lastDevice: str = ""):
        if not self.config:
            return
        for device in self.config.sections():
            self.mainWindow.comboBoxDeviceModel.addItem(device)
        if lastDevice:
            index = self.mainWindow.comboBoxDeviceModel.findText(lastDevice)
            if index != -1:
                self.mainWindow.comboBoxDeviceModel.setCurrentIndex(index)

    def updateZoomOptions(self):
        if not self.config:
            return
        self.mainWindow.comboBoxDeviceZoom.clear()
        currentDevice = self.mainWindow.comboBoxDeviceModel.currentText()
        if currentDevice:
            for key, value in self.config[currentDevice].items():
                self.mainWindow.comboBoxDeviceZoom.addItem(key.replace("zoom_", ""), value)

    def updateFovUmValue(self):
        currentZoom = self.mainWindow.comboBoxDeviceZoom.currentData()
        if currentZoom is not None:
            self.mainWindow.lineEditFovUm.setText(currentZoom)
