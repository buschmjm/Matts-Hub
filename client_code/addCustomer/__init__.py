from ._anvil_designer import addCustomerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class addCustomer(addCustomerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Hide panels and confirm button on load
    self.new_customer_panel.visible = False
    self.confirm_selection.visible = False
    self.load_customers()
    # Clear any initial selection
    self.select_customer.selected_value = ''
    
  def check_new_customer_fields(self):
    """Validate all required fields are filled"""
    return all([
      self.name_input.text and self.name_input.text.strip(),
      self.email_input.text and self.email_input.text.strip()
    ])
    
  def load_customers(self):
    # Get customers from Stripe
    customers = anvil.server.call('list_customers')
    # Add empty initial option and "Create New" option
    self.select_customer.items = [('Select a customer...', '')] + [('Create New', None)] + [
        (f"{c['name']} ({c['email']})", c['id']) for c in customers
    ]
    
  def select_customer_change(self, **event_args):
    selected_value = self.select_customer.selected_value
    
    # Only proceed if a valid selection is made (not the empty initial option)
    if selected_value == '':
      self.new_customer_panel.visible = False
      self.confirm_selection.visible = False
    elif selected_value is None:
      # New customer selected
      self.new_customer_panel.visible = True
      self.confirm_selection.visible = False  # Hide until fields are valid
    else:
      # Existing customer selected
      self.new_customer_panel.visible = False
      self.confirm_selection.visible = True

  def input_changed(self, **event_args):
    """Called when any input field changes"""
    if self.select_customer.selected_value is None:
      # Show confirm button only if all required fields are filled
      self.confirm_selection.visible = self.check_new_customer_fields()

  def confirm_selection_click(self, **event_args):
    selected_value = self.select_customer.selected_value
    parent = get_open_form()
    
    if selected_value and selected_value != '':
      # Existing customer selected - switch to bill form
      self.visible = False
      parent.add_bill_1.visible = True
    else:
      # New customer - create then switch to bill form
      self.create_customer_click()
      
  def create_customer_click(self, **event_args):
    # Validate inputs
    if not self.check_new_customer_fields():
      alert("Name and email are required!")
      return
      
    # Create new customer
    try:
      customer = anvil.server.call('create_customer',
        name=self.name_input.text.strip(),
        phone=self.phone_input.text.strip(),
        email=self.email_input.text.strip(),
        address=self.address_input.text.strip()
      )
      alert("Customer created successfully!")
      self.load_customers()  # Reload the dropdown
      self.clear_inputs()
      # After successful customer creation, navigate to addBill
      if customer:
        get_open_form().add_bill_1.visible = True
        self.visible = False
    except Exception as e:
      alert(f"Error creating customer: {str(e)}")
      
  def clear_inputs(self):
    self.name_input.text = ""
    self.phone_input.text = ""
    self.email_input.text = ""
    self.address_input.text = ""
