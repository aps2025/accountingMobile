class Bill {
  final int? id;
  final String name;
  final double amount;
  final String frequency;
  final int dueDate;
  final String? category;
  final String? notes;
  final String startDate;
  final String status;
  final String? paymentMethod;
  final String createdAt;
  final String updatedAt;

  Bill({
    this.id,
    required this.name,
    required this.amount,
    required this.frequency,
    required this.dueDate,
    this.category,
    this.notes,
    required this.startDate,
    this.status = 'active',
    this.paymentMethod,
    required this.createdAt,
    required this.updatedAt,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'amount': amount,
      'frequency': frequency,
      'due_date': dueDate,
      'category': category,
      'notes': notes,
      'start_date': startDate,
      'status': status,
      'payment_method': paymentMethod,
      'created_at': createdAt,
      'updated_at': updatedAt,
    };
  }

  factory Bill.fromMap(Map<String, dynamic> map) {
    return Bill(
      id: map['id'] as int?,
      name: map['name'] as String,
      amount: map['amount'] as double,
      frequency: map['frequency'] as String,
      dueDate: map['due_date'] as int,
      category: map['category'] as String?,
      notes: map['notes'] as String?,
      startDate: map['start_date'] as String,
      status: map['status'] as String? ?? 'active',
      paymentMethod: map['payment_method'] as String?,
      createdAt: map['created_at'] as String,
      updatedAt: map['updated_at'] as String,
    );
  }
}
