import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/carrera.dart';
import '../models/materia.dart';
import '../models/estudiante.dart';
import '../models/calificacion.dart';

class ApiService {
  static const String baseUrl = 'http://localhost:8000/api';

  // CARRERAS
  static Future<List<Carrera>> getCarreras() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/carreras'));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body) as List<dynamic>;
        return data.map((c) => Carrera.fromJson(c as Map<String, dynamic>)).toList();
      }
      throw Exception('Error al cargar carreras');
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> createCarrera(Carrera carrera) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/carreras'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(carrera.toJson()),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al crear carrera');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> updateCarrera(int id, Carrera carrera) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/carreras/$id'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(carrera.toJson()),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al actualizar carrera');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> deleteCarrera(int id) async {
    try {
      final response = await http.delete(Uri.parse('$baseUrl/carreras/$id'));
      if (response.statusCode != 200) {
        throw Exception('Error al eliminar carrera');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // MATERIAS
  static Future<List<Materia>> getMaterias() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/materias'));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body) as List<dynamic>;
        return data.map((m) => Materia.fromJson(m as Map<String, dynamic>)).toList();
      }
      throw Exception('Error al cargar materias');
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> createMateria(Materia materia) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/materias'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(materia.toJson()),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al crear materia');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> updateMateria(int id, Materia materia) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/materias/$id'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(materia.toJson()),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al actualizar materia');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> deleteMateria(int id) async {
    try {
      final response = await http.delete(Uri.parse('$baseUrl/materias/$id'));
      if (response.statusCode != 200) {
        throw Exception('Error al eliminar materia');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // ESTUDIANTES
  static Future<List<Estudiante>> getEstudiantes() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/estudiantes'));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body) as List<dynamic>;
        return data.map((e) => Estudiante.fromJson(e as Map<String, dynamic>)).toList();
      }
      throw Exception('Error al cargar estudiantes');
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> createEstudiante(Estudiante estudiante) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/estudiantes'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(estudiante.toJson()),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al crear estudiante');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> updateEstudiante(int id, Estudiante estudiante) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/estudiantes/$id'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(estudiante.toJson()),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al actualizar estudiante');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> deleteEstudiante(int id) async {
    try {
      final response = await http.delete(Uri.parse('$baseUrl/estudiantes/$id'));
      if (response.statusCode != 200) {
        throw Exception('Error al eliminar estudiante');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  // CALIFICACIONES
  static Future<List<Calificacion>> getCalificaciones() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/calificaciones'));
      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body) as List<dynamic>;
        return data.map((c) => Calificacion.fromJson(c as Map<String, dynamic>)).toList();
      }
      throw Exception('Error al cargar calificaciones');
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> createCalificacion(Calificacion calificacion) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/calificaciones'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(calificacion.toJson()),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al crear calificación');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> updateCalificacion(int id, Calificacion calificacion) async {
    try {
      final response = await http.put(
        Uri.parse('$baseUrl/calificaciones/$id'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'calificacion': calificacion.calificacion,
          'periodo': calificacion.periodo,
        }),
      );
      if (response.statusCode != 200) {
        throw Exception('Error al actualizar calificación');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }

  static Future<void> deleteCalificacion(int id) async {
    try {
      final response = await http.delete(Uri.parse('$baseUrl/calificaciones/$id'));
      if (response.statusCode != 200) {
        throw Exception('Error al eliminar calificación');
      }
    } catch (e) {
      throw Exception('Error: $e');
    }
  }
}
