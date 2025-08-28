import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QColor, QPalette
from Overlay_Widget import OverlayWidget 
from Simulation import AspiradoraCuadrado

#Se crea una clase, de la POO
#Se ocupa un entorno virtual por lo que cambiar el interpretador de python a env
#Recuerde cargar las librerias del archivo Requerimientos.txt
class MainWindow(QMainWindow):
     #Generamos un cosntructor
   
    def __init__(self):
        #Inicializamos el contructor, método inicializador de la clase padre QMainWindow
        super().__init__()
        self.setGeometry(100, 30, 1400, 830)
        self.setWindowTitle("Interfaz estilo simulación")
        self.initUI()
        self.show()

    def initUI(self):
        # Fondo rosa pastel
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#EEC9F2"))  # rosa pastel
        self.setPalette(palette)

        # Widget central que contiene todo el contenido
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(50, 20, 50, 20)  # margen desde los bordes
        self.setCentralWidget(central_widget)

        # Widget azul cielo claro con esquinas redondeadas 
        container = QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #87CEEB;  /* azul cielo */
                border-radius: 20px;
            }
        """)
        central_layout.addWidget(container)

        grid = QGridLayout(container)
        grid.setContentsMargins(0, 80, 0, 0)
        grid.setSpacing(0)

        # Sección celada A (frame)
        self.frame_left = QFrame()
        self.frame_left.setStyleSheet("background-color: #00FFFF; border-radius: 10px;")
        self.frame_left.setContentsMargins = (0,0,0,0)
        self.frame_left.setObjectName("frame_left")
        grid.addWidget(self.frame_left, 0, 0, 2, 1)
        self.frame_data(self.frame_left)  # Llamada a la función informativa
        
        # Sección celada B (frame)
        self.frame_center = QFrame()
        self.frame_center.setStyleSheet("background-color: #8FEAFA; border-radius: 10px;")
        self.frame_center.setObjectName("frame_center")
        self.frame_center.setContentsMargins = (0,0,0,0)
        grid.addWidget(self.frame_center, 0, 1,2, 1)
        self.frame_data(self.frame_center)  # Llamada a la función informativa
        

        # Sección celada graficas (frame)
        self.frame_right = QFrame()
        self.frame_right.setStyleSheet("background-color: white; border-radius: 10px;")
        grid.addWidget(self.frame_right, 0, 2, 3, 1)

        right_layout = QVBoxLayout(self.frame_right)
        lbl = QLabel("GRÁFICA DE RENDIMIENTO (ejemplo)")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(lbl)

        botton1 = QPushButton("Abrir archivo .xlsx")
        botton1.setStyleSheet("""
            QPushButton {
                background-color: #C1E1C1;
                border: none;
                border-radius: 10px;
                padding: 8px 12px;
            }
            QPushButton:hover {
                background-color: #A9DCA9;
            }
        """)
        right_layout.addWidget(botton1)

        pixmap = QPixmap("Aspiradora.png").scaled(150, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.overlay = OverlayWidget(pixmap, parent=container, img_x=50, img_y=450)
        self.resizeEvent(None)  # Forzar ajuste inicial
        self.overlay.show()
        
        
        # Crear controlador de movimiento en cuadrado
        self.aspiradora_cuadrado = AspiradoraCuadrado(
            overlay=self.overlay,
            bottom_left=(50,450),
            width=500,
            height=350,
            duration=1000
        )
        self.aspiradora_cuadrado.start()
               
        # Aquí mismo das órdenes sin botones
        #self.overlay.set_position(50, 50)              # Se coloca en (50,50)
        #self.overlay.move_to(300, 200, duration=2000)  # Se mueve hasta (300,200) en 2 segundos
        #QTimer.singleShot(2500, lambda: self.overlay.rotate_image(90))   # Se rota 90 grados
        #self.check_move()  # Inicia la revisión del movimiento para rotar al finalizar 90 grados
        
        


################################Funciones Main Windows#############################################
        
    def resizeEvent(self, event):
        # Overlay cubre exactamente el container
        container = self.centralWidget().findChild(QFrame)
        if container:
            self.overlay.setGeometry(container.rect())

            # Limitar overlay al ancho combinado de frame_left + frame_center
            left = self.frame_left.x()
            right = self.frame_center.x() + self.frame_center.width()
            self.overlay.frames_width = right - left
            # Altura máxima del overlay: igual que el container o el frame más alto
            self.overlay.frames_height = container.height()

        super().resizeEvent(event)
        
    # Esperar a que termine el movimiento revisando la bandera
    def check_move(self):
        if self.overlay.move_finished:
            self.overlay.rotate_image(90)
        else:
            QTimer.singleShot(500, self.check_move)  # sigue revisando cada 30ms

################################Funciones informativas xd#############################################

    #Funcion para imprimir la información de un frame, indica el tipo de dato que requiere
    def frame_data(self, frame: QFrame): 
        # Nombre del frame
        print(f"Frame: {frame.objectName()}") 
        # Tamaño dentro de su propio sistema
        size = frame.size()
        print(f"Tamaño: {size.width()} x {size.height()}")
        # Posición relativa a su padre inmediato
        geom = frame.geometry()
        print(f"[Padre] x={geom.x()}, y={geom.y()}, w={geom.width()}, h={geom.height()}")
        # Posición relativa a la ventana principal
        pos_win = frame.mapTo(self, frame.pos())
        print(f"[Ventana principal] x={pos_win.x()}, y={pos_win.y()}")
        # Posición absoluta en pantalla (monitor)
        pos_abs = frame.mapToGlobal(frame.pos())
        print(f"[Pantalla global] x={pos_abs.x()}, y={pos_abs.y()}")
        
def limpiar_terminal():
        """Limpia la terminal en Windows."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
if __name__ == "__main__":
    limpiar_terminal()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
