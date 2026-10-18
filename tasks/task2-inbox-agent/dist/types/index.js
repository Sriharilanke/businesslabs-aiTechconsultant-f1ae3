"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ReviewActionSchema = exports.ProcessEmailInputSchema = void 0;
const zod_1 = require("zod");
exports.ProcessEmailInputSchema = zod_1.z.object({
    id: zod_1.z.string().optional(),
    sender_email: zod_1.z.string().email(),
    sender_name: zod_1.z.string().min(1),
    subject: zod_1.z.string().min(1),
    body: zod_1.z.string().min(5),
    conversation_history: zod_1.z.array(zod_1.z.string()).optional()
});
exports.ReviewActionSchema = zod_1.z.object({
    action: zod_1.z.enum(["approve", "edit", "reject", "escalate"]),
    edited_reply: zod_1.z.string().optional(),
    feedback_notes: zod_1.z.string().optional(),
    reviewer_name: zod_1.z.string().default("Consultant Reviewer")
});
