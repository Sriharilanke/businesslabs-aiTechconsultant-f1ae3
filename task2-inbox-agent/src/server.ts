import express from "express";
import cors from "cors";
import { config } from "./config";
import { apiRouter } from "./routes/api";
import { knowledgeClient } from "./knowledge-client/client";

const app = express();

app.use(cors());
app.use(express.json());

// Health Check
app.get("/health", async (req, res) => {
  const task1Online = await knowledgeClient.checkHealth();
  res.json({
    status: "healthy",
    service: "Task 2 - Inbox Agent Service",
    task1_connected: task1Online,
    port: config.PORT,
    prompt_version: config.PROMPT_VERSION
  });
});

// Mount API routes
app.use("/api", apiRouter);

if (process.env.NODE_ENV !== "test") {
  app.listen(config.PORT, () => {
    console.log(`[Task 2] Inbox Agent service running on http://localhost:${config.PORT}`);
    console.log(`[Task 2] Connected to Task 1 Knowledge Brain at ${config.TASK1_API_URL}`);
  });
}

export default app;
