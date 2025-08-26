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
        self.target_x = self.img_x
        self.target_y = self.img_y
        self.speed = 5  # pixeles por tick
        self.frames_width = 0
        self.frames_height = 0
        self.frames_x = 0
        self.frames_y = 0

        # Timer de animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)
        self.timer.start(30)

        # Fondo transparente y no bloquear eventos de los frames
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.show()

    def move_to(self, x, y):
        """Define la nueva posición objetivo dentro de los frames"""
        self.target_x = max(0, min(x, self.frames_width - self.pixmap.width()))
        self.target_y = max(0, min(y, self.frames_height - self.pixmap.height()))

    def update_position(self):
        # Movimiento gradual hacia la posición objetivo
        if self.img_x < self.target_x:
            self.img_x = min(self.img_x + self.speed, self.target_x)
        elif self.img_x > self.target_x:
            self.img_x = max(self.img_x - self.speed, self.target_x)

        if self.img_y < self.target_y:
            self.img_y = min(self.img_y + self.speed, self.target_y)
        elif self.img_y > self.target_y:
            self.img_y = max(self.img_y - self.speed, self.target_y)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Dibujar relativo a la posición de los frames
        painter.drawPixmap(self.frames_x + self.img_x, self.frames_y + self.img_y, self.pixmap)
        painter.end()

#Se crea una clase, de la POO
#Se ocupa un entorno virtual por lo que cambiar el interpretador de python a env
#Recuerde cargar las librerias del archivo Requerimientos.txt
class MainWindow(QMainWindow):
    #Generamos un constructor de la clase
    def __init__(self):
        #Inicializamos el contructor, método inicializador de la clase padre QMainWindow
        super().__init__()
        self.setGeometry(100, 30, 1400, 830)
        self.setWindowTitle("Project Vaccum Cleaner")
        self.initUI()
        self.show()

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setStyleSheet("background-color: #262626;") #Color de gris para la interfaz

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
        
        # Ejemplo de mover la imagen a una posición después de 1 segundo
        QTimer.singleShot(1000, lambda: self.overlay.move_to(200, 150))
        QTimer.singleShot(3000, lambda: self.overlay.move_to(50, 250))

    def resizeEvent(self, event):
        # Overlay cubre todo el central_widget
        self.overlay.setGeometry(0, 0, self.centralWidget().width(), self.centralWidget().height())

        # Posición y tamaño combinado de los dos frames
        frames_x = self.frame_left.x()
        frames_y = self.frame_left.y()
        frames_width = self.frame_left.width() + self.frame_center.width()
        frames_height = self.frame_left.height()

        self.overlay.frames_x = frames_x
        self.overlay.frames_y = frames_y
        self.overlay.frames_width = frames_width
        self.overlay.frames_height = frames_height

        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
