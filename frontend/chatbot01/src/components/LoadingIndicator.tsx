
const LoadingIndicator = () => {
  return (
    <div className="flex items-center gap-3 text-black dark:text-white font-medium select-none">
      {/* Small Container (Scales down icon) */}
      <div className="relative w-12 h-6 flex items-center justify-center">
        
        {/* Soft Background Contrast Glow */}
        <div className="absolute inset-0 bg-black/10 dark:bg-white/10 blur-md rounded-full" />

        {/* Two-Loop Infinity Path SVG */}
        <svg viewBox="0 0 100 50" className="w-full h-full relative z-10 overflow-visible">
          <defs>
            {/* Crisp High-Contrast Shadow Filter */}
            <filter id="bwGlow" x="-50%" y="-50%" width="200%" height="200%">
              <feDropShadow dx="0" dy="0" stdDeviation="3" floodColor="currentColor" floodOpacity="0.8" />
            </filter>
          </defs>

          {/* Faded Base Track */}
          <path
            d="M 50 25 C 65 10, 85 10, 85 25 C 85 40, 65 40, 50 25 C 35 10, 15 10, 15 25 C 15 40, 35 40, 50 25 Z"
            fill="none"
            stroke="currentColor"
            strokeWidth="7"
            strokeOpacity="0.2"
            strokeLinecap="round"
          />

          {/* Animated Pure Black/White Dash */}
          <path
            d="M 50 25 C 65 10, 85 10, 85 25 C 85 40, 65 40, 50 25 C 35 10, 15 10, 15 25 C 15 40, 35 40, 50 25 Z"
            fill="none"
            stroke="currentColor"
            strokeWidth="7"
            strokeLinecap="round"
            filter="url(#bwGlow)"
            className="animate-[infinityDashSlow_3.5s_ease-in-out_infinite]"
            style={{
              strokeDasharray: "75 145",
            }}
          />
        </svg>
      </div>

      <span className="text-sm font-semibold tracking-wide">AI is thinking...</span>

      <style>{`
        @keyframes infinityDashSlow {
          0% {
            stroke-dashoffset: 220;
          }
          100% {
            stroke-dashoffset: 0;
          }
        }
      `}</style>
    </div>
  );
};

export default LoadingIndicator;