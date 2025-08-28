
from PyQt6.QtWidgets import  QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import  QPainter,  QTransform

class OverlayWidget(QWidget):
    def __init__(self, pixmap, parent=None, img_x =50, img_y=50):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.pixmap = pixmap
        self.img_x = img_x
        self.img_y = img_y
        self.frames_width = 0
        self.frames_height = 0
        self.max_x = None
        self.max_y = None
        self.angle = 0
        self.move_finished = False # bandera para detectar fin de movimiento

        
        self.show()

        # Timer solo para repintar la imagen (no mueve nada)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(10)

    def set_position(self, x, y):
        """Coloca la imagen en (x,y) respetando márgenes del overlay"""
        max_x = self.frames_width - self.pixmap.width()
        max_y = self.frames_height - self.pixmap.height()
        print(f"Maximos permitidos: ({max_x}, {max_y})")
        self.img_x = max(0, min(x, max_x))
        self.img_y = max(0, min(y, max_y))
        self.update()

    def move_to(self, x, y, duration=1000):
        """
        Mueve suavemente la imagen desde su posición actual hasta (x,y).
        - x, y: coordenadas finales
        - duration: tiempo total en ms (ej: 1000 = 1s)
        """
        
        start_x, start_y = self.img_x, self.img_y
        steps = max(1, duration // 30)  # número de pasos según los 30ms del timer
        dx = (x - start_x) / steps
        dy = (y - start_y) / steps

        def step(i=0):
            if i < steps:
                self.set_position(self.img_x + dx, self.img_y + dy)
                QTimer.singleShot(30, lambda: step(i+1))
                print(f"Moviendo a ({self.img_x:.1f}, {self.img_y:.1f})")
            else:
                self.move_finished = True  # ¡El movimiento terminó!

        self.move_finished = False  # reiniciar bandera
        step()

    def rotate_image(self, angle):
        """Rota la imagen al ángulo indicado (grados)"""
        self.angle = angle
        transform = QTransform().rotate(self.angle)
        self.pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(int(self.img_x), int(self.img_y), self.pixmap)