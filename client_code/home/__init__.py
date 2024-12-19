from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class home(homeTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Hide forms initially
    self.add_customer_1.visible = False
    self.add_bill_1.visible = False
    
    # Delay adding event handler until needed
    self._setup_complete = False
    
    self._products_loaded = False
    self._products = None
    # Start loading products immediately
    self.load_products_async()
    
  def setup_handlers(self):
    """Lazy initialization of event handlers"""
    if not self._setup_complete:
      self.add_customer_1.add_event_handler('x-customer-selected', self.customer_selected)
      self._setup_complete = True

  def load_products_async(self):
    """Load products asynchronously"""
    try:
      self._products = anvil.server.call('list_products')
      self._products_loaded = True
    except Exception as e:
      alert(f"Error loading products: {str(e)}")
      
  def collect_payment_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.setup_handlers()  # Ensure handlers are set up
    self.add_customer_1.visible = True
    self.add_bill_1.visible = False
    # Trigger customer list reload when showing the form
    self.add_customer_1.reload_customers()
    
  def customer_selected(self, customer_id, **event_args):
    """Handle customer selection"""
    # Hide customer form and show bill form
    self.add_customer_1.visible = False
    self.add_bill_1.visible = True
    # Pass both customer_id and products to the bill form
    self.add_bill_1.set_customer(customer_id, self._products if self._products_loaded else None)

