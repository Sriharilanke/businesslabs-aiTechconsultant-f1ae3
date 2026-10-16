import dotenv from "dotenv";
dotenv.config();

export const config = {
  PORT: parseInt(process.env.TASK2_PORT || "8002", 10),
  TASK1_API_URL: process.env.TASK1_API_URL || "http://127.0.0.1:8001",
  TASK1_TIMEOUT_MS: parseInt(process.env.TASK1_TIMEOUT_MS || "8000", 10),
  AUTONOMY_CONSECUTIVE_THRESHOLD: 20,
  PROMPT_VERSION: "v2.1.0-inbox-safety-calibrated",
  COMPANY_NAME: "Apex Consulting & Software Labs",
  SUPPORT_EMAIL: "support@apexconsulting.io"
};
