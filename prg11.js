const express = require('express');
const app = express();
app.use(express.json());

const inventory = {
  'item_101': { name: 'Wireless Mouse', price: 29.99, stock: 15 },
  'item_102': { name: 'Mechanical Keyboard', price: 89.99, stock: 5 },
  'item_103': { name: 'USB-C Hub', price: 45.00, stock: 0 }
};
const orders = [];

// POST /addOrders
app.post('/addOrders', (req, res) => {
  const { userId, items } = req.body;
  if (!userId || !Array.isArray(items) || !items.length) {
    return res.status(400).json({ error: 'userId and non-empty items array required.' });
  }

  // Validate items & stock first
  for (const { itemId, quantity } of items) {
    const item = inventory[itemId];
    if (!item) return res.status(404).json({ error: `Item ${itemId} not found.` });
    if (quantity <= 0 || item.stock < quantity) {
      return res.status(400).json({ error: `Insufficient stock for ${item.name}.` });
    }
  }

  // Deduct stock & calculate total
  const processedItems = items.map(({ itemId, quantity }) => {
    const item = inventory[itemId];
    item.stock -= quantity;
    return { itemId, name: item.name, price: item.price, quantity, subtotal: item.price * quantity };
  });

  const totalAmount = processedItems.reduce((sum, item) => sum + item.subtotal, 0);
  const order = { orderId: `ORD-${Date.now()}`, userId, items: processedItems, totalAmount, createdAt: new Date().toISOString() };
  orders.push(order);

  res.status(201).json({ message: 'Order placed', order });
});

// GET /showOrders or GET /showOrders/:userId
app.get(['/showOrders', '/showOrders/:userId'], (req, res) => {
  const userId = req.params.userId || req.query.userId;
  if (!userId) return res.status(400).json({ error: 'userId parameter required.' });

  const userOrders = orders
    .filter(o => o.userId === userId)
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));

  res.json({ count: userOrders.length, orders: userOrders });
});

app.listen(3000, () => console.log('Server running on http://localhost:3000'));

