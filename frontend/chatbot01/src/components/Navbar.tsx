
import {
  Bell,
  Menu,
  User,
  X,
  Home,
  BookOpen,
  Settings,
} from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const unreadNotifications = 3;

  return (
    <>
      {/* ================= NAVBAR ================= */}
      <nav className="fixed top-0 left-0 right-0 h-16 bg-gray-200 shadow-md z-[100]">

        <div className="h-full flex items-center justify-between px-4 md:px-8">

          {/* MENU BUTTON */}
          <button
            type="button"
            onClick={() => setIsMenuOpen(true)}
            className="flex items-center justify-center w-10 h-10 rounded-lg hover:bg-gray-300"
          >
            <Menu size={28} />
          </button>

          {/* TITLE */}
          <h1 className="text-base sm:text-xl md:text-2xl lg:text-3xl font-bold italic text-gray-800 text-center">
            Adaptive Learning System
          </h1>

          {/* RIGHT ICONS */}
          <div className="flex items-center gap-2 md:gap-4">

            {/* PROFILE */}
            <Link
              to="/profile"
              className="flex items-center justify-center w-10 h-10 rounded-lg hover:bg-gray-300"
            >
              <User size={26} />
            </Link>

            {/* NOTIFICATION */}
            <Link
              to="/notification"
              className="relative flex items-center justify-center w-10 h-10 rounded-lg hover:bg-gray-300"
              aria-label="Notifications"
            >
              <Bell size={26} />

              {/* Notification Badge */}
              {unreadNotifications > 0 && (
                <span className="absolute -top-1 -right-1 min-w-5 h-5 px-1 flex items-center justify-center bg-red-500 text-white text-xs font-bold rounded-full border-2 border-gray-200">
                  {unreadNotifications > 9
                    ? "9+"
                    : unreadNotifications}
                </span>
              )}
            </Link>

          </div>
        </div>
      </nav>

      {/* ================= OVERLAY ================= */}
      {isMenuOpen && (
        <div
          onClick={() => setIsMenuOpen(false)}
          className="fixed inset-0 bg-black/30 z-[110]"
        />
      )}

      {/* ================= MENU ================= */}
      <div
        className={`fixed top-0 left-0 h-screen w-72 max-w-[85vw] bg-white shadow-2xl z-[120] transform transition-transform duration-300 ${
          isMenuOpen
            ? "translate-x-0"
            : "-translate-x-full"
        }`}
      >

        {/* MENU HEADER */}
        <div className="h-16 flex items-center justify-between px-5 border-b">

          <h2 className="text-xl font-bold">
            Menu
          </h2>

          <button
            type="button"
            onClick={() => setIsMenuOpen(false)}
            className="w-10 h-10 flex items-center justify-center rounded-lg hover:bg-gray-100"
          >
            <X size={26} />
          </button>

        </div>

        {/* MENU ITEMS */}
        <div className="flex flex-col p-3">

          {/* HOME */}
          <Link
            to="/"
            onClick={() => setIsMenuOpen(false)}
            className="flex items-center gap-4 px-4 py-4 rounded-xl hover:bg-gray-100"
          >
            <Home size={22} />
            <span>Home</span>
          </Link>

          {/* COURSES */}
          <Link
            to="/courses"
            onClick={() => setIsMenuOpen(false)}
            className="flex items-center gap-4 px-4 py-4 rounded-xl hover:bg-gray-100"
          >
            <BookOpen size={22} />
            <span>Courses</span>
          </Link>

          {/* PROFILE */}
          <Link
            to="/profile"
            onClick={() => setIsMenuOpen(false)}
            className="flex items-center gap-4 px-4 py-4 rounded-xl hover:bg-gray-100"
          >
            <User size={22} />
            <span>Profile</span>
          </Link>

          {/* SETTINGS */}
          <Link
            to="/settings"
            onClick={() => setIsMenuOpen(false)}
            className="flex items-center gap-4 px-4 py-4 rounded-xl hover:bg-gray-100"
          >
            <Settings size={22} />
            <span>Settings</span>
          </Link>

        </div>
      </div>
    </>
  );
};

export default Navbar;

