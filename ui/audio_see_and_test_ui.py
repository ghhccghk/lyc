from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale,QPointF, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame, QSpacerItem,QSizePolicy
from PySide6.QtWidgets import QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout, QLabel


from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, HyperlinkCard,InfoBar,
                            ComboBoxSettingCard, ScrollArea, ExpandLayout, InfoBarPosition)
from qframelesswindow import AcrylicWindow
from qfluentwidgets import ScrollArea
from qfluentwidgets import FluentIcon as FIF

# from b import PlotWidget
import os

basedir = os.path.dirname(__file__)


class audioInterface(ScrollArea):
    def __init__(self, sizeHintdb: tuple[int, int], parent=None):
        super().__init__(parent=parent)
        # setting label
        self.setObjectName("audioInterface")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        # setting label
        self.settingLabel = QLabel(self.tr("音频可视化和控制郊狼"), self)

        self.name = SettingCardGroup(self.tr('显示实时频谱'), self.scrollWidget)
        # self.testcard =PlotWidget()

        self.__initWidget()

    def __initWidget(self):
        #self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # self.setViewportMargins(0, 95, 0, 20)
        self.setViewportMargins(0, 75, 0, 20)
        self.setWidget(self.scrollWidget)
        #self.scrollWidget.resize(1000, 800)
        self.setWidgetResizable(True)

        # # initialize style sheet
        self.__setQss()

        # initialize layout
        self.__initLayout()
        #self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(50, 20)
        # self.settingLabel.setFont(self.afont)
        # self.name.addSettingCard(self.testcard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.name)


    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'light' #if isDarkTheme() else 'light'
        with open(os.path.join(basedir, '../res/icons/system/qss/', theme, 'setting_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())
