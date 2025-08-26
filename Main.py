import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap, QPainter

class OverlayWidget(QWidget):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap
        self.img_x = 50
        self.img_y = 50
        self.dx = 3
        self.dy = 3
        self.frames_width = 0
        self.frames_height = 0

        # Timer para animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_image)
        self.timer.start(30)

        # Fondo transparente y no bloquear eventos de los frames
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.show()

    def move_image(self):
        # Límites basados en los frames reales
        max_x = self.frames_width - self.pixmap.width()
        max_y = self.frames_height - self.pixmap.height()

        if self.img_x >= max_x or self.img_x <= 0:
            self.dx *= -1
        if self.img_y >= max_y or self.img_y <= 0:
            self.dy *= -1

        self.img_x += self.dx
        self.img_y += self.dy
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.img_x, self.img_y, self.pixmap)
        painter.end()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 30, 1400, 830)
        self.setWindowTitle("Frames con imagen animada")
        self.initUI()
        self.show()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout de 3 columnas x 3 filas
        grid = QGridLayout()
        grid.setContentsMargins(0,0,0,0)
        grid.setSpacing(0)
        central_widget.setLayout(grid)

        # Frames
        self.frame_left = QFrame()
        self.frame_left.setStyleSheet("background-color: #00FFFF;")
        grid.addWidget(self.frame_left, 0, 0, 3, 1)

        self.frame_center = QFrame()
        self.frame_center.setStyleSheet("background-color: #8FEAFA;")
        grid.addWidget(self.frame_center, 0, 1, 3, 1)

        # Columna derecha vacía
        grid.setColumnStretch(0,2)
        grid.setColumnStretch(1,2)
        grid.setColumnStretch(2,1)
        grid.setRowStretch(0,1)
        grid.setRowStretch(1,1)
        grid.setRowStretch(2,1)

        # Imagen PNG con transparencia
        pixmap = QPixmap("Aspiradora_nofondo").scaled(
            100, 100,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        # Widget overlay para animar la imagen
        self.overlay = OverlayWidget(pixmap, parent=central_widget)
        self.overlay.show()

    def resizeEvent(self, event):
        # Overlay cubre todo el central_widget
        self.overlay.setGeometry(0, 0, self.centralWidget().width(), self.centralWidget().height())

        # Actualizar límites de movimiento según frames
        self.overlay.frames_width = self.frame_left.height() + self.frame_center.height()
        self.overlay.frames_height = self.frame_left.width()

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
