# main.py
import sys
from PyQt5.QtWidgets import QApplication
from scheduler import PlanificadorSJF
from visualizer import VisualizadorSJF

def main():
    app = QApplication(sys.argv)
    planificador = PlanificadorSJF()
    visualizador = VisualizadorSJF(planificador)
    visualizador.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()