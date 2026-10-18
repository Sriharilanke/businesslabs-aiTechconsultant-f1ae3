"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.draftGenerator = exports.DraftGenerator = void 0;
const config_1 = require("../config");
class DraftGenerator {
    generateDraft(email, classification, knowledge, isCategoryAutonomyActive = false) {
        const senderName = email.sender_name.split(" ")[0] || "Valued Client";
        const category = classification.category;
        const sources = knowledge.sources || [];
        const disclaimers = [];
        let customerSummary = "";
        let suggestedReply = "";
        let recommendedNextAction = "";
        let followUpDate = undefined;
        let humanApprovalRequired = true;
        // Build customer request summary
        customerSummary = `Customer ${email.sender_name} inquiries regarding '${email.subject}'. Category: ${category.toUpperCase()} (Urgency: ${classification.urgency}, Risk: ${classification.risk_level}).`;
        // 1. Safety Guardrail: Refund / Financial
        if (category === "refund_cancellation") {
            humanApprovalRequired = true;
            disclaimers.push("Financial policy: Automated drafts cannot authorize monetary disbursements or binding cancellations without finance manager review.");
            suggestedReply = [
                `Dear ${senderName},`,
                ``,
                `Thank you for contacting ${config_1.config.COMPANY_NAME} Support regarding your account subscription.`,
                ``,
                `We have received your cancellation and refund inquiry. As per our standard billing protocol, our accounting department reviews transaction history and billing cycles prior to processing payment reversals to the original payment method.`,
                ``,
                `For self-service management, members can also control recurring renewals directly under 'Manage Account > Change Plan > Stop Recurring Billing' in their member dashboard.`,
                ``,
                `A senior billing specialist has been assigned to your ticket to verify your transaction records and provide a formal confirmation within 1 business day.`,
                ``,
                `Best regards,`,
                `${config_1.config.COMPANY_NAME} Support Team`
            ].join("\n");
            recommendedNextAction = "Assign ticket to Billing Operations for transaction audit and Stripe reversal authorization.";
            followUpDate = new Date(Date.now() + 24 * 3600 * 1000).toISOString().split("T")[0];
        }
        // 2. Safety Guardrail: Quotes & Pricing
        else if (category === "quote_request" || category === "project_request") {
            humanApprovalRequired = true;
            disclaimers.push("Commercial policy: AI assistants cannot offer binding price quotes or guaranteed delivery deadlines.");
            let knowledgeNote = "";
            if (knowledge.sources && knowledge.sources.length > 0) {
                knowledgeNote = `Initial feasibility check indicates that parts of this request may be supported through built-in platform configurations (${knowledge.sources[0].title}), which can significantly optimize project timeline and cost.\n\n`;
            }
            suggestedReply = [
                `Dear ${senderName},`,
                ``,
                `Thank you for reaching out to ${config_1.config.COMPANY_NAME} with your project requirements regarding "${email.subject}".`,
                ``,
                `Our technical consulting team specializes in architectural scoping, custom extensions, and enterprise workflows. ${knowledgeNote}To prepare an accurate Scope of Work (SOW) and developer task breakdown with transparent low/likely/high hour estimates, we would like to schedule a brief 25-minute technical discovery call.`,
                ``,
                `Please let us know your availability over the next two business days, or share any additional technical specifications.`,
                ``,
                `Warm regards,`,
                `Senior Technical Consulting Practice, ${config_1.config.COMPANY_NAME}`
            ].join("\n");
            recommendedNextAction = "Schedule technical scoping call with Solutions Architect and prepare Meeting-to-Scope analysis.";
            followUpDate = new Date(Date.now() + 48 * 3600 * 1000).toISOString().split("T")[0];
        }
        // 3. Safety Guardrail: Complaints / Dissatisfaction
        else if (category === "complaint") {
            humanApprovalRequired = true;
            disclaimers.push("Executive escalation: Customer sentiment flagged critical/high risk. Human manager review required before sending.");
            suggestedReply = [
                `Dear ${senderName},`,
                ``,
                `Thank you for bringing this situation directly to our attention. I understand your frustration regarding ${email.subject.toLowerCase()}, and I sincerely apologize for the disruption this has caused your operations.`,
                ``,
                `Please be assured that your concern has been escalated directly to our Lead Technical Consultant and Service Leadership team. We are currently performing an expedited review of your site configuration and recent platform logs.`,
                ``,
                `A dedicated team member will contact you within 2 hours with a comprehensive update and concrete resolution plan.`,
                ``,
                `Sincerely,`,
                `Client Operations Leadership, ${config_1.config.COMPANY_NAME}`
            ].join("\n");
            recommendedNextAction = "Immediate executive review and technical diagnostic triage.";
            followUpDate = new Date(Date.now() + 2 * 3600 * 1000).toISOString().split("T")[0];
        }
        // 4. Follow-Up
        else if (category === "follow_up") {
            humanApprovalRequired = true;
            suggestedReply = [
                `Dear ${senderName},`,
                ``,
                `Thank you for following up with us regarding "${email.subject}".`,
                ``,
                `We are actively tracking your previous request. Our technical team is reviewing the necessary details and will have a comprehensive status update for you shortly.`,
                ``,
                `If you have any urgent updates or additional requirements in the meantime, please feel free to reply directly to this email.`,
                ``,
                `Best regards,`,
                `${config_1.config.COMPANY_NAME} Client Support`
            ].join("\n");
            recommendedNextAction = "Check status of open ticket/deliverable with assigned consultant.";
            followUpDate = new Date(Date.now() + 24 * 3600 * 1000).toISOString().split("T")[0];
        }
        // 5. How-To & Troubleshooting (Grounded in Knowledge Brain)
        else {
            if (knowledge.status === "answered" && sources.length > 0) {
                const topSource = sources[0];
                const citationUrls = sources.map(s => `• ${s.title}: ${s.url}`).join("\n");
                let visualGuidance = "";
                if (knowledge.images && knowledge.images.length > 0) {
                    const img = knowledge.images[0];
                    visualGuidance = `\n\nVisual UI Reference:\n${img.description}`;
                }
                suggestedReply = [
                    `Dear ${senderName},`,
                    ``,
                    `Thank you for reaching out to ${config_1.config.COMPANY_NAME} Support.`,
                    ``,
                    `Here is the step-by-step guidance for your inquiry:`,
                    ``,
                    `${knowledge.answer}`,
                    `${visualGuidance}`,
                    ``,
                    `For complete documentation, you can also review the official knowledge base guides:`,
                    `${citationUrls}`,
                    ``,
                    `Please let us know if you need any additional assistance.`,
                    ``,
                    `Best regards,`,
                    `${config_1.config.COMPANY_NAME} Support Team`
                ].join("\n");
                recommendedNextAction = "Send resolution guide and monitor customer response.";
                // Autonomy eligibility condition:
                // Only low-risk how-to questions with high confidence and verified knowledge can qualify for autonomous sending
                if (isCategoryAutonomyActive && classification.risk_level === "low" && knowledge.confidence >= 0.80) {
                    humanApprovalRequired = false;
                }
                else {
                    humanApprovalRequired = true;
                }
            }
            else {
                // Knowledge Brain could not answer
                humanApprovalRequired = true;
                disclaimers.push("Knowledge Brain returned insufficient evidence. Escalated to Tier 2 technical team.");
                suggestedReply = [
                    `Dear ${senderName},`,
                    ``,
                    `Thank you for contacting ${config_1.config.COMPANY_NAME} Support regarding "${email.subject}".`,
                    ``,
                    `Your question requires specialized configuration details that are currently being verified with our senior technical consultants. We are reviewing your specific setup and will reply with a detailed solution shortly.`,
                    ``,
                    `Thank you for your patience.`,
                    ``,
                    `Best regards,`,
                    `${config_1.config.COMPANY_NAME} Technical Support`
                ].join("\n");
                recommendedNextAction = "Technical expert review required to answer undocumented product behavior.";
                followUpDate = new Date(Date.now() + 24 * 3600 * 1000).toISOString().split("T")[0];
            }
        }
        return {
            category,
            customer_request_summary: customerSummary,
            suggested_reply: suggestedReply,
            supporting_sources: sources,
            risk_level: classification.risk_level,
            human_approval_required: humanApprovalRequired,
            autonomous_eligible: !humanApprovalRequired,
            recommended_next_action: recommendedNextAction,
            follow_up_date: followUpDate,
            disclaimers
        };
    }
}
exports.DraftGenerator = DraftGenerator;
exports.draftGenerator = new DraftGenerator();
