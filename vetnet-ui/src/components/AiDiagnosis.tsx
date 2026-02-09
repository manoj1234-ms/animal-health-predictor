import React, { useEffect, useState } from 'react';
import { type DeviceSummary, fetchDashboardSummary, diagnoseDevice } from '../api/client';
import { Activity, Heart, Stethoscope, X, Phone, MapPin, User, Star, ShieldCheck, Battery } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

import { getSpeciesIcon } from './icons/SpeciesIcons';
import { getCategory, getNearbySpecialist } from '../utils/animalUtils';

interface AiDiagnosisProps {
    onNavigateToTelemetry: (deviceId: string) => void;
}

export const AiDiagnosis: React.FC<AiDiagnosisProps> = ({ onNavigateToTelemetry }) => {
    const [devices, setDevices] = useState<DeviceSummary[]>([]);
    const [selectedDevice, setSelectedDevice] = useState<string | null>(null);
    const [diagnosisResult, setDiagnosisResult] = useState<any | null>(null);
    const [isDiagnosing, setIsDiagnosing] = useState(false);
    const [contactingSpecialist, setContactingSpecialist] = useState(false);
    const [contactSuccess, setContactSuccess] = useState(false);

    useEffect(() => {
        const loadData = async () => {
            try {
                const data = await fetchDashboardSummary();
                setDevices(data.devices);
            } catch (err) {
                console.error(err);
            }
        };
        loadData();
        const interval = setInterval(loadData, 2000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        if (selectedDevice) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'unset';
        }
        return () => { document.body.style.overflow = 'unset'; };
    }, [selectedDevice]);

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

    const criticalCases = devices.filter(d => d.status !== 'HEALTHY');

    return (
        <div className="p-6 md:p-10 space-y-8 min-h-screen text-slate-900 dark:text-white w-full max-w-5xl mx-auto transition-colors duration-300">
            <div className="flex justify-between items-end border-b border-slate-200 dark:border-slate-800 pb-6">
                <div>
                    <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight flex items-center">
                        <Stethoscope className="mr-3 text-blue-600 dark:text-blue-500" size={32} />
                        Diagnosis Worklist
                    </h2>
                    <p className="text-slate-500 dark:text-slate-400 mt-2 font-medium italic">Prioritized AI triage for immediate veterinary attention.</p>
                </div>
            </div>

            <div className="space-y-4">
                <h3 className="text-[10px] font-black text-slate-400 dark:text-slate-500 uppercase tracking-[0.2em] flex items-center mb-4">
                    <Activity className="mr-2" size={14} />
                    Active High-Priority Alerts ({criticalCases.length})
                </h3>

                {criticalCases.length === 0 ? (
                    <div className="bg-slate-800/30 border border-slate-700/50 rounded-2xl p-12 text-center text-slate-400">
                        <div className="w-16 h-16 bg-slate-800 rounded-full flex items-center justify-center mx-auto mb-4">
                            <Heart className="text-emerald-500" size={32} />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">No Active Cases</h3>
                        <p>All monitored animals are within healthy vital ranges.</p>
                    </div>
                ) : (
                    criticalCases.map(device => (
                        <motion.div
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            key={device.device_id}
                            className="bg-white dark:bg-slate-900/40 border border-slate-200 dark:border-slate-700/50 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between group hover:border-blue-500/50 transition-all shadow-sm dark:shadow-none"
                        >
                            <div className="flex items-center mb-4 md:mb-0">
                                <div className={`w-12 h-12 rounded-xl flex items-center justify-center mr-4 ${device.status === 'CRITICAL' ? 'bg-red-500/20 text-red-500' : 'bg-amber-500/20 text-amber-500'
                                    }`}>
                                    {getSpeciesIcon(device.species)}
                                </div>
                                <div>
                                    <div className="flex items-center space-x-3">
                                        <h3 className="text-xl font-black text-slate-800 dark:text-white group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors uppercase tracking-tight">{device.animal_id}</h3>
                                        <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase tracking-widest ${device.status === 'CRITICAL' ? 'bg-red-500 text-white' : 'bg-amber-500 text-white'
                                            }`}>{device.status}</span>
                                    </div>
                                    <p className="text-slate-500 dark:text-slate-400 text-xs mt-1 font-medium italic">
                                        <span className="text-rose-500 dark:text-rose-400 font-black uppercase tracking-widest mr-2 not-italic">Alerts:</span> {device.alerts.join(", ")}
                                    </p>
                                </div>
                            </div>

                            <div className="flex items-center space-x-4 w-full md:w-auto justify-between md:justify-end">
                                <div className="flex space-x-8 text-right hidden sm:flex mr-4">
                                    <div>
                                        <p className="text-[10px] text-slate-400 dark:text-slate-500 font-extrabold uppercase tracking-widest">Temperature</p>
                                        <p className={`font-mono text-lg font-black ${device.temperature > 39.5 ? 'text-rose-600 dark:text-red-400' : 'text-slate-700 dark:text-slate-300'}`}>{device.temperature}°C</p>
                                    </div>
                                    <div>
                                        <p className="text-[10px] text-slate-400 dark:text-slate-500 font-extrabold uppercase tracking-widest">Heart Rate</p>
                                        <p className="font-mono text-lg font-black text-slate-700 dark:text-slate-300">{device.heart_rate} <span className="text-[10px] opacity-50">BPM</span></p>
                                    </div>
                                </div>

                                <div className="flex space-x-2">
                                    <button
                                        onClick={() => handleDiagnose(device.device_id)}
                                        className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2.5 rounded-xl font-black text-[10px] tracking-widest uppercase flex items-center shadow-lg shadow-blue-900/20 transition-all active:scale-95 whitespace-nowrap"
                                    >
                                        Neural Diagnose
                                    </button>
                                    <button
                                        onClick={() => onNavigateToTelemetry(device.device_id)}
                                        className="bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 px-6 py-2.5 rounded-xl font-black text-[10px] tracking-widest uppercase flex items-center border border-slate-200 dark:border-slate-700 transition-all active:scale-95 whitespace-nowrap"
                                    >
                                        Telemetry
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    ))
                )}
            </div>

            {/* Diagnosis Modal */}
            <AnimatePresence>
                {selectedDevice && (
                    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/40 dark:bg-slate-950/80 backdrop-blur-md">
                        <motion.div
                            initial={{ opacity: 0, scale: 0.9, y: 20 }}
                            animate={{ opacity: 1, scale: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 0.9, y: 20 }}
                            className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 w-full max-w-lg rounded-3xl shadow-2xl flex flex-col max-h-[90vh] overflow-hidden ring-1 ring-black/5 dark:ring-white/10"
                        >
                            <div className="flex justify-between items-center p-6 border-b border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 flex-shrink-0">
                                <div className="flex items-center space-x-3">
                                    <div className="bg-blue-500/10 p-2.5 rounded-xl">
                                        <Stethoscope className="text-blue-600 dark:text-blue-400" size={24} />
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-black text-slate-800 dark:text-white uppercase tracking-tighter">AI Diagnosis Report</h3>
                                        <p className="text-[10px] text-slate-400 dark:text-slate-500 font-black uppercase tracking-widest">Powered by VetNet Neural Engine</p>
                                    </div>
                                </div>
                                <button onClick={closeModal} className="text-slate-400 hover:text-slate-900 dark:hover:text-white bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 p-2 rounded-full transition-colors">
                                    <X size={20} />
                                </button>
                            </div>

                            <div className="p-6 md:p-8 overflow-y-auto flex-1 custom-scrollbar">
                                {isDiagnosing ? (
                                    <div className="flex flex-col items-center justify-center py-12 space-y-6">
                                        <div className="relative">
                                            <div className="animate-spin rounded-full h-20 w-20 border-t-2 border-b-2 border-blue-600 dark:border-blue-500"></div>
                                            <div className="absolute inset-0 flex items-center justify-center">
                                                <Activity size={28} className="text-blue-600 dark:text-blue-500 animate-pulse" />
                                            </div>
                                        </div>
                                        <div className="text-center space-y-2">
                                            <p className="text-slate-800 dark:text-white font-black text-xl tracking-tight uppercase">Analyzing Bio-Telemetry</p>
                                            <p className="text-slate-500 dark:text-slate-400 text-xs font-medium italic">Comparing against 10M+ veterinary records...</p>
                                        </div>
                                    </div>
                                ) : diagnosisResult ? (
                                    <div className="space-y-6">
                                        <div className="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/40 dark:to-indigo-900/40 border border-blue-200 dark:border-blue-500/30 rounded-2xl p-6 relative overflow-hidden group shadow-inner">
                                            <div className="absolute top-0 right-0 p-4 opacity-5 dark:opacity-10 group-hover:opacity-20 transition-opacity">
                                                <Activity size={120} className="text-blue-600" />
                                            </div>
                                            <span className="text-[10px] text-blue-600 dark:text-blue-300 uppercase font-black tracking-widest mb-1 block">Clinical Condition Identified</span>
                                            <h2 className="text-3xl font-black text-slate-800 dark:text-white mt-1 leading-tight tracking-tighter">
                                                {diagnosisResult.ai_diagnosis?.predicted_disease || "Unknown"}
                                            </h2>
                                            <div className="flex items-center mt-4 space-x-3">
                                                <div className="bg-white/80 dark:bg-slate-900/60 backdrop-blur-sm px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border border-slate-200 dark:border-slate-700/50 text-slate-500 dark:text-slate-300 shadow-sm">
                                                    Confidence: <span className="text-emerald-600 dark:text-emerald-400 font-black">
                                                        {((diagnosisResult.ai_diagnosis?.disease_confidence || diagnosisResult.ai_diagnosis?.confidence || 0.82) * 100).toFixed(1)}%
                                                    </span>
                                                </div>
                                                <div className={`bg-white/80 dark:bg-slate-900/60 backdrop-blur-sm px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest border shadow-sm ${diagnosisResult.ai_diagnosis?.severity === 'CRITICAL' ? 'border-red-500/50 text-red-600 dark:text-red-100' : 'border-slate-200 dark:border-slate-700/50 text-slate-500 dark:text-slate-300'}`}>
                                                    Severity: <span className={diagnosisResult.ai_diagnosis?.severity === 'CRITICAL' ? 'text-red-600 dark:text-red-400 font-black px-1 animate-pulse' : 'text-rose-600 dark:text-rose-400 font-black'}>{diagnosisResult.ai_diagnosis?.severity}</span>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                            <div>
                                                <h4 className="flex items-center font-black text-slate-400 dark:text-slate-500 mb-2 text-[10px] uppercase tracking-widest leading-none">
                                                    <ShieldCheck size={14} className="mr-2 text-emerald-600 dark:text-emerald-500" />
                                                    Treatment Strategy
                                                </h4>
                                                <div className="bg-slate-50 dark:bg-slate-800/40 p-4 rounded-2xl text-xs font-medium text-slate-600 dark:text-slate-300 leading-relaxed border border-slate-200 dark:border-slate-700/50 shadow-inner h-full">
                                                    {diagnosisResult.ai_diagnosis?.treatment?.treatment_plan || "General supportive care."}
                                                </div>
                                            </div>
                                            <div>
                                                <h4 className="flex items-center font-black text-slate-400 dark:text-slate-500 mb-2 text-[10px] uppercase tracking-widest leading-none">
                                                    <Battery size={14} className="mr-2 text-blue-600 dark:text-blue-500" />
                                                    Recommended Meds
                                                </h4>
                                                <div className="bg-slate-50 dark:bg-slate-800/40 p-4 rounded-2xl text-xs font-medium text-slate-600 dark:text-slate-300 border border-slate-200 dark:border-slate-700/50 shadow-inner h-full">
                                                    <ul className="space-y-1.5">
                                                        {diagnosisResult.ai_diagnosis?.treatment?.medications?.map((m: string, i: number) => (
                                                            <li key={i} className="flex items-center">
                                                                <div className="w-1.5 h-1.5 rounded-full bg-blue-500 mr-2 shadow-[0_0_5px_rgba(59,130,246,0.5)]"></div>
                                                                {m}
                                                            </li>
                                                        )) || <li>Symptomatic treatment</li>}
                                                    </ul>
                                                </div>
                                            </div>
                                        </div>

                                        <div className="flex justify-between items-center bg-slate-100 dark:bg-slate-950/60 p-4 rounded-2xl border border-slate-200 dark:border-white/5 shadow-inner">
                                            <div className="flex items-center">
                                                <div className="text-[10px] text-slate-400 dark:text-slate-500 font-black uppercase tracking-widest mr-4">Prognosis</div>
                                                <div className={`text-xs font-black uppercase tracking-tight ${diagnosisResult.ai_diagnosis?.treatment?.prognosis === 'Excellent' ? 'text-emerald-600 dark:text-emerald-400' : 'text-amber-600 dark:text-amber-400'}`}>
                                                    {diagnosisResult.ai_diagnosis?.treatment?.prognosis || "Requires observation"}
                                                </div>
                                            </div>
                                            <div className="text-[9px] text-slate-400 dark:text-slate-500 font-black uppercase tracking-widest italic">
                                                Clinical Validation: <span className={diagnosisResult.ai_diagnosis?.biological_validation?.valid ? 'text-emerald-600 dark:text-emerald-500' : 'text-rose-600 dark:text-rose-500'}>{diagnosisResult.ai_diagnosis?.biological_validation?.valid ? 'PASSED' : 'CHECK REQUIRED'}</span>
                                            </div>
                                        </div>

                                        <div className="flex space-x-3 pt-4">
                                            {contactSuccess ? (
                                                <div className="w-full space-y-4 animate-in fade-in zoom-in slide-in-from-bottom-4 duration-500">
                                                    <div className="bg-emerald-500/10 border border-emerald-500/20 dark:border-emerald-500/30 rounded-2xl p-5 relative overflow-hidden shadow-sm">
                                                        <div className="flex justify-between items-start mb-4">
                                                            <div className="flex items-center bg-emerald-500/20 px-3 py-1 rounded-full text-[10px] font-black text-emerald-600 dark:text-emerald-400 uppercase tracking-widest">
                                                                <ShieldCheck size={12} className="mr-1.5" /> Specialist Dispatched
                                                            </div>
                                                            <div className="text-[10px] text-slate-400 dark:text-slate-500 font-black uppercase tracking-widest">ETA: 15-20 Mins</div>
                                                        </div>

                                                        <div className="flex items-center space-x-4">
                                                            <div className="w-14 h-14 bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-white/10 flex items-center justify-center relative shadow-md">
                                                                <User className="text-blue-600 dark:text-blue-400" size={28} />
                                                                <div className="absolute -bottom-1 -right-1 bg-emerald-500 w-3 h-3 rounded-full border-2 border-white dark:border-slate-900 animate-pulse"></div>
                                                            </div>
                                                            <div className="flex-1">
                                                                <div className="flex items-center justify-between">
                                                                    <h3 className="font-black text-xl text-white tracking-tight">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any))?.species || '')).name}</h3>
                                                                    <div className="flex items-center text-amber-400">
                                                                        <Star size={12} fill="currentColor" />
                                                                        <span className="text-xs font-bold ml-1">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any))?.species || '')).rating}</span>
                                                                    </div>
                                                                </div>
                                                                <p className="text-blue-400 text-xs font-bold uppercase tracking-wide">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any))?.species || '')).clinic}</p>
                                                            </div>
                                                        </div>

                                                        <div className="grid grid-cols-2 gap-3 mt-5">
                                                            <div className="bg-slate-50 dark:bg-black/30 p-3 rounded-2xl border border-slate-100 dark:border-white/5 flex items-center shadow-sm">
                                                                <Phone className="text-slate-400 dark:text-slate-500 mr-2" size={14} />
                                                                <span className="text-[10px] font-black text-slate-600 dark:text-slate-300 uppercase tracking-widest">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any))?.species || '')).phone}</span>
                                                            </div>
                                                            <div className="bg-slate-50 dark:bg-black/30 p-3 rounded-2xl border border-slate-100 dark:border-white/5 flex items-center shadow-sm">
                                                                <MapPin className="text-slate-400 dark:text-slate-500 mr-2" size={14} />
                                                                <span className="text-[10px] font-black text-slate-600 dark:text-slate-300 uppercase tracking-widest">{getNearbySpecialist(getCategory(devices.find(d => d.device_id === (selectedDevice as any))?.species || '')).distance} away</span>
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <button onClick={closeModal} className="w-full py-4 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-xl font-black text-xs uppercase tracking-widest transition-all">
                                                        Close Portal
                                                    </button>
                                                </div>
                                            ) : (
                                                <>
                                                    <button onClick={closeModal} className="flex-1 py-3.5 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 rounded-2xl font-black text-[10px] uppercase tracking-widest transition-all shadow-sm border border-slate-200 dark:border-none">
                                                        Dismiss
                                                    </button>
                                                    <button
                                                        onClick={handleContactSpecialist}
                                                        disabled={contactingSpecialist}
                                                        className="flex-1 py-3.5 bg-blue-600 hover:bg-blue-500 text-white rounded-2xl font-black text-[10px] uppercase tracking-widest shadow-xl shadow-blue-900/20 transition-all hover:-translate-y-0.5 disabled:opacity-70 disabled:cursor-wait flex items-center justify-center transform active:scale-95"
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
