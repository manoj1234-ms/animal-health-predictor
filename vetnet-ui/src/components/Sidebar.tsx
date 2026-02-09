
import React from 'react';
import { LayoutDashboard, Stethoscope, Activity, Map, Settings, Menu, FileText } from 'lucide-react';
import { useSettings } from '../context/SettingsContext';

interface SidebarProps {
    activeTab: string;
    setActiveTab: (tab: string) => void;
    isOpen: boolean;
    toggleSidebar: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab, isOpen, toggleSidebar }) => {
    const { t } = useSettings();
    const menuItems = [
        { id: 'dashboard', label: t('dashboard'), icon: LayoutDashboard },
        { id: 'diagnostics', label: t('diagnostics'), icon: Stethoscope },
        { id: 'telemetry', label: t('telemetry'), icon: Activity },
        { id: 'map', label: t('map'), icon: Map },
        { id: 'reports', label: t('reports'), icon: FileText },
        { id: 'settings', label: t('settings'), icon: Settings },
    ];

    return (
        <>
            {/* Mobile Toggle */}
            <div className="md:hidden fixed top-4 left-4 z-50">
                <button onClick={toggleSidebar} className="p-2 bg-vet-secondary rounded-md text-white">
                    <Menu size={24} />
                </button>
            </div>

            {/* Sidebar Container */}
            <div className={`fixed inset-y-0 left-0 transform ${isOpen ? 'translate-x-0' : '-translate-x-full'} md:relative md:translate-x-0 transition-transform duration-200 ease-in-out z-30 w-64 bg-white dark:bg-vet-secondary text-slate-600 dark:text-white border-r border-slate-200 dark:border-gray-800 flex flex-col`}>
                <div className="p-6 border-b border-slate-100 dark:border-gray-800">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-teal-600 dark:from-blue-400 dark:to-teal-400 bg-clip-text text-transparent">
                        VetNet AI
                    </h1>
                    <p className="text-xs text-slate-400 dark:text-gray-400 mt-1 uppercase tracking-widest font-black">Enterprise Health</p>
                </div>

                <nav className="flex-1 py-6 space-y-2 px-3 text-slate-500 dark:text-gray-400">
                    {menuItems.map((item) => {
                        const Icon = item.icon;
                        const isActive = activeTab === item.id;
                        return (
                            <button
                                key={item.id}
                                onClick={() => setActiveTab(item.id)}
                                className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all ${isActive
                                    ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20'
                                    : 'hover:bg-slate-100 dark:hover:bg-vet-primary hover:text-blue-600 dark:hover:text-white font-medium'
                                    }`}
                            >
                                <Icon size={20} />
                                <span className="">{item.label}</span>
                            </button>
                        );
                    })}
                </nav>

                <div className="p-4 border-t border-slate-100 dark:border-gray-800">
                    <div className="bg-gradient-to-br from-indigo-50 to-blue-50 dark:from-indigo-900 dark:to-purple-900 rounded-2xl p-4 border border-indigo-100 dark:border-none">
                        <p className="text-xs font-black text-indigo-400 dark:text-indigo-200 uppercase tracking-widest">System Status</p>
                        <div className="flex items-center mt-2 space-x-2">
                            <span className="relative flex h-3 w-3">
                                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                                <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                            </span>
                            <span className="text-sm font-bold text-slate-700 dark:text-white">Active Node</span>
                        </div>
                    </div>
                </div>
            </div>
        </>
    );
};
