from ._anvil_designer import addBillTemplate
from anvil import *
import anvil.server

class addBill(addBillTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.customer_id = None
    self.billing_data = None
    self.bill_items = []
    
    # Initialize component states
    self.product_picker.items = []
    self.quantity_box.enabled = False
    self.add_button.enabled = False
    
    # Initialize labels
    self.subtotal_label.text = "Subtotal: $0.00"
    self.tax_label.text = "Tax: $0.00"
    self.total_label.text = "Total: $0.00"
    
    # Set up grid columns
    self.bill_items_panel.columns = [
      {'id': 'name', 'title': 'Item', 'data_key': 'name'},
      {'id': 'quantity', 'title': 'Quantity', 'data_key': 'quantity'},
      {'id': 'price', 'title': 'Price', 'data_key': 'price'},
      {'id': 'total', 'title': 'Total', 'data_key': 'total'},
      {'id': 'taxable', 'title': 'Taxable', 'data_key': 'taxable'}
    ]

  def set_customer(self, customer_id):
    """Set customer and load billing data"""
    self.customer_id = customer_id
    if customer_id:
      self.load_billing_data()

  def load_billing_data(self):
    """Load all necessary billing data from server"""
    try:
      self.product_picker.items = [('Loading...', None)]
      self.billing_data = anvil.server.call('get_billing_data', self.customer_id)
      self.update_display()
    except Exception as e:
      alert(f"Error loading billing data: {str(e)}")

  def update_display(self):
    """Update the display with current billing data"""
    if self.billing_data:
      # Update labels with customer info
      self.label_2.text = f"Items for {self.billing_data['customer']['name']}"
      
      # Populate product dropdown
      if self.billing_data and 'products' in self.billing_data:
        self.product_picker.items = [
          ('Select a product...', None)
        ] + [
          (f"{p['name']} - ${p['prices'][0]['unit_amount']/100:.2f}", p) 
          for p in self.billing_data['products'] 
          if p.get('prices')
        ]

  def product_picker_change(self, **event_args):
    """Handle product selection"""
    if self.product_picker.selected_value:
      self.quantity_box.enabled = True
      self.add_button.enabled = True
    else:
      self.quantity_box.enabled = False
      self.add_button.enabled = False

  def add_button_click(self, **event_args):
    """Add item to bill"""
    try:
      product = self.product_picker.selected_value
      if not product:
        return
        
      quantity = float(self.quantity_box.text or 0)
      price = product['prices'][0]['unit_amount'] / 100
      
      self.bill_items.append({
        'name': product['name'],
        'quantity': quantity,
        'price': price,
        'total': quantity * price,
        'taxable': True
      })
      
      self.refresh_bill_items()
      self.product_picker.selected_value = None
      self.quantity_box.text = ""
      
    except ValueError:
      alert("Please enter a valid quantity")

  def refresh_bill_items(self):
    """Update the bill items display"""
    self.bill_items_panel.rows = self.bill_items
    self.calculate_totals()

  def calculate_totals(self):
    """Update total amounts"""
    subtotal = sum(item['total'] for item in self.bill_items)
    taxable = sum(item['total'] for item in self.bill_items if item['taxable'])
    tax = taxable * 0.0825  # 8.25% tax rate
    
    self.subtotal_label.text = f"Subtotal: ${subtotal:.2f}"
    self.tax_label.text = f"Tax: ${tax:.2f}"
    self.total_label.text = f"Total: ${(subtotal + tax):.2f}"

  def radio_button_1_copy_clicked(self, **event_args):
    """Credit Card selected"""
    pass

  def radio_button_1_clicked(self, **event_args):
    """Cash selected"""
    pass
