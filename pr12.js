const express = require("express");
const app = express();
app.use(express.json());

// Existing API improved using local AI
app.get("/api/data", async (req, res) => {
    const data = { id: 1, name: "Sample Data" };

    try {
        const response = await fetch("http://localhost:11434/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                model: "llama3.2",
                messages: [{
                    role: "user",
                    content: `Write a short success message for this data: ${JSON.stringify(data)}`
                }],
                stream: false
            })
        });

        if (!response.ok) {
            throw new Error(`Ollama returned HTTP ${response.status}`);
        }

        const result = await response.json();

        res.status(200).json({
            success: true,
            status: "success",
            message: result.message.content,
            data: data
        });
    } catch (error) {
        console.error("AI error:", error.message);

        res.status(500).json({
            success: false,
            status: "error",
            message: error.message,
            data: null
        });
    }
});

// Handle invalid routes
app.use((req, res) => {
    res.status(404).json({
        success: false,
        status: "not_found",
        message: "API endpoint not found",
        data: null
    });
});

app.listen(3000, () => {
    console.log("API running on http://localhost:3000");
});

