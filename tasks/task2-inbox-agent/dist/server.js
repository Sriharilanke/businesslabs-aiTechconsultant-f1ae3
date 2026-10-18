"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const config_1 = require("./config");
const api_1 = require("./routes/api");
const client_1 = require("./knowledge-client/client");
const app = (0, express_1.default)();
app.use((0, cors_1.default)());
app.use(express_1.default.json());
// Health Check
app.get("/health", async (req, res) => {
    const task1Online = await client_1.knowledgeClient.checkHealth();
    res.json({
        status: "healthy",
        service: "Task 2 - Inbox Agent Service",
        task1_connected: task1Online,
        port: config_1.config.PORT,
        prompt_version: config_1.config.PROMPT_VERSION
    });
});
// Mount API routes
app.use("/api", api_1.apiRouter);
if (process.env.NODE_ENV !== "test") {
    app.listen(config_1.config.PORT, () => {
        console.log(`[Task 2] Inbox Agent service running on http://localhost:${config_1.config.PORT}`);
        console.log(`[Task 2] Connected to Task 1 Knowledge Brain at ${config_1.config.TASK1_API_URL}`);
    });
}
exports.default = app;
