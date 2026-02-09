import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './components/Dashboard';
import { AiDiagnosis } from './components/AiDiagnosis';
import { Telemetry } from './components/Telemetry';
import { MapView } from './components/MapView';
import { Reports } from './components/Reports';
import { Settings } from './components/Settings';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedDeviceId, setSelectedDeviceId] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const navigateToDevice = (tab: string, deviceId: string) => {
    setSelectedDeviceId(deviceId);
    setActiveTab(tab);
  };

  return (
    <div className="flex h-screen transition-colors duration-300 bg-slate-50 text-slate-900 dark:bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] dark:from-slate-900 dark:via-[#0b0c15] dark:to-black overflow-hidden font-sans dark:text-gray-100">
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        isOpen={isSidebarOpen}
        toggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
      />

      <main className="flex-1 overflow-auto relative w-full">
        {activeTab === 'dashboard' && <Dashboard onNavigateToTelemetry={(id) => navigateToDevice('telemetry', id)} />}
        {activeTab === 'diagnostics' && <AiDiagnosis onNavigateToTelemetry={(id) => navigateToDevice('telemetry', id)} />}
        {activeTab === 'telemetry' && <Telemetry preselectedId={selectedDeviceId} />}
        {activeTab === 'map' && <MapView onTrackDevice={(id) => navigateToDevice('telemetry', id)} />}
        {activeTab === 'reports' && <Reports />}
        {activeTab === 'settings' && <Settings />}
      </main>
    </div>
  );
}

export default App;
