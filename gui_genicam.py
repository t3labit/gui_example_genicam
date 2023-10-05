import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QVBoxLayout, QPushButton,QHBoxLayout, QFileDialog, QPlainTextEdit
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer,Qt
import cv2
from camera_genicam import GigeCamera
from cv_utils import resize, write_image_opencv, read_image_opencv
import os
import time
from datetime import datetime

class StreamingApp(QWidget):
    def __init__(self):
        super().__init__()

        # UI components
        self.init_ui()

        # Start video capture
        self.cam = GigeCamera()

        # Set timer to read frame from video capture
        self.fps = 10
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_image)
        #self.timer.start(self.fps)  # 30fps

        # Init
        self.img = None
        self.img_ref = None

        # load_img_ref
        self.load_img_ref()

        # Start camera by default
        self._on_btn_cam_start()
            
    def init_ui(self):
        # Main Vertical Layout
        layout = QVBoxLayout()

        # Button Layout (Horizontal)
        btn_layout = QHBoxLayout()

        # Cams  Layout (Refernce and Video)
        layout_cams = QHBoxLayout()

        # Start Button
        self.btn_cam_start = QPushButton('Start', self)
        self.btn_cam_start.clicked.connect(self._on_btn_cam_start)
        btn_layout.addWidget(self.btn_cam_start)

        # Stop Button
        self.btn_cam_stop = QPushButton('Stop', self)
        self.btn_cam_stop.clicked.connect(self._on_btn_cam_stop)
        btn_layout.addWidget(self.btn_cam_stop)

        # Save imgae
        self.btn_set_reference = QPushButton('Set Reference', self)
        self.btn_set_reference.clicked.connect(self._on_btn_set_reference)
        btn_layout.addWidget(self.btn_set_reference)

        # Run imgae
        self.btn_run = QPushButton('Run', self)
        self.btn_run.clicked.connect(self._on_btn_run)
        btn_layout.addWidget(self.btn_run)

        self.btn_save_image = QPushButton('Save Image', self)
        self.btn_save_image.clicked.connect(self._on_btn_save_image)
        btn_layout.addWidget(self.btn_save_image)

        # Add button layout to the main layout
        layout.addLayout(btn_layout)

        # Cams  Layout (Refernce and Video)
        layout_img = QVBoxLayout()
        label_img_text = QLabel("Cam Streaming")
        label_img_text.setAlignment(Qt.AlignCenter) 
        self.label_img = QLabel()
        layout_img.addWidget(label_img_text)
        layout_img.addWidget(self.label_img)
        layout_cams.addLayout(layout_img)
        
        layout_img_ref = QVBoxLayout()
        label_img_ref_text = QLabel("Reference Image")
        label_img_ref_text.setAlignment(Qt.AlignCenter) 
        self.label_img_ref = QLabel()
        layout_img_ref.addWidget(label_img_ref_text)
        layout_img_ref.addWidget(self.label_img_ref)
        layout_cams.addLayout(layout_img_ref)
        
        layout.addLayout(layout_cams)

        # Layout box
        self.log_box = QPlainTextEdit(self)
        self.log_box.setReadOnly(True)  # Make the log box read-only
        layout.addWidget(self.log_box)

        self.setLayout(layout)
        self.setWindowTitle('Video Streamer')
        self.setGeometry(100, 100, 1300, 600)

    def load_img_ref(self):
        path = os.path.join("data", "reference.png")
        if os.path.exists(path):
            self.img_ref = read_image_opencv(path)
            self.visualize_img(self.img_ref, self.label_img_ref)
            self.log_box.appendPlainText('[Reference] Loaded reference.png')
        
    def _on_image(self):
        ret, self.img = self.cam.get_image()
        if ret:
            self.visualize_img(self.img, self.label_img)

    def _on_btn_cam_start(self):
        self.cam.start()
        self.timer.start(self.fps)
        self.btn_cam_start.setEnabled(False)
        self.btn_cam_stop.setEnabled(True)
        self.log_box.appendPlainText('[Cam] Cam streaming started')

    def _on_btn_cam_stop(self):
        self.timer.stop()
        self.cam.stop()
        self.btn_cam_start.setEnabled(True)
        self.btn_cam_stop.setEnabled(False)
        # Clear Image
        self.label_img.clear()
        self.log_box.appendPlainText('[Cam] Cam streaming stopped')
        
    def _on_btn_set_reference(self):
        if self.img is not None:
            self.img_ref = self.img.copy()
            path = "data"
            if not os.path.exists(path):
                os.makedirs(path)
            write_image_opencv(os.path.join("data", "reference.png"), self.img_ref)
            self.visualize_img(self.img_ref, self.label_img_ref)
            self.log_box.appendPlainText('[Reference] Reference image updated')

    def _on_btn_save_image(self):
        #folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        #if folder_path:
        #    print(f'Selected folder path: {folder_path}')
        path = "data/images"
        if not os.path.exists(path):
            os.makedirs(path)
        date_str = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(path, f'image_{date_str}.png')
        write_image_opencv(filename, self.img)
        self.log_box.appendPlainText(f'[Saving] Saved image: {filename}')

    def _on_btn_run(self):
        if self.img is not None:
            self.log_box.appendPlainText('[Algorithm] ok/not')

    def closeEvent(self, event):
        self.timer.stop()
        self.cam.stop()
        self.cam.close()
 
    def visualize_img(self, img, qt_obj):
        # qt_obj has to be a Qlabel (self.label_img, self.label_img_ref)
        # Visualize
        img_vis = resize(img, 640)
        img_qt = QImage(img_vis, img_vis.shape[1], img_vis.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img_qt)
        qt_obj.setPixmap(pix)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = StreamingApp()
    mainWin.show()
    sys.exit(app.exec_())
