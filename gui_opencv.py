import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
import cv2

class StreamingApp(QWidget):
    def __init__(self):
        super().__init__()

        # UI components
        self.initUI()

        # Start video capture
        self.cap = cv2.VideoCapture(0)

        # Set timer to read frame from video capture
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.nextFrameSlot)
        self.timer.start(30)  # 30fps

    def initUI(self):
        # Layout
        layout = QVBoxLayout()

        # Video Label
        self.label = QLabel()
        layout.addWidget(self.label)

        # Start Button
        self.btn_start = QPushButton('Start Streaming', self)
        self.btn_start.clicked.connect(self.start)
        layout.addWidget(self.btn_start)

        # Stop Button
        self.btn_stop = QPushButton('Stop Streaming', self)
        self.btn_stop.clicked.connect(self.stop)
        layout.addWidget(self.btn_stop)

        self.setLayout(layout)
        self.setWindowTitle('Video Streamer')
        self.setGeometry(100, 100, 800, 600)

    def nextFrameSlot(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.label.setPixmap(pix)

    def start(self):
        self.timer.start(30)
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def stop(self):
        self.timer.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = StreamingApp()
    mainWin.show()
    sys.exit(app.exec_())
