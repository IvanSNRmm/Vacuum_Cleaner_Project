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
        # Crear un widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Crear el layout principal
        layout = QHBoxLayout(central_widget)

        # Frame 1
        frame1 = QFrame()
        frame1.setStyleSheet("background-color: blue;")
        layout.addWidget(frame1)

        # Frame 2
        frame2 = QFrame()
        frame2.setStyleSheet("background-color: green;")
        layout.addWidget(frame2)

        # Asignar layout al widget central
        central_widget.setLayout(layout)

               

if  __name__ == '__main__':
    app = QApplication(sys.argv)
    Window = Main_Window()
    sys.exit(app.exec())
        
        
