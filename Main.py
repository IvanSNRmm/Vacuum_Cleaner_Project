import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

#Se crea una clase, de la POO
#Se ocupa un entorno virtual por lo que cambiar el interpretador de python a Vir_env
#Recuerde cargar las librerias del archivo Requerimientos.txt

class Main_Window(QMainWindow):
    #Generamos un cosntructor
    #INGRESAR VALOR BAUD 115200
    def __init__(self):
    #Inicializamos el contructor, método inicializador de la clase padre QMainWindow
        super().__init__()
        self.Generate_Window()
        
    def Generate_Window(self):
        self.setGeometry(200,25,1200,850) #Tamaño de la ventana y posición al generarse
        self.setWindowTitle("Proyecto Rendimiento")
        #self.setStyleSheet("""
        #background: qlineargradient(
        #        x1:0, y1:0,
        #        x2:1, y2:0,
        #        stop:0 blue,
        #        stop:0.5 blue,
        #        stop:0.5 green,
        #        stop:1 green
        #    );
        #""")
        
        self.setStyleSheet("background-color: #262626;")#Color de gris para la interfaz
        self.Generate_frames()
        self.show()
    
    def Generate_frames(self):
        # Crear widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear layout tipo cuadrícula
        grid = QGridLayout()

        # Frame columna izquierda (ocupa 3 filas)
        frame_left = QFrame()
        frame_left.setStyleSheet("background-color: #00FFFF;")
        grid.addWidget(frame_left, 0, 0, 3, 1)  # row, col, rowSpan, colSpan

        # Frame columna derecha (ocupa 3 filas)
        frame_right = QFrame()
        frame_right.setStyleSheet("background-color: #8FEAFA;")
        grid.addWidget(frame_right, 0, 1, 3, 1)

        # --- Ajustar proporciones de columnas ---
        grid.setColumnStretch(0, 1)  # columna izquierda
        grid.setColumnStretch(1, 1)  # columna derecha

        # --- Ajustar proporciones de filas ---
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(2, 1)

        # Asignar layout al widget central
        central_widget.setLayout(grid)
                

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = Main_Window()
    sys.exit(app.exec())
        
        
