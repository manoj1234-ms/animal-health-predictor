import React, { useEffect, useState } from 'react';
import { type DeviceSummary, fetchDashboardSummary, diagnoseDevice } from '../api/client';
import { Activity, Thermometer, Heart, Battery, AlertTriangle, Stethoscope, X, Search, Filter, Phone, MapPin, User, Star, ShieldCheck } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

import { getSpeciesIcon } from './icons/SpeciesIcons';
import { getCategory, getNearbySpecialist } from '../utils/animalUtils';

interface DashboardProps {
    onNavigateToTelemetry: (deviceId: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onNavigateToTelemetry }) => {
    const [devices, setDevices] = useState<DeviceSummary[]>([]);
    const [error, setError] = useState<string | null>(null);

    // Dashboard Filter & Search State
    const [activeTab, setActiveTab] = useState<'OVERVIEW' | 'FARM' | 'ZOO' | 'PET'>('OVERVIEW');
    const [searchTerm, setSearchTerm] = useState('');
    const [filterStatus, setFilterStatus] = useState<'ALL' | 'CRITICAL' | 'WARNING' | 'HEALTHY'>('ALL');

    // Diagnosis Modal State
    const [selectedDevice, setSelectedDevice] = useState<string | null>(null);
    const [diagnosisResult, setDiagnosisResult] = useState<any | null>(null);
    const [isDiagnosing, setIsDiagnosing] = useState(false);

    const [contactingSpecialist, setContactingSpecialist] = useState(false);
    const [contactSuccess, setContactSuccess] = useState(false);

    const refreshData = async () => {
        try {
            const data = await fetchDashboardSummary();
            setDevices(data.devices);
            setError(null);
        } catch (err) {
            console.error(err);
            setError('Failed to connect to IoT Gateway');
        }
    };

    useEffect(() => {
        refreshData();
        const interval = setInterval(refreshData, 2000); // Poll every 2s
        return () => clearInterval(interval);
    }, []);

    const handleDiagnose = async (deviceId: string) => {
        setSelectedDevice(deviceId);
        setIsDiagnosing(true);
        setDiagnosisResult(null);
        setContactSuccess(false);
        try {
            const result = await diagnoseDevice(deviceId);
            setDiagnosisResult(result);
        } catch (err) {
            console.error(err);
            setDiagnosisResult({ error: "Diagnosis Failed" });
        } finally {
            setIsDiagnosing(false);
        }
    };

    const handleContactSpecialist = () => {
        setContactingSpecialist(true);
        setTimeout(() => {
            setContactingSpecialist(false);
            setContactSuccess(true);
        }, 2000);
    };

    const closeModal = () => {
        setSelectedDevice(null);
        setDiagnosisResult(null);
        setContactSuccess(false);
    };

    const filteredDevices = devices.filter(device => {
        const category = getCategory(device.species);
        const matchesTab = activeTab === 'OVERVIEW' ||
            (activeTab === 'FARM' && category === 'Farm') ||
            (activeTab === 'ZOO' && category === 'Zoo') ||
            (activeTab === 'PET' && category === 'Pet');

        const matchesSearch = device.animal_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            device.device_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            device.species.toLowerCase().includes(searchTerm.toLowerCase());
        const matchesStatus = filterStatus === 'ALL' || device.status === filterStatus;

        return matchesTab && matchesSearch && matchesStatus;
    });

    const stats = {
        total: filteredDevices.length,
        critical: filteredDevices.filter(d => d.status === 'CRITICAL').length,
        warning: filteredDevices.filter(d => d.status === 'WARNING').length,
        healthy: filteredDevices.filter(d => d.status === 'HEALTHY').length,
    };

    return (
        <div className="p-6 md:p-10 space-y-8 min-h-screen text-slate-900 dark:text-white relative overflow-x-hidden w-full transition-colors duration-300">
            {/* Header with Tabs */}
            <div className="flex flex-col space-y-6">
                <div className="flex flex-col xl:flex-row justify-between items-start xl:items-center gap-6">
                    <div>
                        <h2 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-emerald-600 dark:from-blue-400 dark:to-emerald-400 tracking-tight">VetNet AI Manager</h2>
                        <p className="text-slate-500 dark:text-slate-400 mt-2 font-medium italic">
                            {activeTab === 'OVERVIEW' && `Monitoring all ${devices.length} entities`}
                            {activeTab === 'FARM' && `Livestock Management System`}
                            {activeTab === 'ZOO' && `Exotic Species Monitoring`}
                            {activeTab === 'PET' && `Small Animal Clinic View`}
                        </p>
                    </div>

                    <div className="flex flex-col md:flex-row gap-4 w-full xl:w-auto">
                        {/* Stats Cards */}
                        <div className="flex space-x-4">
                            {[
                                { label: 'Critical', val: stats.critical, color: 'text-rose-600 dark:text-rose-500', shadow: 'rgba(225,29,72,0.2)' },
                                { label: 'Warning', val: stats.warning, color: 'text-amber-600 dark:text-amber-500', shadow: 'rgba(217,119,6,0.2)' },
                                { label: 'Healthy', val: stats.healthy, color: 'text-emerald-600 dark:text-emerald-500', shadow: 'rgba(5,150,105,0.2)' }
                            ].map((stat, i) => (
                                <div key={i} className="bg-white dark:bg-slate-800/50 backdrop-blur-md px-6 py-3 rounded-2xl border border-slate-200 dark:border-slate-700/50 flex flex-col items-center min-w-[90px] flex-1 shadow-sm dark:shadow-none">
                                    <span className="text-slate-400 dark:text-slate-400 text-[10px] uppercase tracking-widest font-black">{stat.label}</span>
                                    <span className={`text-2xl font-black ${stat.color}`}>{stat.val}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Navigation Tabs */}
                <div className="flex space-x-1 p-1 bg-slate-200 dark:bg-slate-800/50 rounded-xl w-full md:w-fit border border-slate-200 dark:border-slate-700/50 shadow-inner">
                    {(['OVERVIEW', 'FARM', 'ZOO', 'PET'] as const).map((tab) => (
                        <button
                            key={tab}
                            onClick={() => setActiveTab(tab)}
                            className={`px-6 py-2.5 rounded-lg text-xs font-black tracking-widest transition-all duration-200 ${activeTab === tab
                                ? 'bg-white dark:bg-blue-600 text-blue-600 dark:text-white shadow-lg dark:shadow-blue-900/40 border border-slate-200 dark:border-none'
                                : 'text-slate-500 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'
                                }`}
                        >
                            {tab === 'OVERVIEW' ? 'Global View' :
                                tab === 'FARM' ? 'Farm Ops' :
                                    tab === 'ZOO' ? 'Zoo Net' : 'Clinic'}
                        </button>
                    ))}
                </div>
            </div>

            {/* Controls Bar */}
            <div className="bg-white/80 dark:bg-slate-800/30 backdrop-blur-xl p-4 rounded-2xl border border-slate-200 dark:border-slate-700/50 flex flex-col md:flex-row gap-4 justify-between items-center shadow-sm dark:shadow-none">
                <div className="relative w-full md:w-96 group">
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <Search className="h-5 w-5 text-slate-400 group-focus-within:text-blue-500 transition-colors" />
                    </div>
                    <input
                        type="text"
                        placeholder="Search animals, IDs, or species..."
                        className="block w-full pl-10 pr-3 py-2.5 border border-slate-200 dark:border-slate-700 rounded-xl leading-5 bg-slate-100 dark:bg-slate-900/50 text-slate-700 dark:text-slate-300 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                <div className="flex gap-3 w-full md:w-auto overflow-x-auto pb-2 md:pb-0">
                    <div className="flex items-center space-x-2 bg-slate-100 dark:bg-slate-900/50 px-3 py-2 rounded-xl border border-slate-200 dark:border-slate-700">
                        <Filter size={16} className="text-slate-400" />
                        <span className="text-xs font-black text-slate-400 dark:text-slate-500 uppercase tracking-widest">Status:</span>
                        <select
                            value={filterStatus}
                            onChange={(e) => setFilterStatus(e.target.value as any)}
                            className="bg-transparent text-sm font-bold text-slate-600 dark:text-slate-300 focus:outline-none cursor-pointer"
                        >
                            <option value="ALL">All Units</option>
                            <option value="CRITICAL">Critical</option>
                            <option value="WARNING">Warning</option>
                            <option value="HEALTHY">Healthy</option>
                        </select>
                    </div>
                </div>
            </div>

            {error && (
                <div className="bg-red-500/10 border border-red-500/20 text-red-200 p-4 rounded-xl flex items-center backdrop-blur-sm animate-in fade-in slide-in-from-top-4">
                    <AlertTriangle className="mr-3" />
                    {error} (Ensure backend is running on :8002)
                </div>
            )}

            {/* Grid of Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                <AnimatePresence mode='popLayout'>
                    {filteredDevices.map((device) => (
                        <motion.div
                            layout
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            transition={{ type: "spring", stiffness: 300, damping: 25 }}
                            key={device.device_id}
                            className={`relative overflow-hidden rounded-3xl border p-6 transition-all backdrop-blur-xl flex flex-col justify-between group hover:shadow-2xl hover:-translate-y-1 duration-300 ${device.status === 'CRITICAL'
                                ? 'bg-red-500/10 dark:bg-red-500/10 border-red-500/30 shadow-[0_0_30px_rgba(239,68,68,0.15)] dark:shadow-[0_0_30px_rgba(239,68,68,0.15)]'
                                : device.status === 'WARNING'
                                    ? 'bg-amber-500/10 dark:bg-amber-500/10 border-amber-500/30 shadow-[0_0_30px_rgba(245,158,11,0.15)] dark:shadow-[0_0_30px_rgba(245,158,11,0.15)]'
                                    : 'bg-white dark:bg-slate-800/40 border-slate-200 dark:border-slate-700/50 hover:border-blue-500/50 shadow-sm dark:shadow-none'
                                }`}
                        >
                            {/* Top Section */}
                            <div>
                                {/* Status Indicator */}
                                <div className={`absolute top-4 right-4 px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${device.status === 'CRITICAL' ? 'bg-red-500 text-white shadow-lg shadow-red-500/40 animate-pulse' :
                                    device.status === 'WARNING' ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/40' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/20'
                                    }`}>
                                    {device.status}
                                </div>

                                <div className="flex justify-between items-start mb-6">
                                    <div>
                                        <h3 className="text-xl font-black text-slate-800 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{device.animal_id}</h3>
                                        <p className="text-[10px] font-black text-slate-400 dark:text-slate-500 mt-1 uppercase tracking-widest leading-none">{device.species} // {device.device_id.substring(0, 8)}</p>
                                    </div>
                                </div>

                                {/* Icon Display */}
                                <div className="absolute top-16 right-4 opacity-10 scale-[2.5] pointer-events-none group-hover:opacity-20 group-hover:scale-[3] transition-all duration-500 rotate-12">
                                    {getSpeciesIcon(device.species)}
                                </div>

                                <div className="space-y-4 relative z-10">
                                    <div className="flex justify-between items-center p-3 rounded-2xl bg-slate-50 dark:bg-slate-900/30 border border-slate-100 dark:border-slate-800/50 shadow-inner">
                                        <div className="flex items-center text-slate-500 dark:text-slate-300">
                                            <Thermometer size={18} className="mr-3 text-rose-500" />
                                            <span className="text-xs font-black uppercase tracking-widest">Temp</span>
                                        </div>
                                        <span className={`font-mono text-lg font-black ${device.status === 'CRITICAL' && device.alerts.some(a => a.includes('Temp') || a.includes('Fever')) ? 'text-rose-600 dark:text-rose-400 drop-shadow-[0_0_8px_rgba(244,63,94,0.3)]' : 'text-slate-700 dark:text-slate-200'
                                            }`}>
                                            {device.temperature}°C
                                        </span>
                                    </div>

                                    <div className="flex justify-between items-center p-3 rounded-2xl bg-slate-50 dark:bg-slate-900/30 border border-slate-100 dark:border-slate-800/50 shadow-inner">
                                        <div className="flex items-center text-slate-500 dark:text-slate-300">
                                            <Heart size={18} className="mr-3 text-rose-500" />
                                            <span className="text-xs font-black uppercase tracking-widest">Heart Rate</span>
                                        </div>
                                        <span className="font-mono text-lg font-black text-slate-700 dark:text-slate-200">
                                            {device.heart_rate} <span className="text-[10px] text-slate-400 dark:text-slate-500 font-black uppercase">bpm</span>
                                        </span>
                                    </div>

                                    <div className="space-y-2">
                                        <div className="flex justify-between text-xs text-slate-400 font-medium">
                                            <span>Activity Level</span>
                                            <span>{Math.round(device.activity)}%</span>
                                        </div>
                                        <div className="w-full bg-slate-700/50 rounded-full h-1.5 overflow-hidden">
                                            <motion.div
                                                initial={{ width: 0 }}
                                                animate={{ width: `${Math.min(device.activity, 100)}%` }}
                                                className={`h-full rounded-full ${device.activity < 20 ? 'bg-amber-500' : 'bg-blue-500'}`}
                                            />
                                        </div>
                                    </div>
                                </div>

                                {/* Alerts Section */}
                                {device.alerts.length > 0 && (
                                    <div className="mt-5 pt-4 border-t border-slate-700/30">
                                        {device.alerts.map((alert, idx) => (
                                            <div key={idx} className="flex items-start text-xs font-semibold text-rose-300 mb-2 last:mb-0 bg-rose-500/10 p-2 rounded-lg border border-rose-500/20">
                                                <AlertTriangle size={14} className="mr-2 mt-0.5 flex-shrink-0 text-rose-500" />
                                                {alert}
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>

                            {/* Bottom Section: Diagnosis Button */}
                            <div className="mt-6 space-y-3 pt-4 border-t border-slate-700/30">
                                <div className="grid grid-cols-2 gap-3">
                                    {(device.status === 'CRITICAL' || device.status === 'WARNING') && (
                                        <button
                                            onClick={() => handleDiagnose(device.device_id)}
                                            className="flex items-center justify-center space-x-2 py-2.5 bg-rose-600 hover:bg-rose-500 text-white rounded-xl transition-all font-bold text-xs active:scale-95 shadow-lg shadow-rose-900/20"
                                        >
                                            <Stethoscope size={14} />
                                            <span>DIAGNOSE</span>
                                        </button>
                                    )}
                                    <button
                                        onClick={() => onNavigateToTelemetry(device.device_id)}
                                        className={`flex items-center justify-center space-x-2 py-2.5 rounded-xl transition-all font-bold text-xs active:scale-95 ${(device.status === 'CRITICAL' || device.status === 'WARNING')
                                            ? 'bg-slate-700 hover:bg-slate-600 text-slate-200 col-span-1'
                                            : 'bg-blue-600 hover:bg-blue-500 text-white col-span-2 shadow-lg shadow-blue-900/20'
                                            }`}
                                    >
                                        <Activity size={14} />
                                        <span>VIEW LIVE</span>
                                    </button>
                                </div>

                                <div className="flex justify-between items-center text-[10px] font-bold text-slate-500 uppercase tracking-widest">
                                    <span>Sync: {device.seconds_ago}s ago</span>
                                    <div className="flex items-center">
                                        <Battery size={14} className={`mr-1.5 ${device.battery < 20 ? 'text-red-500' : 'text-emerald-500'}`} />
                                        {device.battery}%
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {filteredDevices.length === 0 && (
                    <div className="col-span-full flex flex-col items-center justify-center py-20 text-slate-500 opacity-60">
                        <Search size={48} className="mb-4" />
                        <p className="text-lg font-medium">No animals found matching your criteria.</p>
                    </div>
                )}
            </div>

            {/* Diagnosis Modal (Available globally) */}
            <AnimatePresence>
                {selectedDevice && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: 20 }}
                            className="bg-slate-900 border border-slate-700 w-full max-w-lg rounded-3xl shadow-2xl overflow-hidden ring-1 ring-white/10"
                        >
                            <div className="flex justify-between items-center p-6 border-b border-slate-800 bg-slate-900/50">
                                <div className="flex items-center space-x-3">
                                    <div className="bg-blue-500/20 p-2.5 rounded-xl">
                                        <Stethoscope className="text-blue-400" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-bold text-white">AI Diagnosis Report</h3>
                                        <p className="text-xs text-slate-400 font-light">Powered by VetNet Neural Engine</p>
                                    </div>
                                </div>
                                <button onClick={closeModal} className="text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 p-2 rounded-full transition-colors">
                                    <X size={20} />
                                </button>
                            </div>

                            <div className="p-8">
                                {isDiagnosing ? (
                                    <div className="flex flex-col items-center justify-center py-12 space-y-6">
                                        <div className="relative">
                                            <div className="animate-spin rounded-full h-20 w-20 border-t-2 border-b-2 border-blue-500"></div>
                                            <div className="absolute inset-0 flex items-center justify-center">
                                                <Activity size={28} className="text-blue-500 animate-pulse" />
                                            </div>
                                        </div>
                                        <div className="text-center space-y-2">
                                            <p className="text-white font-medium text-xl">Analyzing Bio-Telemetry</p>
                                            <p className="text-slate-400 text-sm">Comparing against 10M+ veterinary records...</p>
                                        </div>
                                    </div>
                                ) : diagnosisResult ? (
                                    <div className="space-y-6">
                                        <div className="bg-gradient-to-br from-blue-900/40 to-indigo-900/40 border border-blue-500/30 rounded-2xl p-6 relative overflow-hidden group">
                                            <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                                                <Activity size={120} />
                                            </div>
                                            <span className="text-xs text-blue-300 uppercase font-black tracking-widest mb-1 block">Most Likely Condition</span>
                                            <h2 className="text-3xl font-black text-white mt-1 leading-tight tracking-tight">
                                                {diagnosisResult.ai_diagnosis?.predicted_disease || "Unknown"}
                                            </h2>
                                            <div className="flex items-center mt-4 space-x-3">
                                                <div className="bg-slate-900/60 backdrop-blur-sm px-4 py-1.5 rounded-full text-sm border border-slate-700/50 text-slate-300">
                                                    Confidence: <span className="text-emerald-400 font-bold">{(diagnosisResult.ai_diagnosis?.confidence * 100).toFixed(1)}%</span>
                                                </div>
                                                <div className={`bg-slate-900/60 backdrop-blur-sm px-4 py-1.5 rounded-full text-sm border ${diagnosisResult.ai_diagnosis?.severity === 'CRITICAL' ? 'border-red-500/50 text-red-100' : 'border-slate-700/50 text-slate-300'}`}>
                                                    Severity: <span className={diagnosisResult.ai_diagnosis?.severity === 'CRITICAL' ? 'text-red-400 font-black px-1 animate-pulse' : 'text-rose-400 font-bold'}>{diagnosisResult.ai_diagnosis?.severity}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <h4 className="flex items-center font-bold text-slate-300 mb-2 text-xs uppercase tracking-wide">
                                                    <ShieldCheck size={14} className="mr-2 text-emerald-500" />
                                                    Treatment Strategy
                                                </h4>
                                                <div className="bg-slate-800/40 p-4 rounded-xl text-sm text-slate-300 leading-relaxed border border-slate-700/50 shadow-inner h-full">
                                                    {diagnosisResult.ai_diagnosis?.treatment?.treatment_plan || "General supportive care."}
                                                </div>
                                            </div>
                                            <div>
                                                <h4 className="flex items-center font-bold text-slate-300 mb-2 text-xs uppercase tracking-wide">
                                                    <Battery size={14} className="mr-2 text-blue-500" />
                                                    Recommended Medication
                                                </h4>
                                                <div className="bg-slate-800/40 p-4 rounded-xl text-sm text-slate-300 border border-slate-700/50 shadow-inner h-full">
                                                    <ul className="space-y-1">
                                                        {diagnosisResult.ai_diagnosis?.treatment?.medications?.map((m: string, i: number) => (
                                                            <li key={i} className="flex items-center">
                                                                <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mr-2"></div>
                                                                {m}
                                                            </li>
                                                        )) || <li>Symptomatic treatment</li>}
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex justify-between items-center bg-slate-900/60 p-4 rounded-xl border border-white/5">
                                            <div className="flex items-center">
                                                <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mr-4">Prognosis</div>
                                                <div className={`text-sm font-bold ${diagnosisResult.ai_diagnosis?.treatment?.prognosis === 'Excellent' ? 'text-emerald-400' : 'text-amber-400'}`}>
                                                    {diagnosisResult.ai_diagnosis?.treatment?.prognosis || "Requires observation"}
                                                </div>
                                            </div>
                                            <div className="text-[10px] text-slate-500 font-mono italic">
                                                Clinical Validation: {diagnosisResult.ai_diagnosis?.biological_validation?.valid ? 'PASSED' : 'CHECK REQUIRED'}
                                            </div>
                                        </div>

                                        <div className="flex space-x-3 pt-4">
                                            {contactSuccess ? (
                                                <div className="w-full space-y-4 animate-in fade-in zoom-in slide-in-from-bottom-4 duration-500">
                                                    <div className="bg-emerald-500/10 border border-emerald-500/30 rounded-2xl p-5 relative overflow-hidden">
                                                        <div className="flex justify-between items-start mb-4">
                                                            <div className="flex items-center bg-emerald-500/20 px-3 py-1 rounded-full text-[10px] font-black text-emerald-400 uppercase tracking-widest">
                                                                <ShieldCheck size={12} className="mr-1.5" /> Specialist Dispatched
                                                            </div>
                                                            <div className="text-xs text-slate-400 font-mono">ETA: 15-20 Mins</div>
                                                        </div>

                                                        <div className="flex items-center space-x-4">
                                                            <div className="w-14 h-14 bg-slate-800 rounded-2xl border border-white/10 flex items-center justify-center relative shadow-lg">
                                                                <User className="text-blue-400" size={28} />
                                                                <div className="absolute -bottom-1 -right-1 bg-emerald-500 w-3 h-3 rounded-full border-2 border-slate-900 animate-pulse"></div>
                                                            </div>
                                                            <div className="flex-1">
                                                                <div className="flex items-center justify-between">
                                                                    <h3 className="font-black text-xl text-white tracking-tight">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any).device_id)?.species || '')).name}</h3>
                                                                    <div className="flex items-center text-amber-400">
                                                                        <Star size={12} fill="currentColor" />
                                                                        <span className="text-xs font-bold ml-1">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any).device_id)?.species || '')).rating}</span>
                                                                    </div>
                                                                </div>
                                                                <p className="text-blue-400 text-xs font-bold uppercase tracking-wide">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any).device_id)?.species || '')).clinic}</p>
                                                            </div>
                                                        </div>

                                                        <div className="grid grid-cols-2 gap-3 mt-5">
                                                            <div className="bg-black/30 p-3 rounded-xl border border-white/5 flex items-center">
                                                                <Phone className="text-slate-500 mr-2" size={14} />
                                                                <span className="text-xs font-mono text-slate-300">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any).device_id)?.species || '')).phone}</span>
                                                            </div>
                                                            <div className="bg-black/30 p-3 rounded-xl border border-white/5 flex items-center">
                                                                <MapPin className="text-slate-500 mr-2" size={14} />
                                                                <span className="text-xs font-bold text-slate-300">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any).device_id)?.species || '')).distance} away</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <button onClick={closeModal} className="w-full py-4 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl font-black text-xs uppercase tracking-widest transition-all">
                                                        Close Portal
                                                    </button>
                                                </div>
                                            ) : (
                                                <>
                                                    <button onClick={closeModal} className="flex-1 py-3.5 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl font-bold transition-colors">
                                                        Dismiss
                                                    </button>
                                                    <button
                                                        onClick={handleContactSpecialist}
                                                        disabled={contactingSpecialist}
                                                        className="flex-1 py-3.5 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold shadow-lg shadow-blue-900/40 transition-all hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-wait flex items-center justify-center"
                                                    >
                                                        {contactingSpecialist ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> : 'Contact Specialist'}
                                                    </button>
                                                </>
                                            )}
                                        </div>
                                    </div>
                                ) : (
                                    <div className="text-center text-rose-400 bg-rose-900/20 p-6 rounded-xl border border-rose-900/50">
                                        DIAGNOSIS FAILED. PLEASE TRY AGAIN.
                                    </div>
                                )}
                            </div>
                        </motion.div>
                    </div>
                )}
            </AnimatePresence>
        </div>
    );
};
