
const express = require("express");

const app = express();
app.use(express.json());

app.get("/", (req, res) => {
    res.json({
        success: true,
        message: "Backend API is running"
    });
});

app.get("/api/data", async (req, res) => {
    try {
        const apiKey = process.env.OLLAMA_API_KEY;

        if (!apiKey) {
            return res.status(500).json({
                success: false,
                status: "error",
                message: "OLLAMA_API_KEY is not configured",
                data: null
            });
        }

        const response = await fetch("https://ollama.com/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: "gemma4:31b",
                messages: [
                    {
                        role: "user",
                        content: "Give a short success message for a backend API."
                    }
                ],
                stream: false
            })
        });

        const result = await response.json();

        if (!response.ok) {
            return res.status(response.status).json({
                success: false,
                status: "error",
                message: result.error || "AI request failed",
                data: null
            });
        }

        return res.status(200).json({
            success: true,
            status: "success",
            message: result.message?.content || "AI response received",
            data: {
                id: 1,
                name: "Sample Data"
            }
        });
    } catch (error) {
        return res.status(502).json({
            success: false,
            status: "error",
            message: "Unable to connect to the AI service",
            data: null
        });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server running on port ${PORT}`);
});
