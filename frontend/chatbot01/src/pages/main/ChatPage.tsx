import { useState } from "react";
import ChatWindow from "../../components/ChatWindow";
import ChatInput from "../../components/ChatInput";
import LoadingIndicator from "../../components/LoadingIndicator";

interface MessageType {
  id: string;
  text: string;
  timestamp: string;
}

const ChatPage = () => {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Text that will be inserted into the typing box
  const [inputValue, setInputValue] = useState("");

  const handleSendMessage = (text: string) => {
    if (!text.trim()) return;

    const newMessage: MessageType = {
      id: Date.now().toString(),
      text: text,
      timestamp: new Date().toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      }),
    };

    setMessages((prev) => [...prev, newMessage]);

    setInputValue("");
    setIsLoading(true);

    setTimeout(() => {
      setIsLoading(false);
    }, 3000);
  };

  // Button uses this function to put text inside input
  const handleButtonClick = (text: string) => {
    setInputValue(text);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] justify-between max-w-4xl mx-auto w-full">

      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto pr-2">
        <ChatWindow
          messages={messages}
          onButtonClick={handleButtonClick}
        />

        {isLoading && (
          <div className="mt-4">
            <LoadingIndicator />
          </div>
        )}
      </div>

      {/* Chat input */}
      <div className="mt-4 bg-white pb-4">
        <ChatInput
          inputValue={inputValue}
          setInputValue={setInputValue}
          onSendMessage={handleSendMessage}
        />
      </div>

    </div>
  );
};

export default ChatPage;