import os
import subprocess
import re
import glob
import sys
from pathlib import Path

# Tabla de peligrosidad para cada tipo de movimiento
MOVEMENT_DANGER = {
    # Movimientos seguros (0 puntos)
    'MOVE_NONE': 0,
    'MOVE_START': 0,
    'MOVE_HOME': 0,
    'MOVE_END': 0,
    'MOVE_FRONT': 0,
    
    # Riesgo muy bajo (1-2 puntos)
    'MOVE_LEFT_90': 1,
    'MOVE_RIGHT_90': 1,
    'MOVE_LEFT_180': 2,
    'MOVE_RIGHT_180': 2,
    'MOVE_DIAGONAL': 1,
    
    # Movimientos de exploración (1 punto)
    'MOVE_LEFT': 1,
    'MOVE_RIGHT': 1,
    'MOVE_BACK': 1,
    'MOVE_LEFT_INPLACE': 1,
    'MOVE_RIGHT_INPLACE': 1,
    'MOVE_BACK_WALL': 1,
    'MOVE_BACK_STOP': 1,
    
    # Riesgo medio (3-5 puntos) - Transiciones diagonales simples
    'MOVE_LEFT_TO_45': 3,
    'MOVE_RIGHT_TO_45': 3,
    'MOVE_LEFT_FROM_45': 3,
    'MOVE_RIGHT_FROM_45': 3,
    
    # Riesgo alto (6-10 puntos) - Giros diagonales complejos
    'MOVE_LEFT_TO_135': 6,
    'MOVE_RIGHT_TO_135': 6,
    'MOVE_LEFT_45_TO_45': 8,
    'MOVE_RIGHT_45_TO_45': 8,
    'MOVE_LEFT_FROM_45_180': 6,
    'MOVE_RIGHT_FROM_45_180': 6,
}

def parse_total_distance(output):
    """Extrae el valor de Total Distance del output del simulador"""
    if not output:
        return None
    pattern = r'Total Distance:\s*(\d+)'
    match = re.search(pattern, output)
    if match:
        return int(match.group(1))
    return None

def parse_total_time(output):
    """Extrae el valor de Total Time del output del simulador"""
    if not output:
        return None
    pattern = r'Total Time:\s*(\d+\.\d+)'
    match = re.search(pattern, output)
    if match:
        return float(match.group(1))
    return None

def parse_movement_sequence(output):
    """
    Extrae y parsea la secuencia de movimientos del output del simulador.
    Retorna una lista de tuplas (movement_name, count).
    """
    if not output:
        return []
    
    # Buscar la línea que empieza con MOVE_START y termina con MOVE_HOME
    pattern = r'^(MOVE_START.*MOVE_HOME)$'
    match = re.search(pattern, output, re.MULTILINE)
    
    if not match:
        return []
    
    sequence_line = match.group(1)
    movements = []
    
    # Dividir por ' > '
    parts = sequence_line.split(' > ')
    
    for part in parts:
        part = part.strip()
        
        # Verificar si tiene el formato NxMOVEMENT_NAME
        count_match = re.match(r'(\d+)x(.+)', part)
        if count_match:
            count = int(count_match.group(1))
            movement_name = count_match.group(2)
            movements.append((movement_name, count))
        else:
            # Movimiento único
            movements.append((part, 1))
    
    return movements

