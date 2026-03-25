class Estudiante {
  final int? id;
  final String nombre;
  final String email;
  final int carreraId;

  Estudiante({
    this.id,
    required this.nombre,
    required this.email,
    required this.carreraId,
  });

  factory Estudiante.fromJson(Map<String, dynamic> json) {
    return Estudiante(
      id: json['id'] as int?,
      nombre: json['nombre'] as String,
      email: json['email'] as String,
      carreraId: json['carrera_id'] as int,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'nombre': nombre,
      'email': email,
      'carrera_id': carreraId,
    };
  }
}
