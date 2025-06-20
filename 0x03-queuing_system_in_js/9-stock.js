#!/usr/bin/yarn dev
import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';

const app = express();
const port = 1245;

const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

const client = createClient();
client.on('error', (err) => console.log(`Redis client not connected to the server: ${err}`));

const getItemById = (id) => listProducts.find((item) => item.itemId === id);

const reserveStockById = (itemId, stock) => client.set(`item.${itemId}`, stock);
const getAsync = promisify(client.get).bind(client);

const getCurrentReservedStockById = async (itemId) => {
  const stock = await getAsync(`item.${itemId}`);
  return stock;
};

app.get('/list_products', (req, res) => res.json(listProducts));

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) return res.json({ status: 'Product not found' });

  const currentStock = await getCurrentReservedStockById(itemId) || item.initialAvailableQuantity;
  res.json({ ...item, currentQuantity: parseInt(currentStock) });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const item = getItemById(itemId);
  if (!item) return res.json({ status: 'Product not found' });

  const currentStock = await getCurrentReservedStockById(itemId);
  const stock = currentStock !== null ? parseInt(currentStock) : item.initialAvailableQuantity;

  if (stock < 1) return res.json({ status: 'Not enough stock available', itemId });

  reserveStockById(itemId, stock - 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

app.listen(port, () => console.log(`Server running on port ${port}`));
