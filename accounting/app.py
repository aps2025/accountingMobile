"""
app.py - Flask Web Application for Bill Manager

A web-based version of the Bill Manager that reuses the backend logic.
Provides REST API endpoints and serves a responsive HTML UI.

Run with: python app.py
Access at: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from models import Bill, BillRepository
from calculator import BillCalculator
from validators import BillValidator
import json

app = Flask(__name__)

# Initialize backend components
repository = BillRepository()
calculator = BillCalculator(repository)
validator = BillValidator()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


# ==================== API ENDPOINTS ====================

@app.route('/api/bills', methods=['GET'])
def get_bills():
    """Get all active bills."""
    try:
        bills = repository.get_active()
        return jsonify({'success': True, 'bills': bills})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bills/all', methods=['GET'])
def get_all_bills():
    """Get all bills (including inactive)."""
    try:
        bills = repository.get_all()
        return jsonify({'success': True, 'bills': bills})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bills/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    """Get a specific bill by ID."""
    try:
        bill = repository.get_by_id(bill_id)
        if bill:
            return jsonify({'success': True, 'bill': bill})
        else:
            return jsonify({'success': False, 'error': 'Bill not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bills', methods=['POST'])
def create_bill():
    """Create a new bill."""
    try:
        data = request.get_json()
        
        # Validate input
        is_valid, error = validator.validate_bill_data(
            data.get('name', ''),
            str(data.get('amount', '')),
            data.get('frequency', ''),
            str(data.get('due_date', '')),
            data.get('status', 'active')
        )
        
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400
        
        # Create bill
        bill = Bill(
            name=data['name'],
            amount=float(data['amount']),
            frequency=data['frequency'],
            due_date=int(data['due_date']),
            category=data.get('category', ''),
            notes=data.get('notes', ''),
            payment_method=data.get('payment_method', ''),
            status=data.get('status', 'active')
        )
        
        bill_id = repository.create(bill)
        return jsonify({'success': True, 'bill_id': bill_id, 'message': 'Bill created successfully'}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bills/<int:bill_id>', methods=['PUT'])
def update_bill(bill_id):
    """Update an existing bill."""
    try:
        data = request.get_json()
        
        # Get existing bill
        existing_bill = repository.get_by_id(bill_id)
        if not existing_bill:
            return jsonify({'success': False, 'error': 'Bill not found'}), 404
        
        # Validate input
        is_valid, error = validator.validate_bill_data(
            data.get('name', existing_bill['name']),
            str(data.get('amount', existing_bill['amount'])),
            data.get('frequency', existing_bill['frequency']),
            str(data.get('due_date', existing_bill['due_date'])),
            data.get('status', existing_bill['status'])
        )
        
        if not is_valid:
            return jsonify({'success': False, 'error': error}), 400
        
        # Update bill
        bill = Bill(
            name=data.get('name', existing_bill['name']),
            amount=float(data.get('amount', existing_bill['amount'])),
            frequency=data.get('frequency', existing_bill['frequency']),
            due_date=int(data.get('due_date', existing_bill['due_date'])),
            category=data.get('category', existing_bill['category']),
            notes=data.get('notes', existing_bill['notes']),
            payment_method=data.get('payment_method', existing_bill['payment_method']),
            status=data.get('status', existing_bill['status'])
        )
        
        success = repository.update(bill_id, bill)
        if success:
            return jsonify({'success': True, 'message': 'Bill updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Failed to update bill'}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bills/<int:bill_id>', methods=['DELETE'])
def delete_bill(bill_id):
    """Delete a bill."""
    try:
        success = repository.delete(bill_id)
        if success:
            return jsonify({'success': True, 'message': 'Bill deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Bill not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get expense statistics."""
    try:
        monthly_total = calculator.calculate_monthly_total()
        yearly_total = calculator.calculate_yearly_total()
        
        return jsonify({
            'success': True,
            'monthly_total': monthly_total,
            'yearly_total': yearly_total
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all bill categories."""
    try:
        categories = repository.get_categories()
        return jsonify({'success': True, 'categories': categories})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bills/category/<category>', methods=['GET'])
def get_bills_by_category(category):
    """Get bills by category."""
    try:
        bills = repository.get_by_category(category)
        return jsonify({'success': True, 'bills': bills})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/summary', methods=['GET'])
def get_summary():
    """Get comprehensive expense summary."""
    try:
        summary = calculator.get_expense_summary()
        return jsonify({'success': True, 'summary': summary})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'success': False, 'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'success': False, 'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("Starting Bill Manager Web Application...")
    print("Access the app at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    app.run(debug=True, host='0.0.0.0', port=5000)
