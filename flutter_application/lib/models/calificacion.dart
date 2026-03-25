class Calificacion {
  final int? id;
  final int estudianteId;
  final int materiaId;
  final double calificacion;
  final String periodo;

  Calificacion({
    this.id,
    required this.estudianteId,
    required this.materiaId,
    required this.calificacion,
    this.periodo = '2024-1',
  });

  factory Calificacion.fromJson(Map<String, dynamic> json) {
    return Calificacion(
      id: json['id'] as int?,
      estudianteId: json['estudiante_id'] as int,
      materiaId: json['materia_id'] as int,
      calificacion: (json['calificacion'] as num).toDouble(),
      periodo: json['periodo'] as String? ?? '2024-1',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'estudiante_id': estudianteId,
      'materia_id': materiaId,
      'calificacion': calificacion,
      'periodo': periodo,
    };
  }
}
