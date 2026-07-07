import tkinter as tk
from tkinter import ttk, messagebox
from models import Bill, BillRepository
from calculator import BillCalculator
from validators import BillValidator
from datetime import datetime

class BillManagerUI:
    """Tkinter UI for the Bill Manager application."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Bill Manager")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize backend components
        self.repository = BillRepository()
        self.calculator = BillCalculator(self.repository)
        self.validator = BillValidator()
        
        self.frequencies = ["monthly", "weekly", "bi-weekly", "quarterly", "yearly"]
        self.statuses = ["active", "inactive"]
        
        self.setup_ui()
        self.refresh_bills()
    
    def setup_ui(self):
        """Setup the main UI layout."""
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(header_frame, text="Bill Manager", font=("Arial", 20, "bold"), 
                               bg="#2c3e50", fg="white")
        header_label.pack(pady=10)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#f0f0f0")
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Form
        left_panel = tk.Frame(main_container, bg="white", relief=tk.RIDGE, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=(0, 10))
        
        self.setup_form(left_panel)
        
        # Right panel - Bills list and stats
        right_panel = tk.Frame(main_container, bg="#f0f0f0")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.setup_list_and_stats(right_panel)
    
    def setup_form(self, parent):
        """Setup the bill entry form."""
        form_title = tk.Label(parent, text="Add/Edit Bill", font=("Arial", 14, "bold"), 
                             bg="white", fg="#2c3e50")
        form_title.pack(pady=10, padx=10)
        
        # Form fields
        fields = [
            ("Bill Name:", "name"),
            ("Amount:", "amount"),
            ("Frequency:", "frequency"),
            ("Due Date (1-31):", "due_date"),
            ("Category:", "category"),
            ("Payment Method:", "payment_method"),
            ("Status:", "status"),
            ("Notes:", "notes"),
        ]
        
        self.form_fields = {}
        
        for label_text, field_name in fields:
            frame = tk.Frame(parent, bg="white")
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            label = tk.Label(frame, text=label_text, font=("Arial", 10), bg="white", width=18, anchor="w")
            label.pack(side=tk.LEFT)
            
            if field_name == "frequency":
                var = tk.StringVar(value=self.frequencies[0])
                combo = ttk.Combobox(frame, textvariable=var, values=self.frequencies, width=20, state="readonly")
                combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.form_fields[field_name] = var
            elif field_name == "status":
                var = tk.StringVar(value="active")
                combo = ttk.Combobox(frame, textvariable=var, values=self.statuses, width=20, state="readonly")
                combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.form_fields[field_name] = var
            elif field_name == "notes":
                text = tk.Text(frame, height=3, width=25, font=("Arial", 9))
                text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                self.form_fields[field_name] = text
            else:
                entry = tk.Entry(frame, font=("Arial", 10), width=25)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.form_fields[field_name] = entry
        
        # Buttons frame
        button_frame = tk.Frame(parent, bg="white")
        button_frame.pack(fill=tk.X, padx=10, pady=15)
        
        add_btn = tk.Button(button_frame, text="Add Bill", command=self.add_bill, 
                           bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=12)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        update_btn = tk.Button(button_frame, text="Update Bill", command=self.update_bill, 
                              bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=12)
        update_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = tk.Button(button_frame, text="Clear", command=self.clear_form, 
                             bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), width=12)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        self.selected_bill_id = None
    
    def setup_list_and_stats(self, parent):
        """Setup the bills list and statistics."""
        # Stats frame
        stats_frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, bd=1)
        stats_frame.pack(fill=tk.X, padx=0, pady=(0, 10))
        
        stats_title = tk.Label(stats_frame, text="Statistics", font=("Arial", 12, "bold"), 
                              bg="white", fg="#2c3e50")
        stats_title.pack(pady=5)
        
        stats_inner = tk.Frame(stats_frame, bg="white")
        stats_inner.pack(fill=tk.X, padx=10, pady=5)
        
        self.monthly_label = tk.Label(stats_inner, text="Monthly Total: $0.00", 
                                     font=("Arial", 10), bg="white", fg="#27ae60")
        self.monthly_label.pack(anchor="w")
        
        self.yearly_label = tk.Label(stats_inner, text="Yearly Total: $0.00", 
                                    font=("Arial", 10), bg="white", fg="#27ae60")
        self.yearly_label.pack(anchor="w")
        
        # Bills list frame
        list_frame = tk.Frame(parent, bg="white", relief=tk.RIDGE, bd=1)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        list_title = tk.Label(list_frame, text="Bills", font=("Arial", 12, "bold"), 
                             bg="white", fg="#2c3e50")
        list_title.pack(pady=5)
        
        # Treeview with scrollbar
        tree_frame = tk.Frame(list_frame, bg="white")
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        columns = ("ID", "Name", "Amount", "Frequency", "Due", "Category", "Status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, height=15, show="headings", 
                                yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        # Define column headings and widths
        widths = [30, 120, 70, 80, 50, 80, 70]
        for col, width in zip(columns, widths):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<Double-1>", self.on_bill_select)
        
        # Action buttons frame
        action_frame = tk.Frame(list_frame, bg="white")
        action_frame.pack(fill=tk.X, padx=10, pady=10)
        
        refresh_btn = tk.Button(action_frame, text="Refresh", command=self.refresh_bills, 
                               bg="#3498db", fg="white", font=("Arial", 9))
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        delete_btn = tk.Button(action_frame, text="Delete Selected", command=self.delete_bill, 
                              bg="#e74c3c", fg="white", font=("Arial", 9))
        delete_btn.pack(side=tk.LEFT, padx=5)
    
    def add_bill(self):
        """Add a new bill."""
        name = self.form_fields["name"].get().strip()
        amount = self.form_fields["amount"].get().strip()
        frequency = self.form_fields["frequency"].get()
        due_date = self.form_fields["due_date"].get().strip()
        category = self.form_fields["category"].get().strip()
        payment_method = self.form_fields["payment_method"].get().strip()
        status = self.form_fields["status"].get()
        notes = self.form_fields["notes"].get("1.0", tk.END).strip()
        
        # Validate all inputs
        is_valid, error = self.validator.validate_bill_data(name, amount, frequency, due_date, status)
        if not is_valid:
            messagebox.showerror("Error", error)
            return
        
        # Create bill object and save
        bill = Bill(name, float(amount), frequency, int(due_date), category, notes, payment_method, status)
        bill_id = self.repository.create(bill)
        
        messagebox.showinfo("Success", f"Bill added successfully! (ID: {bill_id})")
        self.clear_form()
        self.refresh_bills()
    
    def update_bill(self):
        """Update the selected bill."""
        if self.selected_bill_id is None:
            messagebox.showerror("Error", "Please select a bill to update!")
            return
        
        name = self.form_fields["name"].get().strip()
        amount = self.form_fields["amount"].get().strip()
        frequency = self.form_fields["frequency"].get()
        due_date = self.form_fields["due_date"].get().strip()
        category = self.form_fields["category"].get().strip()
        payment_method = self.form_fields["payment_method"].get().strip()
        status = self.form_fields["status"].get()
        notes = self.form_fields["notes"].get("1.0", tk.END).strip()
        
        # Validate all inputs
        is_valid, error = self.validator.validate_bill_data(name, amount, frequency, due_date, status)
        if not is_valid:
            messagebox.showerror("Error", error)
            return
        
        # Create bill object and update
        bill = Bill(name, float(amount), frequency, int(due_date), category, notes, payment_method, status)
        self.repository.update(self.selected_bill_id, bill)
        
        messagebox.showinfo("Success", "Bill updated successfully!")
        self.clear_form()
        self.refresh_bills()
    
    def delete_bill(self):
        """Delete the selected bill."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a bill to delete!")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this bill?"):
            bill_id = int(self.tree.item(selected[0])["values"][0])
            self.repository.delete(bill_id)
            messagebox.showinfo("Success", "Bill deleted successfully!")
            self.clear_form()
            self.refresh_bills()
    
    def on_bill_select(self, event):
        """Handle bill selection from the list."""
        selected = self.tree.selection()
        if not selected:
            return
        
        bill_id = int(self.tree.item(selected[0])["values"][0])
        bill = self.repository.get_by_id(bill_id)
        
        if bill:
            self.selected_bill_id = bill_id
            self.form_fields["name"].delete(0, tk.END)
            self.form_fields["name"].insert(0, bill["name"])
            
            self.form_fields["amount"].delete(0, tk.END)
            self.form_fields["amount"].insert(0, str(bill["amount"]))
            
            self.form_fields["frequency"].set(bill["frequency"])
            
            self.form_fields["due_date"].delete(0, tk.END)
            self.form_fields["due_date"].insert(0, str(bill["due_date"]))
            
            self.form_fields["category"].delete(0, tk.END)
            self.form_fields["category"].insert(0, bill["category"] or "")
            
            self.form_fields["payment_method"].delete(0, tk.END)
            self.form_fields["payment_method"].insert(0, bill["payment_method"] or "")
            
            self.form_fields["status"].set(bill["status"])
            
            self.form_fields["notes"].delete("1.0", tk.END)
            self.form_fields["notes"].insert("1.0", bill["notes"] or "")
    
    def clear_form(self):
        """Clear all form fields."""
        self.form_fields["name"].delete(0, tk.END)
        self.form_fields["amount"].delete(0, tk.END)
        self.form_fields["frequency"].set(self.frequencies[0])
        self.form_fields["due_date"].delete(0, tk.END)
        self.form_fields["category"].delete(0, tk.END)
        self.form_fields["payment_method"].delete(0, tk.END)
        self.form_fields["status"].set("active")
        self.form_fields["notes"].delete("1.0", tk.END)
        self.selected_bill_id = None
    
    def refresh_bills(self):
        """Refresh the bills list and statistics."""
        # Clear the tree
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Load bills
        bills = self.repository.get_active()
        for bill in bills:
            values = (
                bill["id"],
                bill["name"],
                f"${bill['amount']:.2f}",
                bill["frequency"],
                bill["due_date"],
                bill["category"] or "-",
                bill["status"]
            )
            self.tree.insert("", tk.END, values=values)
        
        # Update statistics
        monthly_total = self.calculator.calculate_monthly_total()
        yearly_total = self.calculator.calculate_yearly_total()
        
        self.monthly_label.config(text=f"Monthly Total: ${monthly_total:.2f}")
        self.yearly_label.config(text=f"Yearly Total: ${yearly_total:.2f}")


def main():
    root = tk.Tk()
    app = BillManagerUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
