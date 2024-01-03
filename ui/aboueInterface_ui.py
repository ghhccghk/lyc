from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale,QPointF, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame


from qframelesswindow import AcrylicWindow
from qfluentwidgets import PushButton,ComboBox,VBoxLayout, setTheme, Theme, setThemeColor, setFont, ExpandLayout,SpinBox,SwitchButton, Theme, FluentIcon,ToolButton,ScrollArea,CheckBox
from qfluentwidgets.multimedia import MediaPlayBarButton
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase
from qfluentwidgets.components.widgets.label import CaptionLabel

import os

basedir = os.path.dirname(__file__)


class aboueInterface(ScrollArea):
    def __init__(self, sizeHintdb: tuple[int, int], parent=None):
        super().__init__(parent=parent)
        # setting label
        self.setObjectName("aboueInterface")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        afont = QFont()
        afont.setFamily("黑体")  # 字体
        afont.setPointSize(14)  # 字体大小
        afont.setBold(True)  # 粗体

        self.about = QtWidgets.QLabel('关于',self)
        self.about.setFont(afont)
        self.about.move(45, 70)

        self.aboutname = QtWidgets.QLabel('应用程序名字',self)
        self.aboutname.setFont(afont)
        self.aboutname.move(190, 110)

