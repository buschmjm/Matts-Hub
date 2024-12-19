import anvil.stripe
import anvil.secrets
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import stripe
from stripe.error import StripeError

# Initialize Stripe
stripe.api_key = anvil.secrets.get_secret('stripeKey')

@anvil.server.callable
def get_billing_data(customer_id):
    """Get all necessary billing data in one call"""
    try:
        # Get customer details and products in parallel
        customer = stripe.Customer.retrieve(customer_id)
        products = stripe.Product.list(active=True)
        
        # Format the response
        billing_data = {
            'customer': {
                'id': customer.id,
                'name': customer.name,
                'email': customer.email,
            },
            'products': [{
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'images': product.images,
                'prices': [{
                    'id': price.id,
                    'unit_amount': price.unit_amount,
                    'currency': price.currency
                } for price in stripe.Price.list(product=product.id, active=True).data]
            } for product in products.data]
        }
        return billing_data
    except StripeError as e:
        raise Exception(f"Failed to fetch billing data: {e.user_message}")
