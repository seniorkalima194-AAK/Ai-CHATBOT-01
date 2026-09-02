const LoadingIndicator = () => {
  return (
    <div className="flex items-center gap-2 text-gray-500">

      <div className="flex gap-1">
        <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>

        <span
          className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
          style={{ animationDelay: "0.15s" }}
        ></span>

        <span
          className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
          style={{ animationDelay: "0.3s" }}
        ></span>
      </div>

      <span>AI is thinking...</span>

    </div>
  );
};

export default LoadingIndicator;