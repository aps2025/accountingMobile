import 'package:flutter/material.dart';
import '../models/bill.dart';
import '../database/database_helper.dart';
import '../services/validators.dart';
import '../services/calculator.dart';

class AddBillScreen extends StatefulWidget {
  const AddBillScreen({super.key});

  @override
  State<AddBillScreen> createState() => _AddBillScreenState();
}

class _AddBillScreenState extends State<AddBillScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _amountController = TextEditingController();
  final _dueDateController = TextEditingController();
  final _categoryController = TextEditingController();
  final _notesController = TextEditingController();
  
  String _frequency = 'monthly';
  String _paymentMethod = '';
  
  final DatabaseHelper _dbHelper = DatabaseHelper.instance;
  final BillCalculator _calculator = BillCalculator();

  final List<String> _frequencies = [
    'weekly',
    'biweekly', 
    'monthly',
    'quarterly',
    'yearly',
  ];

  @override
  void dispose() {
    _nameController.dispose();
    _amountController.dispose();
    _dueDateController.dispose();
    _categoryController.dispose();
    _notesController.dispose();
    super.dispose();
  }

  Future<void> _saveBill() async {
    if (_formKey.currentState!.validate()) {
      final now = DateTime.now().toIso8601String();
      final bill = Bill(
        name: _nameController.text,
        amount: double.parse(_amountController.text),
        frequency: _frequency,
        dueDate: int.parse(_dueDateController.text),
        category: _categoryController.text.isEmpty ? null : _categoryController.text,
        notes: _notesController.text.isEmpty ? null : _notesController.text,
        startDate: now.split('T')[0],
        paymentMethod: _paymentMethod.isEmpty ? null : _paymentMethod,
        createdAt: now,
        updatedAt: now,
      );

      await _dbHelper.createBill(bill);
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Bill saved successfully')),
        );
        _clearForm();
      }
    }
  }

  void _clearForm() {
    _nameController.clear();
    _amountController.clear();
    _dueDateController.clear();
    _categoryController.clear();
    _notesController.clear();
    setState(() {
      _frequency = 'monthly';
      _paymentMethod = '';
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16.0),
      child: Form(
        key: _formKey,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextFormField(
              controller: _nameController,
              decoration: const InputDecoration(
                labelText: 'Bill Name',
                border: OutlineInputBorder(),
              ),
              validator: Validators.validateName,
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _amountController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Amount',
                border: OutlineInputBorder(),
                prefixText: '\$',
              ),
              validator: Validators.validateAmount,
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              value: _frequency,
              decoration: const InputDecoration(
                labelText: 'Frequency',
                border: OutlineInputBorder(),
              ),
              items: _frequencies.map((String frequency) {
                return DropdownMenuItem<String>(
                  value: frequency,
                  child: Text(frequency.capitalize()),
                );
              }).toList(),
              onChanged: (String? newValue) {
                setState(() {
                  _frequency = newValue!;
                });
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _dueDateController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Due Date (1-31)',
                border: OutlineInputBorder(),
              ),
              validator: Validators.validateDueDate,
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _categoryController,
              decoration: const InputDecoration(
                labelText: 'Category (optional)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _notesController,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'Notes (optional)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: TextEditingController(text: _paymentMethod),
              decoration: const InputDecoration(
                labelText: 'Payment Method (optional)',
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                _paymentMethod = value;
              },
            ),
            const SizedBox(height: 24),
            Row(
              children: [
                Expanded(
                  child: ElevatedButton(
                    onPressed: _saveBill,
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.green,
                      foregroundColor: Colors.white,
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: const Text('Save Bill'),
                  ),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: OutlinedButton(
                    onPressed: _clearForm,
                    style: OutlinedButton.styleFrom(
                      padding: const EdgeInsets.symmetric(vertical: 16),
                    ),
                    child: const Text('Clear'),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${substring(1)}";
  }
}
