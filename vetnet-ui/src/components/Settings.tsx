import React, { useState } from 'react';
import { useSettings } from '../context/SettingsContext';
import { Settings as SettingsIcon, Bell, Shield, Cloud, LogOut, ChevronRight, Moon, Sun, Monitor, Save } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export const Settings: React.FC = () => {
    const { theme, setTheme, language, setLanguage, timezone, setTimezone } = useSettings();
    const [activeSection, setActiveSection] = useState('general');
    const [tempThreshold, setTempThreshold] = useState(39.5);
    const [notifications, setNotifications] = useState(true);
    const [isSaving, setIsSaving] = useState(false);

    const sections = [
        { id: 'general', label: 'General', icon: SettingsIcon },
        { id: 'notifications', label: 'Notifications', icon: Bell },
        { id: 'security', label: 'Security', icon: Shield },
        { id: 'api', label: 'API & Integrations', icon: Cloud },
    ];

    return (
        <div className="p-6 md:p-10 min-h-screen text-slate-900 dark:text-white w-full max-w-5xl mx-auto flex flex-col md:flex-row gap-8 transition-colors duration-300">
            {/* Sidebar Navigation */}
            <div className="w-full md:w-64 flex flex-col space-y-2">
                <h2 className="text-2xl font-black text-slate-900 dark:text-white mb-6 flex items-center tracking-tight">
                    <SettingsIcon className="mr-3 text-blue-600 dark:text-slate-400" />
                    Settings
                </h2>

                <nav className="space-y-1">
                    {sections.map(section => (
                        <button
                            key={section.id}
                            onClick={() => setActiveSection(section.id)}
                            className={`w-full text-left px-4 py-3 rounded-xl font-black text-[10px] uppercase tracking-widest flex items-center justify-between group transition-all ${activeSection === section.id
                                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20'
                                : 'text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-white/5 hover:text-blue-600 dark:hover:text-white'
                                }`}
                        >
                            <div className="flex items-center">
                                <section.icon size={18} className={`mr-3 ${activeSection === section.id ? 'text-blue-200' : 'text-slate-500 group-hover:text-slate-300'}`} />
                                {section.label}
                            </div>
                            {activeSection === section.id && <ChevronRight size={16} />}
                        </button>
                    ))}
                </nav>

                <div className="mt-auto pt-8 border-t border-slate-200 dark:border-white/10">
                    <button className="w-full text-left px-4 py-3 rounded-xl font-black text-[10px] uppercase tracking-widest text-rose-500 hover:bg-rose-500/10 hover:text-rose-600 transition-colors flex items-center">
                        <LogOut size={18} className="mr-3" />
                        Sign Out
                    </button>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 bg-white dark:bg-slate-900/40 border border-slate-200 dark:border-white/5 rounded-3xl p-8 backdrop-blur-xl min-h-[600px] relative overflow-hidden shadow-2xl dark:shadow-none">
                <AnimatePresence mode="wait">
                    {activeSection === 'general' && (
                        <motion.div
                            key="general"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-8"
                        >
                            <div>
                                <h3 className="text-xl font-black text-slate-900 dark:text-white mb-1 uppercase tracking-tight">Display Settings</h3>
                                <p className="text-slate-500 dark:text-slate-400 text-xs font-medium italic">Customize your dashboard appearance.</p>
                            </div>

                            <div className="grid grid-cols-3 gap-4">
                                {['light', 'dark', 'system'].map((t) => (
                                    <button
                                        key={t}
                                        onClick={() => setTheme(t as any)}
                                        className={`p-4 rounded-2xl border flex flex-col items-center justify-center space-y-3 transition-all ${theme === t
                                            ? 'bg-blue-600 border-blue-500 text-white shadow-xl shadow-blue-900/20 ring-2 ring-blue-500 dark:ring-blue-400 ring-offset-2 ring-offset-white dark:ring-offset-slate-900'
                                            : 'bg-slate-50 dark:bg-slate-800/50 border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
                                            }`}
                                    >
                                        {t === 'light' ? <Sun size={24} /> : t === 'dark' ? <Moon size={24} /> : <Monitor size={24} />}
                                        <span className="capitalize font-black text-[10px] uppercase tracking-widest">{t} Mode</span>
                                    </button>
                                ))}
                            </div>

                            <div className="space-y-4 pt-6 border-t border-slate-100 dark:border-white/5">
                                <h3 className="text-xl font-black text-slate-900 dark:text-white uppercase tracking-tight">Localization</h3>
                                <div className="grid grid-cols-2 gap-6">
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest">Language</label>
                                        <select
                                            value={language}
                                            onChange={(e) => setLanguage(e.target.value as any)}
                                            className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-700 dark:text-white focus:outline-none focus:border-blue-500 transition-all font-medium text-sm"
                                        >
                                            <option value="English (US)">English (US)</option>
                                            <option value="Spanish">Spanish</option>
                                            <option value="French">French</option>
                                        </select>
                                    </div>
                                    <div className="space-y-2">
                                        <label className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest">Timezone</label>
                                        <select
                                            value={timezone}
                                            onChange={(e) => setTimezone(e.target.value as any)}
                                            className="w-full bg-slate-50 dark:bg-black/20 border border-slate-200 dark:border-white/10 rounded-xl px-4 py-2.5 text-slate-700 dark:text-white focus:outline-none focus:border-blue-500 transition-all font-medium text-sm"
                                        >
                                            <option value="UTC">UTC (Coordinated Universal Time)</option>
                                            <option value="EST">EST (Eastern Standard Time)</option>
                                            <option value="PST">PST (Pacific Standard Time)</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {activeSection === 'notifications' && (
                        <motion.div
                            key="notifications"
                            initial={{ opacity: 0, x: 20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, x: -20 }}
                            className="space-y-8"
                        >
                            <div>
                                <h3 className="text-xl font-black text-slate-900 dark:text-white mb-1 uppercase tracking-tight">Alert Configuration</h3>
                                <p className="text-slate-500 dark:text-slate-400 text-xs font-medium italic">Set thresholds for automatic alerts.</p>
                            </div>

                            <div className="bg-slate-50 dark:bg-slate-800/30 p-6 rounded-3xl border border-slate-200 dark:border-white/5 space-y-6 shadow-inner">
                                <div className="flex justify-between items-center">
                                    <div>
                                        <h4 className="font-black text-slate-800 dark:text-white uppercase tracking-tight">Enable Push Notifications</h4>
                                        <p className="text-[10px] text-slate-400 dark:text-slate-500 uppercase font-black tracking-widest">Receive alerts directly to your browser.</p>
                                    </div>
                                    <button
                                        onClick={() => setNotifications(!notifications)}
                                        className={`w-12 h-6 rounded-full transition-colors relative ${notifications ? 'bg-emerald-500 shadow-[0_0_10px_rgba(16,185,129,0.3)]' : 'bg-slate-300 dark:bg-slate-600'}`}
                                    >
                                        <div className={`w-4 h-4 rounded-full bg-white absolute top-1 transition-transform shadow-md ${notifications ? 'left-7' : 'left-1'}`}></div>
                                    </button>
                                </div>

                                <div className="space-y-4">
                                    <div className="flex justify-between">
                                        <label className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest">Critical Temperature Threshold</label>
                                        <span className="text-sm font-black text-amber-600 dark:text-amber-400 font-mono">{tempThreshold}°C</span>
                                    </div>
                                    <input
                                        type="range"
                                        min="38"
                                        max="42"
                                        step="0.1"
                                        value={tempThreshold}
                                        onChange={(e) => setTempThreshold(parseFloat(e.target.value))}
                                        className="w-full h-1.5 bg-slate-200 dark:bg-slate-700 rounded-lg appearance-none cursor-pointer accent-blue-600 dark:accent-amber-500"
                                    />
                                    <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest italic opacity-60 text-right">Alerts triggering above {tempThreshold}°C will be flagged.</p>
                                </div>
                            </div>
                        </motion.div>
                    )}
                    {/* More sections can be added similarly */}
                </AnimatePresence>

                <div className="absolute bottom-8 right-8">
                    <button
                        onClick={() => {
                            setIsSaving(true);
                            setTimeout(() => setIsSaving(false), 1500);
                        }}
                        className="bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-3 rounded-xl font-bold shadow-lg shadow-emerald-900/20 flex items-center transition-all active:scale-95 disabled:opacity-50"
                    >
                        {isSaving ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-2"></div> : <Save size={18} className="mr-2" />}
                        {isSaving ? 'Synchronizing...' : 'Save Changes'}
                    </button>
                </div>
            </div>
        </div>
    );
};
