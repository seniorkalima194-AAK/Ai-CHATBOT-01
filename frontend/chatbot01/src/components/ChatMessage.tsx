import { HandIcon } from 'lucide-react';

// 1. Explicitly define the props structure
interface ChatMessageProps {
  isWelcomeScreen?: boolean;
}

const ChatMessage = ({ isWelcomeScreen = false }: ChatMessageProps) => {
  if (!isWelcomeScreen) return null;

  return (
    <div className="flex flex-col items-center justify-center py-20 text-center gap-4">
      <div className="flex items-center gap-3">
        <h2 className="text-3xl md:text-5xl font-bold text-gray-800 tracking-tight">
          Hello
        </h2>
        <HandIcon size={40} className="text-gray-900" />
      </div>
      <p className="text-gray-500 text-lg max-w-md">
        How can I help you adjust your learning system paths today?
      </p>
    </div>
  );
};

export default ChatMessage;
