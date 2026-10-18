"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.emailClassifier = exports.EmailClassifier = void 0;
class EmailClassifier {
    classify(subject, body) {
        const text = `${subject} \n ${body}`.toLowerCase();
        const matchesAny = (patterns) => {
            return patterns.some(p => {
                if (typeof p === "string") {
                    return text.includes(p);
                }
                return p.test(text);
            });
        };
        // 1. Complaint Detection (High / Critical Risk)
        const isComplaint = matchesAny([
            /\blawyer\b/,
            /\bsue\b/,
            /\blegal\b/,
            /\bthreat\b/,
            /\bunacceptable\b/,
            /\bhorrible\b/,
            /\bdisaster\b/,
            /\bterrible\b/,
            /\bdisappointed\b/,
            /\bsubstandard\b/,
            "ruined our launch",
            "escalate to management",
            "without reply from your support",
            "threatening legal action"
        ]);
        if (isComplaint) {
            const isCritical = matchesAny([/\blawyer\b/, /\bsue\b/, /\blegal\b/, "chargeback"]);
            return {
                category: "complaint",
                urgency: isCritical ? "high" : "medium",
                risk_level: isCritical ? "critical" : "high",
                confidence: 0.95,
                reasoning: "Customer expresses significant dissatisfaction or escalatory intent."
            };
        }
        // 2. Refund or Cancellation Detection (High Financial Risk)
        const isRefund = matchesAny([
            /\brefund\b/,
            /\bcancel\b/,
            /\bchargeback\b/,
            "money back",
            "billing error",
            "terminate account",
            "prorated refund",
            "duplicate charge"
        ]);
        if (isRefund) {
            return {
                category: "refund_cancellation",
                urgency: text.includes("immediately") || text.includes("unauthorized") ? "high" : "medium",
                risk_level: "high",
                confidence: 0.96,
                reasoning: "Inquiry directly involves financial refund, billing error, or subscription termination."
            };
        }
        // 3. Quote Request (Commercial Risk)
        const isQuote = matchesAny([
            /\bquote\b/,
            /\bpricing\b/,
            /\bcost\b/,
            /\bretainer\b/,
            /\bbudget\b/,
            "how much would it cost",
            "hourly rate",
            "estimate cost",
            "what would your consulting team charge",
            "formal cost quote"
        ]);
        if (isQuote) {
            return {
                category: "quote_request",
                urgency: "medium",
                risk_level: "high",
                confidence: 0.93,
                reasoning: "Commercial pricing inquiry requiring scoping before financial commitment."
            };
        }
        // 4. Project Request (Scope Risk)
        const isProject = matchesAny([
            "custom feature",
            "bespoke",
            "custom two-way sync",
            "build a new",
            "hire you to",
            "develop an integration",
            "redesign our",
            "custom portal",
            "custom escrow",
            "hipaa compliant"
        ]);
        if (isProject) {
            return {
                category: "project_request",
                urgency: "medium",
                risk_level: "high",
                confidence: 0.92,
                reasoning: "Client requests custom engineering, architecture overhaul, or bespoke design deliverables."
            };
        }
        // 5. Follow-Up (Context & Continuity Risk)
        const isFollowUp = matchesAny([
            "following up",
            "any update",
            "checking in",
            "status of our",
            "status update",
            "did you receive",
            "per my previous email",
            "ticket #"
        ]);
        if (isFollowUp) {
            return {
                category: "follow_up",
                urgency: text.includes("urgent") || text.includes("hours") ? "high" : "medium",
                risk_level: "medium",
                confidence: 0.94,
                reasoning: "Customer inquiring about pending deliverables, ticket progress, or previous correspondence."
            };
        }
        // 6. Troubleshooting (Moderate Risk)
        const isTroubleshooting = matchesAny([
            /\berror\b/,
            /\bbroken\b/,
            /\bfailed\b/,
            /\bblurry\b/,
            /\bstretched\b/,
            /\boverlaps\b/,
            /\bwarning\b/,
            /\bspam\b/,
            /\bduplicate\b/,
            "not working",
            "not appearing",
            "disabled on mobile",
            "grayed out",
            "not displaying",
            "not showing",
            "connection not secure"
        ]);
        if (isTroubleshooting) {
            return {
                category: "troubleshooting",
                urgency: text.includes("production down") || text.includes("cannot checkout") ? "high" : "medium",
                risk_level: "medium",
                confidence: 0.92,
                reasoning: "Technical defect, visual glitch, or integration malfunction reported."
            };
        }
        // 7. How-To Question (Default operational guidance)
        return {
            category: "how_to",
            urgency: "low",
            risk_level: "low",
            confidence: 0.90,
            reasoning: "Customer seeking operational instructions or configuration guidance."
        };
    }
}
exports.EmailClassifier = EmailClassifier;
exports.emailClassifier = new EmailClassifier();
