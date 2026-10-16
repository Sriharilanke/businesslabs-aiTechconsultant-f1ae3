import { z } from "zod";

export type EmailCategory =
  | "how_to"
  | "troubleshooting"
  | "project_request"
  | "refund_cancellation"
  | "complaint"
  | "quote_request"
  | "follow_up";

export type RiskLevel = "low" | "medium" | "high" | "critical";

export type ReviewDecision = "approved" | "edited" | "rejected" | "escalated";

export interface EmailMessage {
  id: string;
  sender_email: string;
  sender_name: string;
  subject: string;
  body: string;
  received_at: string;
  expected_category?: EmailCategory;
  expected_risk?: RiskLevel;
}

export interface ClassificationResult {
  category: EmailCategory;
  urgency: "low" | "medium" | "high";
  risk_level: RiskLevel;
  confidence: number;
  reasoning: string;
}

export interface Task1Citation {
  title: string;
  url: string;
  snippet: string;
  relevance_score: number;
  section_heading?: string;
  image_urls?: string[];
}

export interface Task1QueryResponse {
  answer: string;
  status: "answered" | "insufficient_evidence" | "escalated";
  sources: Task1Citation[];
  images?: Array<{
    image_url: string;
    description: string;
    alt_text?: string;
    ui_elements?: string[];
    uncertainty_score?: number;
  }>;
  confidence: number;
  needs_human: boolean;
  escalation_id?: number;
}

export interface StructuredDraft {
  category: EmailCategory;
  customer_request_summary: string;
  suggested_reply: string;
  supporting_sources: Task1Citation[];
  risk_level: RiskLevel;
  human_approval_required: boolean;
  autonomous_eligible: boolean;
  recommended_next_action: string;
  follow_up_date?: string;
  disclaimers: string[];
}

export interface EmailInteractionRecord {
  id: string;
  email: EmailMessage;
  classification: ClassificationResult;
  draft: StructuredDraft;
  human_decision?: ReviewDecision;
  human_edited_reply?: string;
  rejection_reason?: string;
  reviewed_by?: string;
  reviewed_at?: string;
  is_sent: boolean;
  sent_at?: string;
  prompt_version: string;
}

export interface CategoryAutonomyState {
  category: EmailCategory;
  consecutive_unmodified_sends: number;
  autonomy_enabled: boolean;
  total_approved: number;
  total_edited: number;
  total_rejected: number;
  last_downgrade_reason?: string;
  is_high_risk_exempt: boolean; // refunds, complaints, commercial quotes always require human sign-off
}

export const ProcessEmailInputSchema = z.object({
  id: z.string().optional(),
  sender_email: z.string().email(),
  sender_name: z.string().min(1),
  subject: z.string().min(1),
  body: z.string().min(5),
  conversation_history: z.array(z.string()).optional()
});

export const ReviewActionSchema = z.object({
  action: z.enum(["approve", "edit", "reject", "escalate"]),
  edited_reply: z.string().optional(),
  feedback_notes: z.string().optional(),
  reviewer_name: z.string().default("Consultant Reviewer")
});
