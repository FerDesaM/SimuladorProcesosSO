import sys
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor

# Función para leer los datos del archivo TXT
def leer_datos_archivo(nombre_archivo):
    datos = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            tiempo, proceso = linea.strip().split(", ")
            tiempo = int(tiempo.split()[1])
            proceso = int(proceso.split()[1])
            datos.append((tiempo, proceso))
    return datos

class DiagramaGantt(QWidget):
    def __init__(self, datos):
        super().__init__()
        self.datos = datos
        self.tiempo_actual = 0

        self.setWindowTitle("Simulación Diagrama de Gantt")
        self.setGeometry(100, 100, 800, 300)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.table.setRowCount(len(set([d[1] for d in datos])))  # Una fila por proceso
        self.table.setColumnCount(max([d[0] for d in datos]) + 1)  # Columnas por cada unidad de tiempo

        # Configurar la tabla
        procesos = sorted(list(set([d[1] for d in datos])))
        self.procesos_map = {proceso: idx for idx, proceso in enumerate(procesos)}
        for idx, proceso in enumerate(procesos):
            self.table.setVerticalHeaderItem(idx, QTableWidgetItem(str(proceso)))

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

        # Iniciar un temporizador para actualizar la tabla
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizar_diagrama)
        self.timer.start(1000)  # Actualización cada segundo

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
    # Nombre del archivo que contiene los datos
    archivo_datos = "resultado.txt"

    # Leer los datos del archivo
    datos = leer_datos_archivo(archivo_datos)

    # Crear la aplicación PyQt5
    app = QApplication(sys.argv)
    ventana = DiagramaGantt(datos)
    ventana.show()
    sys.exit(app.exec_())
