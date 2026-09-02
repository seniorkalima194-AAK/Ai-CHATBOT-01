
import { useState } from "react";
import {
  User,
  Palette,
  Bell,
  Bot,
  Globe,
  Shield,
  Database,
  LogOut,
  Moon,
  Sun,
  Save,
} from "lucide-react";

const SettingsPage = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [language, setLanguage] = useState("English");
  const [model, setModel] = useState("Default AI");
  const [name, setName] = useState("");

  const handleSave = () => {
    alert("Settings saved successfully!");
  };

  return (
    <div
      className={`min-h-screen px-4 pb-10 pt-24 transition-colors md:px-8 ${
        darkMode ? "bg-gray-900 text-white" : "bg-gray-100 text-gray-800"
      }`}
    >
      <div className="mx-auto max-w-5xl">

        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold md:text-4xl">
            Settings
          </h1>

          <p
            className={`mt-2 ${
              darkMode ? "text-gray-400" : "text-gray-500"
            }`}
          >
            Manage your AI chatbot preferences and account settings.
          </p>
        </div>

        {/* Profile */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="mb-6 flex items-center gap-3">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <User size={22} />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                Profile
              </h2>

              <p className="text-sm text-gray-500">
                Manage your profile information.
              </p>
            </div>
          </div>

          <label className="mb-2 block text-sm font-medium">
            Display Name
          </label>

          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-black"
          />
        </section>

        {/* Appearance */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="mb-6 flex items-center gap-3">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <Palette size={22} />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                Appearance
              </h2>

              <p className="text-sm text-gray-500">
                Customize how the chatbot looks.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">
                Dark Mode
              </p>

              <p className="text-sm text-gray-500">
                Switch between light and dark appearance.
              </p>
            </div>

            <button
              type="button"
              onClick={() => setDarkMode(!darkMode)}
              className="flex items-center gap-2 rounded-xl bg-gray-200 px-4 py-2 font-medium text-gray-800 transition hover:bg-gray-300"
            >
              {darkMode ? (
                <>
                  <Moon size={18} />
                  Dark
                </>
              ) : (
                <>
                  <Sun size={18} />
                  Light
                </>
              )}
            </button>
          </div>
        </section>

        {/* Notifications */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="mb-6 flex items-center gap-3">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <Bell size={22} />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                Notifications
              </h2>

              <p className="text-sm text-gray-500">
                Control your notification preferences.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">
                Enable Notifications
              </p>

              <p className="text-sm text-gray-500">
                Receive notifications about your chatbot.
              </p>
            </div>

            <button
              type="button"
              onClick={() => setNotifications(!notifications)}
              className={`rounded-full px-5 py-2 text-sm font-medium ${
                notifications
                  ? "bg-black text-white"
                  : "bg-gray-200 text-gray-700"
              }`}
            >
              {notifications ? "Enabled" : "Disabled"}
            </button>
          </div>
        </section>

        {/* AI Model */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="mb-6 flex items-center gap-3">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <Bot size={22} />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                AI Model
              </h2>

              <p className="text-sm text-gray-500">
                Select the AI model used for conversations.
              </p>
            </div>
          </div>

          <label className="mb-2 block text-sm font-medium">
            AI Model
          </label>

          <select
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:border-black"
          >
            <option>Default AI</option>
            <option>Fast AI</option>
            <option>Advanced AI</option>
          </select>
        </section>

        {/* Language */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="mb-6 flex items-center gap-3">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <Globe size={22} />
            </div>

            <div>
              <h2 className="text-xl font-semibold">
                Language
              </h2>

              <p className="text-sm text-gray-500">
                Choose your preferred language.
              </p>
            </div>
          </div>

          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full rounded-xl border border-gray-300 bg-white px-4 py-3 outline-none focus:border-black"
          >
            <option>English</option>
            <option>Swahili</option>
            <option>French</option>
            <option>Spanish</option>
          </select>
        </section>

        {/* Privacy */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="flex items-center gap-4">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <Shield size={22} />
            </div>

            <div className="flex-1">
              <h2 className="text-xl font-semibold">
                Privacy & Security
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Manage your privacy and security preferences.
              </p>
            </div>

            <button
              type="button"
              className="rounded-xl border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-gray-50"
            >
              Manage
            </button>
          </div>
        </section>

        {/* Data */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="flex items-center gap-4">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <Database size={22} />
            </div>

            <div className="flex-1">
              <h2 className="text-xl font-semibold">
                Data Management
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Manage your conversations and application data.
              </p>
            </div>

            <button
              type="button"
              className="rounded-xl border border-gray-300 px-4 py-2 text-sm font-medium hover:bg-gray-50"
            >
              Manage
            </button>
          </div>
        </section>

        {/* Save */}
        <div className="mb-6 flex justify-end">
          <button
            type="button"
            onClick={handleSave}
            className="flex items-center gap-2 rounded-xl bg-black px-6 py-3 font-medium text-white transition hover:bg-gray-800"
          >
            <Save size={18} />
            Save Settings
          </button>
        </div>

        {/* Logout */}
        <section
          className={`rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="flex items-center gap-4">
            <div className="rounded-xl bg-red-100 p-3 text-red-600">
              <LogOut size={22} />
            </div>

            <div className="flex-1">
              <h2 className="font-semibold text-red-600">
                Sign Out
              </h2>

              <p className="mt-1 text-sm text-gray-500">
                Sign out of your AI chatbot account.
              </p>
            </div>

            <button
              type="button"
              className="rounded-xl bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700"
            >
              Sign Out
            </button>
          </div>
        </section>

      </div>
    </div>
  );
};

export default SettingsPage;

