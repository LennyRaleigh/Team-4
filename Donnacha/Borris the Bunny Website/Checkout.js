// Load the cart from localStorage, or use an empty array if nothing is saved
let cart = JSON.parse(localStorage.getItem("cart")) || [];


// Reads the cart and builds the order summary on the page
function displayOrder() {

    // Get the div where cart items will be shown
    let orderProducts = document.getElementById("orderProducts");

    // Get the span where the total price will be shown
    let totalPrice = document.getElementById("totalPrice");

    // Clear anything already in the order section before rebuilding it
    orderProducts.innerHTML = "";

    // Running total that increases as we loop through each item
    let total = 0;


    // If the cart is empty, show a message and stop here
    if (cart.length === 0) {

        orderProducts.innerHTML = `
            <p>Your cart is empty.</p>
        `;

        totalPrice.textContent = "0.00";

        return;
    }


    // Loop through every item in the cart and create a card for each one
    cart.forEach(product => {

        // Calculate the price for this item (price × quantity)
        let itemTotal = product.price * product.quantity;

        // Add this item's total to the running grand total
        total += itemTotal;


        // Create a new div element to hold this item's details
        let item = document.createElement("div");

        // Apply the order-item CSS class for styling
        item.className = "order-item";

        // Fill the card with the item name, quantity, and price
        item.innerHTML = `
            <h4>${product.name}</h4>

            <p>
                Quantity: ${product.quantity}
            </p>

            <p class="item-price">
                €${itemTotal.toFixed(2)}
            </p>
        `;

        // Add the finished card into the order section on the page
        orderProducts.appendChild(item);

    });

    // Show the final total price rounded to 2 decimal places
    totalPrice.textContent = total.toFixed(2);

}


// Listen for the form being submitted when the user clicks Place Order
document.getElementById("checkoutForm").addEventListener("submit", function(event) {

    // Stop the page from refreshing (default form behaviour)
    event.preventDefault();

    // If the cart is empty, warn the user and stop here
    if (cart.length === 0) {

        alert("Your cart is empty!");

        return;

    }

    // Tell the user their order was placed successfully
    alert("Order placed successfully!");

    // Clear the cart from localStorage so it resets after checkout
    localStorage.removeItem("cart");

    // Send the user back to the home page
    window.location.href = "HomePage.html";

});


// Run displayOrder straight away so the cart loads when the page opens
displayOrder();
