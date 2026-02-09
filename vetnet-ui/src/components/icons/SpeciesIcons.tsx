import { Activity, Dog, Cat, Bird, Fish, Squirrel, Rat, Bug } from 'lucide-react';

export const CowIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M7 21a4 4 0 0 1-4-4V9a5 5 0 1 1 10 0v8a4 4 0 0 1-4 4Z" /><path d="M11 21a4 4 0 0 1-4-4V9" /><path d="M22 17a3 3 0 0 1-3 3h-2v-4a3 3 0 0 1 3-3 3 3 0 0 1 2 4Z" /></svg>
);

export const PigIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><circle cx="12" cy="12" r="10" /><path d="M10 11a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" /><path d="M14 11a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z" /><path d="M12 15a2 2 0 0 1-2-2h4a2 2 0 0 1-2 2Z" /><path d="M12 2v2" /><path d="M12 20v2" /></svg>
);

export const LionIcon = ({ className }: { className?: string }) => (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}><path d="M3 14c.83.642 2.077 1.017 3.5 1c1.423.017 2.67-.358 3.5-1c.83-.642 2.077-1.017 3.5-1c1.423-.017 2.67.358 3.5 1" /><path d="M8 22v-5" /><path d="M16 22v-5" /><path d="M12 2v2" /><path d="M3.17 6.13c2.58-2.26 6.13-2.6 9.83-1.13c1.78.7 3.58 2.3 4.8 4" /></svg>
);

export const getSpeciesIcon = (species: string, size: number = 24) => {
    const iconSize = size;
    switch (species) {
        // Pets
        case 'Dog': return <Dog size={iconSize} className="text-blue-400" />;
        case 'Cat': return <Cat size={iconSize} className="text-purple-400" />;
        case 'Rabbit': return <Squirrel size={iconSize} className="text-amber-300" />;
        case 'GuineaPig': return <Squirrel size={iconSize} className="text-orange-300" />;
        case 'Ferret': return <Rat size={iconSize} className="text-slate-400" />;
        case 'Parrot': return <Bird size={iconSize} className="text-emerald-400" />;
        case 'Fish': return <Fish size={iconSize} className="text-cyan-400" />;

        // Farm
        case 'Cattle': return <CowIcon className={`text-green-400 w-${iconSize / 4} h-${iconSize / 4}`} />;
        case 'Buffalo': return <CowIcon className={`text-slate-600 w-${iconSize / 4} h-${iconSize / 4}`} />;
        case 'Pig': return <PigIcon className={`text-pink-400 w-${iconSize / 4} h-${iconSize / 4}`} />;
        case 'Sheep': return <Activity size={iconSize} className="text-slate-100" />;
        case 'Goat': return <Activity size={iconSize} className="text-slate-300" />;
        case 'Horse': return <Activity size={iconSize} className="text-amber-700" />;
        case 'Chicken': return <Bird size={iconSize} className="text-yellow-400" />;
        case 'Turkey': return <Bird size={iconSize} className="text-red-400" />;
        case 'Duck': return <Bird size={iconSize} className="text-blue-300" />;
        case 'Llama':
        case 'Alpaca': return <Activity size={iconSize} className="text-tan-400" />;

        // Zoo
        case 'Lion': return <LionIcon className={`text-orange-500 w-${iconSize / 4} h-${iconSize / 4}`} />;
        case 'Tiger': return <LionIcon className={`text-orange-600 w-${iconSize / 4} h-${iconSize / 4}`} />;
        case 'Elephant': return <Activity size={iconSize} className="text-gray-400" />;

        // Exotic
        case 'Lizard':
        case 'Snake':
        case 'Turtle': return <Bug size={iconSize} className="text-emerald-600" />;

        default: return <Activity size={iconSize} className="text-blue-400" />;
    }
};
