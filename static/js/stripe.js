// A reference to Stripe.js initialized with your real test publishable API key.
let stripe = Stripe(
  'pk_test_51JanYjLhxVHD1FOp86EV5oqU9KRQanYdTm5s0FpZvU0U5IuEWmdCQkxb0zeJTmZN2qoreogVTQGmWtGI8hi2jlmo00A05wetmf'
)

// The items the customer wants to buy
let purchase = {
  items: [{ amount: 5555 }]
}

// Disable the button until we have Stripe set up on the page
document.querySelector('button').disabled = true
fetch('/create-payment-intent', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(purchase)
})
  .then(function (result) {
    return result.json()
  })
  .then(function (data) {
    let elements = stripe.elements()

    let style = {
      base: {
        color: '#32325d',
        fontFamily: 'Arial, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
          color: '#32325d'
        }
      },
      invalid: {
        fontFamily: 'Arial, sans-serif',
        color: '#fa755a',
        iconColor: '#fa755a'
      }
    }

    let card = elements.create('card', { style: style })
    // Stripe injects an iframe into the DOM
    card.mount('#card-element')

    card.on('change', function (event) {
      // Disable the Pay button if there are no card details in the Element
      document.querySelector('button').disabled = event.empty
      document.querySelector('#card-error').textContent = event.error
        ? event.error.message
        : ''
    })

    let form = document.getElementById('payment-form')
    form.addEventListener('submit', function (event) {
      event.preventDefault()
      // Complete payment when the submit button is clicked
      payWithCard(stripe, card, data.clientSecret)
    })
  })

// Calls stripe.confirmCardPayment
// If the card requires authentication Stripe shows a pop-up modal to
// prompt the user to enter authentication details without leaving your page.
let payWithCard = function (stripe, card, clientSecret) {
  loading(true)
  stripe
    .confirmCardPayment(clientSecret, {
      payment_method: {
        card: card
      }
    })
    .then(function (result) {
      if (result.error) {
        // Show error to your customer
        showError(result.error.message)
      } else {
        // The payment succeeded!
        orderComplete(result.paymentIntent.id)
      }
    })
}

/* ------- UI helpers ------- */

// Shows a success message when the payment is complete
let orderComplete = function (paymentIntentId) {
  loading(false)
  document
    .querySelector('.result-message a')
    .setAttribute(
      'href',
      'https://dashboard.stripe.com/test/payments/' + paymentIntentId
    )
  document.querySelector('.result-message').classList.remove('hidden')
  document.querySelector('button').disabled = true
}

// Show the customer the error from Stripe if their card fails to charge
let showError = function (errorMsgText) {
  loading(false)
  let errorMsg = document.querySelector('#card-error')
  errorMsg.textContent = errorMsgText
  setTimeout(function () {
    errorMsg.textContent = ''
  }, 4000)
}

// Show a spinner on payment submission
let loading = function (isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector('button').disabled = true
    document.querySelector('#spinner').classList.remove('hidden')
    document.querySelector('#button-text').classList.add('hidden')
  } else {
    document.querySelector('button').disabled = false
    document.querySelector('#spinner').classList.add('hidden')
    document.querySelector('#button-text').classList.remove('hidden')
  }
}
