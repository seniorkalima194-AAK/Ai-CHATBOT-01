import type { AnswerMode } from "../services/chatService";

export interface ChatMessage {
  id: string;
  role: "user" | "assistant" | "system";
  text: string;
  timestamp: string;
  answerMode?: AnswerMode;
  sourceCount?: number;
}
