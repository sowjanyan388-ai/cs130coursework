const express = require("express");
const app = express();

// Existing API - Improved Response
app.get("/api/data", (req, res) => {

    res.status(200).json({
        success: true,
        status: "success",
        message: "Data retrieved successfully",
        data: {
            id: 1,
            name: "abc",
            course: "BCA"
        }
    });

});

// Invalid API
app.use((req, res) => {

    res.status(404).json({
        success: false,
        status: "error",
        message: "API endpoint not found",
        data: null
    });

});
app.listen(3000, () => {
    console.log("API running on http://localhost:3000");
});


