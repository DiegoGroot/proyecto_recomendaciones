import 'package:flutter/material.dart';
import 'screens/carreras_screen.dart';
import 'screens/materias_screen.dart';
import 'screens/estudiantes_screen.dart';
import 'screens/calificaciones_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SIRA - Sistema de Recomendaciones Académicas',
      theme: ThemeData(
        primarySwatch: Colors.blue,
        useMaterial3: true,
      ),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int _selectedIndex = 0;

  final List<Widget> _screens = [
    const CarrerasScreen(),
    const MateriasScreen(),
    const EstudiantesScreen(),
    const CalificacionesScreen(),
  ];

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _screens[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        items: const <BottomNavigationBarItem>[
          BottomNavigationBarItem(
            icon: Icon(Icons.school),
            label: 'Carreras',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.book),
            label: 'Materias',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.person),
            label: 'Estudiantes',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.grade),
            label: 'Calificaciones',
          ),
        ],
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        type: BottomNavigationBarType.fixed,
      ),
    );
  }
}
