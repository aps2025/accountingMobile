import 'dart:convert';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import 'package:share_plus/share_plus.dart';
import '../models/bill.dart';
import '../database/database_helper.dart';

class DataTransferService {
  final DatabaseHelper _dbHelper = DatabaseHelper.instance;

  Future<String> exportToJson() async {
    final bills = await _dbHelper.getAllBills();
    
    final List<Map<String, dynamic>> billsJson = bills.map((bill) => bill.toMap()).toList();
    
    final Map<String, dynamic> exportData = {
      'version': '1.0',
      'exportDate': DateTime.now().toIso8601String(),
      'bills': billsJson,
    };
    
    return jsonEncode(exportData);
  }

  Future<void> exportToFile() async {
    try {
      final jsonData = await exportToJson();
      
      final result = await FilePicker.platform.saveFile(
        dialogTitle: 'Save Bills Data',
        fileName: 'bills_backup_${DateTime.now().millisecondsSinceEpoch}.json',
        type: FileType.custom,
        allowedExtensions: ['json'],
      );

      if (result != null) {
        final file = File(result);
        await file.writeAsString(jsonData);
      }
    } catch (e) {
      throw Exception('Failed to export data: $e');
    }
  }

  Future<void> exportAndShare() async {
    try {
      final jsonData = await exportToJson();
      
      final tempDir = Directory.systemTemp;
      final tempFile = File('${tempDir.path}/bills_backup_${DateTime.now().millisecondsSinceEpoch}.json');
      await tempFile.writeAsString(jsonData);
      
      await Share.shareFiles([tempFile.path], text: 'Bill Manager Data Backup');
      
      await tempFile.delete();
    } catch (e) {
      throw Exception('Failed to share data: $e');
    }
  }

  Future<int> importFromJson(String jsonData) async {
    try {
      final Map<String, dynamic> data = jsonDecode(jsonData);
      
      if (!data.containsKey('bills')) {
        throw Exception('Invalid data format');
      }

      final List<dynamic> billsJson = data['bills'];
      int importedCount = 0;

      for (final billJson in billsJson) {
        final bill = Bill.fromMap(billJson as Map<String, dynamic>);
        
        // Check if bill already exists by ID
        final existingBills = await _dbHelper.getAllBills();
        final exists = existingBills.any((b) => b.id == bill.id);
        
        if (!exists) {
          await _dbHelper.createBill(bill);
          importedCount++;
        }
      }

      return importedCount;
    } catch (e) {
      throw Exception('Failed to import data: $e');
    }
  }

  Future<int> importFromFile() async {
    try {
      final result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['json'],
        dialogTitle: 'Select Bills Data File',
      );

      if (result != null && result.files.single.path != null) {
        final file = File(result.files.single.path!);
        final jsonData = await file.readAsString();
        return await importFromJson(jsonData);
      }

      return 0;
    } catch (e) {
      throw Exception('Failed to import file: $e');
    }
  }
}
