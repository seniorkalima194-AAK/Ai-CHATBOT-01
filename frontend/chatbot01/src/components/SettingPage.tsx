<<<<<<< HEAD
import { useState } from "react";
=======

import { useEffect, useRef, useState, type ChangeEvent } from "react";
>>>>>>> 32a8a1eb78db1ff0ffe8b7c9e503ca83704b020f
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
  FileUp,
  LoaderCircle,
  RefreshCw,
  FileText,
  Trash2,
} from "lucide-react";
import {
  deleteUploadedTextbook,
  getDocumentStatus,
  getUploadedTextbooks,
  uploadTextbooks,
  type DocumentStatus,
  type UploadedTextbook,
} from "../services/chatService";

const SettingsPage = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [notifications, setNotifications] = useState(true);
  const [language, setLanguage] = useState("English");
  const [model, setModel] = useState("Default AI");
  const [name, setName] = useState("");
  const [bookStatus, setBookStatus] = useState<DocumentStatus | null>(null);
  const [uploadedBooks, setUploadedBooks] = useState<UploadedTextbook[]>([]);
  const [bookMessage, setBookMessage] = useState("");
  const [bookError, setBookError] = useState("");
  const [isLoadingBooks, setIsLoadingBooks] = useState(false);
  const [deletingBook, setDeletingBook] = useState<string | null>(null);
  const bookInputRef = useRef<HTMLInputElement>(null);

  const refreshBookLibrary = async () => {
    try {
      setBookError("");
      const [status, uploads] = await Promise.all([
        getDocumentStatus(),
        getUploadedTextbooks(),
      ]);
      setBookStatus(status);
      setUploadedBooks(uploads);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to reach the book library.";
      setBookError(`Book library is unavailable: ${message}`);
    }
  };

  useEffect(() => {
    void refreshBookLibrary();
  }, []);

  const handleBookSelection = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files ?? []);
    event.target.value = "";
    if (files.length === 0) return;

    setIsLoadingBooks(true);
    setBookError("");
    setBookMessage("");
    try {
      const results = await uploadTextbooks(files);
      const indexed = results.filter((result) => result.status === "indexed");
      const failed = results.filter((result) => result.status === "failed");
      const passages = indexed.reduce((total, result) => total + result.chunks_indexed, 0);
      setBookMessage(
        `${indexed.length} book${indexed.length === 1 ? "" : "s"} ready for questions (${passages} searchable passages).${
          failed.length ? ` ${failed.length} PDF${failed.length === 1 ? " could" : "s could"} not be read.` : ""
        }`,
      );
      await refreshBookLibrary();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to upload the selected PDF.";
      setBookError(`Upload failed: ${message}`);
    } finally {
      setIsLoadingBooks(false);
    }
  };

  const handleDeleteUploadedBook = async (book: UploadedTextbook) => {
    const confirmed = window.confirm(
      `Remove "${book.filename}"? The AI will no longer use information from this PDF.`,
    );
    if (!confirmed) return;

    setDeletingBook(book.filename);
    setBookError("");
    setBookMessage("");
    try {
      const result = await deleteUploadedTextbook(book.filename);
      setBookMessage(
        `${book.filename} was removed from this device and ${result.chunks_removed} searchable passage${result.chunks_removed === 1 ? "" : "s"}.`,
      );
      await refreshBookLibrary();
    } catch (error) {
      const message = error instanceof Error ? error.message : "Unable to remove the uploaded PDF.";
      setBookError(`Could not remove ${book.filename}: ${message}`);
    } finally {
      setDeletingBook(null);
    }
  };

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
        <div className="mb-8">
          <h1 className="text-3xl font-bold md:text-4xl">Settings</h1>

          <p className={`mt-2 ${darkMode ? "text-gray-400" : "text-gray-500"}`}>
            Manage your AI chatbot preferences and account settings.
          </p>
        </div>

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
              <h2 className="text-xl font-semibold">Profile</h2>

              <p className="text-sm text-gray-500">
                Manage your profile information.
              </p>
            </div>
          </div>

          <label className="mb-2 block text-sm font-medium">Display Name</label>

          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter your name"
            className="w-full rounded-xl border border-gray-300 px-4 py-3 outline-none transition focus:border-black"
          />
        </section>

