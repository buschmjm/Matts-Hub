from ._anvil_designer import RowTemplate2Template
from anvil import *
import anvil.server
import stripe.checkout
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate2(RowTemplate2Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Set up initial values from item data
    self.name_label.text = self.item['item_name']
    self.price_label.text = f"${self.item['item_price']:.2f}"
    self.quantity_box.text = str(self.item['item_quantity'])
    self.taxable_checkbox.checked = self.item['taxable']

  def quantity_box_lost_focus(self, **event_args):
    """Update quantity when focus leaves the textbox"""
    index = self.parent.get_components().index(self)
    self.parent.raise_event('x-quantity-changed', 
                           item_index=index, 
                           new_quantity=self.quantity_box.text)

  def taxable_checkbox_change(self, **event_args):
    """Update taxable status when checkbox changes"""
    index = self.parent.get_components().index(self)
    self.parent.raise_event('x-taxable-changed',
                           item_index=index,
                           taxable=self.taxable_checkbox.checked)

  def remove_button_click(self, **event_args):
    """Remove this item from the list"""
    index = self.parent.get_components().index(self)
    self.parent.raise_event('x-remove-item', item_index=index)
