import type { ReactNode } from "react";

import type { ChatMessage } from "../types/chat";

interface ChatWindowProps {
  messages: ChatMessage[];
  onButtonClick: (text: string) => void;
}

function normaliseAnswerText(text: string): string {
  return text
    .replace(/\\n/g, "\n")
    .replace(/\\"/g, '"')
    .replace(/\\(?=[*\u2022])/g, "")
    .trim();
}

function AnswerText({ text }: { text: string }) {
  const lines = normaliseAnswerText(text).split(/\r?\n/);
  const blocks: ReactNode[] = [];
  let lineIndex = 0;

  while (lineIndex < lines.length) {
    const line = lines[lineIndex].trim();
    if (!line) {
      lineIndex += 1;
      continue;
    }

    const bullet = /^(?:[-*\u2022])\s+(.+)$/.exec(line);
    const numbered = /^(\d+)[.)]\s+(.+)$/.exec(line);
    if (bullet || numbered) {
      const ordered = Boolean(numbered);
      const items: string[] = [];
      while (lineIndex < lines.length) {
        const itemMatch = ordered
          ? /^(\d+)[.)]\s+(.+)$/.exec(lines[lineIndex].trim())
          : /^(?:[-*\u2022])\s+(.+)$/.exec(lines[lineIndex].trim());
        if (!itemMatch) break;
        items.push(itemMatch[ordered ? 2 : 1]);
        lineIndex += 1;
      }
      const List = ordered ? "ol" : "ul";
      blocks.push(
        <List
          key={`list-${lineIndex}`}
          className={ordered ? "list-decimal space-y-1 pl-5" : "list-disc space-y-1 pl-5"}
        >
          {items.map((item, itemIndex) => <li key={itemIndex}>{item}</li>)}
        </List>,
      );
      continue;
    }

    const paragraph: string[] = [];
    while (lineIndex < lines.length) {
      const current = lines[lineIndex].trim();
      if (!current || /^(?:[-*\u2022])\s+/.test(current) || /^\d+[.)]\s+/.test(current)) {
        break;
      }
      paragraph.push(current);
      lineIndex += 1;
    }
    blocks.push(<p key={`paragraph-${lineIndex}`}>{paragraph.join(" ")}</p>);
  }

  return <div className="space-y-3 whitespace-normal leading-7">{blocks}</div>;
}

const ChatWindow = ({ messages, onButtonClick }: ChatWindowProps) => (
  <div className="space-y-4 pb-4">
    {messages.map((message) => {
      const isUser = message.role === "user";
      const isSystem = message.role === "system";
      return (
        <div
          key={message.id}
          className={isSystem ? "flex justify-center" : isUser ? "flex justify-end" : "flex justify-start"}
        >
          <div className={isSystem ? "max-w-[90%] text-center" : "max-w-[85%]"}>
            <div
              className={
                isSystem
                  ? "rounded-xl bg-blue-50 px-4 py-2 text-sm text-blue-900"
                  : isUser
                    ? "rounded-2xl bg-black px-4 py-3 text-white"
                    : "rounded-2xl border border-gray-200 bg-white px-4 py-3 text-gray-800 shadow-sm"
              }
            >
              {isUser || isSystem ? message.text : <AnswerText text={message.text} />}
            </div>
            {message.role === "assistant" && (
              <p className="mt-1 text-xs text-gray-400">
                {message.answerMode === "pdf_grounded"
                  ? `Based on ${message.sourceCount ?? 0} textbook excerpt${message.sourceCount === 1 ? "" : "s"}`
                  : "General knowledge"}
              </p>
            )}
            <p className={`mt-1 text-xs text-gray-400 ${isUser ? "text-right" : "text-left"}`}>
              {message.timestamp}
            </p>
          </div>
        </div>
      );
    })}

    {messages.length === 0 && (
      <div className="flex flex-col items-center justify-center py-20 text-center">
        <h1 className="mb-2 text-2xl font-semibold">How can I help you?</h1>
        <p className="mb-6 text-gray-500">Ask a question or add PDF textbooks with the paperclip.</p>
        <div className="flex flex-wrap justify-center gap-3">
          {["What is biology?", "What is photosynthesis?", "Explain respiration", "What is the capital of France?"].map((question) => (
            <button
              key={question}
              type="button"
              onClick={() => onButtonClick(question)}
              className="rounded-xl border border-gray-300 px-4 py-2 transition hover:bg-gray-100"
            >
              {question}
            </button>
          ))}
        </div>
      </div>
    )}
  </div>
);

export default ChatWindow;
