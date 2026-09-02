interface MessageType {
  id: string;
  text: string;
  timestamp: string;
}

interface ChatWindowProps {
  messages: MessageType[];
  onButtonClick: (text: string) => void;
}

const ChatWindow = ({
  messages,
  onButtonClick,
}: ChatWindowProps) => {
  return (
    <div className="space-y-4">

      {/* Messages */}
      {messages.map((message) => (
        <div
          key={message.id}
          className="flex justify-end"
        >
          <div className="max-w-[80%]">

            <div className="bg-black text-white rounded-2xl px-4 py-3">
              {message.text}
            </div>

            <p className="text-xs text-gray-400 mt-1 text-right">
              {message.timestamp}
            </p>

          </div>
        </div>
      ))}

      {/* Show suggestion buttons when there are no messages */}
      {messages.length === 0 && (
        <div className="flex flex-col items-center justify-center py-20">

          <h1 className="text-2xl font-semibold mb-2">
            How can I help you?
          </h1>

          <p className="text-gray-500 mb-6">
            Choose a suggestion or type your own question.
          </p>

          {/* Suggestion buttons */}
          <div className="flex flex-wrap justify-center gap-3">

            <button
              type="button"
              onClick={() =>
                onButtonClick("Explain React to me")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              Explain React
            </button>

            <button
              type="button"
              onClick={() =>
                onButtonClick("Help me write JavaScript code")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              Write JavaScript
            </button>

            <button
              type="button"
              onClick={() =>
                onButtonClick("Teach me TypeScript")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              Learn TypeScript
            </button>

            <button
              type="button"
              onClick={() =>
                onButtonClick("Help me build a React website")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              Build a React website
            </button>

          </div>

        </div>
      )}

    </div>
  );
};

export default ChatWindow;