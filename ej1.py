from ortools.sat.python import cp_model

def optimize_routing():
    # Datos de ejemplo
    num_vehicles = 2
    num_locations = 5
    depot = 0  # La ubicación del almacén central

    # Matriz de distancias entre ubicaciones
    distances = [
        [0, 10, 15, 20, 25],
        [10, 0, 35, 40, 45],
        [15, 35, 0, 50, 55],
        [20, 40, 50, 0, 60],
        [25, 45, 55, 60, 0]
    ]

    # Capacidad de los vehículos
    vehicle_capacity = [100, 100]

    # Demanda de las ubicaciones (dejando el almacén en cero)
    demands = [0, 10, 15, 5, 20]

    # Crear el modelo
    model = cp_model.CpModel()

    # Variables de decisión
    x = {}
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                x[i, j] = model.NewBoolVar(f'x[{i}][{j}]')

    # Función objetivo: minimizar la distancia total recorrida
    model.Minimize(
        sum(distances[i][j] * x[i, j] for i in range(num_locations) for j in range(num_locations) if i != j)
    )

    # Restricciones

    # Cada ubicación es visitada exactamente una vez
    for i in range(num_locations):
        model.Add(sum(x[i, j] for j in range(num_locations) if i != j) == 1)

    # La capacidad de los vehículos no se debe superar
    for v in range(num_vehicles):
        model.Add(sum(demands[j] * x[i, j] for i in range(num_locations) for j in range(num_locations) if i != j) <= vehicle_capacity[v])

    # Restricciones de simetría
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                model.Add(x[i, j] == x[j, i])

    # Crear el solucionador
    solver = cp_model.CpSolver()

    # Configurar parámetros de búsqueda (opcional)
    solver.parameters.max_time_in_seconds = 10

    # Resolver el problema
    status = solver.Solve(model)

    # Mostrar la solución
    if status == cp_model.OPTIMAL:
        print("Solución óptima encontrada")
        print(f"Distancia total recorrida: {solver.ObjectiveValue()}")
        for v in range(num_vehicles):
            print(f"Ruta del vehículo {v + 1}:")
            route = [depot]
            next_location = depot
            while True:
                for j in range(num_locations):
                    if next_location != j and solver.Value(x[next_location, j]) == 1:
                        route.append(j)
                        next_location = j
                        break
                if next_location == depot:
                    break
            print(route)
    else:
        print("No se encontró solución óptima")

if __name__ == "__main__":
    optimize_routing()
