import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar'; 
import AppRouters from './routers/AppRouters';

const App = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
      <Navbar />

      <div className="flex flex-1 pt-20 h-screen overflow-hidden">
        
        <div className="hidden md:block w-64 flex-shrink-0 border-gray-200">
          <Sidebar />
        </div>

        <main className="flex-1 flex flex-col h-full  relative overflow-y-auto px-4 md:px-8 py-6">
          <AppRouters />
        </main>

      </div>
    </div>
  );
};

export default App;
