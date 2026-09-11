import { useState } from "react";
import {
  signInWithEmailAndPassword,
  GoogleAuthProvider,
  signInWithPopup,
} from "firebase/auth";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, Mail, Lock, Sparkles, Loader2 } from "lucide-react";
import { auth } from "../../config/firebase";

const LoginPage = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [googleLoading, setGoogleLoading] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  // Login with email and password
  const handleLogin = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!email || !password) {
      setError("Please enter your email and password.");
      return;
    }

    try {
      setLoading(true);

      await signInWithEmailAndPassword(auth, email, password);

      setSuccess("Login successful! Redirecting...");

      setTimeout(() => {
        navigate("/chat");
      }, 1000);
    } catch (error: any) {
      console.error(error);

      switch (error.code) {
        case "auth/invalid-email":
          setError("Please enter a valid email address.");
          break;

        case "auth/user-not-found":
          setError("No account found with this email.");
          break;

        case "auth/wrong-password":
        case "auth/invalid-credential":
          setError("Incorrect email or password.");
          break;

        case "auth/too-many-requests":
          setError("Too many attempts. Please try again later.");
          break;

        default:
          setError("Login failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  // Login with Google
  const handleGoogleLogin = async () => {
    setError("");
    setSuccess("");

    try {
      setGoogleLoading(true);

      const provider = new GoogleAuthProvider();

      await signInWithPopup(auth, provider);

      setSuccess("Google login successful! Redirecting...");

      setTimeout(() => {
        navigate("/chat");
      }, 1000);
    } catch (error: any) {
      console.error(error);

      if (error.code === "auth/popup-closed-by-user") {
        setError("Google login was cancelled.");
      } else {
        setError("Google login failed. Please try again.");
      }
    } finally {
      setGoogleLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-full overflow-hidden bg-[#0b0014] text-white">
      {/* Background effects */}
      <div className="absolute -left-32 -top-32 h-[450px] w-[450px] rounded-full bg-purple-700/30 blur-[120px]" />

      <div className="absolute -bottom-32 -right-32 h-[500px] w-[500px] rounded-full bg-fuchsia-600/20 blur-[130px]" />

      <div className="absolute left-1/2 top-1/2 h-[400px] w-[400px] -translate-x-1/2 -translate-y-1/2 rounded-full bg-purple-500/10 blur-[100px]" />

      {/* Main */}
      <div className="relative flex min-h-screen items-center justify-center px-4 py-10">
        <div className="grid w-full max-w-6xl overflow-hidden rounded-3xl border border-white/10 bg-white/[0.04] shadow-2xl backdrop-blur-xl lg:grid-cols-2">

          {/* Left side */}
          <div className="relative hidden min-h-[700px] overflow-hidden lg:flex">
            {/* Glow */}
            <div className="absolute left-1/2 top-1/2 h-80 w-80 -translate-x-1/2 -translate-y-1/2 rounded-full bg-purple-600/30 blur-[100px]" />

            <div className="relative z-10 flex flex-col justify-center px-12 xl:px-20">

              {/* Logo */}
              <div className="mb-10 flex items-center gap-3">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-purple-500 to-fuchsia-600 shadow-lg shadow-purple-500/30">
                  <Sparkles size={24} />
                </div>

                <div>
                  <h2 className="text-xl font-bold">AI Chatbot</h2>
                  <p className="text-xs text-gray-400">
                    Intelligent conversations
                  </p>
                </div>
              </div>

              <h1 className="max-w-lg text-5xl font-bold leading-tight">
                Welcome back to the{" "}
                <span className="bg-gradient-to-r from-purple-400 via-fuchsia-400 to-pink-400 bg-clip-text text-transparent">
                  future of AI.
                </span>
              </h1>

              <p className="mt-6 max-w-md text-lg leading-8 text-gray-400">
                Sign in and continue your conversations with your intelligent
                AI assistant.
              </p>

              {/* AI decoration */}
              <div className="relative mt-14 flex h-40 w-full max-w-md items-center justify-center">
                <div className="absolute h-32 w-32 animate-pulse rounded-full border border-purple-400/30" />

                <div className="absolute h-24 w-24 rounded-full border border-fuchsia-400/30" />

                <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-purple-500 to-fuchsia-600 shadow-xl shadow-purple-500/40">
                  <Sparkles size={28} />
                </div>

                <div className="absolute left-10 top-5 h-2 w-2 animate-ping rounded-full bg-purple-400" />
                <div className="absolute right-10 bottom-5 h-2 w-2 animate-pulse rounded-full bg-fuchsia-400" />
              </div>

              <div className="mt-8 flex gap-3 text-sm text-gray-500">
                <span>Secure</span>
                <span>•</span>
                <span>Fast</span>
                <span>•</span>
                <span>AI Powered</span>
              </div>
            </div>
          </div>

          {/* Right side */}
          <div className="flex items-center justify-center px-6 py-10 sm:px-10 lg:px-14">
            <div className="w-full max-w-md">

              {/* Mobile logo */}
              <div className="mb-8 flex items-center justify-center gap-3 lg:hidden">
                <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-purple-500 to-fuchsia-600">
                  <Sparkles size={22} />
                </div>

                <h2 className="text-xl font-bold">AI Chatbot</h2>
              </div>

              {/* Heading */}
              <div className="mb-8 text-center lg:text-left">
                <h2 className="text-3xl font-bold">
                  Welcome back 👋
                </h2>

                <p className="mt-2 text-gray-400">
                  Sign in to continue to your account
                </p>
              </div>

              {/* Error */}
              {error && (
                <div className="mb-5 rounded-xl border border-red-500/20 bg-red-500/10 px-4 py-3 text-sm text-red-300">
                  {error}
                </div>
              )}

              {/* Success */}
              {success && (
                <div className="mb-5 rounded-xl border border-green-500/20 bg-green-500/10 px-4 py-3 text-sm text-green-300">
                  {success}
                </div>
              )}

              {/* Form */}
              <form onSubmit={handleLogin} className="space-y-5">

                {/* Email */}
                <div>
                  <label className="mb-2 block text-sm font-medium text-gray-300">
                    Email address
                  </label>

                  <div className="relative">
                    <Mail
                      size={19}
                      className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
                    />

                    <input
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="you@example.com"
                      className="w-full rounded-xl border border-white/10 bg-white/[0.05] py-3.5 pl-12 pr-4 text-white outline-none transition placeholder:text-gray-600 focus:border-purple-500 focus:bg-white/[0.08] focus:ring-2 focus:ring-purple-500/20"
                    />
                  </div>
                </div>

                {/* Password */}
                <div>
                  <div className="mb-2 flex items-center justify-between">
                    <label className="text-sm font-medium text-gray-300">
                      Password
                    </label>

                    <Link
                      to="/forgot-password"
                      className="text-sm text-purple-400 transition hover:text-purple-300"
                    >
                      Forgot password?
                    </Link>
                  </div>

                  <div className="relative">
                    <Lock
                      size={19}
                      className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-500"
                    />

                    <input
                      type={showPassword ? "text" : "password"}
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      placeholder="Enter your password"
                      className="w-full rounded-xl border border-white/10 bg-white/[0.05] py-3.5 pl-12 pr-12 text-white outline-none transition placeholder:text-gray-600 focus:border-purple-500 focus:bg-white/[0.08] focus:ring-2 focus:ring-purple-500/20"
                    />

                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500 transition hover:text-white"
                    >
                      {showPassword ? (
                        <EyeOff size={19} />
                      ) : (
                        <Eye size={19} />
                      )}
                    </button>
                  </div>
                </div>

                {/* Remember */}
                <div className="flex items-center gap-2">
                  <input
                    id="remember"
                    type="checkbox"
                    className="h-4 w-4 rounded border-white/20 bg-white/5 accent-purple-600"
                  />

                  <label
                    htmlFor="remember"
                    className="text-sm text-gray-400"
                  >
                    Remember me
                  </label>
                </div>

                {/* Login button */}
                <button
                  type="submit"
                  disabled={loading}
                  className="flex w-full items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-purple-600 to-fuchsia-600 py-3.5 font-semibold shadow-lg shadow-purple-600/20 transition hover:scale-[1.01] hover:from-purple-500 hover:to-fuchsia-500 disabled:cursor-not-allowed disabled:opacity-60"
                >
                  {loading ? (
                    <>
                      <Loader2 size={20} className="animate-spin" />
                      Signing in...
                    </>
                  ) : (
                    "Sign in"
                  )}
                </button>
              </form>

              {/* Divider */}
              <div className="my-7 flex items-center gap-4">
                <div className="h-px flex-1 bg-white/10" />
                <span className="text-sm text-gray-500">OR</span>
                <div className="h-px flex-1 bg-white/10" />
              </div>

              {/* Google */}
              <button
                type="button"
                onClick={handleGoogleLogin}
                disabled={googleLoading}
                className="flex w-full items-center justify-center gap-3 rounded-xl border border-white/10 bg-white/[0.04] py-3.5 font-medium transition hover:bg-white/[0.08] disabled:cursor-not-allowed disabled:opacity-60"
              >
                {googleLoading ? (
                  <Loader2 size={20} className="animate-spin" />
                ) : (
                  <svg
                    width="20"
                    height="20"
                    viewBox="0 0 24 24"
                  >
                    <path
                      fill="#4285F4"
                      d="M21.35 12.23c0-.79-.07-1.55-.2-2.27H12v4.3h5.23a4.47 4.47 0 0 1-1.94 2.93v2.43h3.14c1.84-1.69 2.92-4.18 2.92-7.39z"
                    />
                    <path
                      fill="#34A853"
                      d="M12 21.75c2.63 0 4.84-.87 6.45-2.36l-3.14-2.43c-.87.58-1.98.92-3.31.92-2.54 0-4.7-1.72-5.47-4.03H3.29v2.51A9.74 9.74 0 0 0 12 21.75z"
                    />
                    <path
                      fill="#FBBC05"
                      d="M6.53 13.85A5.85 5.85 0 0 1 6.22 12c0-.64.11-1.26.31-1.85V7.64H3.29A9.75 9.75 0 0 0 2.25 12c0 1.57.38 3.05 1.04 4.36l3.24-2.51z"
                    />
                    <path
                      fill="#EA4335"
                      d="M12 6.12c1.43 0 2.71.49 3.72 1.46l2.79-2.79C16.84 3.22 14.63 2.25 12 2.25a9.74 9.74 0 0 0-8.71 5.39l3.24 2.51C7.3 7.84 9.46 6.12 12 6.12z"
                    />
                  </svg>
                )}

                {googleLoading ? "Connecting..." : "Continue with Google"}
              </button>

              {/* Register */}
              <p className="mt-8 text-center text-sm text-gray-400">
                Don't have an account?{" "}
                <Link
                  to="/register"
                  className="font-semibold text-purple-400 transition hover:text-purple-300"
                >
                  Create account
                </Link>
              </p>

              {/* Footer */}
              <p className="mt-8 text-center text-xs text-gray-600">
                By continuing, you agree to our Terms of Service and Privacy
                Policy.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;