def calculate_danger_percentage(movements):
    """
    Calcula el porcentaje de peligrosidad basado en los movimientos.
    Aplica multiplicadores exponenciales para giros diagonales concatenados.
    
    Args:
        movements: Lista de tuplas (movement_name, count)
    
    Returns:
        float: Porcentaje de peligrosidad (0-100+)
    """
    if not movements:
        return 0.0
    
    total_danger = 0.0
    consecutive_dangerous_count = 0
    total_movements = 0
    
    for movement_name, count in movements:
        base_danger = MOVEMENT_DANGER.get(movement_name, 0)
        
        # Contar movimientos totales
        total_movements += count
        
        for _ in range(count):
            # Determinar si es un movimiento peligroso (danger >= 3)
            if base_danger >= 3:
                consecutive_dangerous_count += 1
                
                # Aplicar multiplicador exponencial basado en concatenación
                # multiplier = 1 + (consecutive_count * 0.3)^1.2
                if consecutive_dangerous_count > 1:
                    multiplier = 1 + pow((consecutive_dangerous_count - 1) * 0.3, 1.2)
                else:
                    multiplier = 1.0
                
                danger_points = base_danger * multiplier
            else:
                # Movimiento seguro o de bajo riesgo
                danger_points = base_danger
                consecutive_dangerous_count = 0  # Reset contador
            
            total_danger += danger_points
    
    # Normalizar el peligro total
    # Usar un factor de escala ajustado basado en movimientos totales
    if total_movements > 0:
        # Factor de escala: asume ~2 puntos promedio por movimiento como "medio"
        # 50% = ~1 punto promedio por movimiento
        danger_percentage = (total_danger / total_movements) * 50.0
    else:
        danger_percentage = 0.0
    
    # Limitar a un rango razonable (0-100), pero permitir valores >100 para casos extremos
    return min(100.0, danger_percentage)

def run_simulator(maze_file, floodfill_type, simulator_path, explore_type):
    """Ejecuta el simulador con un tipo de floodfill y explore específicos"""
    cmd = [simulator_path, f'-floodfill-type={floodfill_type}', f'-explore-type={explore_type}', maze_file]
    
    # DEBUG: Imprimir comando para verificar
    # print(f"    CMD: {' '.join(cmd)}")
    
    try:
        # FIX: encoding='utf-8' con errors='ignore' y verificar None
        result = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            timeout=30,
            encoding='utf-8',
            errors='ignore'
        )
        # Verificar que stdout y stderr no sean None antes de concatenar
        stdout = result.stdout if result.stdout is not None else ""
        stderr = result.stderr if result.stderr is not None else ""
        return stdout + stderr
    except subprocess.TimeoutExpired:
        print(f"  Timeout floodfill {floodfill_type} explore {explore_type}")
        return ""
    except Exception as e:
        print(f"  Error floodfill {floodfill_type} explore {explore_type}: {str(e)[:50]}")
        return ""

def process_maze(simulator_path, maze_folder, output_file, explore_type):
    """Procesa todos los laberintos de la carpeta con un explore_type específico"""
    # Buscar archivos .map y .txt
    maze_files = []
    for ext in ['*.map', '*.txt']:
        maze_files.extend(glob.glob(os.path.join(maze_folder, ext)))
    
    maze_files = sorted(set(maze_files))  # Eliminar duplicados y ordenar
    
    if not maze_files:
        print("No se encontraron archivos .map o .txt")
        return
    
    results = []

    print(f"Procesando {len(maze_files)} laberintos con explore_type={explore_type}...")
    
    for maze_file in maze_files:
        print(f"Procesando: {os.path.basename(maze_file)}")
        
        distances = []
        dangers = []
        cell_counts = []
        times = []
        for floodfill_type in [0, 1, 2, 3]:
            output = run_simulator(maze_file, floodfill_type, simulator_path, explore_type)
            distance = parse_total_distance(output)
            
            if distance is not None:
                distances.append(str(distance))
                print(f"  Floodfill {floodfill_type} - Distancia: {distance}")
            else:
                distances.append("ERROR")
                print(f"  Floodfill {floodfill_type}: ERROR")

            time = parse_total_time(output)
            
            if time is not None:
                times.append(str(time))
                print(f"  Floodfill {floodfill_type} - Tiempo: {time}")
            else:
                times.append("ERROR")
                print(f"  Floodfill {floodfill_type}: ERROR")
            
            # Calcular peligrosidad para este tipo de floodfill
            movements = parse_movement_sequence(output)
            if movements:
                danger_pct = calculate_danger_percentage(movements)
                dangers.append(f"{danger_pct:.1f}")
                print(f"  Floodfill {floodfill_type} - Peligrosidad: {danger_pct:.1f}%")
            else:
                dangers.append("0.0")
                print(f"  Floodfill {floodfill_type} - Peligrosidad: N/A")
            # Extraer número de casillas óptimas
            cell_count = parse_optimal_cells(output)
            cell_counts.append(str(cell_count))
            print(f"  Floodfill {floodfill_type} - Casillas: {cell_count}")
        maze_name = Path(maze_file).stem
        result_line = f"{distances[0]}\t{distances[1]}\t{distances[2]}\t{distances[3]}\t{dangers[0]}\t{dangers[1]}\t{dangers[2]}\t{dangers[3]}\t{cell_counts[0]}\t{cell_counts[1]}\t{cell_counts[2]}\t{cell_counts[3]}\t{times[0]}\t{times[1]}\t{times[2]}\t{times[3]}\t\"{maze_name}\""
        results.append(result_line)
    
    # Escribir resultados al archivo
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("0\t1\t2\t3\tp0\tp1\tp2\tp3\tc0\tc1\tc2\tc3\tt0\tt1\tt2\tt3\tnombre\n")
            for line in results:
                f.write(line + "\n")
        print(f"\nResultados guardados en: {output_file}")
    except Exception as e:
        print(f"Error escribiendo archivo: {e}")
    
    print(f"Total laberintos procesados: {len(results)}")

