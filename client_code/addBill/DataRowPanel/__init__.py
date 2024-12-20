from ._anvil_designer import DataRowPanelTemplate
from anvil import *

class DataRowPanel(DataRowPanelTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)

  def quantity_changed(self, **event_args):
    """Handle quantity changes"""
    try:
      new_quantity = float(self.quantity_box.text or 0)
      self.item['quantity'] = new_quantity
      self.item['total'] = new_quantity * self.item['price']
      self.total_label.text = f"${self.item['total']:.2f}"
      self.parent.raise_event('x-item-changed')
    except ValueError:
      self.quantity_box.text = str(self.item['quantity'])

  def taxable_changed(self, **event_args):
    """Handle taxable checkbox changes"""
    self.item['taxable'] = self.taxable_box.checked
    self.parent.raise_event('x-item-changed')
