import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QHBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor

# Función para leer los datos del archivo TXT
def leer_datos_archivo(nombre_archivo):
    datos = []
    try:
        with open(nombre_archivo, 'r') as archivo:
            for linea in archivo:
                tiempo, proceso = linea.strip().split(", ")
                tiempo = int(tiempo.split()[1])
                proceso = int(proceso.split()[1])
                datos.append((tiempo, proceso))
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no se encontró.")
    return datos

class DiagramaGantt(QWidget):
    def __init__(self):
        super().__init__()
        self.datos = []
        self.tiempo_actual = 0
        self.simulando = False

        self.setWindowTitle("Simulación Diagrama de Gantt")
        self.setGeometry(100, 100, 800, 400)

        # Layout principal
        self.layout = QVBoxLayout()

        # Layout para los botones
        self.boton_layout = QHBoxLayout()

        # Crear los botones
        self.boton_cp0 = QPushButton("cp0")
        self.boton_cp1 = QPushButton("cp1")
        self.boton_cp2 = QPushButton("cp2")

        # Agregar botones al layout de los botones
        self.boton_layout.addWidget(self.boton_cp0)
        self.boton_layout.addWidget(self.boton_cp1)
        self.boton_layout.addWidget(self.boton_cp2)

        # Agregar el layout de los botones al layout principal
        self.layout.addLayout(self.boton_layout)

        # Configurar la tabla
        self.table = QTableWidget()
        self.table.setRowCount(0)  # Inicialmente no hay filas
        self.table.setColumnCount(0)  # Inicialmente no hay columnas

        # Agregar la tabla al layout principal
        self.layout.addWidget(self.table)

        # Layout para los botones Go y Restart
        self.control_layout = QHBoxLayout()

        # Crear los botones Go y Restart
        self.boton_go = QPushButton("Go")
        self.boton_restart = QPushButton("Restart")

        # Conectar los botones a las funciones correspondientes
        self.boton_go.clicked.connect(self.iniciar_simulacion)
        self.boton_restart.clicked.connect(self.restart_simulacion)

        # Agregar los botones al layout
        self.control_layout.addWidget(self.boton_go)
        self.control_layout.addWidget(self.boton_restart)

        # Agregar el layout de control al layout principal
        self.layout.addLayout(self.control_layout)

        self.setLayout(self.layout)

        # Iniciar un temporizador para actualizar la tabla
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_diagrama)

        # Conectar los botones de cp0, cp1 y cp2 a sus respectivas funciones
        self.boton_cp0.clicked.connect(lambda: self.cargar_datos('resultado.txt'))
        self.boton_cp1.clicked.connect(lambda: self.cargar_datos('resultado1.txt'))
        self.boton_cp2.clicked.connect(lambda: self.cargar_datos('resultado2.txt'))

    def cargar_datos(self, archivo):
        """Cargar los datos del archivo seleccionado y actualizar la tabla."""
        self.datos = leer_datos_archivo(archivo)
        if self.datos:
            self.tiempo_actual = 0  # Reiniciar el tiempo actual
            self.simulando = False  # Detener la simulación si estaba corriendo
            self.boton_go.setText("Go")  # Cambiar el texto del botón Go

            # Limpiar la tabla
            self.table.clearContents()

            # Configurar la tabla según los nuevos datos
            procesos = sorted(list(set([d[1] for d in self.datos])))
            self.procesos_map = {proceso: idx for idx, proceso in enumerate(procesos)}
            self.table.setRowCount(len(procesos))  # Establecer el número de filas
            self.table.setColumnCount(max([d[0] for d in self.datos]) + 1)  # Establecer el número de columnas

            for idx, proceso in enumerate(procesos):
                self.table.setVerticalHeaderItem(idx, QTableWidgetItem(str(proceso)))

    def iniciar_simulacion(self):
        """Inicia la simulación cuando se hace clic en el botón Go."""
        if not self.simulando:
            self.simulando = True
            self.timer.start(1000)  # Actualización cada segundo
            self.boton_go.setText("Stop")  # Cambiar el texto de Go a Stop
        else:
            self.timer.stop()
            self.simulando = False
            self.boton_go.setText("Go")  # Cambiar el texto de Stop a Go

    def restart_simulacion(self):
        """Reinicia la simulación desde el principio cuando se hace clic en el botón Restart."""
        self.tiempo_actual = 0
        self.simulando = False
        self.boton_go.setText("Go")  # Asegurarse de que el botón Go está en "Go"

        # Limpiar la tabla
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.table.setItem(row, col, QTableWidgetItem())  # Eliminar cualquier celda existente

        self.timer.start(1000)  # Reiniciar la simulación (comienza de nuevo con Go)

    def actualizar_diagrama(self):
        if self.tiempo_actual >= len(self.datos):
            self.timer.stop()
            return

        tiempo, proceso = self.datos[self.tiempo_actual]
        fila = self.procesos_map[proceso]
        columna = tiempo
        item = QTableWidgetItem()
        item.setBackground(QColor(100, 150, 255))  # Pintar la celda
        item.setTextAlignment(Qt.AlignCenter)
        self.table.setItem(fila, columna, item)
        self.table.setItem(fila, columna, QTableWidgetItem(f"T{tiempo}"))

        self.tiempo_actual += 1

if __name__ == "__main__":
    # Crear la aplicación PyQt5
    app = QApplication(sys.argv)
    ventana = DiagramaGantt()
    ventana.show()
    sys.exit(app.exec_())
