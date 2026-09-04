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
                onButtonClick("If you were me as a junior software developer what should you learn from the start")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              Computer software knowledge
            </button>

            <button
              type="button"
              onClick={() =>
                onButtonClick("justfy the term biology think as a genius")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              what is biology
            </button>

            <button
              type="button"
              onClick={() =>
                onButtonClick("Give me the mathematics exercises that had written according to my sysllabus of Tanzania but ask me first which level i am in so as you could answer better extract from the pdfs you know")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              Mathematics examination questions
            </button>

            <button
              type="button"
              onClick={() =>
                onButtonClick("Elezea kuhusu historia ya  Kiswahili ")
              }
              className="border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-100 transition"
            >
              Kiswahili
            </button>

          </div>

        </div>
      )}

    </div>
  );
};

export default ChatWindow;