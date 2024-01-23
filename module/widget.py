from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QLocale, QPointF, QPropertyAnimation, QObject, Property, QAbstractAnimation, Signal, QTimer, QRegularExpression, QRect, QSize
from PySide6.QtGui import QFontDatabase, QPainter, QFont, QPainterPath, QFontMetrics, QPen, QColor, QIcon, QRegularExpressionValidator, QPixmap, QImage
from PySide6.QtWidgets import QApplication, QWidget, QComboBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFrame, QSpacerItem, QSizePolicy, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,QPushButton

from qfluentwidgets import SwitchSettingCard, HyperlinkCard, InfoBar, ComboBoxSettingCard, ScrollArea, ExpandLayout, InfoBarPosition, SettingCard
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import AcrylicWindow
from qfluentwidgets import PushButton, ComboBox, VBoxLayout, setTheme, Theme, setThemeColor, SpinBox, SwitchButton, FluentIcon, ToolButton, CheckBox
from qfluentwidgets.multimedia import MediaPlayBarButton
from qfluentwidgets.multimedia.media_play_bar import MediaPlayBarBase
from qfluentwidgets.components.widgets.label import CaptionLabel
from typing import Union, List
from qfluentwidgets.components.widgets.switch_button import SwitchButton, IndicatorPosition
from qfluentwidgets.common.icon import FluentIconBase
from qfluentwidgets.common.config import qconfig, isDarkTheme, ConfigItem, OptionsConfigItem
from qfluentwidgets.common.style_sheet import FluentStyleSheet
from qfluentwidgets.common.font import setFont
import os


#######全局变量设置
from module import allset
basedir = os.path.dirname(__file__)
x:int = 520

class ImageWidget(QWidget):
    def __init__(self, image_path, app_name, app_description, max_height, parent=None):
        super(ImageWidget, self).__init__(parent)

        # 保存期望的最大高度
        # self.max_height = max_height

        # 创建一个 QLabel 用于显示图片
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMaximumSize(max_height, max_height)


        # 创建 QLabel 用于显示应用程序名称和简介
        self.name_label = QLabel(app_name, self)
        self.description_label = QLabel(app_description, self)

        # 设置字体样式
        name_font = QFont()
        name_font.setPointSize(20)
        name_font.setBold(True)
        self.name_label.setFont(name_font)


        description_font = QFont()
        description_font.setPointSize(10)
        self.description_label.setFont(description_font)
        # 设置自动换行
        self.description_label.setWordWrap(True)

        # 设置布局
        layout = QHBoxLayout(self)

        # 添加图片左侧的水平伸缩
        layout.addStretch()

        # 创建垂直布局用于放置名称和简介以及上下伸缩
        info_layout = QVBoxLayout()
        info_layout.addStretch()  # 添加顶部垂直伸缩
        info_layout.addWidget(self.name_label)
        info_layout.addStretch()
        info_layout.addWidget(self.description_label)
        info_layout.addStretch()  # 添加底部垂直伸缩
        layout.addWidget(self.image_label)
        layout.addSpacing(75)
        layout.addLayout(info_layout)
        # 添加图片右侧的水平伸缩
        layout.addStretch()

        # 加载并显示图片
        self.load_image(image_path)

    def load_image(self, image_path):
        # 通过 QPixmap 加载图片
        pixmap = QPixmap(image_path)

        # 在 QLabel 中显示图片
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

    # def resizeEvent(self, event):
    #     # 在小部件大小发生变化时调用此方法
    #     super(ImageWidget, self).resizeEvent(event)
    #
    #     # 获取新的小部件大小
    #     new_size = event.size()
    #
    #     # 限制小部件的高度
    #     new_height = min(self.max_height, new_size.height())
    #     new_size.setHeight(new_height)
    #
    #     # 获取当前图片
    #     current_pixmap = self.image_label.pixmap()
    #
    #     if current_pixmap:
    #         # 缩放图片以适应新的小部件大小
    #         scaled_pixmap = current_pixmap.scaled(new_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    #         self.image_label.setPixmap(scaled_pixmap)


