import 'package:flutter/material.dart';
import '../models/estudiante.dart';
import '../models/carrera.dart';
import '../services/api_service.dart';

class EstudiantesScreen extends StatefulWidget {
  const EstudiantesScreen({super.key});

  @override
  State<EstudiantesScreen> createState() => _EstudiantesScreenState();
}

class _EstudiantesScreenState extends State<EstudiantesScreen> {
  late Future<List<Estudiante>> _futureEstudiantes;
  late Future<List<Carrera>> _futureCarreras;
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _emailController = TextEditingController();
  int? _selectedCarreraId;
  Estudiante? _editingEstudiante;

  @override
  void initState() {
    super.initState();
    _futureEstudiantes = ApiService.getEstudiantes();
    _futureCarreras = ApiService.getCarreras();
  }

  void _showDialog({Estudiante? estudiante}) {
    if (estudiante != null) {
      _nombreController.text = estudiante.nombre;
      _emailController.text = estudiante.email;
      _selectedCarreraId = estudiante.carreraId;
      _editingEstudiante = estudiante;
    } else {
      _nombreController.clear();
      _emailController.clear();
      _selectedCarreraId = null;
      _editingEstudiante = null;
    }

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(estudiante != null ? 'Editar Estudiante' : 'Nuevo Estudiante'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: _nombreController,
              decoration: const InputDecoration(labelText: 'Nombre'),
            ),
            TextField(
              controller: _emailController,
              decoration: const InputDecoration(labelText: 'Email'),
              keyboardType: TextInputType.emailAddress,
            ),
            FutureBuilder<List<Carrera>>(
              future: _futureCarreras,
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return DropdownButton<int>(
                    hint: const Text('Selecciona carrera'),
                    value: _selectedCarreraId,
                    items: snapshot.data!
                        .map((c) => DropdownMenuItem(
                              value: c.id,
                              child: Text(c.nombre),
                            ))
                        .toList(),
                    onChanged: (value) {
                      setState(() {
                        _selectedCarreraId = value;
                      });
                    },
                  );
                }
                return const CircularProgressIndicator();
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancelar'),
          ),
          TextButton(
            onPressed: () async {
              final navigator = Navigator.of(context);
              final scaffoldMessenger = ScaffoldMessenger.of(context);
              try {
                final estudiante = Estudiante(
                  nombre: _nombreController.text,
                  email: _emailController.text,
                  carreraId: _selectedCarreraId!,
                );
                if (_editingEstudiante != null) {
                  await ApiService.updateEstudiante(_editingEstudiante!.id!, estudiante);
                } else {
                  await ApiService.createEstudiante(estudiante);
                }
                if (!mounted) return;
                setState(() {
                  _futureEstudiantes = ApiService.getEstudiantes();
                });
                navigator.pop();
              } catch (e) {
                if (!mounted) return;
                scaffoldMessenger.showSnackBar(
                  SnackBar(content: Text('Error: $e')),
                );
              }
            },
            child: const Text('Guardar'),
          ),
        ],
      ),
    );
  }

  void _deleteEstudiante(int id) async {
    try {
      await ApiService.deleteEstudiante(id);
      if (!mounted) return;
      setState(() {
        _futureEstudiantes = ApiService.getEstudiantes();
      });
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Estudiantes'),
        actions: [
          FloatingActionButton(
            onPressed: () => _showDialog(),
            child: const Icon(Icons.add),
          ),
        ],
      ),
      body: FutureBuilder<List<Estudiante>>(
        future: _futureEstudiantes,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else {
            final estudiantes = snapshot.data ?? [];
            return ListView.builder(
              itemCount: estudiantes.length,
              itemBuilder: (context, index) {
                final estudiante = estudiantes[index];
                return ListTile(
                  title: Text(estudiante.nombre),
                  subtitle: Text(estudiante.email),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.edit),
                        onPressed: () => _showDialog(estudiante: estudiante),
                      ),
                      IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () => _deleteEstudiante(estudiante.id!),
                      ),
                    ],
                  ),
                );
              },
            );
          }
        },
      ),
    );
  }

  @override
  void dispose() {
    _nombreController.dispose();
    _emailController.dispose();
    super.dispose();
  }
}
