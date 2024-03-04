const express = require('express');
const mongoose = require('mongoose');
const libraryRoutes = require('./routes/library');

const app = express();
const port = process.env.PORT || 3000;

app.set('view engine', 'pug');
app.use(express.urlencoded({ extended: true }));
app.use('/library', libraryRoutes);

mongoose.connect(process.env.MONGODB_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => {
  console.log('Connected to MongoDB');
  app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
  });
})
.catch(err => console.error('Error connecting to MongoDB:', err));