####qfluentwidgets拿过来魔改
class SimpleMediaPlayBar(MediaPlayBarBase):
    """ Standard media play bar """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.timeLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.leftButtonContainer = QWidget()
        self.centerButtonContainer = QWidget()
        self.rightButtonContainer = QWidget()
        self.leftButtonLayout = QHBoxLayout(self.leftButtonContainer)
        self.centerButtonLayout = QHBoxLayout(self.centerButtonContainer)
        self.rightButtonLayout = QHBoxLayout(self.rightButtonContainer)
        self.like = like(self)

        self.skipBackButton = self.like
        self.skipForwardButton = MediaPlayBarButton(QIcon(os.path.join(basedir,"../res/icons/下一首.png")), self)
        self.playButton.deleteLater()
        self.volumeButton.deleteLater()
        self.currentTimeLabel = CaptionLabel('0:00:00', self)
        self.remainTimeLabel = CaptionLabel('0:00:00', self)

        self.__initWidgets()

    def __initWidgets(self):
        self.setFixedHeight(102)
        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(5, 9, 5, 9)
        self.vBoxLayout.addWidget(self.progressSlider, 1, Qt.AlignTop)
        self.play = Play(self)
        self.LoopStatus = LoopStatus(self)
        self.Shuffle = Shuffle(self)

        self.vBoxLayout.addLayout(self.timeLayout)
        self.timeLayout.setContentsMargins(10, 0, 10, 0)
        self.timeLayout.addWidget(self.currentTimeLabel, 0, Qt.AlignLeft)
        self.timeLayout.addWidget(self.remainTimeLabel, 0, Qt.AlignRight)

        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.buttonLayout.setContentsMargins(0, 0, 0, 0)
        self.leftButtonLayout.setContentsMargins(4, 0, 0, 0)
        self.centerButtonLayout.setContentsMargins(0, 0, 0, 0)
        self.rightButtonLayout.setContentsMargins(0, 0, 4, 0)

        # self.leftButtonLayout.addWidget(self.volumeButton, 0, Qt.AlignLeft)
        self.centerButtonLayout.addWidget(self.Shuffle)
        self.centerButtonLayout.addStretch(3)
        self.centerButtonLayout.addWidget(self.like)
        self.centerButtonLayout.addWidget(self.play)
        self.centerButtonLayout.addWidget(self.skipForwardButton)
        self.centerButtonLayout.addStretch(3)
        self.centerButtonLayout.addWidget(self.LoopStatus)

        self.buttonLayout.addWidget(self.leftButtonContainer, 0, Qt.AlignLeft)
        self.buttonLayout.addWidget(self.centerButtonContainer, 0, Qt.AlignHCenter)
        self.buttonLayout.addWidget(self.rightButtonContainer, 0, Qt.AlignRight)



class Play(MediaPlayBarButton):
    """ Play button """

    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(14, 14))
        self.setPlay(False)

    def setPlay(self, isPlay: bool):
        if isPlay:
            self.setIcon(FluentIcon.PAUSE)
            self.setToolTip(self.tr('Pause'))
        else:
            self.setIcon(FluentIcon.PLAY)
            self.setToolTip(self.tr('Play'))


class like(MediaPlayBarButton):
    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(14, 14))
        self.nolike(False)

    def nolike(self, nolike: bool):
        if nolike:
            self.setIcon(QIcon(os.path.join(basedir,"../res/icons/nolike.svg")))
            self.setToolTip(self.tr('不喜欢'))
        else:
            self.setIcon(QIcon(os.path.join(basedir,"../res/icons/上一首.png")))
            self.setToolTip(self.tr('上一首'))


class Shuffle(MediaPlayBarButton):
      # 随机播放
    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(14, 14))
        self.setShuffle(False)

    def setShuffle(self, isShuffle: bool):
        if isShuffle:
            self.setIcon(QIcon(os.path.join(basedir,"../res/icons/随机播放.svg")))
            self.setToolTip(self.tr('随机播放开启'))
        else:
            self.setIcon(QIcon(os.path.join(basedir,"../res/icons/随机播放关.svg")))
            self.setToolTip(self.tr('随机播放关闭'))

class LoopStatus(MediaPlayBarButton):
      # 单曲，列表循环切换
    def _postInit(self):
        super()._postInit()
        self.setIconSize(QSize(14, 14))
        self.setLoopStatus("None")

    def setLoopStatus(self, isLoopStatus: str):
        if isLoopStatus == "None":
            self.setIcon(QIcon(os.path.join(basedir,"../res/icons/不循环.svg")))
            self.setToolTip(self.tr('列表不循环'))
        if isLoopStatus == "Playlist":
            self.setIcon(QIcon(os.path.join(basedir,"../res/icons/列表循环.svg")))
            self.setToolTip(self.tr('列表循环'))
        if isLoopStatus == "Track":
            self.setIcon(QIcon(os.path.join(basedir,"../res/icons/单曲循环.svg")))
            self.setToolTip(self.tr('当前播放循环'))



