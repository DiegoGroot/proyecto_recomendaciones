"""
EJEMPLOS DE USO DE LA API
Archivo para demostrar cómo usar la API desde código Python
"""

import requests
import json

# URL base de la API
BASE_URL = "http://localhost:5000/api"

# =====================================================
# FUNCIONES AUXILIARES
# =====================================================

def imprimir_respuesta(titulo, respuesta):
    """Imprime una respuesta formateada"""
    print(f"\n{'='*50}")
    print(f"  {titulo}")
    print(f"{'='*50}")
    print(json.dumps(respuesta.json(), indent=2, ensure_ascii=False))
    print(f"Status Code: {respuesta.status_code}\n")

# =====================================================
# EJEMPLOS CON ESCUELAS
# =====================================================

def ejemplo_crear_escuela():
    """Ejemplo: Crear una nueva escuela"""
    print("\n>>> CREAR ESCUELA")
    
    datos = {
        "nombre": "Escuela Innovadora Digital",
        "ciudad": "Lima",
        "nivel": "primaria",
        "calificacion": 4.6
    }
    
    response = requests.post(f"{BASE_URL}/escuelas", json=datos)
    imprimir_respuesta("POST /api/escuelas", response)
    
    return response.json().get('id')

def ejemplo_obtener_escuelas():
    """Ejemplo: Obtener todas las escuelas"""
    print("\n>>> OBTENER TODAS LAS ESCUELAS")
    
    response = requests.get(f"{BASE_URL}/escuelas")
    imprimir_respuesta("GET /api/escuelas", response)

def ejemplo_filtrar_escuelas():
    """Ejemplo: Filtrar escuelas por ciudad"""
    print("\n>>> FILTRAR ESCUELAS POR CIUDAD")
    
    response = requests.get(f"{BASE_URL}/escuelas?ciudad=Lima")
    imprimir_respuesta("GET /api/escuelas?ciudad=Lima", response)

# =====================================================
# EJEMPLOS CON RECOMENDACIONES
# =====================================================

def ejemplo_crear_recomendacion(escuela_id):
    """Ejemplo: Crear una recomendación"""
    print("\n>>> CREAR RECOMENDACIÓN")
    
    datos = {
        "escuela_id": escuela_id,
        "estudiante": "Laura Fernández",
        "motivo": "Infraestructura moderna y profesores certificados",
        "calificacion": 5
    }
    
    response = requests.post(f"{BASE_URL}/recomendaciones", json=datos)
    imprimir_respuesta("POST /api/recomendaciones", response)
    
    return response.json().get('id')

def ejemplo_obtener_recomendaciones():
    """Ejemplo: Obtener todas las recomendaciones"""
    print("\n>>> OBTENER TODAS LAS RECOMENDACIONES")
    
    response = requests.get(f"{BASE_URL}/recomendaciones")
    imprimir_respuesta("GET /api/recomendaciones", response)

def ejemplo_filtrar_recomendaciones():
    """Ejemplo: Filtrar recomendaciones por calificación"""
    print("\n>>> FILTRAR RECOMENDACIONES POR CALIFICACIÓN")
    
    response = requests.get(f"{BASE_URL}/recomendaciones?calificacion=5")
    imprimir_respuesta("GET /api/recomendaciones?calificacion=5", response)

def ejemplo_obtener_recomendacion(rec_id):
    """Ejemplo: Obtener una recomendación específica"""
    print("\n>>> OBTENER RECOMENDACIÓN ESPECÍFICA")
    
    response = requests.get(f"{BASE_URL}/recomendaciones/{rec_id}")
    imprimir_respuesta(f"GET /api/recomendaciones/{rec_id}", response)

def ejemplo_actualizar_recomendacion(rec_id):
    """Ejemplo: Actualizar una recomendación"""
    print("\n>>> ACTUALIZAR RECOMENDACIÓN")
    
    datos = {
        "calificacion": 5,
        "estado": "actualizada",
        "motivo": "Actualización: Excelente programa complementario agregado"
    }
    
    response = requests.put(f"{BASE_URL}/recomendaciones/{rec_id}", json=datos)
    imprimir_respuesta(f"PUT /api/recomendaciones/{rec_id}", response)

def ejemplo_buscar_recomendaciones():
    """Ejemplo: Búsqueda avanzada"""
    print("\n>>> BÚSQUEDA AVANZADA")
    
    response = requests.get(f"{BASE_URL}/recomendaciones/buscar?q=Laura&min_cal=4&max_cal=5")
    imprimir_respuesta("GET /api/recomendaciones/buscar?q=Laura&min_cal=4&max_cal=5", response)

def ejemplo_eliminar_recomendacion(rec_id):
    """Ejemplo: Eliminar una recomendación"""
    print("\n>>> ELIMINAR RECOMENDACIÓN")
    
    response = requests.delete(f"{BASE_URL}/recomendaciones/{rec_id}")
    imprimir_respuesta(f"DELETE /api/recomendaciones/{rec_id}", response)

# =====================================================
# HEALTH CHECK
# =====================================================

def ejemplo_health_check():
    """Ejemplo: Verificar estado de la API"""
    print("\n>>> HEALTH CHECK")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        imprimir_respuesta("GET /api/health", response)
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Error: No se pudo conectar a la API")
        print("Asegúrate de que la API está ejecutándose en http://localhost:5000")
        return False

# =====================================================
# EJEMPLO COMPLETO DE USO
# =====================================================

