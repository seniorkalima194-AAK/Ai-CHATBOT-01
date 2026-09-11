import { useRef, useState } from "react";
import {
  Mail,
  Calendar,
  User,
  Camera,
  Pencil,
  LogOut,
  X,
  Save,
} from "lucide-react";

const ProfilePage = () => {
  const [name, setName] = useState("Abdully kalima");
  const [email, setEmail] = useState("developwithkalima@gmail.com");
  const [studentId, setStudentId] = useState("AL S0001");
  const [joinDate, setJoinDate] = useState("10/07/2030");

  const [profileImage, setProfileImage] = useState(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
  );

  const [isEditing, setIsEditing] = useState(false);

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleImageClick = () => {
    fileInputRef.current?.click();
  };

  const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setProfileImage(imageUrl);
    }
  };

  const handleSave = () => {
    setIsEditing(false);
    alert("Profile updated successfully!");
  };

  const handleCancel = () => {
    setIsEditing(false);
  };

  const handleLogout = () => {
    const confirmLogout = window.confirm("Are you sure you want to log out?");

    if (confirmLogout) {
      alert("Logged out successfully!");
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <header className="bg-slate-300 text-black px-5 py-5 rounded-b-3xl flex items-center justify-center">
        <h1 className="text-2xl md:text-3xl font-semibold text-center">
          My profile
        </h1>
      </header>

      <main className="max-w-2xl mx-auto px-5 py-8">
        <div className="flex flex-col items-center">
          <div className="relative">
            <img
              src={profileImage}
              alt="Profile"
              className="w-36 h-36 md:w-40 md:h-40 rounded-full object-cover border-4 border-blue-400"
            />

            {isEditing && (
              <button
                type="button"
                onClick={handleImageClick}
                className="absolute bottom-1 right-1 bg-blue-500 text-white p-3 rounded-full shadow-lg hover:bg-blue-600 transition"
              >
                <Camera size={20} />
              </button>
            )}

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="hidden"
            />
          </div>

          <span className="mt-3 bg-blue-100 text-blue-600 px-6 py-1 rounded-full font-semibold">
            Student
          </span>

          {!isEditing ? (
            <h2 className="text-3xl font-semibold mt-2 text-gray-800 text-center">
              {name}
            </h2>
          ) : (
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-3 text-center text-2xl border-b-2 border-purple-500 outline-none p-2 w-full max-w-md"
            />
          )}
        </div>

        <div className="mt-10 space-y-4">
          <div className="bg-gray-200 rounded-2xl p-4 flex items-center gap-4">
            <Mail className="text-gray-700 flex-shrink-0" />

            {isEditing ? (
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-transparent outline-none w-full text-lg text-gray-700"
              />
            ) : (
              <span className="text-lg text-gray-700 break-all">{email}</span>
            )}
          </div>

          <div className="bg-gray-200 rounded-2xl p-4 flex items-center gap-4">
            <User className="text-gray-700 flex-shrink-0" />

            {isEditing ? (
              <input
                type="text"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="bg-transparent outline-none w-full text-lg text-gray-700"
              />
            ) : (
              <span className="text-lg text-gray-700">
                Student ID: {studentId}
              </span>
            )}
          </div>

          <div className="bg-gray-200 rounded-2xl p-4 flex items-center gap-4">
            <Calendar className="text-gray-700 flex-shrink-0" />

            {isEditing ? (
              <input
                type="date"
                value={joinDate}
                onChange={(e) => setJoinDate(e.target.value)}
                className="bg-transparent outline-none w-full text-lg text-gray-700"
              />
            ) : (
              <span className="text-lg text-gray-700">
                Join date: {joinDate}
              </span>
            )}
          </div>
        </div>

        {!isEditing ? (
          <div className="flex flex-col sm:flex-row gap-5 justify-between mt-16">
            {/* Edit Profile */}
            <button
              type="button"
              onClick={() => setIsEditing(true)}
              className="flex items-center justify-center gap-2 border-2 border-blue-400 text-blue-500 px-8 py-3 rounded-full font-semibold text-lg hover:bg-blue-50 transition"
            >
              <Pencil size={20} />
              Edit profile
            </button>

            {/* Logout */}
            <button
              type="button"
              onClick={handleLogout}
              className="flex items-center justify-center gap-2 border-2 border-red-400 text-red-500 px-8 py-3 rounded-full font-semibold text-lg hover:bg-red-50 transition"
            >
              <LogOut size={20} />
              Log out
            </button>
          </div>
        ) : (
          <div className="flex flex-col sm:flex-row gap-5 justify-between mt-16">
            <button
              type="button"
              onClick={handleSave}
              className="flex items-center justify-center gap-2 bg-blue-500 text-white px-8 py-3 rounded-full font-semibold text-lg hover:bg-blue-600 transition"
            >
              <Save size={20} />
              Save changes
            </button>

            <button
              type="button"
              onClick={handleCancel}
              className="flex items-center justify-center gap-2 border-2 border-gray-400 text-gray-600 px-8 py-3 rounded-full font-semibold text-lg hover:bg-gray-100 transition"
            >
              <X size={20} />
              Cancel
            </button>
          </div>
        )}
      </main>
    </div>
  );
};

export default ProfilePage;
