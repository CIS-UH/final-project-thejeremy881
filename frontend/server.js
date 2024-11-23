require("dotenv").config(); // Load environment variables
const express = require("express");
const bodyParser = require("body-parser");
const mysql = require("mysql2"); // MySQL library for database connections
const axios = require("axios");

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(express.static("public"));
app.set("view engine", "ejs");

// Base API URL from environment variables
const BACKEND_URL = process.env.BACKEND_URL || "http://127.0.0.1:5000/api";

// Middleware for logging and headers
app.use((req, res, next) => {
    console.log(`${req.method} ${req.url}`);
    res.setHeader("X-Content-Type-Options", "nosniff");
    next();
});

// Function to establish database connection
function database_connection() {
    return mysql.createConnection({
        host: "cis2368fall.cp0g88ua2h4t.us-east-1.rds.amazonaws.com", // Your database host
        user: "thejeremy881", // Your database username
        password: "jetBlue881!", // Your database password
        database: "cis2368falldb", // Your database name
    });
}

// Routes

// Home Route
app.get("/", (req, res) => {
    res.render("index", { message: "Welcome to Stock Brokerage System!" });
});

// Investors Routes
app.get("/investors", async (req, res, next) => {
    try {
        console.log("Fetching investors...");
        const response = await axios.get(`${BACKEND_URL}/investors`);
        res.render("investors", { investors: response.data, success: null, error: null });
    } catch (err) {
        next(err);
    }
});

app.post("/investors", async (req, res, next) => {
    const { firstname, lastname } = req.body;
    if (!firstname || !lastname) {
        return res.status(400).render("error", { message: "First name and last name are required." });
    }
    try {
        await axios.post(`${BACKEND_URL}/investors`, req.body);
        res.redirect("/investors");
    } catch (err) {
        next(err);
    }
});

app.post("/investors/:id/delete", async (req, res, next) => {
    try {
        await axios.delete(`${BACKEND_URL}/investors/${req.params.id}`);
        res.redirect("/investors");
    } catch (err) {
        next(err);
    }
});

