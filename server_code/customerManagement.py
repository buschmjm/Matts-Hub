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
        # Ensure address is properly formatted for Stripe
        if isinstance(address, str):
            # If address is a string, convert it to the expected format
            address = {
                'line1': address,
                'city': '',
                'state': '',
                'postal_code': '',
                'country': 'US'
            }
            
        customer = stripe.Customer.create(
            name=name,
            phone=phone,
            email=email,
            address=address
        )
        return {'id': customer.id, 'name': customer.name, 'email': customer.email}
    except StripeError as e:
        raise Exception(f"Failed to create customer: {e.user_message}")

@anvil.server.callable
def list_products():
    try:
        products = stripe.Product.list(active=True)
        # Return relevant product details including prices
        product_list = []
        for product in products.auto_paging_iter():
            # Get prices for this product
            prices = stripe.Price.list(product=product.id, active=True)
            product_list.append({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'image': product.images[0] if product.images else None,
                'prices': [{
                    'id': price.id,
                    'unit_amount': price.unit_amount,
                    'currency': price.currency,
                    'recurring': price.recurring
                } for price in prices.auto_paging_iter()]
            })
        return product_list
    except StripeError as e:
        raise Exception(f"Failed to fetch products: {e.user_message}")
