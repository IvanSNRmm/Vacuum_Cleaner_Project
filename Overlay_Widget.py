from PyQt6.QtWidgets import  QWidget
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import  QPainter,  QTransform

class OverlayWidget(QWidget):
    def __init__(self, pixmap, parent=None, ):
        super().__init__(parent)
        self.original_pixmap = pixmap
        self.pixmap = pixmap
        self.img_x = 0
        self.img_y = 0
        self.frames_width = 0
        self.frames_height = 0
        self.max_x = None
        self.max_y = None
        self.angle = 0
        # Lista de imágenes extra [{ "pixmap": QPixmap, "x": int, "y": int, "visible": bool }]
        self.extra_images = []
        self.move_finished = False # bandera para detectar fin de movimiento
        self.show()
        # Timer para refrescar la pantalla (performance)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    
   

    ########################## Funciones para imagen principal #################################################

    def set_position(self, x, y):
        """Coloca la imagen dentro de los límites"""
        max_x = max(0, self.frames_width - self.pixmap.width())
        max_y = max(0, self.frames_height - self.pixmap.height())

        self.img_x = max(0, min(x, max_x))
        self.img_y = max(0, min(y, max_y))
        self.update()

    def move_to(self, x, y, duration=1000):
        """Mueve suavemente respetando los límites"""
        start_x, start_y = self.img_x, self.img_y

        # Aplica los límites al destino
        max_x = max(0, self.frames_width - self.pixmap.width())
        max_y = max(0, self.frames_height - self.pixmap.height())
        end_x = max(0, min(x, max_x))
        end_y = max(0, min(y, max_y))

        steps = max(1, duration // 30)
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps

         # Reinicia bandera
        self.move_finished = False

        def step(i=0):
            if i < steps:
                self.set_position(self.img_x + dx, self.img_y + dy)
                QTimer.singleShot(30, lambda: step(i + 1))
            else:
                self.set_position(end_x, end_y)  # Ajusta exacto al final
                self.move_finished = True       # ¡Se completó el movimiento!

        step()

    def rotate_image(self, angle):
        self.angle = angle
        transform = QTransform().rotate(self.angle)
        self.pixmap = self.original_pixmap.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Imagen principal
        painter.drawPixmap(int(self.img_x), int(self.img_y), self.pixmap)
        # Imágenes extra
        for img in self.extra_images:
            if img["visible"]:
                painter.drawPixmap(img["x"], img["y"], img["pixmap"])   
                
     ########################## Funciones para imágenes extra #################################################

    #Agregar imagen secundaria al overlay y devolver su índice para manejarla luego (ocultar, mover, etc)
    def add_extraImage(self, pixmap, x=0, y=0, visible=True):
        """Agrega una imagen secundaria al overlay"""
        self.extra_images.append({
            "pixmap": pixmap,
            "x": x,
            "y": y,
            "visible": visible
        })
        self.update()
        return len(self.extra_images) - 1  # Devuelve el índice para manejarla luego
    # Cambiar posición de una imagen secundaria según su índice    
    def set_position_extraImage(self, index, x, y):
        """Cambia la posición de una imagen secundaria"""
        if 0 <= index < len(self.extra_images):
            self.extra_images[index]["x"] = x
            self.extra_images[index]["y"] = y
            self.update()
    # Hacer visible una imagen secundaria (basura) según su índice
    def show_extraImage(self, index):
        """Hace visible la imagen secundaria"""
        if 0 <= index < len(self.extra_images):
            self.extra_images[index]["visible"] = True
            self.update()
    # Hacer invisible una imagen secundaria (basura) según su índice
    def hide_extraImage(self, index):
        """Oculta la imagen secundaria"""
        if 0 <= index < len(self.extra_images):
            self.extra_images[index]["visible"] = False
            self.update()