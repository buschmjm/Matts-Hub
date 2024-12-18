import anvil.stripe
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import stripe
from stripe.error import StripeError

# Initialize Stripe with the API key from secrets
stripe.api_key = anvil.secrets.get_secret('stripeKey')

@anvil.server.callable
def list_customers():
    try:
        customers = stripe.Customer.list()
        return [{'id': c.id, 'name': c.name, 'email': c.email} for c in customers.auto_paging_iter()]
    except StripeError as e:
        raise Exception(f"Failed to fetch customers: {e.user_message}")

@anvil.server.callable
def create_customer(name, phone, email, address):
    try:
        customer = stripe.Customer.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )
        return {'id': customer.id, 'name': customer.name, 'email': customer.email}
    except StripeError as e:
        raise Exception(f"Failed to create customer: {e.user_message}")
