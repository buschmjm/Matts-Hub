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
    self.new_customer_panel.visible = False
    self.confirm_selection.visible = False
    self._customers_loaded = False
    # Initialize with loading state
    self.select_customer.items = [('Loading...', None)]
    self.select_customer.enabled = False
    
  def form_show(self, **event_args):
    """Load customers when form becomes visible"""
    if not self._customers_loaded:
      self.reload_customers()
    
  @anvil.server.background_task
  def load_customers_async(self):
    """Asynchronously load customers"""
    self.select_customer.items = [('Loading...', None)]
    self.select_customer.enabled = False
    
    try:
      # Direct server call without callback
      customers = anvil.server.call('list_customers')
      self.select_customer.items = [
          ('Select a customer...', None),
          ('Create New', 'new')
      ] + [
          (f"{c['name']} ({c['email']})", c['id']) for c in customers
      ]
      self.select_customer.enabled = True
      self._customers_loaded = True
    except Exception as e:
      alert(f"Error loading customers: {str(e)}")
      self.select_customer.items = [('Error loading customers', None)]
      self.select_customer.enabled = True
    
  def reload_customers(self):
    """Public method to trigger customer list reload"""
    self._customers_loaded = False
    self.load_customers_async()
    
  def check_new_customer_fields(self):
    """Validate all required fields are filled"""
    return all([
      self.name_input.text and self.name_input.text.strip(),
      self.email_input.text and self.email_input.text.strip()
    ])
    
  def select_customer_change(self, **event_args):
    selected_value = self.select_customer.selected_value
    
    # Updated logic for new values
    if selected_value is None:
      # Initial "Select a customer..." option
      self.new_customer_panel.visible = False
      self.confirm_selection.visible = False
    elif selected_value == 'new':
      # "Create New" option
      self.new_customer_panel.visible = True
      self.confirm_selection.visible = False  # Hide until fields are valid
    else:
      # Existing customer selected
      self.new_customer_panel.visible = False
      self.confirm_selection.visible = True

  def input_changed(self, **event_args):
    """Called when any input field changes"""
    if self.select_customer.selected_value == 'new':
      # Show confirm button only if all required fields are filled
      self.confirm_selection.visible = self.check_new_customer_fields()

  def confirm_selection_click(self, **event_args):
    selected_value = self.select_customer.selected_value
    
    if selected_value and selected_value != 'new':
      # Existing customer selected - raise event
      self.raise_event('x-customer-selected', customer_id=selected_value)
    else:
      # New customer - proceed with creation
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
      if customer:
        # Raise event with new customer info
        self.raise_event('x-customer-selected', customer_id=customer['id'])
    except Exception as e:
      alert(f"Error creating customer: {str(e)}")
      
  def clear_inputs(self):
    self.name_input.text = ""
    self.phone_input.text = ""
    self.email_input.text = ""
    self.address_input.text = ""
