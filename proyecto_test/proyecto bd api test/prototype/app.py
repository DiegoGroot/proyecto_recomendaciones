from flask import Flask, request, jsonify
from flask_cors import CORS
from database import db
from config import DB_CONFIG
import mysql.connector

app = Flask(__name__)
CORS(app)

# ============================================
# INICIALIZACIÓN Y VERIFICACIÓN DE BD
# ============================================

def init_database():
    """Crea la BD y tablas si no existen"""
    try:
        # Conectar sin base de datos para crearla
        config_temp = DB_CONFIG.copy()
        database = config_temp.pop('database')
        
        conn = mysql.connector.connect(**config_temp)
        cursor = conn.cursor()
        
        # Crear base de datos
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        conn.database = database
        
        # Crear tabla de escuelas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS escuelas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                ciudad VARCHAR(100),
                nivel VARCHAR(50),
                calificacion DECIMAL(3,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de recomendaciones
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recomendaciones (
                id INT AUTO_INCREMENT PRIMARY KEY,
                escuela_id INT NOT NULL,
                estudiante VARCHAR(100),
                motivo TEXT,
                calificacion INT CHECK(calificacion >= 1 AND calificacion <= 5),
                estado VARCHAR(20) DEFAULT 'activa',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (escuela_id) REFERENCES escuelas(id) ON DELETE CASCADE
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✓ Base de datos inicializada correctamente")
        return True
    except Exception as e:
        print(f"✗ Error inicializando BD: {e}")
        return False

# Inicializar BD
init_database()

# ============================================
# ENDPOINTS - RECOMENDACIONES
# ============================================

@app.route('/api/recomendaciones', methods=['GET'])
def get_recomendaciones():
    """Obtiene todas las recomendaciones con filtros opcionales"""
    db.connect()
    
    try:
        # Parámetros de filtro
        calificacion = request.args.get('calificacion', type=int)
        estado = request.args.get('estado', default='activa')
        escuela_id = request.args.get('escuela_id', type=int)
        
        query = "SELECT * FROM recomendaciones WHERE 1=1"
        params = []
        
        if estado:
            query += " AND estado = %s"
            params.append(estado)
        
        if calificacion:
            query += " AND calificacion = %s"
            params.append(calificacion)
        
        if escuela_id:
            query += " AND escuela_id = %s"
            params.append(escuela_id)
        
        query += " ORDER BY created_at DESC"
        
        resultados = db.execute_query(query, params)
        
        return jsonify({
            'success': True,
            'count': len(resultados) if resultados else 0,
            'data': resultados
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/api/recomendaciones/<int:id>', methods=['GET'])
def get_recomendacion(id):
    """Obtiene una recomendación específica"""
    db.connect()
    
    try:
        resultado = db.execute_query(
            "SELECT * FROM recomendaciones WHERE id = %s", 
            [id]
        )
        
        if not resultado:
            return jsonify({'success': False, 'error': 'Recomendación no encontrada'}), 404
        
        return jsonify({'success': True, 'data': resultado[0]}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/api/recomendaciones', methods=['POST'])
def crear_recomendacion():
    """Crea una nueva recomendación"""
    db.connect()
    
    try:
        data = request.get_json()
        
        # Validaciones
        if not data.get('escuela_id') or not data.get('estudiante'):
            return jsonify({'success': False, 'error': 'Falta escuela_id o estudiante'}), 400
        
        if not 1 <= data.get('calificacion', 0) <= 5:
            return jsonify({'success': False, 'error': 'Calificación debe estar entre 1 y 5'}), 400
        
        # Verificar que la escuela existe
        escuela = db.execute_query(
            "SELECT id FROM escuelas WHERE id = %s",
            [data['escuela_id']]
        )
        
        if not escuela:
            return jsonify({'success': False, 'error': 'Escuela no encontrada'}), 404
        
        # Insertar recomendación
        query = """
            INSERT INTO recomendaciones (escuela_id, estudiante, motivo, calificacion)
            VALUES (%s, %s, %s, %s)
        """
        params = [
            data['escuela_id'],
            data['estudiante'],
            data.get('motivo', ''),
            data.get('calificacion', 3)
        ]
        
        id_nuevo = db.execute_insert(query, params)
        
        if id_nuevo:
            return jsonify({
                'success': True,
                'message': 'Recomendación creada',
                'id': id_nuevo
            }), 201
        else:
            return jsonify({'success': False, 'error': 'Error al crear'}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/api/recomendaciones/<int:id>', methods=['PUT'])
def actualizar_recomendacion(id):
    """Actualiza una recomendación existente"""
    db.connect()
    
    try:
        data = request.get_json()
        
        # Verificar que existe
        resultado = db.execute_query(
            "SELECT id FROM recomendaciones WHERE id = %s",
            [id]
        )
        
        if not resultado:
            return jsonify({'success': False, 'error': 'Recomendación no encontrada'}), 404
        
        # Construir query dinámicamente
        updates = []
        params = []
        
        if 'estudiante' in data:
            updates.append("estudiante = %s")
            params.append(data['estudiante'])
        
        if 'motivo' in data:
            updates.append("motivo = %s")
            params.append(data['motivo'])
        
        if 'calificacion' in data:
            if not 1 <= data['calificacion'] <= 5:
                return jsonify({'success': False, 'error': 'Calificación inválida'}), 400
            updates.append("calificacion = %s")
            params.append(data['calificacion'])
        
        if 'estado' in data:
            updates.append("estado = %s")
            params.append(data['estado'])
        
        if not updates:
            return jsonify({'success': False, 'error': 'No hay campos para actualizar'}), 400
        
        params.append(id)
        query = f"UPDATE recomendaciones SET {', '.join(updates)} WHERE id = %s"
        
        db.execute_update(query, params)
        
        return jsonify({'success': True, 'message': 'Recomendación actualizada'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/api/recomendaciones/<int:id>', methods=['DELETE'])
def eliminar_recomendacion(id):
    """Elimina una recomendación"""
    db.connect()
    
    try:
        rows = db.execute_update(
            "DELETE FROM recomendaciones WHERE id = %s",
            [id]
        )
        
        if rows == 0:
            return jsonify({'success': False, 'error': 'Recomendación no encontrada'}), 404
        
        return jsonify({'success': True, 'message': 'Recomendación eliminada'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/api/recomendaciones/buscar', methods=['GET'])
def buscar_recomendaciones():
    """Búsqueda avanzada de recomendaciones"""
    db.connect()
    
    try:
        busqueda = request.args.get('q', '')
        min_calificacion = request.args.get('min_cal', type=int)
        max_calificacion = request.args.get('max_cal', type=int)
        
        query = """
            SELECT r.*, e.nombre as escuela_nombre 
            FROM recomendaciones r
            JOIN escuelas e ON r.escuela_id = e.id
            WHERE 1=1
        """
        params = []
        
        if busqueda:
            query += " AND (r.estudiante LIKE %s OR r.motivo LIKE %s OR e.nombre LIKE %s)"
            busqueda_pattern = f"%{busqueda}%"
            params = [busqueda_pattern, busqueda_pattern, busqueda_pattern]
        
        if min_calificacion is not None:
            query += " AND r.calificacion >= %s"
            params.append(min_calificacion)
        
        if max_calificacion is not None:
            query += " AND r.calificacion <= %s"
            params.append(max_calificacion)
        
        query += " ORDER BY r.created_at DESC"
        
        resultados = db.execute_query(query, params if params else None)
        
        return jsonify({
            'success': True,
            'count': len(resultados) if resultados else 0,
            'data': resultados
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

# ============================================
# ENDPOINTS - ESCUELAS
# ============================================

@app.route('/api/escuelas', methods=['GET'])
def get_escuelas():
    """Obtiene todas las escuelas"""
    db.connect()
    
    try:
        ciudad = request.args.get('ciudad')
        nivel = request.args.get('nivel')
        
        query = "SELECT * FROM escuelas WHERE 1=1"
        params = []
        
        if ciudad:
            query += " AND ciudad = %s"
            params.append(ciudad)
        
        if nivel:
            query += " AND nivel = %s"
            params.append(nivel)
        
        query += " ORDER BY nombre ASC"
        
        resultados = db.execute_query(query, params)
        
        return jsonify({
            'success': True,
            'count': len(resultados) if resultados else 0,
            'data': resultados
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

@app.route('/api/escuelas', methods=['POST'])
def crear_escuela():
    """Crea una nueva escuela"""
    db.connect()
    
    try:
        data = request.get_json()
        
        if not data.get('nombre'):
            return jsonify({'success': False, 'error': 'Nombre es requerido'}), 400
        
        query = """
            INSERT INTO escuelas (nombre, ciudad, nivel, calificacion)
            VALUES (%s, %s, %s, %s)
        """
        params = [
            data['nombre'],
            data.get('ciudad', ''),
            data.get('nivel', 'primaria'),
            data.get('calificacion', 0.00)
        ]
        
        id_nuevo = db.execute_insert(query, params)
        
        if id_nuevo:
            return jsonify({
                'success': True,
                'message': 'Escuela creada',
                'id': id_nuevo
            }), 201
        else:
            return jsonify({'success': False, 'error': 'Error al crear'}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.disconnect()

# ============================================
# HEALTH CHECK
# ============================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica el estado de la API"""
    return jsonify({
        'status': 'OK',
        'message': 'API de recomendaciones escolar funcionando'
    }), 200

# ============================================
# MANEJO DE ERRORES
# ============================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
