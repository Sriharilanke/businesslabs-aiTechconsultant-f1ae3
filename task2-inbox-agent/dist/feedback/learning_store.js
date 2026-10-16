"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.learningStore = exports.LearningStore = void 0;
const config_1 = require("../config");
class LearningStore {
    records = new Map();
    promptVersions = [
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
            version: config_1.config.PROMPT_VERSION,
            description: "Production version: strict refund/quote guardrails, 20-streak autonomy controls, and citation verification",
            active: true,
            created_at: "2026-10-14T00:00:00Z"
        }
    ];
    addRecord(record) {
        this.records.set(record.id, record);
    }
    getRecord(id) {
        return this.records.get(id);
    }
    getAllRecords() {
        return Array.from(this.records.values());
    }
    updateReview(id, decision, editedReply, reviewedBy) {
        const rec = this.records.get(id);
        if (!rec)
            return;
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
    rollbackPromptVersion(targetVersion) {
        const found = this.promptVersions.find(p => p.version === targetVersion);
        if (!found)
            return false;
        this.promptVersions.forEach(p => (p.active = p.version === targetVersion));
        config_1.config.PROMPT_VERSION = targetVersion;
        return true;
    }
}
exports.LearningStore = LearningStore;
exports.learningStore = new LearningStore();
