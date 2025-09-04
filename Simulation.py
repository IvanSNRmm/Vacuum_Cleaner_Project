from PyQt6.QtCore import QTimer
import time
import random

class AspiradoraCuadrado:
    
    def __init__(self, overlay, bottom_left, width=200, height=150,
                 duration=800, max_iter=100, main_from_Simulation=None):
        self.overlay = overlay
        self.bottom_left = bottom_left
        self.width = width
        self.height = height
        self.duration = duration
        self.max_iter = max_iter
        self.main_from_Simulation = main_from_Simulation

        # Coordenadas de los vértices
        x, y = self.bottom_left
        self.vertices = [
            (x, y),                   # 0 → esquina inferior izquierda
            (x, y - height),          # 1 → esquina superior izquierda
            (x + width, y - height),  # 2 → esquina superior derecha
            (x + width, y)            # 3 → esquina inferior derecha
        ]

        # Mapeo de celdas a vértices
        self.cell_vertex_map = {
            "A": 1,  # celda A ↔ vértice 1
            "B": 3   # celda B ↔ vértice 3
        }

        # Variables de control
        self.iteration = 0
        self.current_index = 0
        self.active_routine = None
        self.secondary_repeats = 0
        self.tercera_repeats = 0
        self.finished = False
        self.running = False

        # Basura en celdas
        self.trash = {"A": False, "B": False}
        self.trash_cooldown = {"A": 0, "B": 0}
        #Contador de basura limpiada
        self.clean_count_A = 0  # Contador de limpiezas en celda A
        self.clean_count_B = 0  # Contador de limpiezas en celda B

        # Descansos
        self.rest_short = False
        self.rest_long = False
        #Contadores de descansos
        self.rest_short_count = 0  # Contador de descansos cortos
        self.rest_long_count = 0   # Contador de descansos largos

        # Temporizador
        self.start_time = None
        self.elapsed_time = 0

        # Control de pasos para evitar solapamientos
        self.step_in_progress = False
        
        # Datos para gráficas de rendimiento
        self.iterations_list_graph = []
        self.total_rest_list_graph = []
        self.total_clean_list_graph = []
        

    # ---------------- Inicio y reset ----------------
    def start(self):
        if not self.running:
            print("▶️ Iniciando rutina de aspiradora...")
            self.start_time = time.time()
            self.running = True
            self.finished = False
            self.iteration = 0
            self.current_index = 0
            self.rest_short_count = 0  # Contador de descansos cortos
            self.rest_long_count = 0   # Contador de descansos largos
            self.run_principal()
        else:
            print("⚠️ La simulación ya está corriendo.")

    def reset(self):
        print("🔄 Reiniciando simulación...")
        self.iteration = 0
        self.current_index = 0
        self.secondary_repeats = 0
        self.tercera_repeats = 0
        self.active_routine = None
        self.finished = False
        self.running = False
        self.trash = {"A": False, "B": False}
        self.trash_cooldown = {"A": 0, "B": 0}
        self.rest_short = False
        self.rest_long = False
        self.step_in_progress = False
        self.rest_short_count = 0  # Contador de descansos cortos
        self.rest_long_count = 0   # Contador de descansos largos
        self.elapsed_time = 0
        self.overlay.set_position(*self.vertices[0])
        self.overlay.rotate_image(0)
        
        

    # ---------------- Rutina Principal ----------------
    def run_principal(self):
        if self.step_in_progress: return
        self.step_in_progress = True
        self.reset_rest_status()
        rotations = {0:0, 1:90, 2:180, 3:270}

        if self._check_finish():
            self.step_in_progress = False
            return

        self.active_routine = "principal"
        self.current_index = (self.current_index + 1) % 4
        next_pos = self.vertices[self.current_index]

        self.overlay.move_to(*next_pos, duration=self.duration)
        self.check_move(rotation_angle=rotations[self.current_index])
        self.iteration += 1

        if self.main_from_Simulation:
            self.main_from_Simulation.update_iteration(self.iteration)
            self._update_graph_data() # Actualiza datos de gráficas
            self.main_from_Simulation.update_table() # Actualiza tabla de rendimiento
            self.main_from_Simulation.update_vacuum_status("Rutina Principal")

        print(f"🔄 Principal → moviéndose a {next_pos} | Iteración: {self.iteration}")

        # Limpia basura si hay en esta celda
        self.try_clean_trash()
        self._generate_trash()

        QTimer.singleShot(self.duration + 200, self._principal_next_step)

    def _principal_next_step(self):
        self.step_in_progress = False
        if self._check_finish(): return

        # Siguiente paso
        if self.current_index == 0:
            self.run_secondary()
        else:
            self.run_principal()

        # ---------------- Rutina Secundaria ----------------
    def run_secondary(self):
        if self.step_in_progress: return
        self.step_in_progress = True
        self.reset_rest_status()
        if self._check_finish():
            self.step_in_progress = False
            return
        self.active_routine = "secundaria"
        self.secondary_repeats = 0
        self.no_trash_in_A = True
        self._secondary_step()

    def _secondary_step(self):
        if self._check_finish():
            self.step_in_progress = False
            return

        rotations = {0:0, 1:180}
        target_index = 1 if self.current_index == 0 else 0
        next_pos = self.vertices[target_index]
        self.current_index = target_index

        self.overlay.move_to(*next_pos, duration=self.duration)
        self.check_move(rotation_angle=rotations[target_index])
        self.iteration += 1
        self.secondary_repeats += 1

        if self.main_from_Simulation:
            self.main_from_Simulation.update_iteration(self.iteration)
            self._update_graph_data() # Actualiza datos de gráficas
            self.main_from_Simulation.update_table() # Actualiza tabla de rendimiento
            self.main_from_Simulation.update_vacuum_status("Rutina Secundaria")

        print(f"➡️ Secundaria → moviéndose a {next_pos} | Iteración: {self.iteration}")

        self._generate_trash()  # Solo detectar basura
        if self.trash["A"]: self.no_trash_in_A = False

        # Tras terminar el movimiento, decide siguiente paso
        QTimer.singleShot(self.duration + 200, self._secondary_next_step)

    def _secondary_next_step(self):
        self.step_in_progress = False
        if self._check_finish(): return

        if self.secondary_repeats < 2:
            # Continúa la secuencia secundaria
            self._secondary_step()
        else:
            # Secuencia terminada → decide si llamar a principal
            #if self.trash["A"] or self.trash["B"]:
            if self.trash["A"]:
                print("♻️ Basura detectada → pasar a principal")
                QTimer.singleShot(100, self.run_principal)
            else:
                # Si no hay basura, hacer descanso corto o continuar ciclo
                self.set_rest_short()
                QTimer.singleShot(self.duration*2, self.run_tercera)
                self.overlay.rotate_image(0)

    # ---------------- Rutina Tercera ----------------
    def run_tercera(self):
        if self.step_in_progress: return
        self.step_in_progress = True
        self.reset_rest_status()
        if self._check_finish():
            self.step_in_progress = False
            return
        self.active_routine = "tercera"
        self._tercera_step()

    def _tercera_step(self):
        if self._check_finish():
            self.step_in_progress = False
            return

        rotations = {0:0, 1:180, 2:90, 3:270}

        # Secuencia de vértices: 0↔1, 2, 3
        if self.tercera_repeats == 0:
            target_index = 1 if self.current_index == 0 else 0
        elif self.tercera_repeats == 1:
            target_index = 2
        elif self.tercera_repeats == 2:
            target_index = 3
        else:
            # Rutina completa
            self.step_in_progress = False
            if not self.trash["A"] and not self.trash["B"]:
                print("😴 Descanso largo (x4)")
                self.set_rest_long()
                QTimer.singleShot(self.duration * 4, self.run_secondary)
                self.overlay.rotate_image(0)
            else:
                # Espera un instante antes de pasar a principal
                QTimer.singleShot(self.duration + 200, self.run_principal)
                self.overlay.rotate_image(0)
            return

        next_pos = self.vertices[target_index]
        self.current_index = target_index
        self.overlay.move_to(*next_pos, duration=self.duration)
        self.check_move(rotation_angle=rotations[self.current_index])
        self.iteration += 1
        self.tercera_repeats += 1

        if self.main_from_Simulation:
            self.main_from_Simulation.update_iteration(self.iteration)
            self._update_graph_data() # Actualiza datos de gráficas
            self.main_from_Simulation.update_table() # Actualiza tabla de rendimiento
            self.main_from_Simulation.update_vacuum_status("Rutina Tercera")

        print(f"🔵 Tercera → moviéndose a {next_pos} | Iteración: {self.iteration}")

        self._generate_trash()  # solo detectar

        # Tras terminar el movimiento, decide siguiente paso
        QTimer.singleShot(self.duration + 200, self._tercera_next_step)

    def _tercera_next_step(self):
        self.step_in_progress = False
        # Si hay basura en A o B, ir a principal
        if self.trash["A"] or self.trash["B"]:
            print("♻️ Basura detectada → pasar a principal")
            QTimer.singleShot(100, self.run_principal)
        else:
            # Continuar con la secuencia
            if self.tercera_repeats <= 3:
                self._tercera_step()

    # ---------------- Manejo de basura ----------------
    def _generate_trash(self):
        min_iterations_for_trash = 5  # Número mínimo de iteraciones antes de que pueda generarse basura

        # Inicializar contadores si no existen
        if not hasattr(self, 'iterations_since_trash'):
            self.iterations_since_trash = {"A": 0, "B": 0}
        for cell in ["A", "B"]:
            self.iterations_since_trash[cell] += 1  # Sumar iteración

            if not self.trash[cell] and self.trash_cooldown[cell] <= 0:
                # Solo generar basura si ya pasaron suficientes iteraciones
                if self.iterations_since_trash[cell] >= min_iterations_for_trash:
                    if random.random() < 0.2:  # Probabilidad de basura
                        self.trash[cell] = True
                        print(f"🗑️ Basura generada en celda {cell}")
                        self.iterations_since_trash[cell] = 0  # Reiniciar contador
            else:
                if self.trash_cooldown[cell] > 0:
                    self.trash_cooldown[cell] -= 1

        if self.main_from_Simulation:
            self.main_from_Simulation.update_trash_images(self.trash)

    def try_clean_trash(self):
        for cell, vertex in self.cell_vertex_map.items():
            if self.trash[cell] and self.current_index == vertex:
                print(f"🧹 Limpiando celda {cell}")
                self.trash[cell] = False
                self.trash_cooldown[cell] = 4
                
                # Incrementar contador de limpieza
                if cell == "A":
                    self.clean_count_A += 1
                elif cell == "B":
                    self.clean_count_B += 1
                
                # Enviar datos al main
                if self.main_from_Simulation:
                    self.main_from_Simulation.update_clean_data(
                        clean_A=self.clean_count_A,
                        clean_B=self.clean_count_B
                    )
                
                if self.main_from_Simulation:
                    self.main_from_Simulation.update_trash_images(self.trash)

    # ---------------- Descansos ----------------
    def set_rest_short(self):
        self.rest_short = True
        self.rest_long = False
        self.rest_short_count += 1  # Incrementa contador
        print(f"😴 Descanso corto (contador={self.rest_short_count})")
        if self.main_from_Simulation:
            self.main_from_Simulation.update_rest_status("Descanso corto")
            # Solo enviar datos, no crear label
            self.main_from_Simulation.update_rest_data(
                short=self.rest_short_count,
                long=self.rest_long_count
            )
            

    def set_rest_long(self):
        self.rest_short = False
        self.rest_long = True
        self.rest_long_count += 1
        print(f"😴 Descanso largo (contador={self.rest_long_count})")
        if self.main_from_Simulation:
            self.main_from_Simulation.update_rest_status("Descanso largo")
                # Solo enviar datos, no crear label
            self.main_from_Simulation.update_rest_data(
                short=self.rest_short_count,
                long=self.rest_long_count
            )
            

    def reset_rest_status(self):
        self.rest_short = False
        self.rest_long = False
        if self.main_from_Simulation:
            self.main_from_Simulation.update_rest_status("No")

    # ---------------- Verificador de fin de simulación ----------------
    def _check_finish(self):
        if self.iteration >= self.max_iter:
            print("⛔ Límite de iteraciones alcanzado, rutina terminada")
            self.finished = True
            self.running = False
            self.elapsed_time = time.time() - self.start_time
            print(f"⏱ Simulación finalizada en {self.elapsed_time:.2f} segundos")
            if self.main_from_Simulation:
                self.main_from_Simulation.update_vacuum_status("Finalizado")
                self.main_from_Simulation.update_time(self.elapsed_time)
                self.main_from_Simulation.resizeEvent(None)  # Forzar ajuste de overlay
            return True
        return False

    # ---------------- Movimiento y rotación ----------------
    def check_move(self, rotation_angle=0):
        if self.overlay.move_finished:
            self.overlay.rotate_image(rotation_angle)
        else:
            QTimer.singleShot(30, lambda: self.check_move(rotation_angle))
    # ---------------- Gráficas de rendimiento ----------------       
    def _update_graph_data(self):
        # Solo agregar cada  iteración o al final
        if self.iteration % 1 == 0 or self.iteration == self.max_iter:
            total_rest = self.rest_short_count + self.rest_long_count
            total_clean = self.clean_count_A 

            self.iterations_list_graph.append(self.iteration)
            self.total_rest_list_graph.append(total_rest)
            self.total_clean_list_graph.append(total_clean)

            # Mandar datos al MainWindow
            if self.main_from_Simulation:
                self.main_from_Simulation.update_graph_data(
                    self.iterations_list_graph,
                    self.total_rest_list_graph,
                    self.total_clean_list_graph
                )
    
