"""
mobile_app.py - Kivy Mobile Application for Bill Manager

A mobile-friendly version of Bill Manager that runs on Android/iOS.
Reuses all backend logic (database, models, calculator, validators).

Run with: python mobile_app.py
Package with: buildozer android debug
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior

from models import Bill, BillRepository
from calculator import BillCalculator
from validators import BillValidator

# Set window size for testing
Window.size = (400, 800)

class BillItem(RecycleDataViewBehavior, BoxLayout):
    """Individual bill item in the list."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 120
        self.padding = 10
        self.spacing = 5
    
    def refresh_view_attrs(self, rv, index, data):
        """Update the view with new data."""
        self.data = data
        self.clear_widgets()
        
        # Bill name and amount
        header = BoxLayout(size_hint_y=0.3, spacing=10)
        header.add_widget(Label(text=data['name'], bold=True, size_hint_x=0.7))
        header.add_widget(Label(text=f"${data['amount']:.2f}", bold=True, color=(0.16, 0.67, 0.38, 1)))
        self.add_widget(header)
        
        # Bill details
        details = BoxLayout(size_hint_y=0.4, spacing=5)
        details.add_widget(Label(text=f"Freq: {data['frequency']}", size_hint_x=0.5, font_size='12sp'))
        details.add_widget(Label(text=f"Due: {data['due_date']}", size_hint_x=0.5, font_size='12sp'))
        self.add_widget(details)
        
        # Category and status
        footer = BoxLayout(size_hint_y=0.3, spacing=5)
        if data.get('category'):
            footer.add_widget(Label(text=data['category'], size_hint_x=0.5, font_size='11sp'))
        footer.add_widget(Label(text=data['status'], size_hint_x=0.5, font_size='11sp'))
        self.add_widget(footer)