class SettingCardGroup(QWidget):
    """ Setting card group """

    def __init__(self,card: QWidget,parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = ExpandLayout()

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSpacing(0)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)
        self.cardLayout.setSpacing(2)

        self.vBoxLayout.addWidget(card)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addLayout(self.cardLayout, 1)

        FluentStyleSheet.SETTING_CARD_GROUP.apply(self)


    def addSettingCard(self, card: QWidget):
        """ add setting card to group """
        card.setParent(self)
        self.cardLayout.addWidget(card)
        self.adjustSize()

    def addSettingCards(self, cards: List[QWidget]):
        """ add setting cards to group """
        for card in cards:
            self.addSettingCard(card)

    def adjustSize(self):
        h = self.cardLayout.heightForWidth(self.width()) + 46
        return self.resize(self.width(), h)

####播放界面

class playWidget(QWidget):
    def __init__(self, label3, label4, label_pic, combo_box, button , bas , parent=None):
        super(playWidget, self).__init__(parent)

        # 传入定义的组件
        self.label3 = label3
        self.label4 = label4
        self.label_pic = label_pic
        self.combo_box = combo_box
        self.button = button
        self.bas = bas

        # 设置布局
        layout = QHBoxLayout(self)
        ####设置播放器文字
        setplaytxtlayout = QHBoxLayout()
        setplaytxtlayout.addStretch()
        setplaytxtlayout.addWidget(self.label3)
        setplaytxtlayout.addWidget(self.label4)
        setplaytxtlayout.addStretch()

        ###设置播放器按钮
        setplaygetlayout = QHBoxLayout()
        setplaygetlayout.addSpacing(5)
        setplaygetlayout.addWidget(self.combo_box)
        setplaygetlayout.addSpacing(5)
        setplaygetlayout.addWidget(self.button)
        setplaygetlayout.addSpacing(5)

        ####播放器控件
        setplaylayout = QHBoxLayout()
        setplaylayout.addWidget(self.bas)


        # 添加图片左侧的水平伸缩
        layout.addStretch()

        # 创建垂直布局用于放置名称和简介以及上下伸缩
        info_layout = QVBoxLayout()
        info_layout.addSpacing(55) # 添加顶部垂直伸缩
        info_layout.addLayout(setplaytxtlayout)
        info_layout.addSpacing(10)
        info_layout.addLayout(setplaygetlayout)
        info_layout.addStretch()  # 添加底部垂直伸缩
        info_layout.addLayout(setplaylayout)

        layout.addWidget(self.label_pic)
        layout.addSpacing(30)
        layout.addLayout(info_layout)
        # 添加图片右侧的水平伸缩
        layout.addStretch()


