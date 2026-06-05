class Validators {
  static String? validateName(String? value) {
    if (value == null || value.isEmpty) {
      return 'Name is required';
    }
    if (value.length < 2) {
      return 'Name must be at least 2 characters';
    }
    return null;
  }

  static String? validateAmount(String? value) {
    if (value == null || value.isEmpty) {
      return 'Amount is required';
    }
    final amount = double.tryParse(value);
    if (amount == null) {
      return 'Please enter a valid number';
    }
    if (amount <= 0) {
      return 'Amount must be greater than 0';
    }
    return null;
  }

  static String? validateFrequency(String? value) {
    if (value == null || value.isEmpty) {
      return 'Frequency is required';
    }
    final validFrequencies = ['weekly', 'biweekly', 'monthly', 'quarterly', 'yearly'];
    if (!validFrequencies.contains(value.toLowerCase())) {
      return 'Please select a valid frequency';
    }
    return null;
  }

  static String? validateDueDate(String? value) {
    if (value == null || value.isEmpty) {
      return 'Due date is required';
    }
    final date = int.tryParse(value);
    if (date == null) {
      return 'Please enter a valid date';
    }
    if (date < 1 || date > 31) {
      return 'Date must be between 1 and 31';
    }
    return null;
  }

  static String? validateCategory(String? value) {
    // Category is optional
    return null;
  }
}
