//'use strict';


let stripe = Stripe('pk_test_51MCOouBhz5NErXMiHEIuedgwZEm3EUF5bzsEcaRQl7hUtlaLx24lz1rlBoryEdLtFnY1MkjFOjDPnTOo1Dzr8T0q00T8K5GWmg');

let elem = document.getElementById('submit');
clientsecret = elem.getAttribute('data-secret');

// Set up Stripe.js and Elements to use in checkout form
let elements = stripe.elements();
let style = {
base: {
  color: "#000",
  lineHeight: '2.4',
  fontSize: '16px'
}
};


let card = elements.create("card", { style: style });
card.mount("#card-element");

card.on('change', function(event) {
let displayError = document.getElementById('card-errors')
if (event.error) {
  displayError.textContent = event.error.message;
  $('#card-errors').addClass('alert alert-info');
} else {
  displayError.textContent = '';
  $('#card-errors').removeClass('alert alert-info');
}
});

let form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
ev.preventDefault();

let custName = document.getElementById("custName").value;
let custAdd = document.getElementById("custAdd").value;
let custAdd2 = document.getElementById("custAdd2").value;
let postCode = document.getElementById("postCode").value;


  $.ajax({
    type: "POST",
    url: 'http://127.0.0.1:8000/orders/add/',
    data: {
      order_key: clientsecret,
      csrfmiddlewaretoken: CSRF_TOKEN,
      action: "post",
    },
    success: function (json) {
      console.log(json.success)

      stripe.confirmCardPayment(clientsecret, {
        payment_method: {
          card: card,
          billing_details: {
            address:{
                line1:custAdd,
                line2:custAdd2
            },
            name: custName
          },
        }
      }).then(function(result) {
        if (result.error) {
          console.log('payment error')
          console.log(result.error.message);
        } else {
          if (result.paymentIntent.status === 'succeeded') {
            console.log('payment processed')
            // There's a risk of the customer closing the window before callback
            // execution. Set up a webhook or plugin to listen for the
            // payment_intent.succeeded event that handles any business critical
            // post-payment actions.
            window.location.replace("http://127.0.0.1:8000/payment/orderplaced/");
          }
        }
      });

    },
    error: function (xhr, errmsg, err) {},
  });



});