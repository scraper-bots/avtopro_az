const Entry = require('../models/entry');

// Retrieve all entries from the database and render a view to display them
exports.getAllEntries = function(req, res) {
    Entry.find({}, (err, entries) => {
        if (err) {
            console.error('Error retrieving entries:', err);
            res.status(500).send('Error retrieving entries');
        } else {
            res.render('all_entries', { entries: entries });
        }
    });
};

// Render a form view for adding a new entry
exports.getAddEntryForm = function(req, res) {
    res.render('add_entry');
};

// Add a new entry to the database
exports.addEntry = function(req, res) {
    const { title, author, genre } = req.body;
    
    const newEntry = new Entry({
        title: title,
        author: author,
        genre: genre
    });
    
    newEntry.save((err) => {
        if (err) {
            console.error('Error adding entry:', err);
            res.status(500).send('Error adding entry');
        } else {
            res.redirect('/library');
        }
    });
};

// Render a form view for editing an existing entry
exports.getEditEntryForm = function(req, res) {
    const entryId = req.params.id;
    
    Entry.findById(entryId, (err, entry) => {
        if (err) {
            console.error('Error retrieving entry for edit:', err);
            res.status(500).send('Error retrieving entry for edit');
        } else {
            res.render('edit_entry', { entry: entry });
        }
    });
};

// Update an existing entry in the database
exports.editEntry = function(req, res) {
    const entryId = req.params.id;
    const { title, author, genre } = req.body;
    
    Entry.findByIdAndUpdate(entryId, { $set: { title: title, author: author, genre: genre } }, (err) => {
        if (err) {
            console.error('Error editing entry:', err);
            res.status(500).send('Error editing entry');
        } else {
            res.redirect('/library');
        }
    });
};

// Delete an entry from the database
exports.deleteEntry = function(req, res) {
    const entryId = req.params.id;
    
    Entry.findByIdAndRemove(entryId, (err) => {
        if (err) {
            console.error('Error deleting entry:', err);
            res.status(500).send('Error deleting entry');
        } else {
            res.redirect('/library');
        }
    });
};
