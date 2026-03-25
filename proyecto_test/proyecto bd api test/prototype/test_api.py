import pytest
import json
from app import app, init_database
from database import db
import mysql.connector

@pytest.fixture
def client():
    """Configurar cliente de prueba"""
    app.config['TESTING'] = True
    init_database()
    
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """Configurar y limpiar BD para cada test"""
    db.connect()
    
    # Limpiar datos antes de cada test
    try:
        db.execute_update("DELETE FROM recomendaciones")
        db.execute_update("DELETE FROM escuelas")
    except:
        pass
    
    db.disconnect()
    yield

# ============================================
# TESTS - HEALTH CHECK
# ============================================

def test_health_check(client):
    """Verifica que la API responde correctamente"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json['status'] == 'OK'

# ============================================
# TESTS - ESCUELAS
# ============================================

def test_crear_escuela(client):
    """Test crear una escuela"""
    data = {
        'nombre': 'Escuela Primaria Ejemplo',
        'ciudad': 'Lima',
        'nivel': 'primaria',
        'calificacion': 4.5
    }
    
    response = client.post('/api/escuelas', 
                          json=data,
                          content_type='application/json')
    
    assert response.status_code == 201
    assert response.json['success'] is True
    assert 'id' in response.json

def test_crear_escuela_sin_nombre(client):
    """Test crear escuela sin nombre (debe fallar)"""
    data = {'ciudad': 'Lima'}
    
    response = client.post('/api/escuelas',
                          json=data,
                          content_type='application/json')
    
    assert response.status_code == 400
    assert response.json['success'] is False

def test_obtener_escuelas(client):
    """Test obtener lista de escuelas"""
    # Crear dos escuelas
    escuelas = [
        {'nombre': 'Escuela A', 'ciudad': 'Lima', 'nivel': 'primaria'},
        {'nombre': 'Escuela B', 'ciudad': 'bar', 'nivel': 'secundaria'}
    ]
    
    for escuela in escuelas:
        client.post('/api/escuelas', json=escuela, content_type='application/json')
    
    response = client.get('/api/escuelas')
    
    assert response.status_code == 200
    assert response.json['count'] == 2
    assert response.json['success'] is True

def test_obtener_escuelas_por_ciudad(client):
    """Test filtrar escuelas por ciudad"""
    escuelas = [
        {'nombre': 'Escuela A', 'ciudad': 'Lima'},
        {'nombre': 'Escuela B', 'ciudad': 'Arequipa'}
    ]
    
    for escuela in escuelas:
        client.post('/api/escuelas', json=escuela, content_type='application/json')
    
    response = client.get('/api/escuelas?ciudad=Lima')
    
    assert response.status_code == 200
    assert response.json['count'] == 1
    assert response.json['data'][0]['nombre'] == 'Escuela A'

# ============================================
# TESTS - RECOMENDACIONES
# ============================================

def test_crear_recomendacion(client):
    """Test crear una recomendación"""
    # Primero crear una escuela
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    # Crear recomendación
    data = {
        'escuela_id': escuela_id,
        'estudiante': 'Juan Pérez',
        'motivo': 'Excelente educación',
        'calificacion': 5
    }
    
    response = client.post('/api/recomendaciones',
                          json=data,
                          content_type='application/json')
    
    assert response.status_code == 201
    assert response.json['success'] is True

def test_crear_recomendacion_calificacion_invalida(client):
    """Test crear recomendación con calificación inválida"""
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    data = {
        'escuela_id': escuela_id,
        'estudiante': 'Juan Pérez',
        'calificacion': 10  # Inválido
    }
    
    response = client.post('/api/recomendaciones',
                          json=data,
                          content_type='application/json')
    
    assert response.status_code == 400
    assert response.json['success'] is False

def test_obtener_recomendaciones(client):
    """Test obtener lista de recomendaciones"""
    # Crear escuela
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    # Crear recomendaciones
    recomendaciones = [
        {'escuela_id': escuela_id, 'estudiante': 'Juan', 'calificacion': 5},
        {'escuela_id': escuela_id, 'estudiante': 'María', 'calificacion': 4}
    ]
    
    for rec in recomendaciones:
        client.post('/api/recomendaciones', json=rec, content_type='application/json')
    
    response = client.get('/api/recomendaciones')
    
    assert response.status_code == 200
    assert response.json['count'] == 2

def test_filtrar_recomendaciones_por_calificacion(client):
    """Test filtrar recomendaciones por calificación"""
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    # Crear recomendaciones con diferentes calificaciones
    for cal in [3, 4, 5]:
        client.post('/api/recomendaciones',
                   json={'escuela_id': escuela_id, 'estudiante': f'Est{cal}', 'calificacion': cal},
                   content_type='application/json')
    
    response = client.get('/api/recomendaciones?calificacion=5')
    
    assert response.status_code == 200
    assert response.json['count'] == 1
    assert response.json['data'][0]['calificacion'] == 5

def test_obtener_recomendacion_por_id(client):
    """Test obtener una recomendación específica"""
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    rec = client.post('/api/recomendaciones',
                     json={'escuela_id': escuela_id, 'estudiante': 'Juan', 'calificacion': 5},
                     content_type='application/json')
    rec_id = rec.json['id']
    
    response = client.get(f'/api/recomendaciones/{rec_id}')
    
    assert response.status_code == 200
    assert response.json['data']['estudiante'] == 'Juan'

def test_actualizar_recomendacion(client):
    """Test actualizar una recomendación"""
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    rec = client.post('/api/recomendaciones',
                     json={'escuela_id': escuela_id, 'estudiante': 'Juan', 'calificacion': 3},
                     content_type='application/json')
    rec_id = rec.json['id']
    
    # Actualizar
    response = client.put(f'/api/recomendaciones/{rec_id}',
                         json={'calificacion': 5, 'estado': 'actualizada'},
                         content_type='application/json')
    
    assert response.status_code == 200
    assert response.json['success'] is True
    
    # Verificar cambio
    get_response = client.get(f'/api/recomendaciones/{rec_id}')
    assert get_response.json['data']['calificacion'] == 5

def test_eliminar_recomendacion(client):
    """Test eliminar una recomendación"""
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    rec = client.post('/api/recomendaciones',
                     json={'escuela_id': escuela_id, 'estudiante': 'Juan', 'calificacion': 5},
                     content_type='application/json')
    rec_id = rec.json['id']
    
    response = client.delete(f'/api/recomendaciones/{rec_id}')
    
    assert response.status_code == 200
    
    # Verificar que no existe
    get_response = client.get(f'/api/recomendaciones/{rec_id}')
    assert get_response.status_code == 404

def test_buscar_recomendaciones(client):
    """Test búsqueda avanzada"""
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Técnica'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    # Crear recomendaciones
    client.post('/api/recomendaciones',
               json={'escuela_id': escuela_id, 'estudiante': 'Juan López', 'calificacion': 5},
               content_type='application/json')
    
    client.post('/api/recomendaciones',
               json={'escuela_id': escuela_id, 'estudiante': 'María García', 'calificacion': 3},
               content_type='application/json')
    
    # Buscar por nombre de estudiante
    response = client.get('/api/recomendaciones/buscar?q=Juan')
    
    assert response.status_code == 200
    assert response.json['count'] == 1
    assert 'Juan' in response.json['data'][0]['estudiante']

def test_buscar_recomendaciones_por_rango_calificacion(client):
    """Test buscar por rango de calificación"""
    escuela = client.post('/api/escuelas',
                         json={'nombre': 'Escuela Test'},
                         content_type='application/json')
    escuela_id = escuela.json['id']
    
    for cal in [1, 2, 3, 4, 5]:
        client.post('/api/recomendaciones',
                   json={'escuela_id': escuela_id, 'estudiante': f'Est{cal}', 'calificacion': cal},
                   content_type='application/json')
    
    response = client.get('/api/recomendaciones/buscar?min_cal=4&max_cal=5')
    
    assert response.status_code == 200
    assert response.json['count'] == 2

# ============================================
# TESTS - ERRORES
# ============================================

def test_endpoint_no_encontrado(client):
    """Test endpoint inexistente"""
    response = client.get('/api/no-existe')
    assert response.status_code == 404

def test_recomendacion_no_encontrada(client):
    """Test obtener recomendación que no existe"""
    response = client.get('/api/recomendaciones/99999')
    assert response.status_code == 404
