from ._anvil_designer import addBillTemplate
from anvil import *
import anvil.server

class addBill(addBillTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.customer_id = None
    self.billing_data = None
    self.bill_items = []

  def set_customer(self, customer_id):
    self.customer_id = customer_id
    if customer_id:
      self.load_billing_data()

  def load_billing_data(self):
    try:
      self.billing_data = anvil.server.call('get_billing_data', self.customer_id)
      if self.billing_data:
        self.label_2.text = f"Items for {self.billing_data['customer']['name']}"
        self.bill_total.text = "Total: $0.00"
        self.taxes_total.text = "Tax: $0.00"
    except Exception as e:
      alert(f"Error loading billing data: {str(e)}")

  def radio_button_1_copy_clicked(self, **event_args):
    """Credit Card selected"""
    pass

  def radio_button_1_clicked(self, **event_args):
    """Cash selected"""
    pass
