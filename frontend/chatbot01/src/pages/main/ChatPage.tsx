import { useState } from "react";

import ChatInput from "../../components/ChatInput";
import ChatWindow from "../../components/ChatWindow";
import LoadingIndicator from "../../components/LoadingIndicator";
import { sendChatQuestion, uploadTextbooks } from "../../services/chatService";
import type { ChatMessage } from "../../types/chat";

function timestamp(): string {
  return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function newMessage(
  role: ChatMessage["role"],
  text: string,
  details: Partial<ChatMessage> = {},
): ChatMessage {
  return { id: crypto.randomUUID(), role, text, timestamp: timestamp(), ...details };
}

const ChatPage = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = async (text: string) => {
    setMessages((previous) => [...previous, newMessage("user", text)]);
    setIsLoading(true);
    try {
      const response = await sendChatQuestion(text);
      setMessages((previous) => [
        ...previous,
        newMessage("assistant", response.answer, {
          answerMode: response.answer_mode,
          sourceCount: response.source_chunks.length,
        }),
      ]);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to reach the chatbot.";
      setMessages((previous) => [...previous, newMessage("system", `Could not get an answer: ${message}`)]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUploadTextbooks = async (files: File[]) => {
    const names = files.slice(0, 3).map((file) => file.name).join(", ");
    const extra = files.length > 3 ? ` and ${files.length - 3} more` : "";
    setMessages((previous) => [
      ...previous,
      newMessage("system", `Adding ${files.length} PDF textbook${files.length === 1 ? "" : "s"}: ${names}${extra}`),
    ]);
    setIsLoading(true);
    try {
      const results = await uploadTextbooks(files);
      const indexed = results.filter((result) => result.status === "indexed");
      const failed = results.filter((result) => result.status === "failed");
      const chunks = indexed.reduce((total, result) => total + result.chunks_indexed, 0);
      const failureNote = failed.length
        ? ` ${failed.length} file${failed.length === 1 ? "" : "s"} could not be read.`
        : "";
      setMessages((previous) => [
        ...previous,
        newMessage(
          "system",
          `${indexed.length} textbook${indexed.length === 1 ? "" : "s"} ready for questions (${chunks} searchable passages).${failureNote}`,
        ),
      ]);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to add the textbooks.";
      setMessages((previous) => [...previous, newMessage("system", `Could not add textbooks: ${message}`)]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="mx-auto flex h-[calc(100vh-8rem)] w-full max-w-4xl flex-col justify-between">
      <div className="flex-1 overflow-y-auto pr-2">
        <ChatWindow messages={messages} onButtonClick={setInputValue} />
        {isLoading && <div className="mt-4"><LoadingIndicator /></div>}
      </div>

      <div className="mt-4 bg-white pb-4">
        <ChatInput
          inputValue={inputValue}
          setInputValue={setInputValue}
          onSendMessage={handleSendMessage}
          onUploadTextbooks={handleUploadTextbooks}
          disabled={isLoading}
        />
      </div>
    </div>
  );
};

export default ChatPage;
