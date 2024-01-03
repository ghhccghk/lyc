from PySide6 import QtWidgets
from PySide6 import QtCore
from PySide6.QtCore import Qt, QLocale, QObject,Signal,QUrl,QRect,QPoint
from PySide6.QtGui import QFontDatabase,QFont,QIcon,QPixmap,QColor, QAction,QGuiApplication
#######全局变量设置
from module import allset

from ui.my_window_ui import LyricLabel

# 字体设置
def setbold(self, checked):
    if checked:
        allset.bold = True
        self.change_font(self)
    else:
        allset.bold = False
        self.change_font(self)

def setunderline(self, checked):
    if checked:
        allset.underline = True
        self.change_font(self)
    else:
        allset.underline = False
        self.change_font(self)

def setpointSize(self):
    allset.pointSize = int(self.ui.pointSize.value())
#        print(pointSize)
    change_font(self)

def setcolor(self,c):
    allset.foncolor = c.name()
    change_font(self)


def setfonta(self,font):
    allset.fonta = font
    change_font(self)

def change_font(self):
    # 创建QFont对象
    self.desktopLyric = LyricLabel()
    qfont = QFont(allset.fonta)
    qfont.setPointSize(allset.pointSize)# 设置字体大小
#        print(fonta)
    qfont.setBold(allset.bold)
    qfont.setUnderline(allset.underline)
    self.ui.label.setStyleSheet("color:"+allset.foncolor)
    self.ui.label.setFont(qfont)
    if self.desktopLyric.isVisible():
        self.desktopLyric.setStyleSheet("color:"+allset.foncolor)
        self.desktopLyric.setFont(qfont)
    else:
        self.desktopLyric.setFont(qfont)

def showColorDialog(self):
    global foncolor
    # print(foncolor)
    colorset = ColorDialog(QColor(allset.foncolor), self.tr('颜色设置'), self.window(),enableAlpha=False)
    colorset.setColor(QColor(allset.foncolor), movePicker=True)
    colorset.colorChanged.connect(lambda c: self.setcolor(c))
    colorset.exec()
