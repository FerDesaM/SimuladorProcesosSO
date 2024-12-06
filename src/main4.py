import time

def generar_procesos_por_segundo(input_file, output_file):
    # Leer datos desde el archivo
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Parsear los datos en una lista de tuplas (tiempo, proceso)
    data = []
    for line in lines:
        parts = line.strip().split(", ")
        tiempo = int(parts[0].split(" ")[1])
        proceso = int(parts[1].split(" ")[1])
        data.append((tiempo, proceso))
    
    # Crear una lista de procesos por cada segundo
    procesos_por_segundo = []
    max_tiempo = max(t[0] for t in data)
    
    for segundo in range(max_tiempo + 1):
        proceso_actual = None
        for tiempo, proceso in data:
            if segundo >= tiempo:
                proceso_actual = proceso
            else:
                break
        if proceso_actual is not None:
            procesos_por_segundo.append(f"Tiempo {segundo}, Proceso {proceso_actual}")
    
    # Guardar el resultado en un archivo de salida
    with open(output_file, 'w') as file:
        for line in procesos_por_segundo:
            file.write(line + "\n")

    print(f"Proceso completado. Resultado guardado en {output_file}")


# Llamada a la función
input_file = "execution_log.txt"  # Archivo de entrada con los datos originales
output_file = "resultado.txt"  # Archivo de salida con el resultado
generar_procesos_por_segundo(input_file, output_file)