// Stocks Routes
app.get("/stocks", async (req, res, next) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/stocks`);
        console.log(response.data); // Debugging
        res.render("stocks", { stocks: response.data, success: null, error: null });
    } catch (err) {
        next(err);
    }
});

app.post("/stocks", async (req, res, next) => {
    const { stockname, abbreviation, currentprice } = req.body;

    if (!stockname || !abbreviation || !currentprice) {
        return res.status(400).render("error", { message: "All stock fields are required." });
    }

    try {
        await axios.post(`${BACKEND_URL}/stocks`, req.body);
        res.redirect("/stocks");
    } catch (err) {
        next(err);
    }
});

app.post("/stocks/:id/delete", async (req, res) => {
    try {
        const response = await axios.delete(`${BACKEND_URL}/stocks/${req.params.id}`);
        res.redirect("/stocks"); // Redirect to the stocks page after deletion
    } catch (err) {
        console.error(`Error deleting stock: ${err.message}`);
        res.status(err.response?.status || 500).send({
            message: err.response?.data?.message || "Internal Server Error",
        });
    }
});

// Bonds Routes
app.get("/bonds", (req, res) => {
    try {
        const conn = database_connection(); // Connect to the database
        conn.query("SELECT * FROM bond", (error, results) => {
            if (error) {
                console.error("Error fetching bonds:", error.message);
                return res.status(500).send({ message: "Error fetching bonds" });
            }
            // Render the bonds.ejs template and pass the bond data
            res.render("bonds", { bonds: results });
            conn.end(); // Close the connection
        });
    } catch (error) {
        console.error("Error fetching bonds:", error.message);
        res.status(500).send({ message: "Error fetching bonds" });
    }
});

app.get("/bonds/:id/edit", (req, res) => {
    const id = req.params.id;

    const conn = database_connection();
    const query = "SELECT * FROM bond WHERE id = ?";
    conn.query(query, [id], (error, results) => {
        if (error) {
            console.error("Error fetching bond:", error.message);
            return res.status(500).send("Error fetching bond.");
        }

        // Render the edit form and pass the bond data
        if (results.length > 0) {
            res.render("edit-bond", { bond: results[0] });
        } else {
            res.status(404).send("Bond not found.");
        }

        conn.end();
    });
});

app.post("/bonds", (req, res) => {
    const { bondname, abbreviation, currentprice } = req.body;

    // Validate input fields
    if (!bondname || !abbreviation || !currentprice) {
        return res.status(400).send("All fields are required.");
    }

    const conn = database_connection();
    const query = "INSERT INTO bond (bondname, abbreviation, currentprice) VALUES (?, ?, ?)";
    conn.query(query, [bondname, abbreviation, currentprice], (error) => {
        if (error) {
            console.error("Error adding bond:", error.message);
            return res.status(500).send("Error adding bond.");
        }

        res.redirect("/bonds"); // Redirect to the bonds list after adding the bond
        conn.end();
    });
});

app.post("/bonds/:id", (req, res) => {
    const id = req.params.id;
    const { bondname, abbreviation, currentprice } = req.body;

    // Validate input fields
    if (!bondname || !abbreviation || !currentprice) {
        return res.status(400).send("All fields are required.");
    }

    const conn = database_connection();
    const query = "UPDATE bond SET bondname = ?, abbreviation = ?, currentprice = ? WHERE id = ?";
    conn.query(query, [bondname, abbreviation, currentprice, id], (error) => {
        if (error) {
            console.error("Error updating bond:", error.message);
            return res.status(500).send("Error updating bond.");
        }

        res.redirect("/bonds"); // Redirect to the bonds list after updating
        conn.end();
    });
});

app.post("/bonds/:id/delete", (req, res) => {
    const id = req.params.id; // Only the ID is required for deletion

    if (!id) {
        return res.status(400).send("Bond ID is required.");
    }

    const conn = database_connection();
    const query = "DELETE FROM bond WHERE id = ?";
    conn.query(query, [id], (error) => {
        if (error) {
            console.error("Error deleting bond:", error.message);
            return res.status(500).send("Error deleting bond.");
        }

        res.redirect("/bonds"); // Redirect to bonds list after successful deletion
        conn.end();
    });
});

// Portfolio Route
app.get("/portfolio", (req, res) => {
    try {
        const conn = database_connection();
        const query = "SELECT id, firstname, lastname FROM investor";

        conn.query(query, (error, results) => {
            if (error) {
                console.error("Error fetching investors:", error.message);
                return res.status(500).send("Error fetching investors.");
            }

            // Render a portfolio selection page and pass the investor data
            res.render("portfolio-selection", { investors: results });
            conn.end();
        });
    } catch (error) {
        console.error("Error:", error.message);
        res.status(500).send("Internal Server Error");
    }
});

// Portfolio Route To Handle Fetching & Displaying an Investor's Portfolio when ID is called

app.get("/portfolio/:id", async (req, res, next) => {
    try {
        const investorId = req.params.id;

        // Fetch portfolio data
        const response = await axios.get(`${BACKEND_URL}/investors/${investorId}/portfolio`);
        console.log("Portfolio Data:", response.data); // Debugging

        const portfolio = response.data;

        // Pass investor_id and portfolio data to the template
        res.render("portfolio", {
            investor_id: investorId, // Pass the investor ID
            stock_transactions: portfolio.stock_transactions,
            bond_transactions: portfolio.bond_transactions,
        });
    } catch (err) {
        console.error("Error fetching portfolio:", err.message);
        next(err);
    }
});

// Centralized Error Handling
app.use((err, req, res, next) => {
    console.error("Error:", err.stack || err.message);
    res.status(500).render("error", { message: "An unexpected error occurred. Please try again later." });
});

// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend running at http://127.0.0.1:${PORT}`);
});




