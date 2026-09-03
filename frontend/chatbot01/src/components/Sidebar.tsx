import { useState } from "react";
import { 
  MessageSquare, 
  Plus, 
  ChevronLeft, 
  Menu, 
  Trash2, 
  Settings, 
  ExternalLink,
  Search,
  X 
} from "lucide-react";
import { Link, useLocation } from "react-router-dom";

const ChatGPTSidebar = () => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [searchQuery, setSearchQuery] = useState(""); // Track search input text
  const location = useLocation();

  const chatHistory = [
    { id: "1", title: "React Navbar Optimization", path: "/c/1" },
    { id: "2", title: "Tailwind Grid Layouts", path: "/c/2" },
    { id: "3", title: "Adaptive Learning Architecture", path: "/c/3" },
    { id: "4", title: "Python API Data Parsing", path: "/c/4" },
  ];

  const filteredHistory = chatHistory.filter((chat) =>
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <aside 
      className={`fixed top-0 left-0 h-screen bg-white text-gray-900
      transition-all duration-300 z-50 flex flex-col justify-between border-r border-[#2f2f2f]
      ${isCollapsed ? "w-0 md:w-16" : "w-64"}`}
    >
      {isCollapsed && (
        <button
          onClick={() => setIsCollapsed(false)}
          className="fixed top-4 left-4 p-2 rounded-lg bg-white border border-[#2f2f2f] text-black hover:text-white hover:bg-gray-900 duration-300 transition z-50 hidden md:block"
          aria-label="Expand Sidebar"
        >
          <Menu size={18} />
        </button>
      )}

      <div className={`flex flex-col h-full w-full ${isCollapsed ? "hidden md:flex" : "flex"}`}>
        
        <div className="p-3.5 flex flex-col gap-2">
          <div className="flex items-center justify-between gap-2">
            {!isCollapsed && (
              <Link to={'/'} className="flex-1 flex items-center justify-between px-3 py-2 border border-[#2f2f2f] rounded-lg text-sm font-medium hover:bg-gray-200 transition-colors">
                <span className="flex items-center gap-2">
                  <MessageSquare size={16} className="text-gray-900" />
                  New chat
                </span>
                <Plus size={16} className="text-gray-400" />
              </Link>
            )}
            
            {!isCollapsed && (
              <button 
                onClick={() => setIsCollapsed(true)}
                className="p-2 rounded-lg border border-[#2f2f2f] text-gray-400 hover:text-gray-900 hover:bg-gray-200 transition-colors"
                aria-label="Collapse Sidebar"
              >
                <ChevronLeft size={18} />
              </button>
            )}
          </div>

          {!isCollapsed && (
            <div className="relative flex items-center mt-1">
              <Search size={16} className="absolute left-3 text-gray-400" />
              <input
                type="text"
                placeholder="Search history..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-9 pr-8 py-1.5 bg-gray-50 border border-gray-200 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-gray-900 focus:bg-white text-gray-900 transition-all"
              />
              {searchQuery && (
                <button 
                  onClick={() => setSearchQuery("")}
                  className="absolute right-2.5 text-gray-400 hover:text-gray-600"
                >
                  <X size={14} />
                </button>
              )}
            </div>
          )}
        </div>

        <div className="flex-1 overflow-y-auto px-2 py-2 custom-scrollbar">
          {!isCollapsed && (
            <>
              <div className="px-3 text-xs font-semibold text-gray-500 mb-2 mt-2">Today</div>
              <div className="flex flex-col gap-0.5">
                {filteredHistory.length > 0 ? (
                  filteredHistory.map((chat) => {
                    const isActive = location.pathname === chat.path;
                    return (
                      <div 
                        key={chat.id}
                        className={`group relative flex items-center justify-between rounded-lg text-sm px-3 py-2 transition-colors cursor-pointer
                        ${isActive ? "bg-gray-900" : "hover:bg-gray-800"}`}
                      >
                        <Link to={chat.path} className="flex items-center gap-2.5 truncate w-full pr-6 text-gray-950">
                          <MessageSquare size={16} className={`flex-shrink-0 ${isActive ? "text-white" : "text-gray-900 group-hover:text-white"}`} />
                          <span className={`truncate text-[13px] ${isActive ? "text-white" : "text-black group-hover:text-white"}`}>{chat.title}</span>
                        </Link>
                        
                        <button className="absolute right-2 opacity-0 group-hover:opacity-100 p-1 text-gray-400 hover:text-red-400 transition-opacity">
                          <Trash2 size={14} />
                        </button>
                      </div>
                    );
                  })
                ) : (
                  <div className="px-3 py-4 text-xs text-gray-400 italic text-center">
                    No results match your search
                  </div>
                )}
              </div>
            </>
          )}
        </div>

        <div className="p-3 border-t border-[#2f2f2f] flex flex-col gap-1 bg-[#171717]">
          {!isCollapsed ? (
            <>
              <button className="flex items-center gap-3 w-full px-3 py-2 text-sm text-gray-300 hover:bg-[#212121] rounded-lg transition-colors">
                <Settings size={16} />
                <span>Settings</span>
              </button>
              <div className="flex items-center justify-between w-full px-3 py-2 mt-1 rounded-lg hover:bg-[#212121] transition-colors cursor-pointer">
                <div className="flex items-center gap-3">
                  <div className="w-6 h-6 rounded-full bg-white text-black to-blue-500 flex items-center justify-center text-[11px] font-bold">
                    C
                  </div>
                  <span className="text-sm font-medium text-gray-200">User Account</span>
                </div>
                <ExternalLink size={14} className="text-gray-500" />
              </div>
            </>
          ) : (
            <div className="flex justify-center py-2">
              <div className="w-7 h-7 rounded-full bg-white flex items-center justify-center text-xs font-bold text-black cursor-pointer">
                C
              </div>
            </div>
          )}
        </div>

      </div>
    </aside>
  );
};

export default ChatGPTSidebar;
