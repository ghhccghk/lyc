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
import os

from module.widget import ImageWidget

basedir = os.path.dirname(__file__)


class aboueInterface(ScrollArea):
    def __init__(self, sizeHintdb: tuple[int, int], parent=None):
        super().__init__(parent=parent)
        # setting label
        self.setObjectName("aboueInterface")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        # setting label
        self.settingLabel = QLabel(self.tr("关于"), self)

        # self.afont = QFont()
        # self.afont.setFamily("黑体")  # 字体
        # self.afont.setPointSize(14)  # 字体大小
        # self.afont.setBold(True)  # 粗体

        # self.about = QtWidgets.QLabel('关于',self)
        # self.about.setFont(afont)
        # self.about.move(45, 70)
        #
        # self.aboutname = QtWidgets.QLabel('应用程序名字',self)
        # self.aboutname.setFont(afont)
        # self.aboutname.move(190, 110)
        self.app_name = SettingCardGroup(self.tr('应用名称和介绍'), self.scrollWidget)
        # About ==============================================================================
        self.aboutGroup = SettingCardGroup(self.tr('外部链接'), self.scrollWidget)
        self.aboutCard = HyperlinkCard(
            "https://github.com/ghhccghk/lyc",
            self.tr('打开 GitHub 界面'),
            QIcon(os.path.join(basedir, '../res/icons/system/home.svg')),
            self.tr('项目网站'),
            self.tr('在我们的GitHub页面上检查更新、并了解更多关于项目的信息'),
            self.aboutGroup
        )
        self.helpCard = HyperlinkCard(
            "https://github.com/ghhccghk/lyc/issues",
            self.tr('打开问题页面'),
            FIF.HELP,
            self.tr('帮助 & 问题'),
            self.tr('在我们的GitHub问题页面上发布您的问题.'),
            self.aboutGroup
        )
        app_name = "名字还没想好"
        app_description = "基于PySide6开发，采用Fluent-Widgets作为UI界面,目前只支持显示来自yesplaymusic的歌词。"
        max_height = 300

        self.testcard = ImageWidget(os.path.join(basedir,"../res/icons/SystemPanel.png"), app_name, app_description, max_height)
        self.testcard.adjustSize()


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
        self.app_name.addSettingCard(self.testcard)
        self.aboutGroup.addSettingCard(self.aboutCard)
        self.aboutGroup.addSettingCard(self.helpCard)


        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.app_name)
        self.expandLayout.addWidget(self.aboutGroup)


    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')

        theme = 'light' #if isDarkTheme() else 'light'
        with open(os.path.join(basedir, '../res/icons/system/qss/', theme, 'setting_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())
