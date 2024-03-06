const express = require('express');
const app = express();
const libraryRoutes = require('./routes/library');

// Middleware setup
app.use(express.json()); // Parse JSON request bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded request bodies

// Route setup
app.use('/library', libraryRoutes);

module.exports = app;
