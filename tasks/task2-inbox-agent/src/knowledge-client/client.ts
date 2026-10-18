import { config } from "../config";
import { Task1QueryResponse } from "../types";

export class KnowledgeBrainClient {
  private baseUrl: string;
  private timeoutMs: number;

  constructor(baseUrl: string = config.TASK1_API_URL, timeoutMs: number = config.TASK1_TIMEOUT_MS) {
    this.baseUrl = baseUrl.replace(/\/$/, "");
    this.timeoutMs = timeoutMs;
  }

  async queryKnowledge(question: string, categoryFilter?: string): Promise<Task1QueryResponse> {
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

      const data = (await response.json()) as Task1QueryResponse;
      return data;
    } catch (err: any) {
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

  async checkHealth(): Promise<boolean> {
    try {
      const resp = await fetch(`${this.baseUrl}/health`, { method: "GET" });
      return resp.ok;
    } catch {
      return false;
    }
  }
}

export const knowledgeClient = new KnowledgeBrainClient();
