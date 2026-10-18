import { EmailCategory, CategoryAutonomyState, ReviewDecision } from "../types";
import { config } from "../config";

export class AutonomyEngine {
  private categoryStates: Map<EmailCategory, CategoryAutonomyState>;

  constructor() {
    this.categoryStates = new Map();
    const categories: EmailCategory[] = [
      "how_to",
      "troubleshooting",
      "project_request",
      "refund_cancellation",
      "complaint",
      "quote_request",
      "follow_up"
    ];

    categories.forEach(cat => {
      // High-risk categories can NEVER be sent autonomously without human review
      const isExempt = ["refund_cancellation", "complaint", "quote_request", "project_request"].includes(cat);
      this.categoryStates.set(cat, {
        category: cat,
        consecutive_unmodified_sends: 0,
        autonomy_enabled: false,
        total_approved: 0,
        total_edited: 0,
        total_rejected: 0,
        is_high_risk_exempt: isExempt
      });
    });
  }

  isUnmodified(originalDraft: string, finalSentText: string): boolean {
    const cleanOrig = originalDraft.replace(/\s+/g, " ").trim().toLowerCase();
    const cleanFinal = finalSentText.replace(/\s+/g, " ").trim().toLowerCase();
    if (cleanOrig === cleanFinal) return true;

    // Character length difference check (within 2% considered minor typo fix)
    const lenDiff = Math.abs(cleanOrig.length - cleanFinal.length);
    const maxLen = Math.max(cleanOrig.length, cleanFinal.length);
    return lenDiff / maxLen < 0.02;
  }

  recordReviewOutcome(
    category: EmailCategory,
    decision: ReviewDecision,
    originalDraft: string,
    finalText?: string,
    downgradeReason?: string
  ): CategoryAutonomyState {
    const state = this.categoryStates.get(category)!;

    if (state.is_high_risk_exempt) {
      // High risk category: update counts but streak never grants autonomy
      if (decision === "approved") state.total_approved++;
      if (decision === "edited") state.total_edited++;
      if (decision === "rejected") state.total_rejected++;
      return { ...state };
    }

    if (decision === "approved") {
      state.total_approved++;
      const unmodified = !finalText || this.isUnmodified(originalDraft, finalText);

      if (unmodified) {
        state.consecutive_unmodified_sends++;
        // Check if 20-streak threshold is reached
        if (state.consecutive_unmodified_sends >= config.AUTONOMY_CONSECUTIVE_THRESHOLD) {
          state.autonomy_enabled = true;
        }
      } else {
        // Minor edit detected
        state.consecutive_unmodified_sends = 0;
        state.total_edited++;
        if (state.autonomy_enabled) {
          state.autonomy_enabled = false;
          state.last_downgrade_reason = "Human edit introduced to drafted text. Autonomy revoked to protect quality.";
        }
      }
    } else if (decision === "edited") {
      state.total_edited++;
      state.consecutive_unmodified_sends = 0;
      if (state.autonomy_enabled) {
        state.autonomy_enabled = false;
        state.last_downgrade_reason = "Reviewer modified draft content. Resetting autonomy count.";
      }
    } else if (decision === "rejected" || decision === "escalated") {
      state.total_rejected++;
      state.consecutive_unmodified_sends = 0;
      if (state.autonomy_enabled) {
        state.autonomy_enabled = false;
        state.last_downgrade_reason = downgradeReason || "Reviewer rejected draft. Immediate safety fallback engaged.";
      }
    }

    return { ...state };
  }

  getCategoryState(category: EmailCategory): CategoryAutonomyState {
    return { ...this.categoryStates.get(category)! };
  }

  getAllStates(): CategoryAutonomyState[] {
    return Array.from(this.categoryStates.values());
  }

  forceSetStreak(category: EmailCategory, streak: number) {
    const state = this.categoryStates.get(category)!;
    state.consecutive_unmodified_sends = streak;
    if (streak >= config.AUTONOMY_CONSECUTIVE_THRESHOLD && !state.is_high_risk_exempt) {
      state.autonomy_enabled = true;
    } else {
      state.autonomy_enabled = false;
    }
  }
}

export const autonomyEngine = new AutonomyEngine();
