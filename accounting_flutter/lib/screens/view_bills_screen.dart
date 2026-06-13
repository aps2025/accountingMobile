import 'package:flutter/material.dart';
import '../models/bill.dart';
import '../database/database_helper.dart';
import '../services/calculator.dart';
import '../services/data_transfer.dart';

class ViewBillsScreen extends StatefulWidget {
  const ViewBillsScreen({super.key});

  @override
  State<ViewBillsScreen> createState() => _ViewBillsScreenState();
}

class _ViewBillsScreenState extends State<ViewBillsScreen> {
  final DatabaseHelper _dbHelper = DatabaseHelper.instance;
  final BillCalculator _calculator = BillCalculator();
  final DataTransferService _dataTransfer = DataTransferService();
  
  List<Bill> _bills = [];
  double _monthlyTotal = 0;
  double _yearlyTotal = 0;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
    });

    final bills = await _dbHelper.getActiveBills();
    final monthlyTotal = await _calculator.calculateMonthlyTotal();
    final yearlyTotal = await _calculator.calculateYearlyTotal();

    setState(() {
      _bills = bills;
      _monthlyTotal = monthlyTotal;
      _yearlyTotal = yearlyTotal;
      _isLoading = false;
    });
  }

  Future<void> _deleteBill(int id) async {
    await _dbHelper.deleteBill(id);
    _loadData();
  }

  Future<void> _exportData() async {
    try {
      await _dataTransfer.exportAndShare();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Data exported successfully')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Export failed: $e')),
        );
      }
    }
  }

  Future<void> _importData() async {
    try {
      final count = await _dataTransfer.importFromFile();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Imported $count bills')),
        );
        _loadData();
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Import failed: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Statistics Bar
        Container(
          padding: const EdgeInsets.all(16),
          color: Colors.green.shade100,
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  Column(
                    children: [
                      const Text(
                        'Monthly Total',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      Text(
                        '\$${_monthlyTotal.toStringAsFixed(2)}',
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.green,
                        ),
                      ),
                    ],
                  ),
                  Column(
                    children: [
                      const Text(
                        'Yearly Total',
                        style: TextStyle(fontWeight: FontWeight.bold),
                      ),
                      Text(
                        '\$${_yearlyTotal.toStringAsFixed(2)}',
                        style: const TextStyle(
                          fontSize: 20,
                          fontWeight: FontWeight.bold,
                          color: Colors.green,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  ElevatedButton.icon(
                    onPressed: _exportData,
                    icon: const Icon(Icons.share),
                    label: const Text('Export Data'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.blue,
                      foregroundColor: Colors.white,
                    ),
                  ),
                  ElevatedButton.icon(
                    onPressed: _importData,
                    icon: const Icon(Icons.download),
                    label: const Text('Import Data'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.orange,
                      foregroundColor: Colors.white,
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
        // Bills List
        Expanded(
          child: _isLoading
              ? const Center(child: CircularProgressIndicator())
              : _bills.isEmpty
                  ? const Center(
                      child: Text(
                        'No bills yet. Add your first bill!',
                        style: TextStyle(fontSize: 16),
                      ),
                    )
                  : ListView.builder(
                      itemCount: _bills.length,
                      itemBuilder: (context, index) {
                        final bill = _bills[index];
                        return Card(
                          margin: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 8,
                          ),
                          child: ListTile(
                            title: Text(
                              bill.name,
                              style: const TextStyle(
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            subtitle: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text('\$${bill.amount.toStringAsFixed(2)}'),
                                Text('${bill.frequency.capitalize()} - Due: ${bill.dueDate}'),
                                if (bill.category != null)
                                  Text('Category: ${bill.category}'),
                              ],
                            ),
                            trailing: IconButton(
                              icon: const Icon(Icons.delete, color: Colors.red),
                              onPressed: () {
                                _showDeleteDialog(bill.id!);
                              },
                            ),
                          ),
                        );
                      },
                    ),
        ),
      ],
    );
  }

  void _showDeleteDialog(int id) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Delete Bill'),
        content: const Text('Are you sure you want to delete this bill?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _deleteBill(id);
            },
            child: const Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }
}

extension StringExtension on String {
  String capitalize() {
    return "${this[0].toUpperCase()}${substring(1)}";
  }
}