def ejecutar_ejemplo_completo():
    """Ejecuta un flujo completo de ejemplo"""
    
    print("\n" + "="*50)
    print("  EJEMPLO COMPLETO DE USO DE LA API")
    print("="*50)
    
    # Verificar que la API está disponible
    if not ejemplo_health_check():
        return
    
    # Crear escuela
    escuela_id = ejemplo_crear_escuela()
    
    # Obtener todas las escuelas
    ejemplo_obtener_escuelas()
    
    # Filtrar escuelas
    ejemplo_filtrar_escuelas()
    
    # Crear recomendación
    rec_id = ejemplo_crear_recomendacion(escuela_id)
    
    # Obtener todas las recomendaciones
    ejemplo_obtener_recomendaciones()
    
    # Filtrar recomendaciones
    ejemplo_filtrar_recomendaciones()
    
    # Obtener una recomendación específica
    ejemplo_obtener_recomendacion(rec_id)
    
    # Actualizar recomendación
    ejemplo_actualizar_recomendacion(rec_id)
    
    # Búsqueda avanzada
    ejemplo_buscar_recomendaciones()
    
    # Nota: No eliminar en el ejemplo para mantener datos para referencias
    # ejemplo_eliminar_recomendacion(rec_id)
    
    print("\n" + "="*50)
    print("  ✓ EJEMPLO COMPLETADO EXITOSAMENTE")
    print("="*50 + "\n")

# =====================================================
# CLASE WRAPPER PARA USO MÁS FÁCIL
# =====================================================

class ClienteAPI:
    """Cliente Python para interactuar con la API"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
    
    # --- ESCUELAS ---
    
    def crear_escuela(self, nombre, ciudad="", nivel="primaria", calificacion=0.0):
        """Crea una nueva escuela"""
        datos = {
            "nombre": nombre,
            "ciudad": ciudad,
            "nivel": nivel,
            "calificacion": calificacion
        }
        return requests.post(f"{self.base_url}/escuelas", json=datos).json()
    
    def obtener_escuelas(self, ciudad=None, nivel=None):
        """Obtiene escuelas con filtros opcionales"""
        params = {}
        if ciudad:
            params['ciudad'] = ciudad
        if nivel:
            params['nivel'] = nivel
        return requests.get(f"{self.base_url}/escuelas", params=params).json()
    
    # --- RECOMENDACIONES ---
    
    def crear_recomendacion(self, escuela_id, estudiante, motivo="", calificacion=3):
        """Crea una nueva recomendación"""
        datos = {
            "escuela_id": escuela_id,
            "estudiante": estudiante,
            "motivo": motivo,
            "calificacion": calificacion
        }
        return requests.post(f"{self.base_url}/recomendaciones", json=datos).json()
    
    def obtener_recomendaciones(self, calificacion=None, estado="activa", escuela_id=None):
        """Obtiene recomendaciones con filtros"""
        params = {}
        if calificacion:
            params['calificacion'] = calificacion
        if estado:
            params['estado'] = estado
        if escuela_id:
            params['escuela_id'] = escuela_id
        return requests.get(f"{self.base_url}/recomendaciones", params=params).json()
    
    def obtener_recomendacion(self, id):
        """Obtiene una recomendación específica"""
        return requests.get(f"{self.base_url}/recomendaciones/{id}").json()
    
    def actualizar_recomendacion(self, id, **kwargs):
        """Actualiza una recomendación"""
        return requests.put(f"{self.base_url}/recomendaciones/{id}", json=kwargs).json()
    
    def eliminar_recomendacion(self, id):
        """Elimina una recomendación"""
        return requests.delete(f"{self.base_url}/recomendaciones/{id}").json()
    
    def buscar_recomendaciones(self, q="", min_cal=None, max_cal=None):
        """Búsqueda avanzada de recomendaciones"""
        params = {}
        if q:
            params['q'] = q
        if min_cal:
            params['min_cal'] = min_cal
        if max_cal:
            params['max_cal'] = max_cal
        return requests.get(f"{self.base_url}/recomendaciones/buscar", params=params).json()

# =====================================================
# EJEMPLO DE USO DE LA CLASE WRAPPER
# =====================================================

def ejemplo_con_wrapper():
    """Ejemplo usando la clase ClienteAPI"""
    print("\n" + "="*50)
    print("  EJEMPLO USANDO WRAPPER CLIENT")
    print("="*50 + "\n")
    
    cliente = ClienteAPI()
    
    # Crear escuela
    escuela = cliente.crear_escuela(
        nombre="Escuela Wrapper Test",
        ciudad="Lima",
        nivel="secundaria",
        calificacion=4.5
    )
    print(f"Escuela creada: {escuela}")
    
    if escuela.get('success'):
        escuela_id = escuela['id']
        
        # Crear recomendación
        rec = cliente.crear_recomendacion(
            escuela_id=escuela_id,
            estudiante="Diego Test",
            motivo="Prueba de wrapper",
            calificacion=5
        )
        print(f"\nRecomendación creada: {rec}")
        
        # Obtener recomendaciones
        recos = cliente.obtener_recomendaciones(escuela_id=escuela_id)
        print(f"\nRecomendaciones: {json.dumps(recos, indent=2, ensure_ascii=False)}")

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":
    print("\n🚀 EJEMPLOS DE USO DE LA API DE RECOMENDACIONES ESCOLARES\n")
    print("Asegúrate de:") 
    print("1. Tener MySQL ejecutándose")
    print("2. Ejecutar 'python app.py' en otra terminal")
    print("3. Ejecutar este script con 'python ejemplos.py'\n")
    
    # Ejecutar ejemplo completo
    ejecutar_ejemplo_completo()
    
    # Ejecutar ejemplo con wrapper (comentar si es necesario)
    # ejemplo_con_wrapper()
