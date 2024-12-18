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
    # Hide both forms initially
    self.add_customer_1.visible = False
    self.add_bill_1.visible = False

  def collect_payment_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Show customer form, hide bill form
    self.add_customer_1.visible = True
    self.add_bill_1.visible = False

