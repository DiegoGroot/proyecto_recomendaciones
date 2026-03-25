import 'package:flutter/material.dart';
import '../models/materia.dart';
import '../models/carrera.dart';
import '../services/api_service.dart';

class MateriasScreen extends StatefulWidget {
  const MateriasScreen({super.key});

  @override
  State<MateriasScreen> createState() => _MateriasScreenState();
}

class _MateriasScreenState extends State<MateriasScreen> {
  late Future<List<Materia>> _futureMaterias;
  late Future<List<Carrera>> _futureCarreras;
  final TextEditingController _nombreController = TextEditingController();
  final TextEditingController _creditosController = TextEditingController();
  int? _selectedCarreraId;
  Materia? _editingMateria;

  @override
  void initState() {
    super.initState();
    _futureMaterias = ApiService.getMaterias();
    _futureCarreras = ApiService.getCarreras();
  }

  void _showDialog({Materia? materia}) {
    if (materia != null) {
      _nombreController.text = materia.nombre;
      _creditosController.text = materia.creditos.toString();
      _selectedCarreraId = materia.carreraId;
      _editingMateria = materia;
    } else {
      _nombreController.clear();
      _creditosController.clear();
      _selectedCarreraId = null;
      _editingMateria = null;
    }

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(materia != null ? 'Editar Materia' : 'Nueva Materia'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            TextField(
              controller: _nombreController,
              decoration: const InputDecoration(labelText: 'Nombre'),
            ),
            TextField(
              controller: _creditosController,
              decoration: const InputDecoration(labelText: 'Créditos'),
              keyboardType: TextInputType.number,
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
                final materia = Materia(
                  nombre: _nombreController.text,
                  carreraId: _selectedCarreraId!,
                  creditos: int.parse(_creditosController.text),
                );
                if (_editingMateria != null) {
                  await ApiService.updateMateria(_editingMateria!.id!, materia);
                } else {
                  await ApiService.createMateria(materia);
                }
                if (!mounted) return;
                setState(() {
                  _futureMaterias = ApiService.getMaterias();
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

  void _deleteMateria(int id) async {
    try {
      await ApiService.deleteMateria(id);
      if (!mounted) return;
      setState(() {
        _futureMaterias = ApiService.getMaterias();
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
        title: const Text('Materias'),
        actions: [
          FloatingActionButton(
            onPressed: () => _showDialog(),
            child: const Icon(Icons.add),
          ),
        ],
      ),
      body: FutureBuilder<List<Materia>>(
        future: _futureMaterias,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          } else {
            final materias = snapshot.data ?? [];
            return ListView.builder(
              itemCount: materias.length,
              itemBuilder: (context, index) {
                final materia = materias[index];
                return ListTile(
                  title: Text(materia.nombre),
                  subtitle: Text('Carrera ID: ${materia.carreraId}, Créditos: ${materia.creditos}'),
                  trailing: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      IconButton(
                        icon: const Icon(Icons.edit),
                        onPressed: () => _showDialog(materia: materia),
                      ),
                      IconButton(
                        icon: const Icon(Icons.delete),
                        onPressed: () => _deleteMateria(materia.id!),
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
    _creditosController.dispose();
    super.dispose();
  }
}
