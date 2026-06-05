import 'package:flutter/material.dart';
import 'screens/home_screen.dart';

void main() {
  runApp(const BillManagerApp());
}

class BillManagerApp extends StatelessWidget {
  const BillManagerApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bill Manager',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}
