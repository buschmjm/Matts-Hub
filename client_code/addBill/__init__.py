from ._anvil_designer import addBillTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class addBill(addBillTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.customer_id = None
    self.billing_data = None
    self.bill_items = []  # Store bill items in memory
    
    # Initialize bill preview grid
    self.bill_preview.columns = [
      {'id': 'name', 'title': 'Item Name', 'data_key': 'name'},
      {'id': 'quantity', 'title': 'Quantity', 'data_key': 'quantity'},
      {'id': 'price', 'title': 'Price Each', 'data_key': 'price'},
      {'id': 'total', 'title': 'Total', 'data_key': 'total'},
      {'id': 'taxable', 'title': 'Taxable', 'data_key': 'taxable'}
    ]
    self.update_bill_preview()
    
    # Initially hide and disable components
    self.product_picker.visible = False
    self.product_picker.enabled = False
    self.quantity_box.enabled = False
    self.add_item_button.enabled = False

  def set_customer(self, customer_id):
    """Set customer and load billing data"""
    self.customer_id = customer_id
    if customer_id:
      self.load_billing_data()

  def load_billing_data(self):
    """Load all necessary billing data from server"""
    try:
      # Show loading state in picker
      self.product_picker.items = [('Loading products...', None)]
      self.product_picker.enabled = False
      
      # Get billing data
      self.billing_data = anvil.server.call('get_billing_data', self.customer_id)
      self.populate_products()
      
    except Exception as e:
      alert(f"Error loading billing data: {str(e)}")
      self.product_picker.items = [('Error loading products', None)]
    finally:
      self.product_picker.visible = True

  def populate_products(self):
    """Populate the product picker with loaded products"""
    if not self.billing_data:
      return
      
    # Format products for dropdown
    self.product_picker.items = [
      ('Select a product...', None)
    ] + [
      (f"{p['name']} - ${p['prices'][0]['unit_amount']/100:.2f}", p) 
      for p in self.billing_data['products'] 
      if p['prices']
    ]
    self.product_picker.enabled = True

  def product_picker_change(self, **event_args):
    """Handle product selection"""
    selected = self.product_picker.selected_value
    if selected:
      self.quantity_box.enabled = True
      self.quantity_box.text = "1"  # Default quantity
      self.add_item_button.enabled = True
    else:
      self.quantity_box.enabled = False
      self.add_item_button.enabled = False

  def add_item_button_click(self, **event_args):
    """Add selected product to bill"""
    selected = self.product_picker.selected_value
    if not selected or not self.quantity_box.text:
      return

    try:
      quantity = float(self.quantity_box.text)
      price = selected['prices'][0]['unit_amount'] / 100  # Convert cents to dollars
      
      new_item = {
        'name': selected['name'],
        'quantity': quantity,
        'price': price,
        'total': quantity * price,
        'taxable': True  # Default to taxable
      }
      
      self.bill_items.append(new_item)
      self.update_bill_preview()
      
      # Reset selection
      self.product_picker.selected_value = None
      self.quantity_box.text = ""
      
    except ValueError:
      alert("Please enter a valid quantity")

  def update_bill_preview(self):
    """Update the bill preview grid"""
    self.bill_preview.rows = self.bill_items
    
    # Update totals
    subtotal = sum(item['total'] for item in self.bill_items)
    taxable_total = sum(item['total'] for item in self.bill_items if item['taxable'])
    tax = taxable_total * 0.0825  # 8.25% tax rate
    total = subtotal + tax
    
    # Update total labels if they exist
    if hasattr(self, 'subtotal_label'):
      self.subtotal_label.text = f"Subtotal: ${subtotal:.2f}"
      self.tax_label.text = f"Tax: ${tax:.2f}"
      self.total_label.text = f"Total: ${total:.2f}"

  def bill_preview_change(self, **event_args):
    """Handle changes in the bill preview grid"""
    # Get the row and column that changed
    row = event_args['row']
    col_id = event_args['column_id']
    new_value = event_args['new_value']
    
    if col_id == 'taxable':
      # Update taxable status
      self.bill_items[row]['taxable'] = new_value
    elif col_id == 'quantity':
      try:
        quantity = float(new_value)
        self.bill_items[row]['quantity'] = quantity
        self.bill_items[row]['total'] = quantity * self.bill_items[row]['price']
      except ValueError:
        self.bill_items[row]['quantity'] = 0
        self.bill_items[row]['total'] = 0
        
    self.update_bill_preview()
