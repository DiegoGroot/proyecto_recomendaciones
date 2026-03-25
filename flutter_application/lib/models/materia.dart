class Materia {
  final int? id;
  final String nombre;
  final int carreraId;
  final int creditos;

  Materia({
    this.id,
    required this.nombre,
    required this.carreraId,
    this.creditos = 3,
  });

  factory Materia.fromJson(Map<String, dynamic> json) {
    return Materia(
      id: json['id'] as int?,
      nombre: json['nombre'] as String,
      carreraId: json['carrera_id'] as int,
      creditos: json['creditos'] as int? ?? 3,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'nombre': nombre,
      'carrera_id': carreraId,
      'creditos': creditos,
    };
  }
}
