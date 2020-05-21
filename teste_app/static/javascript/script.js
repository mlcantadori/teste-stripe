// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/account/apikeys
var stripe = Stripe('pk_test_57dWxCwSlG66Z7OUGv6eXF1i00eXgYKwuH');
var elements = stripe.elements();

// Set up Stripe.js and Elements to use in checkout form
var style = {
  base: {
    color: "#32325d",
  }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

var form = document.getElementById('payment-form');
var clientSecret = document.getElementById('submit').getAttribute("data-secret");

card.addEventListener('change', function(event) {
  var displayError = document.getElementById('card-errors-input');
  if (event.error) {
    displayError.textContent = event.error.message;
  } else {
    displayError.textContent = '';
  }
});

form.addEventListener('submit', function(ev) {
  ev.preventDefault();
  stripe.confirmCardPayment(clientSecret, {
    payment_method: {
      card: card,
      billing_details: {
        name: 'Jenny Rosen'
      }
    }
  }).then(function(result) {
    var displayResult = document.getElementById('card-errors-response');
    if (result.error) {
      // Show error to your customer (e.g., insufficient funds)
      console.log(result.error.message);
      displayResult.textContent = result.error.message;
    } else {
      // The payment has been processed!
      if (result.paymentIntent.status === 'succeeded') {
        displayResult.textContent = "Deu certo oba!";
        // Show a success message to your customer
        // There's a risk of the customer closing the window before callback
        // execution. Set up a webhook or plugin to listen for the
        // payment_intent.succeeded event that handles any business critical
        // post-payment actions.
      }
    }
  });
});
