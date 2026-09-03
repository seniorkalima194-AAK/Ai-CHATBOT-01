
const LoadingIndicator = () => {
  return (
    <div className="flex items-center gap-3 text-gray-500">
      {/* Hand & Pen Container with Shaking/Tilting Animation */}
      <div className="relative w-10 h-10 flex items-center justify-center animate-[handShake_0.6s_ease-in-out_infinite_alternate]">
        
        {/* Animated Spinning Pen */}
        <div 
          className="absolute z-10 w-9 h-1 rounded-full animate-[spin_0.5s_linear_infinite]"
          style={{
            transformOrigin: "45% 50%",
            background: "linear-gradient(to right, #1f2937 60%, #9ca3af 60%, #9ca3af 80%, #111827 80%)",
            boxShadow: "0 1px 3px rgba(0,0,0,0.3)"
          }}
        />

        {/* Hand Illustration SVG */}
        <svg 
          className="absolute text-gray-600 w-8 h-8 pointer-events-none select-none" 
          viewBox="0 0 24 24" 
          fill="none" 
          stroke="currentColor" 
          strokeWidth="1.5" 
          strokeLinecap="round" 
          strokeLinejoin="round"
        >
          <path d="M18 11V6a1.5 1.5 0 0 0-3 0v4" />
          <path d="M15 10V4a1.5 1.5 0 0 0-3 0v6" />
          <path d="M12 10V5a1.5 1.5 0 0 0-3 0v6" />
          <path d="M9 10.5V8a1.5 1.5 0 0 0-3 0v6.5a7.5 7.5 0 0 0 15 0V11a1.5 1.5 0 0 0-3 0" />
        </svg>

      </div>

      <span>AI is thinking...</span>

      {/* Global Style Injection for Custom Hand Shake Keyframes */}
      <style>{`
        @keyframes handShake {
          0% {
            transform: rotate(-8deg) translateY(1px);
          }
          100% {
            transform: rotate(8deg) translateY(-1px);
          }
        }
      `}</style>
    </div>
  );
};

export default LoadingIndicator;