<<<<<<< HEAD
=======
        {/* Book library */}
        <section
          className={`mb-6 rounded-2xl p-6 shadow-sm ${
            darkMode ? "bg-gray-800" : "bg-white"
          }`}
        >
          <div className="mb-5 flex items-center gap-3">
            <div className="rounded-xl bg-gray-100 p-3 text-gray-700">
              <Database size={22} />
            </div>
            <div>
              <h2 className="text-xl font-semibold">Your book library</h2>
              <p className="text-sm text-gray-500">
                Add PDFs that the AI can use when answering your questions.
              </p>
            </div>
          </div>

          <div className="rounded-xl border border-gray-200 bg-gray-50 p-4 text-sm text-gray-600">
            <p>
              In this local installation, uploaded books are copied only to this computer&apos;s
              <code className="mx-1 rounded bg-gray-200 px-1 py-0.5 text-gray-800">backend/Books/uploads</code>
              folder and indexed locally. The original PDF remains in the location you selected.
            </p>
            {bookStatus && (
              <p className="mt-3 font-medium text-gray-800">
                {bookStatus.indexed_files} of {bookStatus.pdf_files} book{bookStatus.pdf_files === 1 ? "" : "s"} ready · {bookStatus.chunks} searchable passages
              </p>
            )}
          </div>

          <input
            ref={bookInputRef}
            type="file"
            accept="application/pdf,.pdf"
            multiple
            className="hidden"
            onChange={handleBookSelection}
          />

          <div className="mt-4 flex flex-wrap gap-3">
            <button
              type="button"
              onClick={() => bookInputRef.current?.click()}
              disabled={isLoadingBooks}
              className="flex items-center gap-2 rounded-xl bg-black px-4 py-2.5 text-sm font-medium text-white transition hover:bg-gray-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {isLoadingBooks ? <LoaderCircle size={18} className="animate-spin" /> : <FileUp size={18} />}
              {isLoadingBooks ? "Uploading book..." : "Upload book"}
            </button>
            <button
              type="button"
              onClick={() => void refreshBookLibrary()}
              disabled={isLoadingBooks}
              className="flex items-center gap-2 rounded-xl border border-gray-300 px-4 py-2.5 text-sm font-medium transition hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-50"
            >
              <RefreshCw size={18} />
              Refresh library
            </button>
          </div>

          <div className="mt-5 border-t border-gray-200 pt-4">
            <h3 className="font-medium">PDFs uploaded by you</h3>
            {uploadedBooks.length === 0 ? (
              <p className="mt-2 text-sm text-gray-500">No PDFs have been uploaded from this device yet.</p>
            ) : (
              <ul className="mt-3 space-y-2">
                {uploadedBooks.map((book) => (
                  <li
                    key={book.source}
                    className="flex items-center gap-3 rounded-xl border border-gray-200 bg-white px-3 py-2"
                  >
                    <FileText size={18} className="shrink-0 text-gray-600" />
                    <div className="min-w-0 flex-1">
                      <p className="truncate text-sm font-medium text-gray-800">{book.filename}</p>
                      <p className="text-xs text-gray-500">
                        {book.status === "indexed"
                          ? `${book.chunks_indexed} searchable passage${book.chunks_indexed === 1 ? "" : "s"}`
                          : book.status}
                      </p>
                    </div>
                    <button
                      type="button"
                      onClick={() => void handleDeleteUploadedBook(book)}
                      disabled={deletingBook !== null || isLoadingBooks}
                      className="flex items-center gap-1 rounded-lg px-2 py-1.5 text-sm font-medium text-red-600 transition hover:bg-red-50 disabled:cursor-not-allowed disabled:opacity-50"
                      aria-label={`Remove ${book.filename}`}
                    >
                      {deletingBook === book.filename ? <LoaderCircle size={16} className="animate-spin" /> : <Trash2 size={16} />}
                      Remove
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {bookMessage && <p className="mt-3 text-sm text-green-700">{bookMessage}</p>}
          {bookError && <p className="mt-3 text-sm text-red-600">{bookError}</p>}
          <p className="mt-4 text-xs text-gray-500">
            Teachers can also copy many PDFs directly into <code>backend/Books</code>; the running backend finds new or changed files automatically.
          </p>
        </section>

        {/* Appearance */}
>>>>>>> 32a8a1eb78db1ff0ffe8b7c9e503ca83704b020f
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
              <h2 className="text-xl font-semibold">Appearance</h2>

              <p className="text-sm text-gray-500">
                Customize how the chatbot looks.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Dark Mode</p>

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
              <h2 className="text-xl font-semibold">Notifications</h2>

              <p className="text-sm text-gray-500">
                Control your notification preferences.
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">Enable Notifications</p>

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
              <h2 className="text-xl font-semibold">AI Model</h2>

              <p className="text-sm text-gray-500">
                Select the AI model used for conversations.
              </p>
            </div>
          </div>

          <label className="mb-2 block text-sm font-medium">AI Model</label>

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
              <h2 className="text-xl font-semibold">Language</h2>

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
              <h2 className="text-xl font-semibold">Privacy & Security</h2>

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
              <h2 className="text-xl font-semibold">Data Management</h2>

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
              <h2 className="font-semibold text-red-600">Sign Out</h2>

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
