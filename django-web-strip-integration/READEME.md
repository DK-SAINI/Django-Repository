User Flow
  After the user clicks the purchase button we need to do the following:

  Create Checkout Session

  Send another XHR request to the server requesting a new Checkout Session ID
  Generate a new Checkout Session and send back the ID
  Redirect to the checkout page for the user to finish their purchase
  Redirect the User Appropriately

  Redirect to a success page after a successful payment
  Redirect to a cancellation page after a cancelled payment
  Confirm Payment with Stripe Webhooks

  Set up the webhook endpoint
  Test the endpoint using the Stripe CLI
  Register the endpoint with Stripe
