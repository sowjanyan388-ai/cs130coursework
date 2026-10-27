const express = require('express');
const app = express();

// Middleware to parse JSON bodies
app.use(express.json());

// In-memory data store
let products = [
    { id: 1, name: 'Laptop', price: 75000 },
    { id: 2, name: 'Mouse', price: 500 },
    { id: 3, name: 'Keyboard', price: 1200 }
];
let nextId = 4;

// a. GET endpoint to return all products
app.get('/products', (req, res) => {
    res.json(products);
});

// b. POST endpoint to add a new product with safety validations
app.post('/products', (req, res) => {
    const { name, price } = req.body;

    // Validation 1: Ensure fields exist
    if (!name || price === undefined) {
        return res.status(400).json({ 
            error: 'Bad Request', 
            message: 'Both name and price are required fields.' 
        });
    }

    // Validation 2: Ensure proper data types
    if (typeof price !== 'number' || price < 0) {
        return res.status(400).json({ 
            error: 'Bad Request', 
            message: 'Price must be a valid positive number.' 
        });
    }

    // Create and save the new product safely
    const product = {
        id: nextId++,
        name: name,
        price: price
    };
    
    products.push(product);
    
    // Respond with HTTP 201 Created
    res.status(201).json(product);
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
