from ._anvil_designer import addCustomerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class addCustomer(addCustomerTemplate):
  def __init__(self, **properties):
    self.init_components(**properties)
    self.new_customer_panel.visible = False
    self.confirm_selection.visible = False
    self._customers_loaded = False
    # Initialize with loading state
    self.select_customer.items = [('Loading...', None)]
    self.select_customer.enabled = False
    self.email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    self.phone_regex = r'^\+?1?\d{9,15}$'
    
  def form_show(self, **event_args):
    """Load customers when form becomes visible"""
    if not self._customers_loaded:
      self.reload_customers()
    
  def load_customers_async(self):
    """Load customers asynchronously"""
    self.select_customer.items = [('Loading...', None)]
    self.select_customer.enabled = False
    
    try:
      # Use anvil.server.call directly - it's already asynchronous
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
    
  def validate_email(self, email):
    """Validate email format"""
    if not email or not email.strip():
      return False
    return bool(re.match(self.email_regex, email.strip()))
    
  def validate_phone(self, phone):
    """Validate phone number format"""
    if not phone or not phone.strip():
      return False
    # Remove any spaces, dashes, or parentheses
    phone_cleaned = re.sub(r'[\s\-\(\)]', '', phone.strip())
    return bool(re.match(self.phone_regex, phone_cleaned))
    
  def check_new_customer_fields(self):
    """Validate all required fields are filled and valid"""
    name_valid = bool(self.name_input.text and self.name_input.text.strip())
    email_valid = self.validate_email(self.email_input.text)
    phone_valid = self.validate_phone(self.phone_input.text)
    address_valid = bool(self.address_input.text and self.address_input.text.strip())
    
    # Update visual feedback
    self.name_input.background = 'white' if name_valid else '#f8f8f8'
    self.email_input.background = 'white' if email_valid else '#f8f8f8'
    self.phone_input.background = 'white' if phone_valid else '#f8f8f8'
    self.address_input.background = 'white' if address_valid else '#f8f8f8'
    
    return all([name_valid, email_valid, phone_valid, address_valid])
    
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
      is_valid = self.check_new_customer_fields()
      self.confirm_selection.visible = is_valid
      self.confirm_selection.enabled = is_valid

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
      # Show specific validation messages
      if not self.name_input.text.strip():
        alert("Name is required!")
      elif not self.validate_email(self.email_input.text):
        alert("Please enter a valid email address!")
      elif not self.validate_phone(self.phone_input.text):
        alert("Please enter a valid phone number!")
      elif not self.address_input.text.strip():
        alert("Address is required!")
      return
      
    # Clean the phone number before sending
    phone_cleaned = re.sub(r'[\s\-\(\)]', '', self.phone_input.text.strip())
      
    # Create new customer
    try:
      customer = anvil.server.call('create_customer',
        name=self.name_input.text.strip(),
        phone=phone_cleaned,
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

  def address_input_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def name_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

  def email_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

  def phone_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass

  def address_input_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    pass


