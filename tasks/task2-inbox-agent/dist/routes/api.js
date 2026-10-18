"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.apiRouter = void 0;
const express_1 = require("express");
const types_1 = require("../types");
const classifier_1 = require("../email/classifier");
const client_1 = require("../knowledge-client/client");
const drafter_1 = require("../drafting/drafter");
const autonomy_engine_1 = require("../feedback/autonomy_engine");
const learning_store_1 = require("../feedback/learning_store");
const dataset_1 = require("../email/dataset");
const config_1 = require("../config");
exports.apiRouter = (0, express_1.Router)();
// 1. Process an incoming email
exports.apiRouter.post("/emails/process", async (req, res) => {
    const parseResult = types_1.ProcessEmailInputSchema.safeParse(req.body);
    if (!parseResult.success) {
        return res.status(400).json({ error: "Invalid email payload", details: parseResult.error.format() });
    }
    const input = parseResult.data;
    const emailMsg = {
        id: input.id || `email_${Date.now()}`,
        sender_email: input.sender_email,
        sender_name: input.sender_name,
        subject: input.subject,
        body: input.body,
        received_at: new Date().toISOString()
    };
    // 1. Classify intent, urgency and risk
    const classification = classifier_1.emailClassifier.classify(emailMsg.subject, emailMsg.body);
    // 2. Query Knowledge Brain (Task 1) over HTTP
    const knowledge = await client_1.knowledgeClient.queryKnowledge(`${emailMsg.subject} ${emailMsg.body}`.substring(0, 300));
    // 3. Check Category Autonomy
    const categoryState = autonomy_engine_1.autonomyEngine.getCategoryState(classification.category);
    const isAutonomyActive = categoryState.autonomy_enabled && !categoryState.is_high_risk_exempt;
    // 4. Generate Structured Draft
    const draft = drafter_1.draftGenerator.generateDraft(emailMsg, classification, knowledge, isAutonomyActive);
    // 5. Store Interaction Record
    const record = {
        id: emailMsg.id,
        email: emailMsg,
        classification,
        draft,
        is_sent: false,
        prompt_version: config_1.config.PROMPT_VERSION
    };
    // If autonomously sent without human intervention
    if (draft.autonomous_eligible) {
        record.is_sent = true;
        record.sent_at = new Date().toISOString();
        record.human_decision = "approved";
        record.reviewed_by = "Autonomous System (20+ Streak Verified)";
        autonomy_engine_1.autonomyEngine.recordReviewOutcome(classification.category, "approved", draft.suggested_reply);
    }
    learning_store_1.learningStore.addRecord(record);
    return res.json({
        record_id: record.id,
        classification,
        knowledge_status: knowledge.status,
        draft,
        autonomous_sent: draft.autonomous_eligible,
        autonomy_status: autonomy_engine_1.autonomyEngine.getCategoryState(classification.category)
    });
});
// 2. Get list of dataset emails and processed history
exports.apiRouter.get("/emails", (req, res) => {
    const datasetWithStatus = dataset_1.CUSTOMER_EMAILS_DATASET.map(email => {
        const existing = learning_store_1.learningStore.getRecord(email.id);
        return {
            email,
            processed: !!existing,
            record: existing || null
        };
    });
    return res.json(datasetWithStatus);
});
// 3. Get single email detail
exports.apiRouter.get("/emails/:id", (req, res) => {
    const emailId = String(req.params.id);
    const record = learning_store_1.learningStore.getRecord(emailId);
    if (!record) {
        const fromDataset = dataset_1.CUSTOMER_EMAILS_DATASET.find(e => e.id === emailId);
        if (!fromDataset) {
            return res.status(404).json({ error: "Email ID not found" });
        }
        return res.json({ email: fromDataset, processed: false, record: null });
    }
    return res.json({ email: record.email, processed: true, record });
});
// 4. Human Review Action (Approve, Edit, Reject, Escalate)
exports.apiRouter.post("/emails/:id/review", (req, res) => {
    const parseResult = types_1.ReviewActionSchema.safeParse(req.body);
    if (!parseResult.success) {
        return res.status(400).json({ error: "Invalid review action", details: parseResult.error.format() });
    }
    const emailId = String(req.params.id);
    const { action, edited_reply, reviewer_name, feedback_notes } = parseResult.data;
    const record = learning_store_1.learningStore.getRecord(emailId);
    if (!record) {
        return res.status(404).json({ error: "Record not found to review" });
    }
    const originalDraft = record.draft.suggested_reply;
    const finalReply = action === "edit" ? edited_reply : originalDraft;
    // Update autonomy state
    const decisionMap = {
        approve: "approved",
        edit: "edited",
        reject: "rejected",
        escalate: "escalated"
    };
    const decision = decisionMap[action];
    const updatedState = autonomy_engine_1.autonomyEngine.recordReviewOutcome(record.classification.category, decision, originalDraft, finalReply, feedback_notes);
    // Update learning store record
    learning_store_1.learningStore.updateReview(record.id, decision, finalReply, reviewer_name);
    return res.json({
        status: "success",
        decision,
        is_sent: record.is_sent,
        updated_autonomy_state: updatedState,
        record: learning_store_1.learningStore.getRecord(record.id)
    });
});
// 5. Get Autonomy states for all 7 categories
exports.apiRouter.get("/autonomy-status", (req, res) => {
    return res.json(autonomy_engine_1.autonomyEngine.getAllStates());
});
// 6. Test Streak endpoint for demo
exports.apiRouter.post("/autonomy/test-streak", (req, res) => {
    const { category, streak } = req.body;
    if (!category || streak === undefined) {
        return res.status(400).json({ error: "Missing category or streak" });
    }
    autonomy_engine_1.autonomyEngine.forceSetStreak(category, parseInt(streak, 10));
    return res.json({
        message: `Streak for category '${category}' set to ${streak}`,
        state: autonomy_engine_1.autonomyEngine.getCategoryState(category)
    });
});
// 7. System stats
exports.apiRouter.get("/stats", (req, res) => {
    const records = learning_store_1.learningStore.getAllRecords();
    const total = records.length;
    const approved = records.filter(r => r.human_decision === "approved").length;
    const edited = records.filter(r => r.human_decision === "edited").length;
    const rejected = records.filter(r => r.human_decision === "rejected").length;
    return res.json({
        total_processed: total,
        total_approved: approved,
        total_edited: edited,
        total_rejected: rejected,
        approval_rate: total > 0 ? Math.round((approved / total) * 100) : 0,
        edit_rate: total > 0 ? Math.round((edited / total) * 100) : 0,
        prompt_version: config_1.config.PROMPT_VERSION,
        dataset_size: dataset_1.CUSTOMER_EMAILS_DATASET.length
    });
});