class BillManagerApp(App):
    """Main Kivy application for Bill Manager."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = BillRepository()
        self.calculator = BillCalculator(self.repository)
        self.validator = BillValidator()
        self.current_edit_id = None
        self.frequencies = ['weekly', 'bi-weekly', 'monthly', 'quarterly', 'yearly']
        self.statuses = ['active', 'inactive']
    
    def build(self):
        """Build the main UI."""
        self.title = 'Bill Manager'
        
        # Main container
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Header
        header = BoxLayout(size_hint_y=0.08, spacing=10)
        header.add_widget(Label(text='💰 Bill Manager', bold=True, font_size='20sp'))
        main_layout.add_widget(header)
        
        # Statistics
        stats_layout = BoxLayout(size_hint_y=0.12, spacing=10)
        
        monthly_box = BoxLayout(orientation='vertical', size_hint_x=0.5)
        monthly_box.add_widget(Label(text='Monthly Total', font_size='12sp'))
        self.monthly_label = Label(text='$0.00', bold=True, font_size='16sp', color=(0.16, 0.67, 0.38, 1))
        monthly_box.add_widget(self.monthly_label)
        stats_layout.add_widget(monthly_box)
        
        yearly_box = BoxLayout(orientation='vertical', size_hint_x=0.5)
        yearly_box.add_widget(Label(text='Yearly Total', font_size='12sp'))
        self.yearly_label = Label(text='$0.00', bold=True, font_size='16sp', color=(0.16, 0.67, 0.38, 1))
        yearly_box.add_widget(self.yearly_label)
        stats_layout.add_widget(yearly_box)
        
        main_layout.add_widget(stats_layout)
        
        # Tabs (Form / List)
        self.tab_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        
        self.form_btn = Button(text='Add Bill', size_hint_x=0.5)
        self.form_btn.bind(on_press=self.show_form)
        self.tab_layout.add_widget(self.form_btn)
        
        self.list_btn = Button(text='View Bills', size_hint_x=0.5)
        self.list_btn.bind(on_press=self.show_list)
        self.tab_layout.add_widget(self.list_btn)
        
        main_layout.add_widget(self.tab_layout)
        
        # Content area (will be replaced by form or list)
        self.content_area = BoxLayout()
        main_layout.add_widget(self.content_area)
        
        # Show form by default
        self.show_form(None)
        self.refresh_stats()
        
        return main_layout
    
    def show_form(self, instance):
        """Show the bill form."""
        self.content_area.clear_widgets()
        
        form_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        scroll = ScrollView()
        
        form_content = GridLayout(cols=1, spacing=10, size_hint_y=None)
        form_content.bind(minimum_height=form_content.setter('height'))
        
        # Form fields
        form_content.add_widget(Label(text='Bill Name', size_hint_y=None, height=30))
        self.name_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_content.add_widget(self.name_input)
        
        form_content.add_widget(Label(text='Amount', size_hint_y=None, height=30))
        self.amount_input = TextInput(multiline=False, input_filter='float', size_hint_y=None, height=40)
        form_content.add_widget(self.amount_input)
        
        form_content.add_widget(Label(text='Frequency', size_hint_y=None, height=30))
        self.frequency_spinner = Spinner(
            text='monthly',
            values=self.frequencies,
            size_hint_y=None,
            height=40
        )
        form_content.add_widget(self.frequency_spinner)
        
        form_content.add_widget(Label(text='Due Date (1-31)', size_hint_y=None, height=30))
        self.due_date_input = TextInput(multiline=False, input_filter='int', size_hint_y=None, height=40)
        form_content.add_widget(self.due_date_input)
        
        form_content.add_widget(Label(text='Category', size_hint_y=None, height=30))
        self.category_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_content.add_widget(self.category_input)
        
        form_content.add_widget(Label(text='Payment Method', size_hint_y=None, height=30))
        self.payment_input = TextInput(multiline=False, size_hint_y=None, height=40)
        form_content.add_widget(self.payment_input)
        
        form_content.add_widget(Label(text='Status', size_hint_y=None, height=30))
        self.status_spinner = Spinner(
            text='active',
            values=self.statuses,
            size_hint_y=None,
            height=40
        )
        form_content.add_widget(self.status_spinner)
        
        form_content.add_widget(Label(text='Notes', size_hint_y=None, height=30))
        self.notes_input = TextInput(multiline=True, size_hint_y=None, height=80)
        form_content.add_widget(self.notes_input)
        
        scroll.add_widget(form_content)
        form_layout.add_widget(scroll)
        
        # Buttons
        button_layout = BoxLayout(size_hint_y=0.15, spacing=5)
        
        submit_btn = Button(text='Add Bill', background_color=(0.27, 0.67, 0.38, 1))
        submit_btn.bind(on_press=self.submit_bill)
        button_layout.add_widget(submit_btn)
        
        clear_btn = Button(text='Clear', background_color=(0.59, 0.65, 0.66, 1))
        clear_btn.bind(on_press=self.clear_form)
        button_layout.add_widget(clear_btn)
        
        form_layout.add_widget(button_layout)
        self.content_area.add_widget(form_layout)
    
    def show_list(self, instance):
        """Show the bills list."""
        self.content_area.clear_widgets()
        
        list_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Refresh button
        refresh_btn = Button(text='Refresh', size_hint_y=0.1, background_color=(0.34, 0.61, 0.86, 1))
        refresh_btn.bind(on_press=self.refresh_list)
        list_layout.add_widget(refresh_btn)
        
        # Bills list
        self.bills_list = RecycleView(size_hint_y=0.9)
        self.bills_list.viewclass = 'BillItem'
        self.bills_list.data = []
        
        self.refresh_list(None)
        list_layout.add_widget(self.bills_list)
        
        self.content_area.add_widget(list_layout)
    
    def refresh_list(self, instance):
        """Refresh the bills list."""
        bills = self.repository.get_active()
        self.bills_list.data = [
            {
                'id': bill['id'],
                'name': bill['name'],
                'amount': bill['amount'],
                'frequency': bill['frequency'],
                'due_date': bill['due_date'],
                'category': bill.get('category', ''),
                'status': bill['status']
            }
            for bill in bills
        ]
    
    def submit_bill(self, instance):
        """Submit the bill form."""
        try:
            name = self.name_input.text.strip()
            amount = self.amount_input.text.strip()
            frequency = self.frequency_spinner.text
            due_date = self.due_date_input.text.strip()
            category = self.category_input.text.strip()
            payment_method = self.payment_input.text.strip()
            status = self.status_spinner.text
            notes = self.notes_input.text.strip()
            
            # Validate
            is_valid, error = self.validator.validate_bill_data(name, amount, frequency, due_date, status)
            if not is_valid:
                self.show_popup('Error', error)
                return
            
            # Create or update bill
            bill = Bill(name, float(amount), frequency, int(due_date), category, notes, payment_method, status)
            
            if self.current_edit_id:
                self.repository.update(self.current_edit_id, bill)
                self.show_popup('Success', 'Bill updated successfully!')
            else:
                self.repository.create(bill)
                self.show_popup('Success', 'Bill added successfully!')
            
            self.clear_form()
            self.refresh_stats()
            self.refresh_list(None)
        
        except Exception as e:
            self.show_popup('Error', str(e))
    
    def clear_form(self, instance=None):
        """Clear the form."""
        self.name_input.text = ''
        self.amount_input.text = ''
        self.frequency_spinner.text = 'monthly'
        self.due_date_input.text = ''
        self.category_input.text = ''
        self.payment_input.text = ''
        self.status_spinner.text = 'active'
        self.notes_input.text = ''
        self.current_edit_id = None
    
    def refresh_stats(self, instance=None):
        """Refresh statistics."""
        monthly = self.calculator.calculate_monthly_total()
        yearly = self.calculator.calculate_yearly_total()
        
        self.monthly_label.text = f'${monthly:.2f}'
        self.yearly_label.text = f'${yearly:.2f}'
    
    def show_popup(self, title, message):
        """Show a popup dialog."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=message))
        
        close_btn = Button(text='OK', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.9, 0.3))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    BillManagerApp().run()
