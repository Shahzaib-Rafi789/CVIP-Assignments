import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QWidget, QFileDialog
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap

import cv2

class VideoPlayerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.center_widget = QWidget()
        self.center_layout = QVBoxLayout()
        self.center_widget.setLayout(self.center_layout)
        self.layout.addWidget(self.center_widget, alignment=Qt.AlignCenter)

        self.buttons_container = QWidget()
        self.buttons_container.setFixedSize(200, 50)
        self.buttons_layout = QHBoxLayout()
        self.buttons_container.setLayout(self.buttons_layout)

        self.file_button = QPushButton("File")
        self.file_button.setCheckable(True)
        self.file_button.clicked.connect(self.toggle_file)

        self.camera_button = QPushButton("Camera")
        self.camera_button.setCheckable(True)
        self.camera_button.clicked.connect(self.toggle_camera)

        self.buttons_layout.addWidget(self.file_button)
        self.buttons_layout.addWidget(self.camera_button)

        self.center_layout.addWidget(self.buttons_container, alignment=Qt.AlignCenter)

        self.video_label = QLabel()
        self.center_layout.addWidget(self.video_label, alignment=Qt.AlignCenter)
        self.video_label = QLabel()
        self.layout.addWidget(self.video_label)

        self.open_button = QPushButton("Open Video/Transmission")
        self.open_button.clicked.connect(self.open_file)
        self.layout.addWidget(self.open_button)

        self.play_pause_button = QPushButton("Play/Pause")
        self.play_pause_button.clicked.connect(self.play_pause)
        self.layout.addWidget(self.play_pause_button)

        self.replay_button = QPushButton("Replay")
        self.replay_button.clicked.connect(self.replay)
        self.layout.addWidget(self.replay_button)

        self.forward_button = QPushButton("Forward 10s")
        self.forward_button.clicked.connect(self.forward)
        self.layout.addWidget(self.forward_button)

        self.backward_button = QPushButton("Backward 10s")
        self.backward_button.clicked.connect(self.backward)
        self.layout.addWidget(self.backward_button)

        self.gray_scale_button = QPushButton("View Mode: Color")
        self.gray_scale_button.clicked.connect(self.toggle_view_mode)
        self.layout.addWidget(self.gray_scale_button)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.video_capture = None
        self.playing = False
        self.file_mode = False
        self.camera_mode = False
        self.view_mode = "Color"
        self.toggle_file()

    def toggle_file(self):
        self.file_mode = True
        self.camera_mode = False

        self.file_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px; padding: 2px;")
        self.camera_button.setStyleSheet("background-color: #ffffff; border-radius: 10px; border: 2px solid #4CAF50;")

    def toggle_camera(self):
        self.camera_mode = True
        self.file_mode = False
        
        self.camera_button.setStyleSheet("background-color: #4CAF50; border-radius: 10px; padding: 2px;")
        self.file_button.setStyleSheet("background-color: #ffffff; border-radius: 10px; border: 2px solid #4CAF50;")

    def open_file(self):

        if self.file_mode:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi)")
            if file_path:
                self.video_capture = cv2.VideoCapture(file_path)

        elif self.camera_mode:
            self.video_capture = cv2.VideoCapture(0)
        
        else:
            return
        
        self.playing = True
        self.timer.start(30)

    def play_pause(self):
        if self.playing:
            self.timer.stop()
            self.playing = False
        else:
            self.timer.start(30)
            self.playing = True

    def replay(self):
        if self.video_capture is not None:
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def backward(self):
        if self.video_capture is not None:
            current_frame_pos = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            new_frame_pos = max(current_frame_pos - 10 * self.video_capture.get(cv2.CAP_PROP_FPS), 0)
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, new_frame_pos)

    def forward(self):
        if self.video_capture is not None:
            current_frame_pos = self.video_capture.get(cv2.CAP_PROP_POS_FRAMES)
            total_frames = self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
            fps = self.video_capture.get(cv2.CAP_PROP_FPS)
            remaining_time = (total_frames - current_frame_pos) / fps

            if remaining_time <= 10:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, total_frames)
            else:
                new_frame_pos = min(current_frame_pos + 10 * fps, total_frames)
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, new_frame_pos)

    def toggle_view_mode(self):
        modes_switch = {"Color" : "Gray Scale",
                        "Gray Scale" : "Black White",
                        "Black White": "Color"}
        
        self.view_mode = modes_switch[self.view_mode]
        self.gray_scale_button.setText("View Mode: " + self.view_mode)

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            if self.view_mode == "Gray Scale":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            elif self.view_mode == "Black White":
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                _, frame = cv2.threshold(frame, 127, 255, cv2.THRESH_BINARY)
            else:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            q_image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.video_label.setPixmap(pixmap)
            self.video_label.setScaledContents(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayerApp()
    window.show()
    sys.exit(app.exec_())