class ComboBoxCard(SettingCard):
    """ Setting card with switch button """

    currentTextChanged = Signal(str)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                  parent=None,):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget

        OnText: "On"
          设置打开按钮文本
        """

        super().__init__(icon, title, content, parent)
        # self.configItem = configItem
        self.ComboBox = ComboBox()

        # add SpinBox to layout
        self.hBoxLayout.addWidget(self.ComboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.ComboBox.currentTextChanged.connect(self.__oncurrentTextChanged)

    def __oncurrentTextChanged(self, isChecked: str):
        """ switch button checked state changed slot """
        self.currentTextChanged.emit(isChecked)

    def addItem(self, Item: str):
        self.ComboBox.addItem(Item)

    def setCurrentIndex(self, CurrentIndex: int):
        self.ComboBox.setCurrentIndex(CurrentIndex)

class SpinBoxCard(SettingCard):
    """ Setting card with switch button """

    valueChanged = Signal(int)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                  parent=None,):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget

        OnText: "On"
          设置打开按钮文本
        """

        super().__init__(icon, title, content, parent)
        # self.configItem = configItem
        self.SpinBox = SpinBox()

        # add SpinBox to layout
        self.hBoxLayout.addWidget(self.SpinBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.SpinBox.valueChanged.connect(self.__onvalueChanged)

    def __onvalueChanged(self, isChecked: int):
        """ switch button checked state changed slot """
        self.valueChanged.emit(isChecked)

    def setValue(self, Value: int):
        self.SpinBox.setValue(Value)

    def setSuffix(self, Value: str):
        self.SpinBox.setSuffix(Value)

    def setSingleStep(self, SingleStep: int):
        self.SpinBox.setSingleStep(SingleStep)

    def setWrapping(self,Wrapping: bool):
        self.SpinBox.setWrapping(Wrapping)

    def setRange(self,mins: int,miax: int):
        self.SpinBox.setRange(mins,miax)

    def value(self):
        return self.SpinBox.value()

class PushCard(SettingCard):
    """ Setting card with a push button """

    clicked = Signal()

    def __init__(self, text, icon: Union[str, QIcon, FluentIconBase], title, content=None, parent=None):
        """
        Parameters
        ----------

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.button = QPushButton(text, self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)

    def setText(self,text):
        self.button.setText(text)

class SwitchCard(SettingCard):
    """ Setting card with switch button """

    checkedChanged = Signal(bool)

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], title, content=None,
                  parent=None, OnText = "On",OffText = "Off"):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget

        OnText: "On"
          设置打开按钮文本
        """
        super().__init__(icon, title, content, parent)
        # self.configItem = configItem
        self.switchButton = SwitchButton()
        # self.switchButton.setChecked(Checked)
        self.switchButton.setOnText(OnText)
        self.switchButton.setOffText(OffText)

        #
        # if configItem:
        #     self.setValue(qconfig.get(configItem))
        #     configItem.valueChanged.connect(self.setValue)

        # add switch button to layout
        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.switchButton.checkedChanged.connect(self.__onCheckedChanged)

    def __onCheckedChanged(self, isChecked: bool):
        """ switch button checked state changed slot """
        self.setValue(isChecked)
        self.checkedChanged.emit(isChecked)

    def setValue(self, isChecked: bool):
        # if self.configItem:
        #     qconfig.set(self.configItem, isChecked)

        self.switchButton.setChecked(isChecked)

    def setChecked(self, isChecked: bool):
        self.setValue(isChecked)

    def isChecked(self):
        return self.switchButton.isChecked()

class hotWidget(QWidget):
    def __init__(self, parent=None):
        super(hotWidget, self).__init__(parent)

        # 创建 QLabel 用于热评
        self.name_label = QLabel(self)
        self.label = QLabel(self)

        # 设置字体样式
        name_font = QFont()
        name_font.setPointSize(15)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        self.name_label.setWordWrap(True)
        self.name_label.setText("test 测试文字test")
        self.label.setText("———— 用户： test")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        self.label.setFont(name_font)

        # 设置布局
        layout = QHBoxLayout(self)
        # 创建垂直布局用于放置名称和简介以及上下伸缩
        info_layout = QVBoxLayout()
        info_layout.addStretch()  # 添加顶部垂直伸缩
        info_layout.addWidget(self.name_label)
        info_layout.addWidget(self.label)
        info_layout.addStretch()  # 添加底部垂直伸缩

        layout.addSpacing(10)
        layout.addLayout(info_layout)
        layout.addSpacing(10)

    def set_hot_content(self, hot, name):
        self.name_label.setText(hot)
        self.label.setText(name)

class LyricLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.lyric1 = ''
        self.lyric2 = ''
    ###读取歌词
    def set_lyrics(self, lyric1, lyric2):
        self.lyric1 = lyric1
        self.lyric2 = lyric2
        self.update_lyric()

    ###歌词显示
    def update_lyric(self):
        global x
        self.setAlignment(Qt.AlignCenter)
        if  self.lyric2 == ""  :
            self.setText(self.lyric1)
            self.adjustSize()
        else:
            self.setText(self.lyric1+'\n'+ self.lyric2)
            self.adjustSize()
        # 获取窗口宽度
        window_width = self.width()
        # # 设置窗口新的位置
        new_x_position = x - window_width / 2
        if allset.ismoving != True:
            self.move(new_x_position, self.pos().y())
        #
        # # 设置窗口新的位置
        # if self.pos().y() - x  > x:
        #     if allset.ismoving != True:
        #         self.move(new_x_position, self.pos().y())
        # else:
        #     new_x_position = x + window_width / 2
        #     if allset.ismoving != True:
        #         self.move(new_x_position, self.pos().y())

    ###歌词动画 废弃
    def start_scroll_animation(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scroll_lyric)
        self.timer.start(300)


    ###歌词滚动 废弃
    def scroll_lyric(self):
        if len(self.lyric1) > 0 and len(self.lyric2) > 0:
            self.lyric1 = self.lyric1[1:] + self.lyric1[0]
            self.lyric2 = self.lyric2[1:] + self.lyric2[0]
            self.setText(self.lyric1 + '\n' + self.lyric2)
        else:
            self.timer.stop()


    ###鼠标行为
    def mousePressEvent(self, e):
        ismoving = allset.ismoving
        if e.button() == Qt.LeftButton:
            self.ismoving = ismoving
            self.start_point = e.globalPos()
            self.window_point = self.frameGeometry().topLeft()

    def mouseMoveEvent(self, e):
        global x
        ismoving = allset.ismoving
        self.ismoving = ismoving
        if self.ismoving:
            relpos = e.globalPos() - self.start_point  # QPoint 类型可以直接相减
            self.move(self.window_point + relpos)      # 所以说 Qt 真是赞！
            window_width = self.width()
            # 计算新的 x 位置
            new_x_position = self.pos().x() + window_width / 2
            x = new_x_position

    # def mouseReleaseEvent(self, e):
        # self.ismoving = False



