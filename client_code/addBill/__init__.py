from ._anvil_designer import addBillTemplate
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class addBill(addBillTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.customer_id = None
    self.products = None
    self.loading_panel.visible = True
    self.product_panel.visible = False

  def set_customer(self, customer_id, products=None):
    """Set customer and initialize products"""
    self.customer_id = customer_id
    if products is None:
      # Products not preloaded, need to load them now
      self.loading_panel.visible = True
      self.product_panel.visible = False
      self.load_products()
    else:
      # Products already loaded
      self.products = products
      self.loading_panel.visible = False
      self.product_panel.visible = True
      self.populate_products()

  def load_customer_details(self):
    """Load any customer-specific details needed for billing"""
    if self.customer_id:
      try:
        # Load any customer-specific data you need
        pass
      except Exception as e:
        alert(f"Error loading customer details: {str(e)}")

  def load_products(self):
    """Load products if they weren't preloaded"""
    try:
      self.products = anvil.server.call('list_products')
      self.loading_panel.visible = False
      self.product_panel.visible = True
      self.populate_products()
    except Exception as e:
      alert(f"Error loading products: {str(e)}")
      
  def populate_products(self):
    """Populate the product picker with loaded products"""
    # Implement your product display logic here
    # This will depend on your specific UI components
    pass

  def product_picker_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
