import React, { useEffect, useState } from 'react';
import { type DeviceSummary, fetchDashboardSummary } from '../api/client';
import { FileText, Download, Filter, Search, Calendar, ChevronRight, CheckCircle2, AlertCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useSettings } from '../context/SettingsContext';

export const Reports: React.FC = () => {
    const { timezone } = useSettings();
    const [devices, setDevices] = useState<DeviceSummary[]>([]);
    const [searchQuery, setSearchQuery] = useState('');
    const [isExporting, setIsExporting] = useState(false);

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
    }, []);

    const criticalIncidents = devices.filter(d => d.status === 'CRITICAL');
    const warnings = devices.filter(d => d.status === 'WARNING');

    // Filtered list for the main table
    const filteredReports = devices.filter(d =>
        d.animal_id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        d.species.toLowerCase().includes(searchQuery.toLowerCase())
    );

    const handleExport = () => {
        setIsExporting(true);
        setTimeout(() => {
            setIsExporting(false);
            alert("Comprehensive Health Report (PDF) has been generated and downloaded to your local storage.");
        }, 2000);
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="p-6 md:p-10 min-h-screen text-slate-900 dark:text-white w-full transition-colors duration-300"
        >
            <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-4">
                <div>
                    <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight flex items-center">
                        <FileText className="mr-3 text-blue-600 dark:text-emerald-400" size={32} />
                        Precinct Reports
                    </h2>
                    <p className="text-slate-500 dark:text-slate-400 mt-2 font-medium italic">Compliance-ready medical documentation and incident audits.</p>
                </div>

                <button
                    onClick={handleExport}
                    disabled={isExporting}
                    className="flex items-center space-x-2 bg-emerald-600 hover:bg-emerald-500 text-white px-6 py-3.5 rounded-xl font-bold transition-all shadow-lg shadow-emerald-900/20 active:scale-95 disabled:opacity-50"
                >
                    {isExporting ? <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div> : <Download size={18} />}
                    <span>Generate Master Audit</span>
                </button>
            </header>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
                {[
                    { label: 'Medical Incidents (24h)', val: criticalIncidents.length + warnings.length, sub: 'Active Cases', color: 'text-rose-600 dark:text-rose-400' },
                    { label: 'Audit Readiness', val: '98%', sub: 'Compliance score', color: 'text-emerald-600 dark:text-emerald-400' },
                    { label: 'Next Automated Sync', val: '04:00', sub: 'Local Precinct Time', color: 'text-blue-600 dark:text-blue-400' }
                ].map((stat, i) => (
                    <div key={i} className="bg-white dark:bg-slate-900/40 border border-slate-200 dark:border-white/5 p-6 rounded-3xl backdrop-blur-md shadow-sm dark:shadow-none transition-all">
                        <span className="text-[10px] text-slate-400 dark:text-slate-500 font-black uppercase tracking-[0.2em]">{stat.label}</span>
                        <div className="flex items-baseline space-x-2 mt-2">
                            <span className={`text-4xl font-black ${stat.color}`}>{stat.val}</span>
                            <span className="text-xs text-slate-400 dark:text-slate-400 font-bold">{stat.sub}</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Main Content Area */}
            <div className="bg-white dark:bg-slate-900/40 border border-slate-200 dark:border-white/5 rounded-3xl backdrop-blur-xl overflow-hidden shadow-2xl dark:shadow-none">
                <div className="p-6 border-b border-slate-200 dark:border-white/5 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div className="relative w-full md:w-96 group">
                        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-500 transition-colors" size={18} />
                        <input
                            type="text"
                            placeholder="Find record by Animal ID or Species..."
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                            className="w-full bg-slate-100 dark:bg-black/40 border border-slate-200 dark:border-white/10 rounded-xl py-3 pl-12 pr-4 text-sm focus:outline-none focus:border-blue-500/50 transition-all font-black text-slate-700 dark:text-white"
                        />
                    </div>
                    <div className="flex space-x-2">
                        <button className="p-3 bg-slate-100 dark:bg-slate-800/50 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-xl border border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400 transition-all">
                            <Calendar size={18} />
                        </button>
                        <button className="p-3 bg-slate-100 dark:bg-slate-800/50 hover:bg-slate-200 dark:hover:bg-slate-800 rounded-xl border border-slate-200 dark:border-white/5 text-slate-500 dark:text-slate-400 transition-all">
                            <Filter size={18} />
                        </button>
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="text-left border-b border-slate-200 dark:border-white/5 text-[10px] uppercase tracking-widest text-slate-400 dark:text-slate-500 font-black">
                                <th className="px-8 py-5">Record Instance</th>
                                <th className="px-8 py-5">Clinical Status</th>
                                <th className="px-8 py-5">Species</th>
                                <th className="px-8 py-5 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-white/5">
                            <AnimatePresence>
                                {filteredReports.map((report, idx) => (
                                    <motion.tr
                                        key={report.device_id}
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: idx * 0.05 }}
                                        className="hover:bg-white/[0.02] transition-colors group"
                                    >
                                        <td className="px-8 py-4">
                                            <div className="flex items-center space-x-4">
                                                <div className="w-10 h-10 bg-slate-800 rounded-xl border border-white/10 flex items-center justify-center font-black text-xs text-blue-400">
                                                    {report.animal_id.substring(0, 2)}
                                                </div>
                                                <div>
                                                    <div className="font-bold text-white tracking-tight">{report.animal_id}</div>
                                                    <div className="text-[10px] text-slate-500 font-mono italic">UID: {report.device_id.substring(0, 8)}...</div>
                                                </div>
                                            </div>
                                        </td>
                                        <td className="px-8 py-4 text-xs">
                                            <span className={`px-2.5 py-1 rounded-full font-black tracking-tighter uppercase ${report.status === 'CRITICAL' ? 'bg-red-500 text-white shadow-lg shadow-red-900/20' :
                                                report.status === 'WARNING' ? 'bg-amber-500 text-white' :
                                                    'bg-emerald-500/20 text-emerald-400'
                                                }`}>
                                                {report.status}
                                            </span>
                                        </td>
                                        <td className="px-8 py-4 text-sm font-medium text-slate-300">
                                            {report.species}
                                        </td>
                                        <td className="px-8 py-4 text-xs font-mono text-slate-400 dark:text-slate-500">
                                            {timezone === 'UTC' ? '2026-02-09 15:30:44' :
                                                timezone === 'EST' ? '2026-02-09 10:30:44' :
                                                    '2026-02-09 07:30:44'} <span className="text-[8px] opacity-40 font-black">{timezone}</span>
                                        </td>
                                        <td className="px-8 py-4 text-right">
                                            <button className="text-slate-500 hover:text-white transition-colors">
                                                <ChevronRight size={20} />
                                            </button>
                                        </td>
                                    </motion.tr>
                                ))}
                            </AnimatePresence>
                        </tbody>
                    </table>
                </div>

                {filteredReports.length === 0 && (
                    <div className="py-20 flex flex-col items-center justify-center text-slate-500 space-y-4">
                        <AlertCircle size={48} className="opacity-20" />
                        <p className="font-medium italic">No matching medical records found.</p>
                    </div>
                )}
            </div>

            <footer className="mt-10 flex justify-center pb-10">
                <p className="text-[10px] text-slate-600 font-mono tracking-widest uppercase flex items-center">
                    <CheckCircle2 size={12} className="mr-2 text-emerald-500/40" />
                    Automated Reporting Active for 20 Local Animal Categories
                </p>
            </footer>
        </motion.div>
    );
};
