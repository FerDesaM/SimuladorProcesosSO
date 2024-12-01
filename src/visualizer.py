import random
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QWidget, QProgressBar, QGridLayout
)
from PyQt5.QtCore import QTimer
from proceso import Proceso
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VisualizadorSJF(QMainWindow):
    def __init__(self, planificador):
        super().__init__()
        self.planificador = planificador
        self.setWindowTitle("Simulador de Planificación SJF")
        self.setGeometry(100, 100, 800, 600)

        # Contenedor principal
        contenedor_principal = QWidget()
        self.setCentralWidget(contenedor_principal)
        layout_principal = QVBoxLayout()
        contenedor_principal.setLayout(layout_principal)

        # Layout de controles
        layout_controles = QHBoxLayout()
        btn_generar = QPushButton("Generar Procesos")
        btn_iniciar = QPushButton("Iniciar Simulación")
        layout_controles.addWidget(btn_generar)
        layout_controles.addWidget(btn_iniciar)
        layout_principal.addLayout(layout_controles)

        # Tabla de procesos
        self.tabla_procesos = QTableWidget()
        self.tabla_procesos.setColumnCount(5)
        self.tabla_procesos.setHorizontalHeaderLabels(["ID", "Llegada", "Ejecución", "Espera", "Retorno"])
        layout_principal.addWidget(self.tabla_procesos)

        # Gráfico de la simulación
        self.figure = plt.figure(figsize=(8, 4))
        self.canvas = FigureCanvas(self.figure)
        layout_principal.addWidget(self.canvas)

        self.label_estado = QLabel("Esperando iniciar...")
        layout_principal.addWidget(self.label_estado)

        # Conexiones
        btn_generar.clicked.connect(self.generar_procesos)
        btn_iniciar.clicked.connect(self.iniciar_simulacion)
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_simulacion)

    def generar_procesos(self):
        self.planificador.procesos.clear()
        self.tabla_procesos.setRowCount(0)
        for i in range(5):
            nombre = f"Proceso-{i + 1}"  # Generar un nombre dinámico
            p = Proceso(i + 1, nombre, random.randint(0, 10), random.randint(5, 20))
            self.planificador.agregar_proceso(p)

        for proceso in self.planificador.procesos:
            row = self.tabla_procesos.rowCount()
            self.tabla_procesos.insertRow(row)
            self.tabla_procesos.setItem(row, 0, QTableWidgetItem(str(proceso.id)))
            self.tabla_procesos.setItem(row, 1, QTableWidgetItem(str(proceso.tiempo_llegada)))
            self.tabla_procesos.setItem(row, 2, QTableWidgetItem(str(proceso.tiempo_ejecucion)))

    def iniciar_simulacion(self):
        if not self.planificador.procesos:
            self.label_estado.setText("Primero genera procesos.")
            return
        self.timer.start(1000)

    def actualizar_simulacion(self):
        self.planificador.avanzar_tiempo()
        estado_procesos = self.planificador.obtener_estado_procesos()

    # Limpiar el gráfico anterior
        self.figure.clear()
        ax = self.figure.add_subplot(111)

    # Definir los datos del gráfico
        ids = [str(p["id"]) for p in estado_procesos]
        ejecuciones = [p["ejecucion"] - p["restante"] for p in estado_procesos]  # Tiempo de ejecución completado
        restantes = [p["restante"] for p in estado_procesos]  # Tiempo restante

    # Crear una gráfica de barras para mostrar la ejecución
        ax.bar(ids, ejecuciones, color='blue', label='Ejecutado')  # Barras azules para ejecución
        ax.bar(ids, restantes, bottom=ejecuciones, color='orange', label='Restante')  # Barras naranjas para el tiempo restante

    # Configuración del gráfico
        ax.set_title("Ejecución de Procesos")
        ax.set_xlabel("ID del Proceso")
        ax.set_ylabel("Tiempo")
        ax.legend()

    # Mostrar el gráfico en la interfaz
        self.canvas.draw()

    # Verifica si todos los procesos han terminado
        if not estado_procesos:
            self.timer.stop()
            self.label_estado.setText("Simulación completada.")