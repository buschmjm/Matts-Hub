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
    # Initially hide the product grid/panel
    self.product_grid.visible = False
    
  def set_customer(self, customer_id):
    """Set customer and load billing data"""
    self.customer_id = customer_id
    if customer_id:
      self.load_billing_data()

  def load_billing_data(self):
    """Load all necessary billing data from server"""
    try:
      # Show loading indicator (assuming you have one in your template)
      self.loading_label.visible = True
      self.product_grid.visible = False
      
      # Get all billing data in one call
      self.billing_data = anvil.server.call('get_billing_data', self.customer_id)
      
      # Populate the UI with the received data
      self.populate_products()
      
    except Exception as e:
      alert(f"Error loading billing data: {str(e)}")
    finally:
      # Hide loading indicator
      self.loading_label.visible = False
      self.product_grid.visible = True

  def populate_products(self):
    """Populate the product grid with loaded products"""
    if not self.billing_data:
      return
      
    # Clear existing items
    self.product_grid.items = []
    
    # Add products to the grid
    self.product_grid.items = [
      {
        'name': p['name'],
        'description': p['description'],
        'price': f"${p['prices'][0]['unit_amount']/100:.2f}" if p['prices'] else 'N/A',
        'product': p  # Store full product data for later use
      }
      for p in self.billing_data['products']
    ]

  def product_picker_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
