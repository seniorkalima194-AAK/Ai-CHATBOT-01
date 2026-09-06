import { useRef, useState, type ChangeEvent, type FormEvent } from "react";
import { FileText, PaperclipIcon, Send, X } from "lucide-react";

interface ChatInputProps {
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (text: string) => Promise<void>;
  onUploadTextbooks: (files: File[]) => Promise<void>;
  disabled?: boolean;
}

const ChatInput = ({
  inputValue,
  setInputValue,
  onSendMessage,
  onUploadTextbooks,
  disabled = false,
}: ChatInputProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const isBusy = disabled || isSubmitting;

  const clearFiles = () => {
    setSelectedFiles([]);
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const handleAttachment = (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files ?? []);
    setSelectedFiles(files);
  };

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();
    const question = inputValue.trim();
    if (!question && selectedFiles.length === 0) return;

    setIsSubmitting(true);
    try {
      if (selectedFiles.length > 0) {
        await onUploadTextbooks(selectedFiles);
        clearFiles();
      }
      if (question) {
        await onSendMessage(question);
        setInputValue("");
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-2xl border border-gray-300 bg-white shadow-sm">
      {selectedFiles.length > 0 && (
        <div className="flex items-center justify-between gap-3 px-4 pt-3">
          <div className="flex min-w-0 items-center gap-2">
            <FileText size={18} className="shrink-0 text-gray-600" />
            <span className="truncate text-sm text-gray-700">
              {selectedFiles.length === 1
                ? selectedFiles[0].name
                : `${selectedFiles.length} PDF textbooks selected`}
            </span>
          </div>
          <button
            type="button"
            onClick={clearFiles}
            disabled={isBusy}
            className="rounded-full p-1 hover:bg-gray-100 disabled:cursor-not-allowed"
            aria-label="Remove selected textbooks"
          >
            <X size={18} />
          </button>
        </div>
      )}

      <div className="flex items-center gap-2 p-2">
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          disabled={isBusy}
          className="rounded-full p-2 transition hover:bg-gray-100 disabled:cursor-not-allowed disabled:opacity-40"
          title="Add PDF textbooks"
          aria-label="Add PDF textbooks"
        >
          <PaperclipIcon size={20} />
        </button>
        <input
          ref={fileInputRef}
          type="file"
          className="hidden"
          onChange={handleAttachment}
          accept="application/pdf,.pdf"
          multiple
        />

        <input
          type="text"
          value={inputValue}
          onChange={(event) => setInputValue(event.target.value)}
          placeholder="Ask a question, or attach PDF textbooks..."
          disabled={isBusy}
          className="flex-1 bg-transparent px-2 py-2 text-gray-800 outline-none disabled:cursor-not-allowed"
        />
        <button
          type="submit"
          disabled={isBusy || (!inputValue.trim() && selectedFiles.length === 0)}
          className="rounded-full bg-black p-2 text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-40"
          title={selectedFiles.length > 0 ? "Add selected textbooks" : "Send question"}
        >
          <Send size={20} />
        </button>
      </div>
    </form>
  );
};

export default ChatInput;
