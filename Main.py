import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFrame, QVBoxLayout, QLabel, QPushButton,QHBoxLayout
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt6.QtGui import QPainter
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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
        self.setGeometry(100, 30, 1400, 800)
        self.setWindowTitle("Interfaz Simulación Aspiradora")
        self.Design_Section()
        #self.showMaximized()
        self.show()

    def Design_Section(self):
        
        #Variables para la simulación
        self.iteration = 0 # Iteración actual
        self.total_clean_A = 0 # Limpiezas totales en A
        self.total_clean_B = 0 # Limpiezas totales en B
        self.rest_short_total = 0  # Descansos cortos totales
        self.rest_long_total = 0 # Descansos largos totales
        # Listas para guardar datos de la gráfica
        self.iterations_list = []       # Número de iteraciones
        self.total_rest_list = []       # Descansos totales por iteración
        self.total_clean_list = []      # Limpiezas totales por iteración
        # Fondo rosa pastel
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#EEC9F2"))  # rosa pastel
        self.setPalette(palette)

        # Widget central que contiene todo el contenido
        central_widget = QWidget()
        central_layout = QVBoxLayout(central_widget)
        central_layout.setContentsMargins(50, 10, 50, 10)  # margen desde los bordes
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
        grid.addWidget(self.frame_left, 0, 0, 3, 1)
        # Layout vertical para frame_left
        frame_left_layout = QVBoxLayout(self.frame_left)
        frame_left_layout.setSpacing(0)
        # Nombre Celda A (frame)
        self.label_cell_A = QLabel("Celda A")
        self.label_cell_A.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter) #Alignación centrada y arriba
        self.label_cell_A.setStyleSheet("color: #2E4053;font-size: 16px; font-weight: bold; background-color: None; padding: 8px; border-radius: 8px;")
        frame_left_layout.addWidget(self.label_cell_A)
        self.frame_data(self.frame_left)  # Llamada a la función informativa
        
        
        # Sección celada B (frame)
        self.frame_center = QFrame()
        self.frame_center.setStyleSheet("background-color: #8FEAFA; border-radius: 10px;")
        self.frame_center.setObjectName("frame_center")
        self.frame_center.setContentsMargins = (0,0,0,0)
        grid.addWidget(self.frame_center, 0, 1,3, 1)
        #Layout vertical para frame_center
        frame_center_layout = QVBoxLayout(self.frame_center)
        frame_center_layout.setSpacing(0)
        #Label Nombre Celda B (frame)
        self.label_cell_B = QLabel("Celda B")
        self.label_cell_B.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter) #Alignación centrada y arriba
        self.label_cell_B.setStyleSheet("color: #2E4053;font-size: 16px; font-weight: bold; background-color: None; padding: 8px; border-radius: 8px;")
        frame_center_layout.addWidget(self.label_cell_B)
        self.frame_data(self.frame_center)  # Llamada a la función informativa
        
        # Sección celada C (frame)
        self.frame_bottom = QFrame()
        self.frame_bottom.setStyleSheet("background-color: #A09F9F; border-radius: 10px;")
        self.frame_bottom.setObjectName("frame_bottom")
        self.frame_bottom.setContentsMargins = (0,0,0,0)
        grid.addWidget(self.frame_bottom, 3, 0,3, 2)
        self.frame_data(self.frame_bottom)  # Llamada a la función informativa
        
        # Layout vertical para frame_bottom
        frame_bottom_layout = QVBoxLayout(self.frame_bottom)
        frame_bottom_layout.setContentsMargins(15, 15, 15, 15)
        frame_bottom_layout.setSpacing(10)

        # Cargar imagen de aspiradora
        vacuum_pixmap = self.load_vaccum_image()
        # Crear overlay para la aspiradora
        self.overlay = OverlayWidget(vacuum_pixmap, parent=container)
        self.resizeEvent(None)  # Forzar ajuste inicial
        self.overlay.set_position(self.overlay.frames_width*0.05,int(self.overlay.frames_height*0.65))  # Posición inicial
        self.overlay.show() # Asegura que el overlay sea visible
        self.overlay.setObjectName("overlay")
        
        # Cargar imagen de basura
        trash_pixmap = self.load_garbage_image()
        # Guardamos los índices para poder manejarlas
        self.trash_A_index = self.overlay.add_extraImage(trash_pixmap, x=100, y=200)
        self.trash_B_index = self.overlay.add_extraImage(trash_pixmap, x=300, y=200)
        # Crear controlador de movimiento en cuadrado
        self.aspiradora_cuadrado = AspiradoraCuadrado(
        overlay=self.overlay,
        bottom_left=(self.overlay.frames_width*0.05,int(self.overlay.frames_height*0.65)),
        width=self.overlay.frames_width*0.7,
        height=self.overlay.frames_height*0.4,
        duration=1000,
        max_iter=20,
        main_from_Simulation = self   # conecta los metodos de simulation con main.py
        )
        
        # Botón para iniciar simulación (centrado)
        self.start_button = QPushButton("🚀 Iniciar Simulación")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: #2E4053;
                border: none;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            } 
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)# Botón para iniciar simulación (centrado), cambiar color cuando está deshabilitado y cuando se pasa el cursor por encima
        
        self.start_button.clicked.connect(self.aspiradora_cuadrado.start) # Conectar el botón a la función start de la aspiradora
        frame_bottom_layout.addWidget(self.start_button) # Agregar al layout vertical frame_bottom_layout detro de frame_bottom
        
        # Botón para reiniciar simulación (centrado)
        self.reset_button = QPushButton("🔄 Reiniciar Simulación")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #F08080;  /* rojo claro */
                color: #2E4053;
                border: none;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
                font-size: 12px;
            } 
            QPushButton:hover {
                background-color: #CD5C5C;  /* rojo oscuro */
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
        """)
        self.reset_button.clicked.connect(lambda: [self.aspiradora_cuadrado.reset(), self.reset_graph(), self.reset_table()])  # Conectar al método reset de la aspiradora y reset de gráfica
        frame_bottom_layout.addWidget(self.reset_button)  # Agregar al layout vertical frame_bottom_layout dentro de frame_bottom
        
        # Después de crear los botones y el overlay
        self.start_button.raise_()
        self.reset_button.raise_()
        self.overlay.stackUnder(self.start_button)
        self.overlay.stackUnder(self.reset_button)
        
        # Estado de la aspiradora
        self.vacuum_label = QLabel("📊 Estado: Esperando")
        self.vacuum_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.vacuum_label.setStyleSheet("color: #2E4053;font-size: 12px; font-weight: bold; background-color: #E8F5E9; padding: 8px; border-radius: 8px;")
        frame_bottom_layout.addWidget(self.vacuum_label)

        # Contador de iteraciones
        self.iteration_label = QLabel("🔄 Iteración: 0/100")
        self.iteration_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.iteration_label.setStyleSheet("color: #2E4053;font-size: 12px;font-weight:bold; background-color: #E3F2FD; padding: 8px; border-radius: 8px;")
        frame_bottom_layout.addWidget(self.iteration_label)
        

        #Faltan: tiempo, celda A y celda B, descanso
        # Tiempo de simulación (transcurrido) 
        self.time_simulation_label = QLabel("⏱️ Tiempo total de simulación: 0s")
        self.time_simulation_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.time_simulation_label.setStyleSheet("color: #2E4053;font-size: 12px;font-weight:bold; background-color: #FFF3E0; padding: 8px; border-radius: 8px;")
        frame_bottom_layout.addWidget(self.time_simulation_label)
        # Estado de la celda A
        self.cell_A_label = QLabel("🟩 Celda A: Estado")  
        self.cell_A_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.cell_A_label.setStyleSheet("color: #2E4053;font-size: 12px;font-weight:bold; background-color: #F3E5F5; padding: 8px; border-radius: 8px;")
        frame_bottom_layout.addWidget(self.cell_A_label)
        # Estado de la celda B 
        self.cell_B_label = QLabel("🟩 Celda B: Estado")
        self.cell_B_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.cell_B_label.setStyleSheet("color: #2E4053;font-size: 12px;font-weight:bold; background-color: #E0F7FA; padding: 8px; border-radius: 8px;")
        frame_bottom_layout.addWidget(self.cell_B_label)
        # Estado de descanso
        self.rest_label = QLabel("💤 Descanso: No")
        self.rest_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.rest_label.setStyleSheet("color: #2E4053;font-size: 12px;font-weight:bold; background-color: #FBE9E7; padding: 8px; border-radius: 8px;")
        frame_bottom_layout.addWidget(self.rest_label)
        
        ##############
        
        
        # Frame para gráficas
        self.frame_right_complete = QFrame()
        self.frame_right_complete.setStyleSheet("background-color: white; border-radius: 10px;")
        grid.addWidget(self.frame_right_complete, 0, 2, 6, 2)
        # Layout vertical
        frame_graph_layout = QVBoxLayout(self.frame_right_complete) 
        # Crear la figura de Matplotlib
        self.fig = Figure(figsize=(5,4))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Gráfica de rendimiento")
        self.ax.set_xlabel("Iteraciones")
        self.ax.set_ylabel("Cantidad total")

        # Canvas para insertar la figura en PyQt
        self.canvas = FigureCanvas(self.fig)
        frame_graph_layout.addWidget(self.canvas)
        
         # ------------------ TABLA DE REGISTRO ------------------
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Iteración", "Limpieza A", "Limpieza B", "Descanso Corto", "Descanso Largo", "Rendimiento"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # No editable
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)

        # Añadir tabla al layout de la gráfica
        frame_graph_layout.addWidget(self.table)
        self.iteration_performance = []  # nueva variable para rendimiento
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #FDFEFE;       /* Fondo general blanco */
                alternate-background-color: #EBF5FB; /* Filas alternadas azul claro */
                gridline-color: #D5DBDB;         /* Color de líneas */
                font-size: 13px;
                color: #1B2631;                  /* Color de texto general */
                selection-background-color: #5DADE2;  /* Fila seleccionada */
                selection-color: white;          /* Texto en fila seleccionada */
            }
            QHeaderView::section {
                background-color: #2E86C1;       /* Encabezado azul */
                color: white;                    /* Texto encabezado blanco */
                font-weight: bold;
                font-size: 14px;
                border: none;
                padding: 5px;
            }
        """)
        
        
    
    
    
    
        
        

    ################################ Funciones MainWindow  #########################################
    ################################ Actualización de la interfaz ################################

    def update_iteration(self, iteration: int):
        """Actualiza el contador de iteraciones"""
        self.iteration_label.setText(f"🔄 Iteración: {iteration}/{self.aspiradora_cuadrado.max_iter}")
        self.iteration = iteration  # Guardar el valor actual de la iteración

    def update_vacuum_status(self, status: str):
        """Actualiza el estado de la aspiradora"""
        self.vacuum_label.setText(f"📊 Estado: {status}")
        self.vacuum_status = status  # Guardar el estado actual

    def update_trash_images(self, trash_states: dict):
        """
        Muestra/oculta imágenes de basura según el estado de las celdas.
        trash_states = {"A": True/False, "B": True/False}
        """
        # Celda A
        if trash_states.get("A", False):
            self.overlay.show_extraImage(self.trash_A_index)
            self.cell_A_label.setText("🟥 Celda A: Basura detectada")
        else:
            self.overlay.hide_extraImage(self.trash_A_index)
            self.cell_A_label.setText("🟩 Celda A: Limpia")

        # Celda B
        if trash_states.get("B", False):
            self.overlay.show_extraImage(self.trash_B_index)
            self.cell_B_label.setText("🟥 Celda B: Basura detectada")
        else:
            self.overlay.hide_extraImage(self.trash_B_index)
            self.cell_B_label.setText("🟩 Celda B: Limpia")
            
        
    def clean_cell(self, cell: str):
        """Limpia la celda y actualiza el estado en la interfaz"""
        if cell == "A":
            self.cell_A_label.setText("🟩 Celda A: Limpia (recién limpiada)")
        elif cell == "B":
            self.cell_B_label.setText("🟩 Celda B: Limpia (recién limpiada)")

    def update_rest_status(self, status: str):
            """Muestra el estado de descansos"""
            self.rest_label.setText(f"💤 Descanso: {status}")
            
    def update_time(self, elapsed):
        self.time_simulation_label.setText(f"⏱️ Tiempo total de simulación: {elapsed:.2f}s")
        
    def update_rest_data(self, short, long):
        # Solo guardar o registrar los valores, no crear label
        self.rest_short_total = short
        self.rest_long_total = long
        print(f"Datos recibidos → Descansos cortos: {short}, Descansos largos: {long}")
        
    def update_clean_data(self, clean_A, clean_B):
        # Solo almacenar o registrar datos
        self.total_clean_A = clean_A
        self.total_clean_B = clean_B
        print(f"Limpiezas → A: {clean_A}, B: {clean_B}")
        
    def update_graph_data(self, iterations_list, rest_list, clean_list):
        self.ax.clear()
        self.ax.set_title("Gráfica de rendimiento")
        self.ax.set_xlabel("Iteraciones")
        self.ax.set_ylabel("Cantidad total")
        self.ax.grid(True)
        self.ax.plot(iterations_list, rest_list, label="Descansos totales", marker='o')
        self.ax.plot(iterations_list, clean_list, label="Limpiezas totales", marker='x')
        self.ax.legend()
        self.canvas.draw()
    
        
    def update_table(self):
        """Agrega una fila nueva con los datos de la iteración"""
        
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        performance = self.calculate_performance(
            iteration=self.iteration, 
            clean_A=self.total_clean_A, 
            clean_B=self.total_clean_B, 
            rest_short=self.rest_short_total, 
            rest_long= self.rest_long_total)
        
        # Insertar valores en cada columna
        self.table.setItem(row, 0, QTableWidgetItem(str(self.iteration)))
        self.table.setItem(row, 1, QTableWidgetItem(str(self.total_clean_A)))
        self.table.setItem(row, 2, QTableWidgetItem(str(self.total_clean_B)))
        self.table.setItem(row, 3, QTableWidgetItem(str(self.rest_short_total)))
        self.table.setItem(row, 4, QTableWidgetItem(str(self.rest_long_total)))
        self.table.setItem(row, 5, QTableWidgetItem(str(str(performance) + "%")))

        # Scroll automático hacia abajo
        self.table.scrollToBottom()

    def reset_table(self):
        """Limpia la tabla y reinicia la lista de rendimiento"""
        self.table.setRowCount(0)
        self.iteration_performance = []
            
        

        
        
        
        
        
               
        # Aquí mismo das órdenes sin botones
        #self.overlay.set_position(50, 50)              # Se coloca en (50,50)
        #self.overlay.move_to(300, 200, duration=2000)  # Se mueve hasta (300,200) en 2 segundos
        #QTimer.singleShot(2500, lambda: self.overlay.rotate_image(90))   # Se rota 90 grados
        #self.check_move()  # Inicia la revisión del movimiento para rotar al finalizar 90 grados
        
        


    ################################Funciones Main Windows#############################################
        
    def resizeEvent(self, event):
        container = self.centralWidget().findChild(QFrame)
        if container:
            bottom_margin = 200  # espacio para botones, labels, etc.
            overlay_rect = container.rect()
            overlay_rect.setHeight(container.height() - bottom_margin)
            self.overlay.setGeometry(overlay_rect)

            left = self.frame_left.x()
            right = self.frame_center.x() + self.frame_center.width()
            self.overlay.frames_width = max(1, min(right - left, 1000))
            self.overlay.frames_height = max(1, min(overlay_rect.height(), 600))

        super().resizeEvent(event)
        
    def load_vaccum_image(self):
        try:
            # Intentar cargar la imagen Aspiradora.png
            pixmap = QPixmap("Aspiradora.png")
            if pixmap.isNull():
                raise FileNotFoundError
            return pixmap.scaled(150, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        except:
            # Si falla, crear una imagen de aspiradora temporal
            print("No se encontró Aspiradora.png, creando imagen temporal de aspiradora")
            pixmap = QPixmap(80, 80)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            painter.setBrush(QColor(50, 50, 50))  # Gris oscuro para la aspiradora
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(5, 5, 70, 70)  # Cuerpo principal
            painter.setBrush(QColor(100, 100, 100))  # Gris más claro para detalles
            painter.drawEllipse(20, 25, 40, 30)  # Parte frontal
            painter.end()
            return pixmap
    
    def load_garbage_image(self):
        try:
            # Intentar cargar la imagen Aspiradora.png
            pixmap = QPixmap("descarga.png")
            if pixmap.isNull():
                raise FileNotFoundError
            return pixmap.scaled(250, 250, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        except:
            # Si falla, crear una imagen de aspiradora temporal
            print("No se encontró Aspiradora.png, no se creará imagen temporal de aspiradora")
            
        
    
        
    ############################### Limpieza de la gráfica #############################################
    def reset_graph(self):
        # Vaciar listas de datos
        self.iterations_list = []
        self.total_rest_list = []
        self.total_clean_list = []

        # Limpiar el eje de la gráfica
        self.ax.clear()

        # Volver a configurar título y etiquetas
        self.ax.set_title("Gráfica de rendimiento")
        self.ax.set_xlabel("Iteraciones")
        self.ax.set_ylabel("Cantidad")

        # Refrescar el canvas
        self.canvas.draw()

        
    

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
        
    def calculate_performance(self, iteration, clean_A, clean_B, rest_short, rest_long):
        """Calcula el rendimiento ponderando descansos cortos y largos como ahorro de iteraciones"""
        if iteration == 0:
            return 0  # evitar división entre 0

        total_cleans = clean_A + clean_B
        total_rest_savings = rest_short * 4 + rest_long * 8

        performance = (total_rest_savings / iteration) * 100 - (total_cleans / iteration) * 50
        return max(0, round(performance, 2))  # limitar a 0 mínimo y redondear a 2 decimales, retorna el rendimiento

#Funcion para limpiar la terminal al iniciar la aplicación fuera de la clase        
def limpiar_terminal():
        """Limpia la terminal en Windows."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
if __name__ == "__main__":
    limpiar_terminal()
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
