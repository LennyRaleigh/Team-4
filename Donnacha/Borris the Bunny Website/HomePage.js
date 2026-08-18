// Stores the name of the edition the user has selected
let selectedEdition = null;

// Stores the price of the edition the user has selected
let selectedPrice = 0;


// Select an edition

// Runs when the user clicks on one of the edition boxes
function selectEdition(name, price) {

    // Save the selected edition name
    selectedEdition = name;

    // Save the selected edition price
    selectedPrice = price;


    // Find all of the edition boxes on the page
    let editions = document.querySelectorAll(".edition");


    // Loop through each edition box
    editions.forEach(edition => {

        // Remove the selected style from every edition
        edition.classList.remove("selected");

    });


    // Add the selected style to the edition that was clicked
    event.currentTarget.classList.add("selected");


    // Find the box where the selected edition will be displayed
    let selectedBox = document.getElementById("selectedEdition");


    // Show the selected edition and its price
    selectedBox.innerHTML = `
        <p>
            Selected: ${name} - €${price.toFixed(2)}
        </p>
    `;


    // Enable the Add to Cart button
    document.getElementById("addGameButton").disabled = false;

}


// Add selected game to cart

// Adds the selected game edition to the shopping cart
function addSelectedEdition() {

    // If no edition has been selected, stop the function
    if (selectedEdition === null) {

        return;

    }


    // Load the cart from localStorage,
    // or use an empty array if nothing is saved
    let cart = JSON.parse(localStorage.getItem("cart")) || [];


    // Check if the selected edition is already in the cart
    let existingProduct = cart.find(
        product => product.name === selectedEdition
    );


    // If the edition is already in the cart,
    // increase its quantity
    if (existingProduct) {

        existingProduct.quantity++;

    } else {

        // If the edition is not already in the cart,
        // add it as a new product
        cart.push({

            name: selectedEdition,

            price: selectedPrice,

            quantity: 1

        });

    }


    // Save the updated cart back into localStorage
    localStorage.setItem("cart", JSON.stringify(cart));


    // Tell the user that the selected edition has been added
    alert(
        selectedEdition +
        " has been added to your cart!"
    );

}s