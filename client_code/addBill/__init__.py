from anvil import *

class addBill(Form):
  def __init__(self, **properties):
    # Initialize the form
    self.init_components(**properties)
    self.customer_id = None
    self.billing_data = None
<<<<<<< HEAD
=======
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
>>>>>>> efee964 (Refactor addBill form; implement bill item management and update preview grid with subtotal, tax, and total calculations)

  def set_customer(self, customer_id):
    self.customer_id = customer_id
    if customer_id:
      self.load_billing_data()

  def load_billing_data(self):
    try:
      self.billing_data = anvil.server.call('get_billing_data', self.customer_id)
      if self.billing_data:
        self.label_2.text = f"Items for {self.billing_data['customer']['name']}"
        self.bill_total.text = "Total: $0.00"
        self.taxes_total.text = "Tax: $0.00"
    except Exception as e:
      alert(f"Error loading billing data: {str(e)}")

  def radio_button_1_copy_clicked(self, **event_args):
    """Credit Card selected"""
    pass

<<<<<<< HEAD
  def radio_button_1_clicked(self, **event_args):
    """Cash selected"""
    pass
=======
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
>>>>>>> efee964 (Refactor addBill form; implement bill item management and update preview grid with subtotal, tax, and total calculations)
