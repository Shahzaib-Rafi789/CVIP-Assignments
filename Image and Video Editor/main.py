import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import numpy as np

class ImageFilterApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Filter App")
        self.setGeometry(100, 100, 900, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.original_label = QLabel()
        self.original_label.setFixedSize(400, 400)
        self.layout.addWidget(self.original_label)

        self.filtered_label = QLabel()
        self.filtered_label.setFixedSize(400, 400)
        self.layout.addWidget(self.filtered_label)

        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)

        self.filter_buttons_layout = QVBoxLayout()
        self.filter_buttons_layout.addWidget(self.open_button)

        self.filters = [
            ("Original", lambda x: x),
            ("Negate", cv2.bitwise_not),
            ("Gaussian Blur", self.apply_gaussian_blur),
            ("Log Transformation", self.apply_log_transformation),
            ("Power Transformation", self.apply_power_transformation)
        ]

        for filter_name, filter_func in self.filters:
            filter_button = QPushButton(filter_name)
            filter_button.clicked.connect(lambda _, f=filter_func: self.apply_filter(f))
            self.filter_buttons_layout.addWidget(filter_button)

        self.layout.addLayout(self.filter_buttons_layout)

        self.image = None
        self.filtered_image = None

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image, self.original_label)
            self.filtered_image = self.image.copy()  # Initially, show original image in the filtered label
            self.display_image(self.filtered_image, self.filtered_label)

    def apply_filter(self, filter_func):
        if self.image is not None:
            self.filtered_image = filter_func(self.image)
            self.display_image(self.filtered_image, self.filtered_label)

    def apply_gaussian_blur(self, image):
        return cv2.GaussianBlur(image, (43, 43), 7)

    def apply_log_transformation(self, image):
        c = 1
        log_transformed_image = c * np.log1p(image)
        scaled_image = ((log_transformed_image - log_transformed_image.min()) / (log_transformed_image.max() - log_transformed_image.min()) * 255).astype(np.uint8)
        return scaled_image

    def apply_power_transformation(self, image):
        c = 1
        g = 3.0
        transformed_image = c * np.power(image, g)
        scaled_image = ((transformed_image - transformed_image.min()) / (transformed_image.max() - transformed_image.min()) * 255).astype(np.uint8)
        return scaled_image

    def display_image(self, image, label):
        height, width, channel = image.shape
        q_image = QImage(image.data, width, height, width * channel, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageFilterApp()
    window.show()
    sys.exit(app.exec_())
