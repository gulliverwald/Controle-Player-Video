from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QIcon, QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QThread, QUrl
import sys
import pyfirmata
import time

board = pyfirmata.Arduino('COM3')

it = pyfirmata.util.Iterator(board)
it.start()

board.digital[8].mode = pyfirmata.INPUT

mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
    
class Worker(QThread):
    @staticmethod
    def run():
        last_sensor_read = False
        mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("./videos/video_principal.avi")))
        mediaPlayer.play()

        while True:
            isActive = board.digital[8].read()

            if isActive == True:
                if last_sensor_read == True:
                    mediaPlayer.setPosition(0)
                elif last_sensor_read == False:
                    mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("./videos/video_principal.avi")))
                    mediaPlayer.play()
            else: 
                if last_sensor_read == False:
                    mediaPlayer.setPosition(0)
                elif last_sensor_read == True:
                    mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile("./videos/video_secundario.avi")))
                    mediaPlayer.play()

            last_sensor_read = isActive
            time.sleep(mediaPlayer.duration()/1000)

        



class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("projector.ico"))
        self.setWindowTitle("Projetor Player")
        self.setGeometry(100, 100, 600, 400)
        self.showFullScreen()

        p = self.palette()
        p.setColor(QPalette.Window, QColor("#000000"))
        self.setPalette(p)

        self.create_player()

    def create_player(self):
        videowidget = QVideoWidget()

        vbox = QVBoxLayout()
        vbox.addWidget(videowidget)

        mediaPlayer.setVideoOutput(videowidget)
        self.setLayout(vbox)

def main():
    app = QApplication(sys.argv)
    window = Window()
    thread = Worker()
    thread.start()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
