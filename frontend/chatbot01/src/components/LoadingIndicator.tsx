const LoadingIndicator = () => {
  return (
<<<<<<< HEAD
    <div
      style={{
        display: "flex",
        alignItems: "center",
        gap: "12px",
        fontFamily: "sans-serif",
        fontWeight: 500,
        userSelect: "none",
        color: "#000000",
      }}
    >
      {/* Icon Container */}
      <div
        style={{
          position: "relative",
          width: "48px",
          height: "24px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <svg
          viewBox="0 0 100 50"
          style={{
            width: "100%",
            height: "100%",
            position: "relative",
            zIndex: 10,
            overflow: "visible",
          }}
        >
          {/* Faded Base Track */}
          <path
            d="M 50 25 C 65 10, 85 10, 85 25 C 85 40, 65 40, 50 25 C 35 10, 15 10, 15 25 C 15 40, 35 40, 50 25 Z"
            fill="none"
            stroke="#000000"
            strokeOpacity="0.2"
            strokeWidth="7"
            strokeLinecap="round"
          />

          {/* Animated Black Dash */}
          <path
            d="M 50 25 C 65 10, 85 10, 85 25 C 85 40, 65 40, 50 25 C 35 10, 15 10, 15 25 C 15 40, 35 40, 50 25 Z"
            fill="none"
            stroke="#000000"
            strokeWidth="7"
            strokeLinecap="round"
            style={{
              strokeDasharray: "75 145",
              animation: "infinityDashSlow 3.5s ease-in-out infinite",
            }}
          />
        </svg>
      </div>

      <span style={{ fontSize: "14px", fontWeight: 600, letterSpacing: "0.025em", color: "#000000" }}>
        AI is thinking...
      </span>
=======
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
>>>>>>> 32a8a1eb78db1ff0ffe8b7c9e503ca83704b020f

    </div>
  );
};

export default LoadingIndicator;