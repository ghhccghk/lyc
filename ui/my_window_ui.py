from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale,QPointF, QPropertyAnimation, QObject, Property,QAbstractAnimation,Signal,QTimer,QRegularExpression,QRect,QSize
from PySide6.QtGui import QFontDatabase,QPainter,QFont,QPainterPath,QFontMetrics,QPen,QColor,QIcon,QRegularExpressionValidator,QPixmap,QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout,QLabel,QLineEdit,QFrame,QSpacerItem, QSizePolicy
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QToolButton, QVBoxLayout, QPushButton

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, HyperlinkCard,InfoBar,
                            ComboBoxSettingCard, ScrollArea, ExpandLayout, InfoBarPosition,SettingCard)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import AcrylicWindow
from qfluentwidgets import PushButton,ComboBox,VBoxLayout, setTheme, Theme, setThemeColor, setFont, ExpandLayout,SpinBox,SwitchButton, Theme, FluentIcon,ToolButton,ScrollArea,CheckBox
from qfluentwidgets.multimedia import MediaPlayBarButton
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase
from qfluentwidgets.components.widgets.label import CaptionLabel
from typing import Union
from qfluentwidgets.components.widgets.switch_button import SwitchButton, IndicatorPosition
from qfluentwidgets.common.icon import FluentIconBase
from qfluentwidgets.common.config import qconfig, isDarkTheme, ConfigItem, OptionsConfigItem

from module.widget import hotWidget, ComboBoxCard,SpinBoxCard,PushCard,SwitchCard,LyricLabel

import qfluentwidgets
import os

from module import allset

basedir = os.path.dirname(__file__)

ismoving = True
allset.ismoving = ismoving

class MyWindowUI(ScrollArea):
    def __init__(self, sizeHintdb: tuple[int, int], parent=None):
        super().__init__(parent=parent)
        self.setObjectName("MyWindowUI")
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.label = QtWidgets.QLabel(self.tr("初始文字"), self)######显示歌词
        self.label.move(50, 100)
#########界面字体控制
        afont = QFont()
        afont.setFamily("黑体")  # 字体
        afont.setPointSize(11)  # 字体大小
        afont.setBold(True)  # 粗体

        ###文本

        ######针对会变动的文字修改保证修改语言后不会文字叠一起
        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(50, 65, 851, 23))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.label8 = QtWidgets.QLabel(self.tr("Tips：如遇歌词显示问题，可提交 Issue,"), self)
        self.label8.move(25, 440)
        self.label8.setFont(afont)
        ##修改字体

        self.label9 = QtWidgets.QLabel(self.tr("歌曲id："), self)
        self.label9.move(299, 440)
        self.label9.setFont(afont)
        ##修改字体

        self.label3 = QtWidgets.QLabel(self.tr("歌词未显示，"), self)
        self.label3.move(125, 60)
        self.label3.setFont(afont)
        ##修改字体

        self.horizontalLayout.addWidget(self.label3)
        self.horizontalLayout.addWidget(self.label8)
        self.horizontalLayout.addWidget(self.label9)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

############################在顶部无需移动
        self.label4 = QtWidgets.QLabel(self.tr("设置"), self)
        self.label4.move(50, 20)
#############################在顶部无需移动

        self.hot = SettingCardGroup(self.tr('当前歌曲网易云热评'), self.scrollWidget)
        self.testcard = hotWidget()
        self.testcard.setMaximumHeight(300)


        self.setting = SettingCardGroup(self.tr('歌词效果设置'), self.scrollWidget)

        self.fontCard = ComboBoxCard(
            FIF.FONT,
            self.tr('字体设置'),
            self.tr('设置歌词的字体'),
            self.setting
        )
        # 获取系统中所有的字体
        fonts = QFontDatabase.families()
        # 将字体添加到下拉列表中
        for font in fonts:
            self.fontCard.addItem(font)
            self.fontCard.setCurrentIndex(0)
        #


        self.boldCard = SwitchCard(
            QIcon(os.path.join(basedir, '../res/icons/粗·.svg')),
            self.tr('字体加粗'),
            self.tr('设置歌词是否加粗'),
            self.setting,
            OnText = self.tr("已加"),
            OffText = self.tr("未加")
        )
        self.boldCard.setChecked(True)


        self.switchunderlineCard = SwitchCard(
            QIcon(os.path.join(basedir, '../res/icons/下划.svg')),
            self.tr('字体加下划线'),
            self.tr('设置歌词是否加下划线'),
            self.setting,
            OnText = self.tr("已加"),
            OffText = self.tr("未加")
        )
        self.switchunderlineCard.setChecked(False)

        self.setcolorCard = PushCard(
            self.tr('设置字体颜色'),
            FIF.PALETTE,
            self.tr('字体颜色'),
            self.tr('修改歌词字体颜色'),
            self.setting
        )


        self.fontsizeCard = SpinBoxCard(
            FIF.FONT_SIZE,
            self.tr('字体大小'),
            self.tr('设置歌词字体的大小'),
            self.setting
        )
        self.fontsizeCard.setRange(1,99)
        self.fontsizeCard.setSuffix("  px")
        self.fontsizeCard.setValue(20)
        self.fontsizeCard.setSingleStep(1)
        self.fontsizeCard.setWrapping(True)


        self.showlyctopCard = SwitchCard(
            FIF.UP,
            self.tr('歌词置顶'),
            self.tr('设置歌词是否置顶'),
            # None,
            self.setting,
            # Checked = True,
            OnText = self.tr("置顶"),
            OffText = self.tr("未置顶")
        )

        self.moveCard = SwitchCard(
            FIF.PIN,
            self.tr('移动开关'),
            self.tr('设置歌词是能移动'),
            # None,
            self.setting,
            # Checked = True,
            OnText = self.tr("可以"),
            OffText = self.tr("不行")
        )
        self.moveCard.checkedChanged.connect(self.ismov)
        self.moveCard.setChecked(True)


        self.showlycCard = PushCard(
            self.tr('显示歌词'),
            FIF.VIEW,
            self.tr('显示歌词'),
            self.tr('设置歌词是否显示在独立窗口'),
            self.setting
        )

        self.__initWidget()
        self.__setQss()


    def __initWidget(self):
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 240, 0, 30)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # # initialize style sheet
        self.__setQss()

        # initialize layout
        self.__initLayout()

    def __initLayout(self):
        self.hot.addSettingCard(self.testcard)
        self.setting.addSettingCard(self.fontCard)
        self.setting.addSettingCard(self.setcolorCard)
        self.setting.addSettingCard(self.boldCard)
        self.setting.addSettingCard(self.switchunderlineCard)
        self.setting.addSettingCard(self.fontsizeCard)
        self.setting.addSettingCard(self.showlyctopCard)
        self.setting.addSettingCard(self.moveCard)
        self.setting.addSettingCard(self.showlycCard)


        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.hot)
        self.expandLayout.addWidget(self.setting)



    def __setQss(self):
        """ set style sheet """
        self.scrollWidget.setObjectName('scrollWidget')
        self.label4.setObjectName('settingLabel')

        theme = 'light' #if isDarkTheme() else 'light'
        with open(os.path.join(basedir, '../res/icons/system/qss/', theme, 'setting_interface.qss'), encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def ismov(self, checked):
        global ismoving
        if checked:
            ismoving = True
            allset.ismoving = ismoving
        else:
            ismoving = False
            allset.ismoving = ismoving

    def heightForWidth(self, width):
        self.setWordWrap(True)  # 设置 label 可以换行
        height = self.fontMetrics().boundingRect(0, 0, width, 0, self.wordWrap()).height()
        return height


