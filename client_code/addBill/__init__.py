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
