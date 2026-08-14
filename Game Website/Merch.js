// Load the cart from localStorage, or use an empty array if no cart is saved
let cart = JSON.parse(localStorage.getItem("cart")) || [];


// Save the current cart to localStorage
function saveCart() {

    localStorage.setItem("cart", JSON.stringify(cart));

}


// Add a product to the cart
function addToCart(name, price) {

    // Check if this product is already in the cart
    let existingProduct = cart.find(
        product => product.name === name
    );


    // If the product is already there, increase its quantity
    if (existingProduct) {

        existingProduct.quantity++;

    } else {

        // If the product is not already there, add it to the cart
        cart.push({
            name: name,
            price: price,
            quantity: 1
        });

    }


    // Save the updated cart
    saveCart();

    // Update the cart display
    updateCart();

}


// Update the number of items and products shown in the cart
function updateCart() {

    // Start the item counter at zero
    let totalItems = 0;


    // Add the quantity of every product together
    cart.forEach(product => {

        totalItems += product.quantity;

    });


    // Update the cart number shown beside the basket icon
    document.getElementById("cartCount").textContent = totalItems;

    // Update the number of items shown inside the cart
    document.getElementById("cartItems").textContent = totalItems;


    // Get the area where the cart products will be displayed
    let cartProducts =
        document.getElementById("cartProducts");


    // Clear the old cart contents before rebuilding it
    cartProducts.innerHTML = "";


    // Loop through every product in the cart
    cart.forEach((product, index) => {

        // Create a new div to hold the product information
        let item = document.createElement("div");

        // Apply the cart-item CSS class to the new div
        item.className = "cart-item";


        // Add the product name, price, quantity and remove button
        item.innerHTML = `

            <p>

                ${product.name}

                <br>

                €${product.price.toFixed(2)}

                <br>

                Quantity: ${product.quantity}

            </p>

            <button onclick="removeFromCart(${index})">

                Remove

            </button>

        `;


        // Add the finished product to the cart
        cartProducts.appendChild(item);

    });

}


// Remove one quantity of a product from the cart
function removeFromCart(index) {

    // If there is more than one of the product, reduce the quantity
    if (cart[index].quantity > 1) {

        cart[index].quantity--;

    } else {

        // If there is only one, remove the product completely
        cart.splice(index, 1);

    }


    // Save the updated cart
    saveCart();

    // Refresh the cart display
    updateCart();

}


// Open or close the shopping cart
function toggleCart() {

    // Get the cart box from the page
    let cartBox =
        document.getElementById("cart");


    // If the cart is currently open, close it
    if (cartBox.style.display === "block") {

        cartBox.style.display = "none";

    } else {

        // Otherwise, open the cart
        cartBox.style.display = "block";

    }

}


// Scroll smoothly to a product category
function scrollToSection(section) {

    document
        .getElementById(section)
        .scrollIntoView({
            behavior: "smooth"
        });

}


// Show all products and scroll back to the top of the products
function showAllProducts() {

    // Get all product sections on the page
    let sections =
        document.querySelectorAll(".product-section");


    // Loop through every product section
    sections.forEach(section => {

        // Make the section visible
        section.style.display = "block";


        // Get all products inside this section
        let products =
            section.querySelectorAll(".product");


        // Make every product visible
        products.forEach(product => {

            product.style.display = "block";

        });

    });


    // Scroll back to the All Products heading
    document.getElementById("all-products")
        .scrollIntoView({
            behavior: "smooth"
        });

}


// Listen for text being typed into the search bar
document
    .getElementById("searchBar")
    .addEventListener("keyup", function() {

        // Get the search text and convert it to lowercase
        let search =
            this.value.toLowerCase();


        // Get all product sections
        let sections =
            document.querySelectorAll(".product-section");


        // Check every product section
        sections.forEach(section => {

            // Get all products inside the current section
            let products =
                section.querySelectorAll(".product");


            // Keep track of whether a product was found
            let foundProduct = false;


            // Check every product against the search
            products.forEach(product => {

                // Get the product name and convert it to lowercase
                let name =
                    product
                        .querySelector("h4")
                        .textContent
                        .toLowerCase();


                // Show the product if its name matches the search
                if (name.includes(search)) {

                    product.style.display = "block";

                    foundProduct = true;

                } else {

                    // Hide the product if it does not match
                    product.style.display = "none";

                }

            });


            // Keep the section visible if it contains a matching product
            if (foundProduct) {

                section.style.display = "block";

            } else {

                // Hide the section if no products were found
                section.style.display = "none";

            }

        });

    });


// Update the cart when the page first loads
updateCart();