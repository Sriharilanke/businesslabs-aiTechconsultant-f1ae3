"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.knowledgeClient = exports.KnowledgeBrainClient = void 0;
const config_1 = require("../config");
class KnowledgeBrainClient {
    baseUrl;
    timeoutMs;
    constructor(baseUrl = config_1.config.TASK1_API_URL, timeoutMs = config_1.config.TASK1_TIMEOUT_MS) {
        this.baseUrl = baseUrl.replace(/\/$/, "");
        this.timeoutMs = timeoutMs;
    }
    async queryKnowledge(question, categoryFilter) {
        const endpoint = `${this.baseUrl}/query`;
        const payload = {
            question,
            category_filter: categoryFilter || null,
            top_k: 4,
            user_id: "inbox-agent-service"
        };
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeoutMs);
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "User-Agent": "Task2-InboxAgent/1.0"
                },
                body: JSON.stringify(payload),
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            if (!response.ok) {
                throw new Error(`Knowledge Brain HTTP error ${response.status}: ${response.statusText}`);
            }
            const data = (await response.json());
            return data;
        }
        catch (err) {
            clearTimeout(timeoutId);
            // Graceful degraded mode when Task 1 is unreachable
            const isTimeout = err.name === "AbortError";
            return {
                answer: isTimeout
                    ? "The Knowledge Brain service timed out while retrieving product documentation."
                    : `The Knowledge Brain service was temporarily unreachable: ${err.message}`,
                status: "insufficient_evidence",
                sources: [],
                confidence: 0.1,
                needs_human: true
            };
        }
    }
    async checkHealth() {
        try {
            const resp = await fetch(`${this.baseUrl}/health`, { method: "GET" });
            return resp.ok;
        }
        catch {
            return false;
        }
    }
}
exports.KnowledgeBrainClient = KnowledgeBrainClient;
exports.knowledgeClient = new KnowledgeBrainClient();
