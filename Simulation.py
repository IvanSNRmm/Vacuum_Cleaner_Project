from PyQt6.QtCore import QTimer

class AspiradoraCuadrado:
    def __init__(self, overlay, bottom_left=(50,50), width=200, height=150, duration=1000):
        self.overlay = overlay
        self.bottom_left = bottom_left
        self.width = width
        self.height = height
        self.duration = duration  # tiempo de movimiento por lado en ms
        self.overlay.set_position(*bottom_left) #Asterisco para desempaquetar

        # Coordenadas de los 4 vértices del cuadrado
        x, y = bottom_left
        self.vertices = [
            (x, y),
            (x, y - height),
            (x + width, y - height),
            (x + width, y)
            
            
            
        ]
        self.current_index = 0  # lado actual
        self.movimientos = 0    # contador de lados recorridos

    def start(self):
        self.move_next()

    def move_next(self):
        # Determinar el siguiente vértice
        start_vertex = self.vertices[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.vertices)
        end_vertex = self.vertices[self.current_index]

        # Mover la aspiradora
        self.overlay.move_to(end_vertex[0], end_vertex[1], duration=self.duration)

        # Esperar a que termine el movimiento y continuar
        QTimer.singleShot(self.duration + int(self.duration*0.5), self.after_move)  # un poquito más de tiempo para asegurar

    def after_move(self):
        # Contabilizar movimiento
        self.movimientos += 1
        print(f"Movimientos realizados: {self.movimientos}")

        # Limitar a 100 movimientos
        if self.movimientos >= 100:
            print("Se alcanzó el límite de 100 movimientos. Deteniendo.")
            return  # No continuar más movimientos

        # Repetir movimiento al siguiente lado
        self.move_next()
