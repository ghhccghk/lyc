import sys
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow
import json
import random
from module import allset

class MyAudioPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        # 获取媒体播放器的状态

    def play(self):
        global tt
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(1)
        res = MyAudioPlayer.getname()
        name = res.get('name', '')
        txt = res.get('txt', '')
        allset.tt = txt
        print(txt)
        fp = 'res/audio/明日方舟-重岳/' + name + '.wav'
        self.player.setSource(QUrl.fromLocalFile(fp))
        print(self.player.mediaStatus())
        self.player.play()


    def getname() -> dict:
        f = open('res/read/明日方舟-重岳.json', 'r')
        content = f.read()
        a = json.loads(content)
        all_keys = MyAudioPlayer.aa(content)
        # 转换为数字，然后获取最大和最小值
        numeric_values = [int(key) for key in all_keys if key.isdigit()]  # 如果包含浮点数可以使用 float(key) 来转换
        max_numeric = max(numeric_values, default=None)
        min_numeric = min(numeric_values, default=None)
        random_number = random.randint(min_numeric, max_numeric)
        a1 = str(random_number)
        a2 = str(random_number) + "-txt"
        return {  "name": a[a1],
                  "txt": a[a2]
                   }

    def aa(content) -> tuple:
        a = json.loads(content)
        # print(a['1-txt'])
        num_keys = []
        # 遍历字典中的键值对
        for key, value  in a.items():
        # 判断值的类型是否为数字
            if key.isdigit() == True:
                num_keys.append(key)
        return num_keys

    def print_status(self):
        print(f"Media status: {status}")
        if status == "MediaStatus.EndOfMedia":
            audioPlayer = MyAudioPlayer()
            audioPlayer.close()
