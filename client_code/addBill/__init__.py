from anvil import *

class addBill(Form):
  def __init__(self, **properties):
    # Initialize the form
    self.init_components(**properties)
    self.customer_id = None
    self.billing_data = None
<<<<<<< HEAD
=======
    self.bill_items = []  # Store bill items in memory
    
    # Initialize bill preview grid
    self.bill_preview.columns = [
      {'id': 'name', 'title': 'Item Name', 'data_key': 'name'},
      {'id': 'quantity', 'title': 'Quantity', 'data_key': 'quantity'},
      {'id': 'price', 'title': 'Price Each', 'data_key': 'price'},
      {'id': 'total', 'title': 'Total', 'data_key': 'total'},
      {'id': 'taxable', 'title': 'Taxable', 'data_key': 'taxable'}
    ]
    self.update_bill_preview()
    
    # Initially hide and disable components
    self.product_picker.visible = False
    self.product_picker.enabled = False

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

<<<<<<< HEAD
  def radio_button_1_clicked(self, **event_args):
    """Cash selected"""
    pass
=======
  def product_picker_change(self, **event_args):
    """Handle product selection"""
    selected = self.product_picker.selected_value
    if selected:
      self.quantity_box.enabled = True
      self.quantity_box.text = "1"  # Default quantity
      self.add_item_button.enabled = True
    else:
      self.quantity_box.enabled = False
      self.add_item_button.enabled = False
