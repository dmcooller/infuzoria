# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'design.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLayout,
    QLineEdit, QMainWindow, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QStatusBar,
    QToolButton, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1017, 696)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.mainLayout = QHBoxLayout()
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.graphicsViewPlaceholder = QWidget(self.centralwidget)
        self.graphicsViewPlaceholder.setObjectName(u"graphicsViewPlaceholder")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsViewPlaceholder.sizePolicy().hasHeightForWidth())
        self.graphicsViewPlaceholder.setSizePolicy(sizePolicy)
        self.graphicsViewPlaceholder.setCursor(QCursor(Qt.CrossCursor))

        self.mainLayout.addWidget(self.graphicsViewPlaceholder)

        self.line = QFrame(self.centralwidget)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.mainLayout.addWidget(self.line)

        self.rightSidebarLayout = QGridLayout()
        self.rightSidebarLayout.setObjectName(u"rightSidebarLayout")
        self.rightSidebarLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.rightSidebarLayout.setVerticalSpacing(6)
        self.rightSidebarLayout.setContentsMargins(0, 10, 10, 10)
        self.line_3 = QFrame(self.centralwidget)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.rightSidebarLayout.addWidget(self.line_3, 9, 0, 1, 3)

        self.pBtnChgPointColor = QPushButton(self.centralwidget)
        self.pBtnChgPointColor.setObjectName(u"pBtnChgPointColor")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.pBtnChgPointColor.sizePolicy().hasHeightForWidth())
        self.pBtnChgPointColor.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(11)
        self.pBtnChgPointColor.setFont(font)

        self.rightSidebarLayout.addWidget(self.pBtnChgPointColor, 2, 1, 1, 2)

        self.pBtnChgLineColor = QPushButton(self.centralwidget)
        self.pBtnChgLineColor.setObjectName(u"pBtnChgLineColor")
        sizePolicy1.setHeightForWidth(self.pBtnChgLineColor.sizePolicy().hasHeightForWidth())
        self.pBtnChgLineColor.setSizePolicy(sizePolicy1)
        self.pBtnChgLineColor.setFont(font)

        self.rightSidebarLayout.addWidget(self.pBtnChgLineColor, 2, 0, 1, 1, Qt.AlignVCenter)

        self.checkBoxSaveDistance = QCheckBox(self.centralwidget)
        self.checkBoxSaveDistance.setObjectName(u"checkBoxSaveDistance")
        self.checkBoxSaveDistance.setFont(font)

        self.rightSidebarLayout.addWidget(self.checkBoxSaveDistance, 23, 0, 1, 3)

        self.sBoxTextSize = QSpinBox(self.centralwidget)
        self.sBoxTextSize.setObjectName(u"sBoxTextSize")
        self.sBoxTextSize.setFont(font)
        self.sBoxTextSize.setMinimum(1)
        self.sBoxTextSize.setValue(25)

        self.rightSidebarLayout.addWidget(self.sBoxTextSize, 8, 0, 1, 1)

        self.pBtnChgTextColor = QPushButton(self.centralwidget)
        self.pBtnChgTextColor.setObjectName(u"pBtnChgTextColor")
        sizePolicy1.setHeightForWidth(self.pBtnChgTextColor.sizePolicy().hasHeightForWidth())
        self.pBtnChgTextColor.setSizePolicy(sizePolicy1)
        self.pBtnChgTextColor.setFont(font)

        self.rightSidebarLayout.addWidget(self.pBtnChgTextColor, 7, 1, 2, 2)

        self.line_4 = QFrame(self.centralwidget)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)

        self.rightSidebarLayout.addWidget(self.line_4, 21, 0, 1, 3)

        self.line_5 = QFrame(self.centralwidget)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)

        self.rightSidebarLayout.addWidget(self.line_5, 12, 0, 1, 3)

        self.sBoxLineHeight = QSpinBox(self.centralwidget)
        self.sBoxLineHeight.setObjectName(u"sBoxLineHeight")
        self.sBoxLineHeight.setFont(font)

        self.rightSidebarLayout.addWidget(self.sBoxLineHeight, 5, 0, 1, 1)

        self.checkBoxAutoFovPx = QCheckBox(self.centralwidget)
        self.checkBoxAutoFovPx.setObjectName(u"checkBoxAutoFovPx")
        self.checkBoxAutoFovPx.setFont(font)

        self.rightSidebarLayout.addWidget(self.checkBoxAutoFovPx, 11, 0, 1, 3)

        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setFont(font)

        self.rightSidebarLayout.addWidget(self.label_4, 4, 1, 1, 2)

        self.line_2 = QFrame(self.centralwidget)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.HLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.rightSidebarLayout.addWidget(self.line_2, 1, 0, 1, 3)

        self.label_6 = QLabel(self.centralwidget)
        self.label_6.setObjectName(u"label_6")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy3)
        font1 = QFont()
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_6.setFont(font1)

        self.rightSidebarLayout.addWidget(self.label_6, 10, 0, 1, 1)

        self.checkBoxSaveLines = QCheckBox(self.centralwidget)
        self.checkBoxSaveLines.setObjectName(u"checkBoxSaveLines")
        self.checkBoxSaveLines.setFont(font)

        self.rightSidebarLayout.addWidget(self.checkBoxSaveLines, 22, 1, 1, 2)

        self.lineEditTotalDistance = QLineEdit(self.centralwidget)
        self.lineEditTotalDistance.setObjectName(u"lineEditTotalDistance")
        self.lineEditTotalDistance.setEnabled(True)
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.lineEditTotalDistance.sizePolicy().hasHeightForWidth())
        self.lineEditTotalDistance.setSizePolicy(sizePolicy4)
        self.lineEditTotalDistance.setMinimumSize(QSize(0, 21))
        self.lineEditTotalDistance.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setPointSize(12)
        self.lineEditTotalDistance.setFont(font2)
        self.lineEditTotalDistance.setReadOnly(True)

        self.rightSidebarLayout.addWidget(self.lineEditTotalDistance, 20, 1, 1, 2)

        self.label_3 = QLabel(self.centralwidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy2.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy2)
        self.label_3.setFont(font)

        self.rightSidebarLayout.addWidget(self.label_3, 4, 0, 1, 1, Qt.AlignBottom)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.rightSidebarLayout.addItem(self.verticalSpacer, 24, 0, 1, 3)

        self.pBtnLoadImg = QPushButton(self.centralwidget)
        self.pBtnLoadImg.setObjectName(u"pBtnLoadImg")
        sizePolicy1.setHeightForWidth(self.pBtnLoadImg.sizePolicy().hasHeightForWidth())
        self.pBtnLoadImg.setSizePolicy(sizePolicy1)
        self.pBtnLoadImg.setMinimumSize(QSize(98, 28))
        self.pBtnLoadImg.setFont(font)

        self.rightSidebarLayout.addWidget(self.pBtnLoadImg, 0, 0, 1, 1, Qt.AlignVCenter)

        self.label_7 = QLabel(self.centralwidget)
        self.label_7.setObjectName(u"label_7")
        sizePolicy2.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy2)
        self.label_7.setFont(font)

        self.rightSidebarLayout.addWidget(self.label_7, 6, 0, 1, 1)

        self.pBtnSaveImg = QPushButton(self.centralwidget)
        self.pBtnSaveImg.setObjectName(u"pBtnSaveImg")
        sizePolicy1.setHeightForWidth(self.pBtnSaveImg.sizePolicy().hasHeightForWidth())
        self.pBtnSaveImg.setSizePolicy(sizePolicy1)
        self.pBtnSaveImg.setMinimumSize(QSize(98, 28))
        self.pBtnSaveImg.setFont(font)

        self.rightSidebarLayout.addWidget(self.pBtnSaveImg, 0, 1, 1, 2)

        self.label_8 = QLabel(self.centralwidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy3.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy3)
        self.label_8.setFont(font1)

        self.rightSidebarLayout.addWidget(self.label_8, 13, 0, 1, 2)

        self.toolBtnSetFovPx = QToolButton(self.centralwidget)
        self.toolBtnSetFovPx.setObjectName(u"toolBtnSetFovPx")

        self.rightSidebarLayout.addWidget(self.toolBtnSetFovPx, 10, 2, 1, 1)

        self.line_10 = QFrame(self.centralwidget)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.HLine)
        self.line_10.setFrameShadow(QFrame.Sunken)

        self.rightSidebarLayout.addWidget(self.line_10, 19, 0, 1, 3)

        self.checkBoxSavePoints = QCheckBox(self.centralwidget)
        self.checkBoxSavePoints.setObjectName(u"checkBoxSavePoints")
        self.checkBoxSavePoints.setFont(font)

        self.rightSidebarLayout.addWidget(self.checkBoxSavePoints, 22, 0, 1, 1)

        self.lineEditFovPx = QLineEdit(self.centralwidget)
        self.lineEditFovPx.setObjectName(u"lineEditFovPx")
        self.lineEditFovPx.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.lineEditFovPx.sizePolicy().hasHeightForWidth())
        self.lineEditFovPx.setSizePolicy(sizePolicy4)
        self.lineEditFovPx.setMinimumSize(QSize(0, 21))
        self.lineEditFovPx.setMaximumSize(QSize(16777215, 16777215))
        self.lineEditFovPx.setFont(font2)
        self.lineEditFovPx.setReadOnly(False)

        self.rightSidebarLayout.addWidget(self.lineEditFovPx, 10, 1, 1, 1)

        self.comboBoxDeviceModel = QComboBox(self.centralwidget)
        self.comboBoxDeviceModel.setObjectName(u"comboBoxDeviceModel")
        self.comboBoxDeviceModel.setFont(font2)

        self.rightSidebarLayout.addWidget(self.comboBoxDeviceModel, 14, 0, 1, 3)

        self.lineEditFovUm = QLineEdit(self.centralwidget)
        self.lineEditFovUm.setObjectName(u"lineEditFovUm")
        self.lineEditFovUm.setEnabled(True)
        sizePolicy4.setHeightForWidth(self.lineEditFovUm.sizePolicy().hasHeightForWidth())
        self.lineEditFovUm.setSizePolicy(sizePolicy4)
        self.lineEditFovUm.setMinimumSize(QSize(0, 21))
        self.lineEditFovUm.setMaximumSize(QSize(16777215, 16777215))
        self.lineEditFovUm.setFont(font2)
        self.lineEditFovUm.setReadOnly(False)

        self.rightSidebarLayout.addWidget(self.lineEditFovUm, 18, 1, 1, 2)

        self.label_5 = QLabel(self.centralwidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy3.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy3)
        self.label_5.setFont(font1)

        self.rightSidebarLayout.addWidget(self.label_5, 18, 0, 1, 1)

        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy3.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy3)
        self.label_2.setFont(font1)

        self.rightSidebarLayout.addWidget(self.label_2, 20, 0, 1, 1)

        self.sBoxPointSize = QSpinBox(self.centralwidget)
        self.sBoxPointSize.setObjectName(u"sBoxPointSize")
        self.sBoxPointSize.setFont(font)

        self.rightSidebarLayout.addWidget(self.sBoxPointSize, 5, 1, 1, 2)

        self.label_16 = QLabel(self.centralwidget)
        self.label_16.setObjectName(u"label_16")
        sizePolicy3.setHeightForWidth(self.label_16.sizePolicy().hasHeightForWidth())
        self.label_16.setSizePolicy(sizePolicy3)
        self.label_16.setFont(font1)

        self.rightSidebarLayout.addWidget(self.label_16, 15, 0, 1, 1)

        self.comboBoxDeviceZoom = QComboBox(self.centralwidget)
        self.comboBoxDeviceZoom.setObjectName(u"comboBoxDeviceZoom")
        self.comboBoxDeviceZoom.setFont(font2)

        self.rightSidebarLayout.addWidget(self.comboBoxDeviceZoom, 15, 1, 1, 2)


        self.mainLayout.addLayout(self.rightSidebarLayout)


        self.horizontalLayout_3.addLayout(self.mainLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1017, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.pBtnLoadImg, self.pBtnSaveImg)
        QWidget.setTabOrder(self.pBtnSaveImg, self.pBtnChgLineColor)
        QWidget.setTabOrder(self.pBtnChgLineColor, self.pBtnChgPointColor)
        QWidget.setTabOrder(self.pBtnChgPointColor, self.sBoxLineHeight)
        QWidget.setTabOrder(self.sBoxLineHeight, self.sBoxPointSize)
        QWidget.setTabOrder(self.sBoxPointSize, self.lineEditTotalDistance)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Infuzoria", None))
        self.pBtnChgPointColor.setText(QCoreApplication.translate("MainWindow", u"Point color", None))
        self.pBtnChgLineColor.setText(QCoreApplication.translate("MainWindow", u"Line color", None))
        self.checkBoxSaveDistance.setText(QCoreApplication.translate("MainWindow", u"Save Distance", None))
        self.pBtnChgTextColor.setText(QCoreApplication.translate("MainWindow", u"Text color", None))
        self.checkBoxAutoFovPx.setText(QCoreApplication.translate("MainWindow", u"Autodetect FOV (px)", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Point size:", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"FOV (px):", None))
        self.checkBoxSaveLines.setText(QCoreApplication.translate("MainWindow", u"Save Lines", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Line height:", None))
        self.pBtnLoadImg.setText(QCoreApplication.translate("MainWindow", u"Load image", None))
#if QT_CONFIG(shortcut)
        self.pBtnLoadImg.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Text Size:", None))
        self.pBtnSaveImg.setText(QCoreApplication.translate("MainWindow", u"Save image", None))
#if QT_CONFIG(shortcut)
        self.pBtnSaveImg.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Device:", None))
#if QT_CONFIG(tooltip)
        self.toolBtnSetFovPx.setToolTip(QCoreApplication.translate("MainWindow", u"Set FOV in pixels manually", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.toolBtnSetFovPx.setStatusTip("")
#endif // QT_CONFIG(statustip)
        self.toolBtnSetFovPx.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.checkBoxSavePoints.setText(QCoreApplication.translate("MainWindow", u"Save Points", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"FOV (\u03bcm):", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Length (\u03bcm):", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Zoom:", None))
    # retranslateUi

