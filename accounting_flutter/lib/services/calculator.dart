import '../models/bill.dart';
import '../database/database_helper.dart';

class BillCalculator {
  final DatabaseHelper _dbHelper = DatabaseHelper.instance;

  Future<double> calculateMonthlyTotal() async {
    final bills = await _dbHelper.getActiveBills();
    double monthlyTotal = 0;

    for (final bill in bills) {
      monthlyTotal += _convertToMonthly(bill.amount, bill.frequency);
    }

    return monthlyTotal;
  }

  Future<double> calculateYearlyTotal() async {
    final monthlyTotal = await calculateMonthlyTotal();
    return monthlyTotal * 12;
  }

  double _convertToMonthly(double amount, String frequency) {
    switch (frequency.toLowerCase()) {
      case 'weekly':
        return amount * 4.33; // Average weeks per month
      case 'biweekly':
        return amount * 2.17; // Average bi-weekly periods per month
      case 'monthly':
        return amount;
      case 'quarterly':
        return amount / 3;
      case 'yearly':
        return amount / 12;
      default:
        return amount;
    }
  }

  double convertToYearly(double amount, String frequency) {
    switch (frequency.toLowerCase()) {
      case 'weekly':
        return amount * 52;
      case 'biweekly':
        return amount * 26;
      case 'monthly':
        return amount * 12;
      case 'quarterly':
        return amount * 4;
      case 'yearly':
        return amount;
      default:
        return amount;
    }
  }
}
