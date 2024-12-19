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

  def set_customer(self, customer_id):
    """Set the customer ID and initialize the form"""
    self.customer_id = customer_id
    # Load customer-specific data here if needed
    self.load_customer_details()

  def load_customer_details(self):
    """Load any customer-specific details needed for billing"""
    if self.customer_id:
      try:
        # Load any customer-specific data you need
        pass
      except Exception as e:
        alert(f"Error loading customer details: {str(e)}")

  def product_picker_change(self, **event_args):
    """This method is called when an item is selected"""
    pass
