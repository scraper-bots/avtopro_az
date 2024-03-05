# MDN Library App

This is a web application for managing a library collection, built as a part of the Odin Project's Express 105 course. The application allows users to view, add, edit, and delete library entries.

## Features

- View a list of library entries.
- Add new library entries.
- Edit existing library entries.
- Delete library entries.

## Technologies Used

- Node.js
- Express.js
- MongoDB
- Mongoose
- Pug (for views)
- Express-validator (for form validation)

## Getting Started

To get started with the project, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/Ismat-Samadov/library-app.git
```

2. Install dependencies:

```bash
cd mdn-library-app
npm install
```

3. Set up MongoDB:
   - If you don't have MongoDB installed locally, sign up for MongoDB Atlas and create a new cluster.
   - Set up a database named `library` with a collection named `entries`.
   - Create a `.env` file and add your MongoDB connection string:

   ```plaintext
   MONGODB_URI=your_mongodb_connection_string
   ```

4. Start the server:

```bash
npm start
```

5. Access the application at `http://localhost:3000` in your web browser.

## Directory Structure

```
project-root/
│
├── controllers/
├── middlewares/
├── models/
├── routes/
├── views/
├── server.js
├── package.json
└── .env
```

- `controllers/`: Contains route handlers and business logic.
- `middlewares/`: Contains middleware functions, such as validation and authentication.
- `models/`: Defines Mongoose schemas for MongoDB.
- `routes/`: Defines Express.js routes.
- `views/`: Contains Pug templates for rendering HTML views.
- `server.js`: Entry point of the application.
- `package.json`: Contains project metadata and dependencies.
- `.env`: Configuration file for environment variables.

## Contributing

Contributions are welcome! If you have suggestions or find any issues, please open an issue or submit a pull request.
