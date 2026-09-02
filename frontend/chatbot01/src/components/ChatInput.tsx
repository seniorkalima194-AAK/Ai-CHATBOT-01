import { useRef, useState } from "react";
import {
  CameraIcon,
  PaperclipIcon,
  Send,
  X,
  FileText,
  Image as ImageIcon,
} from "lucide-react";

interface ChatInputProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (text: string) => void;
}

const ChatInput = ({
  inputValue,
  setInputValue,
  onSendMessage,
}: ChatInputProps) => {

  const fileInputRef = useRef<HTMLInputElement>(null);
  const cameraInputRef = useRef<HTMLInputElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const handleAttachment = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    setSelectedFile(file);

    console.log("Attached file:", file);
  };
  const handleCamera = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (!file) return;

    setSelectedFile(file);

    console.log("Camera image:", file);
  };

  // Send message
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() && !selectedFile) {
      return;
    }

    let message = inputValue;

    // Add file name to message
    if (selectedFile) {
      message = message
        ? `${message}\n📎 ${selectedFile.name}`
        : `📎 ${selectedFile.name}`;
    }

    onSendMessage(message);

    // Clear selected file
    setSelectedFile(null);

    // Clear file input
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    if (cameraInputRef.current) {
      cameraInputRef.current.value = "";
    }
  };
  const removeFile = () => {
    setSelectedFile(null);

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }

    if (cameraInputRef.current) {
      cameraInputRef.current.value = "";
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border border-gray-300 rounded-2xl bg-white shadow-sm"
    >

      {}
      {selectedFile && (
        <div className="flex items-center justify-between px-4 pt-3">

          <div className="flex items-center gap-2 min-w-0">

            {selectedFile.type.startsWith("image/") ? (
              <ImageIcon size={18} className="text-gray-600" />
            ) : (
              <FileText size={18} className="text-gray-600" />
            )}

            <span className="text-sm text-gray-700 truncate">
              {selectedFile.name}
            </span>

          </div>

          <button
            type="button"
            onClick={removeFile}
            className="p-1 rounded-full hover:bg-gray-100"
          >
            <X size={18} />
          </button>

        </div>
      )}

      {}
      <div className="flex items-center gap-2 p-2">

        {}
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          className="p-2 rounded-full hover:bg-gray-100 transition"
          title="Attach file"
        >
          <PaperclipIcon size={20} />
        </button>

        {}
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={handleAttachment}
          accept="image/*,.pdf,.doc,.docx,.txt,.xlsx,.ppt,.pptx"
        />

        {}
        <button
          type="button"
          onClick={() => cameraInputRef.current?.click()}
          className="p-2 rounded-full hover:bg-gray-100 transition"
          title="Take a photo"
        >
          <CameraIcon size={20} />
        </button>

        {}
        <input
          ref={cameraInputRef}
          type="file"
          accept="image/*"
          capture="environment"
          className="hidden"
          onChange={handleCamera}
        />

      
        <input
          type="text"

          value={inputValue}
          
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="Ask anything..."
          className="flex-1 outline-none px-2 py-2 text-gray-800"
        />

        
        <button
          type="submit"
          disabled={!inputValue.trim() && !selectedFile}
          className="p-2 rounded-full bg-black text-white hover:bg-gray-800 disabled:opacity-40 disabled:cursor-not-allowed transition"
          title="Send"
        >
          <Send size={20} />
        </button>

      </div>

    </form>
  );
};

export default ChatInput;