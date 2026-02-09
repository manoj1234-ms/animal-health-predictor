import React, { useEffect, useState } from 'react';
import { type DeviceSummary, fetchDashboardSummary } from '../api/client';
import { Map as MapIcon, Locate, Layers } from 'lucide-react';
import { motion } from 'framer-motion';
import { getCategory, getHabitatName } from '../utils/animalUtils';

// Define Habitat Anchors
const HABITATS = {
    Zoo: { x: 25, y: 30, color: 'rgba(234, 179, 8, 0.05)', border: 'rgba(234, 179, 8, 0.2)' },
    Farm: { x: 50, y: 70, color: 'rgba(34, 197, 94, 0.05)', border: 'rgba(34, 197, 94, 0.2)' },
    Pet: { x: 75, y: 30, color: 'rgba(59, 130, 246, 0.05)', border: 'rgba(59, 130, 246, 0.2)' }
};

const generateLocation = (species: string, index: number) => {
    const category = getCategory(species);
    const anchor = HABITATS[category] || HABITATS.Farm;

    // Spread markers around the anchor
    const angle = (index * 137.5) % 360; // Golden angle for even-ish spread
    const distance = 5 + (index % 5) * 3;

    return {
        x: anchor.x + distance * Math.cos(angle * Math.PI / 180),
        y: anchor.y + distance * Math.sin(angle * Math.PI / 180)
    };
};

interface MapViewProps {
    onTrackDevice: (deviceId: string) => void;
}

