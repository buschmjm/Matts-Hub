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
    # Initially hide the product picker and show loading
    self.product_picker.visible = False
    self.loading_label.text = "Loading products..."
    self.loading_label.visible = True

  def set_customer(self, customer_id):
    """Set customer and load billing data"""
    self.customer_id = customer_id
    if customer_id:
      self.load_billing_data()

  def load_billing_data(self):
    """Load all necessary billing data from server"""
    try:
      self.loading_label.visible = True
      self.product_picker.visible = False
      
      self.billing_data = anvil.server.call('get_billing_data', self.customer_id)
      self.populate_products()
      
    except Exception as e:
      alert(f"Error loading billing data: {str(e)}")
    finally:
      self.loading_label.visible = False
      self.product_picker.visible = True

  def populate_products(self):
    """Populate the product picker with loaded products"""
    if not self.billing_data:
      return
      
    # Format products for dropdown
    self.product_picker.items = [
      (f"{p['name']} - ${p['prices'][0]['unit_amount']/100:.2f}", p) 
      for p in self.billing_data['products'] 
      if p['prices']
    ]

  def product_picker_change(self, **event_args):
    """Handle product selection"""
    selected = self.product_picker.selected_value
    if selected:
      # Update price display
      price = selected['prices'][0]['unit_amount']/100
      self.price_label.text = f"${price:.2f}"
      # Show any additional product details
      self.description_label.text = selected['description'] or "No description available"
      # Enable quantity input and add button if needed
      self.quantity_box.enabled = True
      self.add_item_button.enabled = True
    else:
      # Reset UI elements
      self.price_label.text = ""
      self.description_label.text = ""
      self.quantity_box.enabled = False
      self.add_item_button.enabled = False
