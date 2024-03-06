const mongoose = require('mongoose');
const entrySchema = new mongoose.Schema({
  title: { type: String, required: true },
  author: { type: String, required: true },
  pages: { type: Number, required: true }
});
const Entry = mongoose.model('Entry', entrySchema);
module.exports = mongoose.model('Entry', entrySchema);
