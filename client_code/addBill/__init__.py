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
    # Initially hide and disable the product picker
    self.product_picker.visible = False
    self.product_picker.enabled = False
    # Initialize empty list for selected items
    self.bill_items = []  # Changed from selected_items
    # Set up the repeating panel
    self.selected_items_panel.items = self.bill_items  # Reference the panel by its name

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
      # Enable relevant input fields for quantity/etc
      self.quantity_box.enabled = True
      self.add_item_button.enabled = True
    else:
      # Disable input fields if no product selected
      self.quantity_box.enabled = False
      self.add_item_button.enabled = False

  def add_item_button_click(self, **event_args):
    """Add selected product to the items panel"""
    selected_product = self.product_picker.selected_value
    if not selected_product:
      return
      
    # Create new item dictionary
    new_item = {
      'item_name': selected_product['name'],
      'item_quantity': 1,  # Default quantity
      'item_price': selected_product['prices'][0]['unit_amount'] / 100,  # Convert cents to dollars
      'taxable': True,  # Default to taxable
      'product_id': selected_product['id']  # Store for reference
    }
    
    # Add to bill items list
    self.bill_items.append(new_item)
    # Update repeating panel
    self.selected_items_panel.items = self.bill_items
    
    # Reset product picker
    self.product_picker.selected_value = None
    self.quantity_box.enabled = False
    self.add_item_button.enabled = False

  def update_item_quantity(self, item_index, new_quantity):
    """Update quantity for an item"""
    if 0 <= item_index < len(self.bill_items):
      try:
        qty = int(new_quantity)
        if qty > 0:
          self.bill_items[item_index]['item_quantity'] = qty
          self.selected_items_panel.items = self.bill_items
      except ValueError:
        pass  # Invalid number entered

  def update_item_taxable(self, item_index, taxable):
    """Update taxable status for an item"""
    if 0 <= item_index < len(self.bill_items):
      self.bill_items[item_index]['taxable'] = taxable
      self.selected_items_panel.items = self.bill_items

  def remove_item(self, item_index):
    """Remove an item from the selected items"""
    if 0 <= item_index < len(self.bill_items):
      self.bill_items.pop(item_index)
      self.selected_items_panel.items = self.bill_items
