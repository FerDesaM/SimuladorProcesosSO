from cpu_maestro import CpuMaestro

# Crear una instancia de CpuMaestro con 3 CPUs y 5 procesos
cpu_maestro = CpuMaestro(num_cpus=1, num_procesos=5)

# Llamar al despachador para asignar procesos a las CPUs
cpu_maestro.despachador()

cpu_maestro.modificar_tiempos()

cpu_maestro.mostrar_tiempos()

cpu_maestro.ejecutar_planificacion_RR()
