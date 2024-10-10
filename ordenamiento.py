# ordenamiento.py – versión final: 5 algoritmos de ordenamiento

def burbuja(lista, clave):
    """Burbuja O(n²): compara e intercambia pares adyacentes."""
    arr = lista[:]
    n = len(arr)
    for i in range(n - 1):
        for j in range(n - 1 - i):
            if clave(arr[j]) > clave(arr[j + 1]):
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def seleccion(lista, clave):
    """Seleccion O(n²): busca el minimo en cada pasada."""
    arr = lista[:]
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if clave(arr[j]) < clave(arr[min_idx]):
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

def insercion(lista, clave):
    """Insercion O(n²): inserta cada elemento en su posicion correcta."""
    arr = lista[:]
    for i in range(1, len(arr)):
        actual = arr[i]; j = i - 1
        while j >= 0 and clave(arr[j]) > clave(actual):
            arr[j + 1] = arr[j]; j -= 1
        arr[j + 1] = actual
    return arr

def merge_sort(lista, clave):
    """Merge Sort O(n log n): divide y fusiona recursivamente."""
    if len(lista) <= 1: return lista[:]
    mid = len(lista) // 2
    izq = merge_sort(lista[:mid], clave)
    der = merge_sort(lista[mid:], clave)
    return _merge(izq, der, clave)

def _merge(izq, der, clave):
    resultado = []; i = j = 0
    while i < len(izq) and j < len(der):
        if clave(izq[i]) <= clave(der[j]):
            resultado.append(izq[i]); i += 1
        else:
            resultado.append(der[j]); j += 1
    resultado.extend(izq[i:]); resultado.extend(der[j:])
    return resultado

def quick_sort(lista, clave):
    """Quick Sort O(n log n): divide por pivote recursivamente."""
    arr = lista[:]
    _quick(arr, 0, len(arr) - 1, clave)
    return arr

def _quick(arr, inicio, fin, clave):
    if inicio < fin:
        p = _particion(arr, inicio, fin, clave)
        _quick(arr, inicio, p - 1, clave)
        _quick(arr, p + 1, fin, clave)

def _particion(arr, inicio, fin, clave):
    pivote = clave(arr[fin]); i = inicio - 1
    for j in range(inicio, fin):
        if clave(arr[j]) <= pivote:
            i += 1; arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[fin] = arr[fin], arr[i + 1]
    return i + 1

METODOS = {
    "Burbuja":    burbuja,
    "Seleccion":  seleccion,
    "Insercion":  insercion,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort,
}
