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
    # Initialize empty list for selected items
    self.bill_items = []
    # Show and enable the product picker by default
    self.product_picker.visible = True
    self.product_picker.enabled = True
    # Initialize the repeating panel with empty list
    self.repeating_panel_1.items = self.bill_items  # Changed from selected_items_panel to repeating_panel_1

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
        
        # Populate product picker
        self.product_picker.items = [
          ('Select a product...', None)
        ] + [
          (f"{p['name']} - ${p['prices'][0]['unit_amount']/100:.2f}", p) 
          for p in self.billing_data['products'] 
          if p['prices']
        ]
        
    except Exception as e:
      alert(f"Error loading billing data: {str(e)}")

  def radio_button_1_copy_clicked(self, **event_args):
    """Credit Card selected"""
    pass

  def radio_button_1_clicked(self, **event_args):
    """Cash selected"""
    pass

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

  def add_item_button_click(self, **event_args):
    """Add selected product to the items panel"""
    selected_product = self.product_picker.selected_value
    if not selected_product:
      return
      
    # Create new item dictionary
    new_item = {
      'item_name': selected_product['name'],
      'item_quantity': 1,
      'item_price': selected_product['prices'][0]['unit_amount'] / 100,
      'taxable': True,
      'product_id': selected_product['id']
    }
    
    # Add to bill items list
    self.bill_items.append(new_item)
    # Update repeating panel
    self.repeating_panel_1.items = self.bill_items  # Changed from items_panel
    
    # Reset product picker
    self.product_picker.selected_value = None
    self.quantity_box.enabled = False
    self.add_item_button.enabled = False

  def update_item_quantity(self, item_index, new_quantity):
    """Update quantity for an item"""
    if 0 <= item_index < len(self.bill_items):
      try:
        qty = int(new_quantity)
        if qty > 0:
          self.bill_items[item_index]['item_quantity'] = qty
          self.repeating_panel_1.items = self.bill_items  # Changed from items_panel
      except ValueError:
        pass

  def update_item_taxable(self, item_index, taxable):
    """Update taxable status for an item"""
    if 0 <= item_index < len(self.bill_items):
      self.bill_items[item_index]['taxable'] = taxable
      self.repeating_panel_1.items = self.bill_items  # Changed from items_panel

  def remove_item(self, item_index):
    """Remove an item from the selected items"""
    if 0 <= item_index < len(self.bill_items):
      self.bill_items.pop(item_index)
      self.repeating_panel_1.items = self.bill_items  # Changed from items_panel
