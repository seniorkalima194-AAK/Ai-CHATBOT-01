import { useRef, useState } from "react";
import {
  Menu,
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
  // Profile information
  const [name, setName] = useState("Abdully kalima");
  const [email, setEmail] = useState("developwithkalima@gmail.com");
  const [studentId, setStudentId] = useState("AL S0001");
  const [joinDate, setJoinDate] = useState("10/07/2030");

  // Profile picture
  const [profileImage, setProfileImage] = useState(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
  );

  // Edit mode
  const [isEditing, setIsEditing] = useState(false);

  // Hidden file input
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  // Open file picker
  const handleImageClick = () => {
    fileInputRef.current?.click();
  };

  // Handle uploaded image
  const handleImageChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0];

    if (file) {
      const imageUrl = URL.createObjectURL(file);
      setProfileImage(imageUrl);
    }
  };

  // Save profile
  const handleSave = () => {
    setIsEditing(false);

    alert("Profile updated successfully!");
  };

  // Cancel editing
  const handleCancel = () => {
    setIsEditing(false);
  };

  return (
    <div className="min-h-screen bg-white">

      {/* ================= HEADER ================= */}
      <header className="bg-slate-300 text-black px-5 py-5 rounded-b-3xl flex items-center gap-5">
        
        <button className="hover:bg-purple-700 p-2 rounded-lg">
          <Menu size={30} />
        </button>

        <h1 className="text-2xl md:text-3xl font-semibold">
          My profile
        </h1>

      </header>

      {/* ================= PROFILE ================= */}
      <main className="max-w-2xl mx-auto px-5 py-8">

        {/* Profile Picture */}
        <div className="flex flex-col items-center">

          <div className="relative">

            <img
              src={profileImage}
              alt="Profile"
              className="w-36 h-36 md:w-40 md:h-40 rounded-full object-cover border-4 border-blue-400"
            />

            {/* Camera button */}
            {isEditing && (
              <button
                onClick={handleImageClick}
                className="absolute bottom-1 right-1 bg-blue-500 text-white p-3 rounded-full shadow-lg hover:bg-blue-600"
              >
                <Camera size={20} />
              </button>
            )}

            {/* Hidden file input */}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageChange}
              className="hidden"
            />

          </div>

          {/* Role */}
          <span className="mt-3 bg-blue-100 text-blue-600 px-6 py-1 rounded-full font-semibold">
            Student
          </span>

          {/* Name */}
          {!isEditing ? (
            <h2 className="text-3xl font-semibold mt-2 text-gray-800">
              {name}
            </h2>
          ) : (
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="mt-3 text-center text-2xl border-b-2 border-purple-500 outline-none p-2"
            />
          )}

        </div>

        {/* ================= PROFILE INFORMATION ================= */}

        <div className="mt-10 space-y-4">

          {/* Email */}
          <div className="bg-gray-200 rounded-2xl p-4 flex items-center gap-4">

            <Mail className="text-gray-700" />

            {isEditing ? (
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-transparent outline-none w-full text-lg"
              />
            ) : (
              <span className="text-lg text-gray-700 break-all">
                {email}
              </span>
            )}

          </div>

          {/* Student ID */}
          <div className="bg-gray-200 rounded-2xl p-4 flex items-center gap-4">

            <User className="text-gray-700" />

            {isEditing ? (
              <input
                type="text"
                value={studentId}
                onChange={(e) => setStudentId(e.target.value)}
                className="bg-transparent outline-none w-full text-lg"
              />
            ) : (
              <span className="text-lg text-gray-700">
                Student ID: {studentId}
              </span>
            )}

          </div>

          {/* Join Date */}
          <div className="bg-gray-200 rounded-2xl p-4 flex items-center gap-4">

            <Calendar className="text-gray-700" />

            {isEditing ? (
              <input
                type="date"
                value={joinDate}
                onChange={(e) => setJoinDate(e.target.value)}
                className="bg-transparent outline-none w-full text-lg"
              />
            ) : (
              <span className="text-lg text-gray-700">
                Join date: {joinDate}
              </span>
            )}

          </div>

        </div>

        {/* ================= BUTTONS ================= */}

        {!isEditing ? (

          <div className="flex flex-col sm:flex-row gap-5 justify-between mt-16">

            <button
              onClick={() => setIsEditing(true)}
              className="flex items-center justify-center gap-2 border-2 border-blue-400 text-blue-500 px-8 py-3 rounded-full font-semibold text-lg hover:bg-blue-50"
            >
              <Pencil size={20} />
              Edit profile
            </button>

            <button
              className="flex items-center justify-center gap-2 border-2 border-red-400 text-red-500 px-8 py-3 rounded-full font-semibold text-lg hover:bg-red-50"
            >
              <LogOut size={20} />
              Log out
            </button>

          </div>

        ) : (

          <div className="flex flex-col sm:flex-row gap-5 justify-between mt-16">

            {/* Save */}
            <button
              onClick={handleSave}
              className="flex items-center justify-center gap-2 bg-blue-500 text-white px-8 py-3 rounded-full font-semibold text-lg hover:bg-blue-600"
            >
              <Save size={20} />
              Save changes
            </button>

            {/* Cancel */}
            <button
              onClick={handleCancel}
              className="flex items-center justify-center gap-2 border-2 border-gray-400 text-gray-600 px-8 py-3 rounded-full font-semibold text-lg hover:bg-gray-100"
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