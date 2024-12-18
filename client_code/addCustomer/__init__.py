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
    # Hide panels on load
    self.new_customer_panel.visible = False
    self.confirm_selection.visible = False
    self.load_customers()
    
  def load_customers(self):
    # Get customers from Stripe
    customers = anvil.server.call('list_customers')
    # Add "Create New" option at the top
    self.select_customer.items = [('Create New', None)] + [
        (f"{c['name']} ({c['email']})", c['id']) for c in customers
    ]
    
  def select_customer_change(self, **event_args):
    selected_value = self.select_customer.selected_value
    
    # Show/hide appropriate panels based on selection
    if selected_value is None:
      # New customer selected
      self.new_customer_panel.visible = True
      self.confirm_selection.visible = True
    elif selected_value:
      # Existing customer selected
      self.new_customer_panel.visible = False
      self.confirm_selection.visible = True
    else:
      # No selection
      self.new_customer_panel.visible = False
      self.confirm_selection.visible = False

  def confirm_selection_click(self, **event_args):
    selected_value = self.select_customer.selected_value
    if selected_value:
      # Existing customer selected - navigate to addBill
      get_open_form().add_bill_1.visible = True
      self.visible = False
    else:
      # New customer - proceed with creation
      self.create_customer_click()
      
  def create_customer_click(self, **event_args):
    # Validate inputs
    if not all([self.name_input.text, self.email_input.text]):
      alert("Name and email are required!")
      return
      
    # Create new customer
    try:
      customer = anvil.server.call('create_customer',
        name=self.name_input.text,
        phone=self.phone_input.text,
        email=self.email_input.text,
        address=self.address_input.text
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
