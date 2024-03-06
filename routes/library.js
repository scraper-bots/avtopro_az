const express = require('express');
const router = express.Router();
const libraryController = require('../controllers/libraryController');
const { validateAddEntry } = require('../middlewares/validation');

router.get('/', libraryController.getAllEntries);
router.get('/add', libraryController.getAddEntryForm);
router.post('/add', validateAddEntry, libraryController.addEntry);
router.get('/edit/:id', libraryController.getEditEntryForm);
router.post('/edit/:id', validateAddEntry, libraryController.editEntry);
router.post('/delete/:id', libraryController.deleteEntry);

module.exports = router;
