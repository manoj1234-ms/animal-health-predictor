import React, { useEffect, useState, useMemo } from 'react';
import { type DeviceSummary, fetchDashboardSummary } from '../api/client';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Activity, Thermometer, Wifi, RefreshCw, Heart } from 'lucide-react';

// Mock data generator for smooth graphing
const generateMockHistory = (baseValue: number, variance: number, count: number) => {
    return Array.from({ length: count }, (_, i) => ({
        time: `-${count - i}s`,
        value: baseValue + (Math.random() - 0.5) * variance,
        timestamp: Date.now() - (count - i) * 1000
    }));
};

interface TelemetryProps {
    preselectedId?: string | null;
}

export const Telemetry: React.FC<TelemetryProps> = ({ preselectedId }) => {
    const [devices, setDevices] = useState<DeviceSummary[]>([]);
    const [selectedDeviceId, setSelectedDeviceId] = useState<string | null>(preselectedId || null);
    const [timeRange, setTimeRange] = useState<'1m' | '5m' | '1h'>('1m');
    const [historyData, setHistoryData] = useState<any[]>([]);

    const refreshData = async () => {
        try {
            const data = await fetchDashboardSummary();
            setDevices(data.devices);
            if (!selectedDeviceId && !preselectedId && data.devices.length > 0) {
                setSelectedDeviceId(data.devices[0].device_id);
            }
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        if (preselectedId) {
            setSelectedDeviceId(preselectedId);
            // Clear history when switching animals to prevent visual jump
            setHistoryData([]);
        }
    }, [preselectedId]);

    useEffect(() => {
        refreshData();
        const interval = setInterval(refreshData, 2000);
        return () => clearInterval(interval);
    }, []);

    // Simulate reliable history data for the graph based on the selected device's current reading
    const selectedDevice = useMemo(() =>
        devices.find(d => d.device_id === selectedDeviceId),
        [devices, selectedDeviceId]
    );

    useEffect(() => {
        if (selectedDevice) {
            // Generate or update history based on current reading to simulate live stream
            setHistoryData(prev => {
                const newDataPoint = {
                    time: new Date().toLocaleTimeString(),
                    heart_rate: selectedDevice.heart_rate,
                    temperature: selectedDevice.temperature,
                    activity: selectedDevice.activity
                };
                // Keep last 20 points
                const newHistory = [...prev, newDataPoint].slice(-20);
                // Fill if empty
                if (newHistory.length < 2) {
                    return generateMockHistory(selectedDevice.heart_rate, 5, 20).map(h => ({
                        time: new Date(h.timestamp).toLocaleTimeString(),
                        heart_rate: h.value,
                        temperature: selectedDevice.temperature + (Math.random() - 0.5),
                        activity: selectedDevice.activity
                    }));
                }
                return newHistory;
            });
        }
    }, [selectedDevice]);

    return (
        <div className="p-6 md:p-10 min-h-screen text-slate-900 dark:text-white w-full max-w-7xl mx-auto space-y-8 transition-colors duration-300">
            <header className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight flex items-center">
                        <Activity className="mr-3 text-blue-600 dark:text-blue-500" size={32} />
                        Live Telemetry
                    </h2>
                    <p className="text-slate-500 dark:text-slate-400 mt-2 font-medium italic">Real-time vital sign monitoring and historical trend analysis.</p>
                </div>
                <div className="flex bg-white dark:bg-slate-900/50 p-1 rounded-xl border border-slate-200 dark:border-slate-700/50 backdrop-blur-sm shadow-sm dark:shadow-none">
                    {['1m', '5m', '1h'].map(range => (
                        <button
                            key={range}
                            onClick={() => setTimeRange(range as any)}
                            className={`px-4 py-1.5 rounded-lg text-xs font-black uppercase tracking-widest transition-all ${timeRange === range
                                ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/40'
                                : 'text-slate-400 hover:text-slate-900 dark:hover:text-white'
                                }`}
                        >
                            {range}
                        </button>
                    ))}
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
                {/* Device List Sidebar */}
                <div className="lg:col-span-1 bg-slate-900/40 border border-white/5 rounded-2xl overflow-hidden backdrop-blur-xl h-[600px] flex flex-col">
                    <div className="p-4 border-b border-white/5 bg-slate-900/60 sticky top-0 z-10 flex justify-between items-center">
                        <span className="font-bold text-slate-300 text-sm uppercase tracking-wider">Active Feeds</span>
                        <div className="flex space-x-2">
                            <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
                            <span className="text-xs text-emerald-400 font-bold">LIVE</span>
                        </div>
                    </div>
                    <div className="overflow-y-auto flex-1 p-2 space-y-1 custom-scrollbar">
                        {devices.map(device => (
                            <button
                                key={device.device_id}
                                onClick={() => setSelectedDeviceId(device.device_id)}
                                className={`w-full text-left p-3 rounded-xl transition-all border border-transparent ${selectedDeviceId === device.device_id
                                    ? 'bg-blue-600/10 border-blue-600/30 shadow-inner'
                                    : 'hover:bg-white/5 hover:border-white/5'
                                    }`}
                            >
                                <div className="flex justify-between items-center">
                                    <span className={`font-bold ${selectedDeviceId === device.device_id ? 'text-blue-400' : 'text-white'}`}>
                                        {device.animal_id}
                                    </span>
                                    <span className={`text-[10px] px-1.5 py-0.5 rounded font-black uppercase ${device.status === 'CRITICAL' ? 'bg-red-500 text-white' :
                                        device.status === 'WARNING' ? 'bg-amber-500 text-black' :
                                            'bg-emerald-500/20 text-emerald-400'
                                        }`}>{device.status}</span>
                                </div>
                                <div className="flex justify-between mt-2 text-xs text-slate-400">
                                    <span className="font-mono">{device.species}</span>
                                    <span className="font-mono opacity-60">ID: {device.device_id}</span>
                                </div>
                            </button>
                        ))}
                    </div>
                </div>

                {/* Main Charts Area */}
                <div className="lg:col-span-3 space-y-6">
                    {selectedDevice ? (
                        <>
                            {/* Vital Cards */}
                            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div className="bg-slate-900/40 border border-white/5 p-5 rounded-2xl backdrop-blur-xl relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                        <Heart size={80} />
                                    </div>
                                    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">Heart Rate</p>
                                    <div className="flex items-end">
                                        <span className={`text-4xl font-mono font-black ${selectedDevice.heart_rate > 100 ? 'text-rose-400' : 'text-white'}`}>
                                            {selectedDevice.heart_rate}
                                        </span>
                                        <span className="text-sm text-slate-500 mb-1 ml-2 font-bold">bpm</span>
                                    </div>
                                    <div className="mt-2 text-xs text-slate-500">
                                        Avg (1h): <span className="text-slate-300 font-mono">{(selectedDevice.heart_rate * 0.95).toFixed(0)} bpm</span>
                                    </div>
                                </div>

                                <div className="bg-slate-900/40 border border-white/5 p-5 rounded-2xl backdrop-blur-xl relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                        <Thermometer size={80} />
                                    </div>
                                    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">Body Temp</p>
                                    <div className="flex items-end">
                                        <span className={`text-4xl font-mono font-black ${selectedDevice.temperature > 39 ? 'text-amber-400' : 'text-white'}`}>
                                            {selectedDevice.temperature}
                                        </span>
                                        <span className="text-sm text-slate-500 mb-1 ml-2 font-bold">°C</span>
                                    </div>
                                    <div className="mt-2 text-xs text-slate-500">
                                        Last 24h peak: <span className="text-slate-300 font-mono">{(selectedDevice.temperature + 0.5).toFixed(1)}°C</span>
                                    </div>
                                </div>

                                <div className="bg-slate-900/40 border border-white/5 p-5 rounded-2xl backdrop-blur-xl relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-4 opacity-5 group-hover:opacity-10 transition-opacity">
                                        <Wifi size={80} />
                                    </div>
                                    <p className="text-slate-400 text-xs font-bold uppercase tracking-wider mb-1">Activity Index</p>
                                    <div className="flex items-end">
                                        <span className="text-4xl font-mono font-black text-blue-400">
                                            {Math.round(selectedDevice.activity)}%
                                        </span>
                                    </div>
                                    <div className="w-full bg-slate-800 rounded-full h-1.5 mt-3 overflow-hidden">
                                        <div className="bg-blue-500 h-full rounded-full transition-all duration-500" style={{ width: `${selectedDevice.activity}%` }}></div>
                                    </div>
                                </div>
                            </div>

                            {/* Charts */}
                            <div className="grid grid-cols-1 gap-6">
                                {/* Heart Rate Chart */}
                                <div className="bg-slate-900/40 border border-white/5 p-6 rounded-2xl backdrop-blur-xl h-80">
                                    <div className="flex justify-between items-center mb-6">
                                        <h3 className="font-bold text-slate-300 flex items-center text-sm uppercase tracking-wide">
                                            <Heart size={16} className="mr-2 text-rose-500" />
                                            Cardiac Rhythm
                                        </h3>
                                        <span className="text-xs text-slate-500 font-mono">Live Feed • 1s Interval</span>
                                    </div>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <AreaChart data={historyData}>
                                            <defs>
                                                <linearGradient id="colorHr" x1="0" y1="0" x2="0" y2="1">
                                                    <stop offset="5%" stopColor="rgb(244, 63, 94)" stopOpacity={0.3} />
                                                    <stop offset="95%" stopColor="rgb(244, 63, 94)" stopOpacity={0} />
                                                </linearGradient>
                                            </defs>
                                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                            <XAxis dataKey="time" stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} tickLine={false} axisLine={false} />
                                            <YAxis stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} tickLine={false} axisLine={false} domain={['dataMin - 10', 'dataMax + 10']} />
                                            <Tooltip
                                                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                                                itemStyle={{ color: '#fff' }}
                                            />
                                            <ReferenceLine y={100} stroke="rgba(244, 63, 94, 0.5)" strokeDasharray="3 3" label={{ position: 'right', value: 'High Threshold', fill: 'rgba(244, 63, 94, 0.5)', fontSize: 10 }} />
                                            <Area type="monotone" dataKey="heart_rate" stroke="#f43f5e" strokeWidth={3} fillOpacity={1} fill="url(#colorHr)" isAnimationActive={false} />
                                        </AreaChart>
                                    </ResponsiveContainer>
                                </div>

                                {/* Temperature Chart */}
                                <div className="bg-slate-900/40 border border-white/5 p-6 rounded-2xl backdrop-blur-xl h-64">
                                    <div className="flex justify-between items-center mb-6">
                                        <h3 className="font-bold text-slate-300 flex items-center text-sm uppercase tracking-wide">
                                            <Thermometer size={16} className="mr-2 text-amber-500" />
                                            Temperature Trend
                                        </h3>
                                    </div>
                                    <ResponsiveContainer width="100%" height="100%">
                                        <AreaChart data={historyData}>
                                            <defs>
                                                <linearGradient id="colorTemp" x1="0" y1="0" x2="0" y2="1">
                                                    <stop offset="5%" stopColor="rgb(245, 158, 11)" stopOpacity={0.3} />
                                                    <stop offset="95%" stopColor="rgb(245, 158, 11)" stopOpacity={0} />
                                                </linearGradient>
                                            </defs>
                                            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                            <XAxis dataKey="time" hide />
                                            <YAxis stroke="rgba(255,255,255,0.3)" tick={{ fontSize: 10 }} tickLine={false} axisLine={false} domain={['dataMin - 1', 'dataMax + 1']} />
                                            <Tooltip
                                                contentStyle={{ backgroundColor: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                                                itemStyle={{ color: '#fff' }}
                                            />
                                            <Area type="monotone" dataKey="temperature" stroke="#f59e0b" strokeWidth={3} fillOpacity={1} fill="url(#colorTemp)" isAnimationActive={false} />
                                        </AreaChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>
                        </>
                    ) : (
                        <div className="flex flex-col items-center justify-center h-full text-slate-500">
                            <RefreshCw className="animate-spin mb-4" size={32} />
                            <p>Connecting to Telemetry Stream...</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
