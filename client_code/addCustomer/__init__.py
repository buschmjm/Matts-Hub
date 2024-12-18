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
    self.new_customer_form.visible = False
    self.load_customers()
    
  def load_customers(self):
    # Get customers from Stripe
    customers = anvil.server.call('list_customers')
    # Add "Create New" option at the top
    self.select_customer.items = [('Create New', None)] + [
        (f"{c['name']} ({c['email']})", c['id']) for c in customers
    ]
    
  def select_customer_change(self, **event_args):
    # Show/hide the new customer form based on selection
    selected_value = self.select_customer.selected_value
    self.new_customer_form.visible = (selected_value is None)
    
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
    except Exception as e:
      alert(f"Error creating customer: {str(e)}")
      
  def clear_inputs(self):
    self.name_input.text = ""
    self.phone_input.text = ""
    self.email_input.text = ""
    self.address_input.text = ""
