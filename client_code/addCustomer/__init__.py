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
    self.confirm_selection.visible = True  # Always show the confirm button
    self.confirm_selection.enabled = False  # But start it disabled
    self._customers_loaded = False
    # Initialize with loading state
    self.select_customer.items = [('Loading...', None)]
    self.select_customer.enabled = False
    self.email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    self.phone_regex = r'^\+?1?\d{9,15}$'
    self.validation_errors = {
      'name': '',
      'email': '',
      'phone': '',
      'address': ''
    }
    
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
    
    if selected_value is None:
      # Initial "Select a customer..." option
      self.new_customer_panel.visible = False
      self.confirm_selection.enabled = False
    elif selected_value == 'new':
      # "Create New" option
      self.new_customer_panel.visible = True
      self.confirm_selection.enabled = self.check_new_customer_fields()
    else:
      # Existing customer selected
      self.new_customer_panel.visible = False
      self.confirm_selection.enabled = True

  def input_changed(self, **event_args):
    """Update confirm button state"""
    if self.select_customer.selected_value == 'new':
      # Update button state based on validation
      has_errors = any(self.validation_errors.values())
      self.confirm_selection.enabled = not has_errors
      self.confirm_selection.background = '#f8f8f8' if has_errors else None

  def confirm_selection_click(self, **event_args):
    selected_value = self.select_customer.selected_value
    
    if selected_value and selected_value != 'new':
      # Existing customer selected - store ID and raise event
      self.store_customer_id(selected_value)
      self.raise_event('x-customer-selected', customer_id=selected_value)
    else:
      # New customer - proceed with creation
      self.create_customer_click()
      
  def create_customer_click(self, **event_args):
    """Handle customer creation with improved validation feedback"""
    # Check for any validation errors
    validation_messages = [msg for msg in self.validation_errors.values() if msg]
    if validation_messages:
      alert("\n".join(validation_messages))
      return
      
    # Clean the phone number before sending
    phone_cleaned = re.sub(r'[\s\-\(\)]', '', self.phone_input.text.strip())
      
    # Create new customer with properly formatted address
    try:
      address = {
        'line1': self.address_input.text.strip(),
        'city': '',  # Add these fields to your form if needed
        'state': '',
        'postal_code': '',
        'country': 'US'  # Default to US
      }
      
      customer = anvil.server.call('create_customer',
        name=self.name_input.text.strip(),
        phone=phone_cleaned,
        email=self.email_input.text.strip(),
        address=address
      )
      if customer:
        self.store_customer_id(customer['id'])
        self.raise_event('x-customer-selected', customer_id=customer['id'])
        self.clear_inputs()
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

  def show_validation_message(self, field_name):
    """Display validation message if there's an error and hasn't been shown"""
    if self.validation_errors[field_name] and not getattr(self, f'_{field_name}_error_shown', False):
      Notification(self.validation_errors[field_name], timeout=3).show()
      setattr(self, f'_{field_name}_error_shown', True)

  def name_input_lost_focus(self, **event_args):
    """Validate name field when user leaves it"""
    if not self.name_input.text or not self.name_input.text.strip():
      self.validation_errors['name'] = "Name is required"
      self.name_input.background = '#f8f8f8'
      self.show_validation_message('name')
    else:
      self.validation_errors['name'] = ''
      self.name_input.background = 'white'
      self._name_error_shown = False
    self.input_changed()

  def email_input_lost_focus(self, **event_args):
    """Validate email field when user leaves it"""
    if not self.validate_email(self.email_input.text):
      self.validation_errors['email'] = "Please enter a valid email address"
      self.email_input.background = '#f8f8f8'
      self.show_validation_message('email')
    else:
      self.validation_errors['email'] = ''
      self.email_input.background = 'white'
      self._email_error_shown = False
    self.input_changed()

  def phone_input_lost_focus(self, **event_args):
    """Validate phone field when user leaves it"""
    if not self.validate_phone(self.phone_input.text):
      self.validation_errors['phone'] = "Please enter a valid phone number"
      self.phone_input.background = '#f8f8f8'
      self.show_validation_message('phone')
    else:
      self.validation_errors['phone'] = ''
      self.phone_input.background = 'white'
      self._phone_error_shown = False
    self.input_changed()

  def address_input_lost_focus(self, **event_args):
    """Validate address field when user leaves it"""
    if not self.address_input.text or not self.address_input.text.strip():
      self.validation_errors['address'] = "Address is required"
      self.address_input.background = '#f8f8f8'
      self.show_validation_message('address')
    else:
      self.validation_errors['address'] = ''
      self.address_input.background = 'white'
      self._address_error_shown = False
    self.input_changed()

  def phone_input_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    if not any(self.validation_errors.values()):
      self.create_customer_click()

  def store_customer_id(self, customer_id):
    """Store customer ID in browser's localStorage"""
    from anvil import js
    js.window.localStorage.setItem('temp_customer_id', customer_id)

  # Remove the old change handlers since we're now using lost_focus
  def name_input_change(self, **event_args): pass
  def email_input_change(self, **event_args): pass
  def phone_input_change(self, **event_args): pass
  def address_input_change(self, **event_args): pass


