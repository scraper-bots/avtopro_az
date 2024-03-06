const { body, validationResult } = require('express-validator');

exports.validateAddEntry = [
  body('title').trim().notEmpty().withMessage('Title is required'),
  body('author').trim().notEmpty().withMessage('Author is required'),
  body('pages').trim().isNumeric().withMessage('Pages must be a number'),
      (req, res, next) => {
        const errors = validationResult(req);
        if (!errors.isEmpty()) {
            return res.status(400).json({ errors: errors.array() });
        }
        next();
    }
];
