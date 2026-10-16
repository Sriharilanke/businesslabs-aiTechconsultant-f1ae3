import { EmailInteractionRecord } from "../types";
import { config } from "../config";

export class LearningStore {
  private records: Map<string, EmailInteractionRecord> = new Map();
  private promptVersions: Array<{ version: string; description: string; active: boolean; created_at: string }> = [
    {
      version: "v1.0.0-baseline",
      description: "Initial prompt without explicit financial/refund guardrails",
      active: false,
      created_at: "2026-10-10T00:00:00Z"
    },
    {
      version: "v2.0.0-guarded-tone",
      description: "Added company voice and Knowledge Brain grounding",
      active: false,
      created_at: "2026-10-12T00:00:00Z"
    },
    {
      version: config.PROMPT_VERSION,
      description: "Production version: strict refund/quote guardrails, 20-streak autonomy controls, and citation verification",
      active: true,
      created_at: "2026-10-14T00:00:00Z"
    }
  ];

  addRecord(record: EmailInteractionRecord) {
    this.records.set(record.id, record);
  }

  getRecord(id: string): EmailInteractionRecord | undefined {
    return this.records.get(id);
  }

  getAllRecords(): EmailInteractionRecord[] {
    return Array.from(this.records.values());
  }

  updateReview(id: string, decision: EmailInteractionRecord["human_decision"], editedReply?: string, reviewedBy?: string) {
    const rec = this.records.get(id);
    if (!rec) return;

    rec.human_decision = decision;
    rec.human_edited_reply = editedReply;
    rec.reviewed_by = reviewedBy || "Consultant Reviewer";
    rec.reviewed_at = new Date().toISOString();
    rec.is_sent = decision === "approved" || decision === "edited";
    if (rec.is_sent) {
      rec.sent_at = new Date().toISOString();
    }
    this.records.set(id, rec);
  }

  getPromptVersions() {
    return this.promptVersions;
  }

  rollbackPromptVersion(targetVersion: string): boolean {
    const found = this.promptVersions.find(p => p.version === targetVersion);
    if (!found) return false;
    this.promptVersions.forEach(p => (p.active = p.version === targetVersion));
    config.PROMPT_VERSION = targetVersion;
    return true;
  }
}

export const learningStore = new LearningStore();
