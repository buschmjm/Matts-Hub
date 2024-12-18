import anvil.stripe
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import stripe
from stripe.error import StripeError

stripe.api_key = 'your_secret_key'

try:
    customers = stripe.Customer.search(
        query="name:'Jane Doe'"
    )
    for customer in customers.auto_paging_iter():
        print(f"Customer ID: {customer.id}, Email: {customer.email}")
except StripeError as e:
    print(f"An error occurred: {e.user_message}")
