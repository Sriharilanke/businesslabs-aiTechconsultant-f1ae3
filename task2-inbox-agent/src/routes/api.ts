import { Router, Request, Response } from "express";
import { randomUUID } from "crypto";
import { ProcessEmailInputSchema, ReviewActionSchema, EmailMessage, EmailInteractionRecord } from "../types";
import { emailClassifier } from "../email/classifier";
import { knowledgeClient } from "../knowledge-client/client";
import { draftGenerator } from "../drafting/drafter";
import { autonomyEngine } from "../feedback/autonomy_engine";
import { learningStore } from "../feedback/learning_store";
import { CUSTOMER_EMAILS_DATASET } from "../email/dataset";
import { config } from "../config";

export const apiRouter = Router();

// 1. Process an incoming email
apiRouter.post("/emails/process", async (req: Request, res: Response) => {
  const parseResult = ProcessEmailInputSchema.safeParse(req.body);
  if (!parseResult.success) {
    return res.status(400).json({ error: "Invalid email payload", details: parseResult.error.format() });
  }

  const input = parseResult.data;
  const emailMsg: EmailMessage = {
    id: input.id || `email_${Date.now()}`,
    sender_email: input.sender_email,
    sender_name: input.sender_name,
    subject: input.subject,
    body: input.body,
    received_at: new Date().toISOString()
  };

  // 1. Classify intent, urgency and risk
  const classification = emailClassifier.classify(emailMsg.subject, emailMsg.body);

  // 2. Query Knowledge Brain (Task 1) over HTTP
  const knowledge = await knowledgeClient.queryKnowledge(
    `${emailMsg.subject} ${emailMsg.body}`.substring(0, 300)
  );

  // 3. Check Category Autonomy
  const categoryState = autonomyEngine.getCategoryState(classification.category);
  const isAutonomyActive = categoryState.autonomy_enabled && !categoryState.is_high_risk_exempt;

  // 4. Generate Structured Draft
  const draft = draftGenerator.generateDraft(emailMsg, classification, knowledge, isAutonomyActive);

  // 5. Store Interaction Record
  const record: EmailInteractionRecord = {
    id: emailMsg.id,
    email: emailMsg,
    classification,
    draft,
    is_sent: false,
    prompt_version: config.PROMPT_VERSION
  };

  // If autonomously sent without human intervention
  if (draft.autonomous_eligible) {
    record.is_sent = true;
    record.sent_at = new Date().toISOString();
    record.human_decision = "approved";
    record.reviewed_by = "Autonomous System (20+ Streak Verified)";
    autonomyEngine.recordReviewOutcome(classification.category, "approved", draft.suggested_reply);
  }

  learningStore.addRecord(record);

  return res.json({
    record_id: record.id,
    classification,
    knowledge_status: knowledge.status,
    draft,
    autonomous_sent: draft.autonomous_eligible,
    autonomy_status: autonomyEngine.getCategoryState(classification.category)
  });
});

// 2. Get list of dataset emails and processed history
apiRouter.get("/emails", (req: Request, res: Response) => {
  const datasetWithStatus = CUSTOMER_EMAILS_DATASET.map(email => {
    const existing = learningStore.getRecord(email.id);
    return {
      email,
      processed: !!existing,
      record: existing || null
    };
  });
  return res.json(datasetWithStatus);
});

// 3. Get single email detail
apiRouter.get("/emails/:id", (req: Request, res: Response) => {
  const emailId = String(req.params.id);
  const record = learningStore.getRecord(emailId);
  if (!record) {
    const fromDataset = CUSTOMER_EMAILS_DATASET.find(e => e.id === emailId);
    if (!fromDataset) {
      return res.status(404).json({ error: "Email ID not found" });
    }
    return res.json({ email: fromDataset, processed: false, record: null });
  }
  return res.json({ email: record.email, processed: true, record });
});

// 4. Human Review Action (Approve, Edit, Reject, Escalate)
apiRouter.post("/emails/:id/review", (req: Request, res: Response) => {
  const parseResult = ReviewActionSchema.safeParse(req.body);
  if (!parseResult.success) {
    return res.status(400).json({ error: "Invalid review action", details: parseResult.error.format() });
  }

  const emailId = String(req.params.id);
  const { action, edited_reply, reviewer_name, feedback_notes } = parseResult.data;
  const record = learningStore.getRecord(emailId);
  if (!record) {
    return res.status(404).json({ error: "Record not found to review" });
  }

  const originalDraft = record.draft.suggested_reply;
  const finalReply = action === "edit" ? edited_reply : originalDraft;

  // Update autonomy state
  const decisionMap: Record<string, "approved" | "edited" | "rejected" | "escalated"> = {
    approve: "approved",
    edit: "edited",
    reject: "rejected",
    escalate: "escalated"
  };
  const decision = decisionMap[action];

  const updatedState = autonomyEngine.recordReviewOutcome(
    record.classification.category,
    decision,
    originalDraft,
    finalReply,
    feedback_notes
  );

  // Update learning store record
  learningStore.updateReview(record.id, decision, finalReply, reviewer_name);

  return res.json({
    status: "success",
    decision,
    is_sent: record.is_sent,
    updated_autonomy_state: updatedState,
    record: learningStore.getRecord(record.id)
  });
});

// 5. Get Autonomy states for all 7 categories
apiRouter.get("/autonomy-status", (req: Request, res: Response) => {
  return res.json(autonomyEngine.getAllStates());
});

// 6. Test Streak endpoint for demo
apiRouter.post("/autonomy/test-streak", (req: Request, res: Response) => {
  const { category, streak } = req.body;
  if (!category || streak === undefined) {
    return res.status(400).json({ error: "Missing category or streak" });
  }
  autonomyEngine.forceSetStreak(category, parseInt(streak, 10));
  return res.json({
    message: `Streak for category '${category}' set to ${streak}`,
    state: autonomyEngine.getCategoryState(category)
  });
});

// 7. System stats
apiRouter.get("/stats", (req: Request, res: Response) => {
  const records = learningStore.getAllRecords();
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
    prompt_version: config.PROMPT_VERSION,
    dataset_size: CUSTOMER_EMAILS_DATASET.length
  });
});
