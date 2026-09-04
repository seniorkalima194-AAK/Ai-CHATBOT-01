
const LoadingIndicator = () => {
  return (
    <div className="flex items-center gap-3 text-gray-500 font-medium select-none">
      <div className="relative w-6 h-6 flex items-center justify-center">
        {/* Main rotating sparkle */}
        <svg 
          className="w-5 h-5 text-indigo-600 animate-[spin_3s_linear_infinite]" 
          viewBox="0 0 24 24" 
          fill="currentColor"
        >
          <path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z" />
        </svg>

        {/* Pulsing overlay star */}
        <svg 
          className="absolute w-3 h-3 text-indigo-400 -top-0.5 -right-0.5 animate-ping" 
          viewBox="0 0 24 24" 
          fill="currentColor"
        >
          <path d="M12 0L14.59 9.41L24 12L14.59 14.59L12 24L9.41 14.59L0 12L9.41 9.41L12 0Z" />
        </svg>
      </div>

      <span>AI is thinking...</span>
    </div>
  );
};

export default LoadingIndicator;