def parse_optimal_cells(output):
    """
    Extrae el número de casillas óptimas recorridas (cuenta de bloques '  ███  ' en el output).
    """
    if not output:
        return 0
    # Buscar todas las ocurrencias de '  ███  '
    return len(re.findall(r'  ███  ', output))

def parse_optimal_time(output):
    """
    Extrae el tiempo óptimo de la casilla inferior izquierda de la matriz de tiempos floodfill.
    """
    if not output:
        return 0
    # Buscar el bloque de la matriz de tiempos floodfill
    matrix_started = False
    matrix_lines = []
    for line in output.splitlines():
        if '=== TIEMPOS (FLOODFILL) ===' in line:
            matrix_started = True
            continue
        if matrix_started:
            # Fin del bloque si aparece otra sección
            if line.strip().startswith('==='):
                break
            # Solo líneas de matriz (empiezan por '║')
            if line.strip().startswith('║'):
                matrix_lines.append(line)
    if not matrix_lines:
        return 0
    # Tomar la última línea de la matriz
    last_line = matrix_lines[-1]
    # Extraer el primer valor numérico de la última línea (esquina inferior izquierda)
    # Los valores pueden ser float
    match = re.search(r'║\s*([\d\.]+)', last_line)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0
    return 0

def main():
    # Verificar argumentos
    if len(sys.argv) != 2:
        print("Uso: python procesar_laberintos.py <carpeta_laberintos>")
        print("Ejemplo: python procesar_laberintos.py \"C:\\mis_laberintos\"")
        sys.exit(1)
    
    maze_folder = sys.argv[1]
    SIMULATOR_PATH = r".\maze_sim.exe"
    
    # Verificar que la carpeta existe
    if not os.path.exists(maze_folder):
        print(f"ERROR: No se encuentra la carpeta {maze_folder}")
        sys.exit(1)
    
    # Verificar que el simulador existe
    if not os.path.exists(SIMULATOR_PATH):
        print(f"ERROR: No se encuentra el simulador en {SIMULATOR_PATH}")
        print("Asegúrate de que maze_sim.exe está en la carpeta simulator/")
        sys.exit(1)
    
    # Procesar para cada tipo de exploración
    for explore_type in [0, 1, 2]:
        print(f"\n{'='*60}")
        print(f"PROCESANDO EXPLORE_TYPE = {explore_type}")
        print(f"{'='*60}\n")
        
        output_file = f"bulk_run_results_explore_{explore_type}.txt"
        process_maze(SIMULATOR_PATH, maze_folder, output_file, explore_type)

if __name__ == "__main__":
    main()