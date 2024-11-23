require("dotenv").config(); // Load environment variables
const express = require("express");
const bodyParser = require("body-parser");
const axios = require("axios");

const app = express();

// Middleware
app.use(bodyParser.urlencoded({ extended: true }));
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

// Routes

// Home Route
app.get("/", (req, res) => {
    res.render("index", { message: "Welcome to Stock Brokerage System!" });
});

// Investors Routes
app.get("/investors", async (req, res, next) => {
    try {
        console.log("Fetching investors...");
        const response = await axios.get(`${process.env.BACKEND_URL}/investors`);
        console.log("Investors fetched:", response.data);
        res.render("investors", { investors: response.data, success: null, error: null });
    } catch (err) {
        console.error("Error fetching investors:", err.message);
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
        res.render("stocks", { stocks: response.data });
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

app.post("/stocks/:id/delete", async (req, res, next) => {
    try {
        await axios.delete(`${BACKEND_URL}/stocks/${req.params.id}`);
        res.redirect("/stocks");
    } catch (err) {
        next(err);
    }
});

// Bonds Routes
app.get("/bonds", async (req, res, next) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/bonds`);
        res.render("bonds", { bonds: response.data });
    } catch (err) {
        next(err);
    }
});

app.post("/bonds", async (req, res, next) => {
    const { bondname, abbreviation, currentprice } = req.body;
    if (!bondname || !abbreviation || !currentprice) {
        return res.status(400).render("error", { message: "All bond fields are required." });
    }
    try {
        await axios.post(`${BACKEND_URL}/bonds`, req.body);
        res.redirect("/bonds");
    } catch (err) {
        next(err);
    }
});

app.post("/bonds/:id/delete", async (req, res, next) => {
    try {
        await axios.delete(`${BACKEND_URL}/bonds/${req.params.id}`);
        res.redirect("/bonds");
    } catch (err) {
        next(err);
    }
});

// Portfolio Route
app.get("/portfolio/:id", async (req, res, next) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/investors/${req.params.id}/portfolio`);
        const portfolio = response.data;
        res.render("portfolio", {
            investor_id: portfolio.investor_id,
            stock_transactions: portfolio.stock_transactions,
            bond_transactions: portfolio.bond_transactions
        });
    } catch (err) {
        next(err);
    }
});

// Centralized Error Handling
app.use((err, req, res, next) => {
    console.error("Error:", err.message);
    res.status(500).render("error", { message: "An unexpected error occurred. Please try again later." });
});

// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Frontend running at http://127.0.0.1:${PORT}`);
});


