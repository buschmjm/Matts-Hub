from ._anvil_designer import homeTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class home(homeTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Initialize with the customer form hidden
    self.add_customer_1.visible = False

  def collect_payment_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Toggle visibility of the customer form
    self.add_customer_1.visible = not self.add_customer_1.visible

def form_show(self, **event_args):
  # Add some test faces to the flip card
  self.flip_card_1.add_face(Label(text="Face 1"))
  self.flip_card_1.add_face(TextBox(text="Face 2"))
  self.flip_card_1.add_face(Button(text="Face 3"))
    # Any code you write here will run before the form opens.
