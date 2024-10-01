# BUS SYSTEM PRO – Versión Simple (Python)

Aplicación de escritorio para gestión de pasajes de bus.
Sin base de datos — todo se guarda en listas en memoria.

## Requisitos
- Python 3.10 o superior
- Tkinter (incluido con Python en Windows)

## Ejecutar
```
python main.py
```

## Cuentas de demo
| Usuario   | Contraseña   | Rol           |
|-----------|-------------|---------------|
| admin     | admin123    | Administrador |
| vendedor  | vendedor123 | Vendedor      |

## Archivos
| Archivo          | Descripción                                      |
|------------------|--------------------------------------------------|
| main.py          | Interfaz gráfica: login, venta, pasajeros, rutas |
| datos.py         | Datos en listas (sin base de datos)              |
| ordenamiento.py  | 5 métodos de ordenamiento                        |

## Métodos de ordenamiento
Accede desde **Pasajeros → botón "Ordenar"**:
1. **Burbuja** – O(n²) – compara pares adyacentes
2. **Selección** – O(n²) – busca el mínimo en cada pasada
3. **Inserción** – O(n²) – inserta en posición correcta
4. **Merge Sort** – O(n log n) – divide y fusiona (recursivo)
5. **Quick Sort** – O(n log n) – pivote y partición (recursivo)
