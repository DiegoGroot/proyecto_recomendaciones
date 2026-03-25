class Carrera {
  final int? id;
  final String nombre;
  final String? descripcion;

  Carrera({
    this.id,
    required this.nombre,
    this.descripcion,
  });

  factory Carrera.fromJson(Map<String, dynamic> json) {
    return Carrera(
      id: json['id'] as int?,
      nombre: json['nombre'] as String,
      descripcion: json['descripcion'] as String?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'nombre': nombre,
      'descripcion': descripcion,
    };
  }
}