export const MapView: React.FC<MapViewProps> = ({ onTrackDevice }) => {
    const [devices, setDevices] = useState<DeviceSummary[]>([]);
    const [locations, setLocations] = useState<Record<string, { x: number, y: number }>>({});
    const [selectedDevice, setSelectedDevice] = useState<string | null>(null);

    const refreshData = async () => {
        try {
            const data = await fetchDashboardSummary();
            setDevices(data.devices);

            // Initialize locations if needed
            setLocations(prev => {
                const next = { ...prev };
                data.devices.forEach((d, i) => {
                    if (!next[d.device_id]) {
                        next[d.device_id] = generateLocation(d.species, i);
                    } else {
                        // Add slight jitter to simulate movement
                        next[d.device_id] = {
                            x: Math.max(5, Math.min(95, next[d.device_id].x + (Math.random() - 0.5) * 0.2)),
                            y: Math.max(5, Math.min(95, next[d.device_id].y + (Math.random() - 0.5) * 0.2))
                        };
                    }
                });
                return next;
            });

        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        refreshData();
        const interval = setInterval(refreshData, 2000);
        return () => clearInterval(interval);
    }, []);

    const selectedDeviceInfo = devices.find(d => d.device_id === selectedDevice);

    return (
        <div className="p-6 md:p-10 min-h-screen text-slate-900 dark:text-white w-full h-full flex flex-col transition-colors duration-300">
            <header className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-3xl font-black text-slate-900 dark:text-white tracking-tight flex items-center">
                        <MapIcon className="mr-3 text-blue-600 dark:text-blue-500" size={32} />
                        Geospatial Monitoring
                    </h2>
                    <p className="text-slate-500 dark:text-slate-400 mt-2 font-medium italic">Live GPS tracking of herd movements and habitat utilization.</p>
                </div>
                <div className="flex bg-white dark:bg-slate-900/50 p-2 rounded-xl border border-slate-200 dark:border-white/5 space-x-4 text-[10px] font-black uppercase tracking-widest backdrop-blur-md shadow-sm dark:shadow-none">
                    <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.5)]"></div>
                        <span className="text-slate-500 dark:text-slate-400">Zoo</span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.5)]"></div>
                        <span className="text-slate-500 dark:text-slate-400">Farm</span>
                    </div>
                    <div className="flex items-center space-x-2">
                        <div className="w-2 h-2 rounded-full bg-amber-500 shadow-[0_0_8px_rgba(245,158,11,0.5)]"></div>
                        <span className="text-slate-500 dark:text-slate-400">Pet Clinic</span>
                    </div>
                </div>
            </header>

            {/* Map Container */}
            <div className="flex-1 bg-white dark:bg-slate-900/40 border border-slate-200 dark:border-slate-700/50 rounded-3xl backdrop-blur-xl relative overflow-hidden shadow-2xl dark:shadow-none flex flex-col md:flex-row">

                {/* Visual Map Area */}
                <div className="flex-1 relative bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-slate-900 via-[#0a0a0a] to-black min-h-[500px]">
                    {/* Grid Overlay */}
                    <div className="absolute inset-0" style={{
                        backgroundImage: 'linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px)',
                        backgroundSize: '50px 50px'
                    }}></div>

                    {/* Habitat Zones Background Visuals */}
                    {Object.entries(HABITATS).map(([name, h]) => (
                        <div
                            key={name}
                            className="absolute transform -translate-x-1/2 -translate-y-1/2 rounded-[40%] flex items-center justify-center border transition-all duration-1000"
                            style={{
                                left: `${h.x}%`,
                                top: `${h.y}%`,
                                width: '30%',
                                height: '35%',
                                backgroundColor: h.color,
                                borderColor: h.border,
                                filter: 'blur(20px)',
                            }}
                        >
                            <span className="text-[40px] font-black opacity-10 uppercase tracking-[20px] select-none">{name}</span>
                        </div>
                    ))}

                    {/* Radar Sweep Effect */}
                    <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <div className="w-[80%] h-[80%] border border-emerald-500/5 rounded-full animate-[spin_10s_linear_infinite] border-t-emerald-500/20"></div>
                    </div>

                    {/* Devices */}
                    {devices.map((device) => {
                        const loc = locations[device.device_id] || { x: 50, y: 50 };
                        const isSelected = selectedDevice === device.device_id;

                        return (
                            <motion.button
                                key={device.device_id}
                                layout
                                initial={{ opacity: 0, scale: 0 }}
                                animate={{
                                    opacity: 1,
                                    scale: 1,
                                    left: `${loc.x}%`,
                                    top: `${loc.y}%`
                                }}
                                transition={{ type: 'spring', damping: 20, stiffness: 100 }}
                                onClick={() => setSelectedDevice(device.device_id)}
                                className="absolute transform -translate-x-1/2 -translate-y-1/2 group z-10 focus:outline-none"
                            >
                                <div className={`relative flex items-center justify-center transition-all duration-300 ${isSelected ? 'scale-150 z-50' : 'group-hover:scale-125'}`}>
                                    {/* Pulse Ring for Critical */}
                                    {device.status === 'CRITICAL' && (
                                        <div className="absolute w-12 h-12 rounded-full bg-red-500/30 animate-ping"></div>
                                    )}

                                    {/* Marker */}
                                    <div className={`w-3 h-3 rounded-full border shadow-lg ${device.status === 'CRITICAL' ? 'bg-red-500 border-white' :
                                        device.status === 'WARNING' ? 'bg-amber-500 border-white' :
                                            getCategory(device.species) === 'Zoo' ? 'bg-blue-400 border-white/50' :
                                                getCategory(device.species) === 'Farm' ? 'bg-green-400 border-white/50' :
                                                    'bg-blue-500 border-white/50'
                                        }`}></div>

                                    {/* Selection Glow */}
                                    {isSelected && (
                                        <div className="absolute inset-0 bg-white/40 blur-sm rounded-full animate-pulse"></div>
                                    )}

                                    {/* Tooltip Label */}
                                    <div className={`absolute top-6 left-1/2 -translate-x-1/2 whitespace-nowrap bg-black/80 text-white text-[10px] px-2 py-1 rounded backdrop-blur-md border border-white/10 pointer-events-none transition-opacity ${isSelected || device.status === 'CRITICAL' ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'}`}>
                                        <span className="font-bold">{device.animal_id}</span>
                                        <span className="block text-[8px] text-slate-400">{device.species}</span>
                                    </div>
                                </div>
                            </motion.button>
                        );
                    })}
                </div>

                {/* Sidebar Info Panel */}
                <div className="w-full md:w-80 bg-slate-900/80 border-l border-white/5 p-6 backdrop-blur-2xl flex flex-col">
                    <h3 className="text-sm font-bold text-slate-400 uppercase tracking-widest mb-6">Sector Detail</h3>

                    {selectedDeviceInfo ? (
                        <div className="space-y-6 animate-in fade-in slide-in-from-right-4">
                            <div className="p-5 bg-slate-800/40 rounded-2xl border border-white/5 shadow-inner">
                                <div className="flex justify-between items-start mb-2">
                                    <h2 className="text-2xl font-bold text-white tracking-tight">{selectedDeviceInfo.animal_id}</h2>
                                    <span className={`px-2 py-0.5 rounded text-[10px] font-black uppercase ${selectedDeviceInfo.status === 'CRITICAL' ? 'bg-red-500 text-white' :
                                        selectedDeviceInfo.status === 'WARNING' ? 'bg-amber-500 text-white' :
                                            'bg-emerald-500/20 text-emerald-400'
                                        }`}>{selectedDeviceInfo.status}</span>
                                </div>
                                <p className="text-xs text-slate-500 font-mono mb-6 pb-4 border-b border-white/5">DEVICE_ID: {selectedDevice}</p>

                                <div className="grid grid-cols-2 gap-3">
                                    <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                                        <span className="block text-[9px] text-slate-500 font-bold uppercase mb-1">Habitat</span>
                                        <span className={`font-bold text-xs ${getCategory(selectedDeviceInfo.species) === 'Zoo' ? 'text-blue-400' :
                                            getCategory(selectedDeviceInfo.species) === 'Farm' ? 'text-green-400' :
                                                'text-amber-400'
                                            }`}>{getHabitatName(selectedDeviceInfo.species)}</span>
                                    </div>
                                    <div className="bg-black/40 p-3 rounded-xl border border-white/5">
                                        <span className="block text-[9px] text-slate-500 font-bold uppercase mb-1">Movement</span>
                                        <span className="font-bold text-xs text-white">Lively</span>
                                    </div>
                                </div>
                            </div>

                            <div className="space-y-2">
                                <button
                                    onClick={() => onTrackDevice(selectedDevice || '')}
                                    className="w-full py-4 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-bold text-sm shadow-lg shadow-blue-900/40 transition-all flex items-center justify-center active:scale-95"
                                >
                                    <Locate size={18} className="mr-2" /> Live Track Animal
                                </button>
                                <button className="w-full py-3 bg-slate-800/50 hover:bg-slate-800 text-slate-400 rounded-xl font-bold text-xs border border-white/5 transition-all">
                                    Export Movement Logs
                                </button>
                            </div>
                        </div>
                    ) : (
                        <div className="flex-1 flex flex-col items-center justify-center text-slate-500 text-center">
                            <Layers size={48} className="mb-4 opacity-50" />
                            <p className="text-sm">Select a marker on the map to view animal details.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};
