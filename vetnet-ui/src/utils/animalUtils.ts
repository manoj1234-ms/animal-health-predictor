export type AnimalCategory = 'Zoo' | 'Farm' | 'Pet';

export const ZOO_SPECIES = ['Lion', 'Tiger', 'Elephant'];
export const FARM_SPECIES = ['Cattle', 'Buffalo', 'Sheep', 'Goat', 'Pig', 'Chicken', 'Horse', 'Turkey', 'Duck', 'Llama', 'Alpaca'];

export const getCategory = (species: string): AnimalCategory => {
    if (ZOO_SPECIES.includes(species)) return 'Zoo';
    if (FARM_SPECIES.includes(species)) return 'Farm';
    return 'Pet';
};

export const getHabitatName = (species: string): string => {
    const category = getCategory(species);
    switch (category) {
        case 'Zoo': return 'Exotic Safari Zone';
        case 'Farm': return 'Open Grazing Range';
        case 'Pet': return 'Medical Center';
        default: return 'Default Sector';
    }
};

export interface Specialist {
    name: string;
    clinic: string;
    phone: string;
    distance: string;
    location: string;
    rating: number;
    availability: string;
}

export const getNearbySpecialist = (category: AnimalCategory): Specialist => {
    switch (category) {
        case 'Zoo':
            return {
                name: "Dr. Selina Kyle",
                clinic: "Exotic Wildlife Sanctuary",
                phone: "+1 (555) 902-1234",
                distance: "12.4 km",
                location: "West Safari Drive, Zone 4",
                rating: 4.9,
                availability: "Available Now"
            };
        case 'Farm':
            return {
                name: "Dr. Alan Grant",
                clinic: "Central Valley Livestock Clinic",
                phone: "+1 (555) 443-8890",
                distance: "4.2 km",
                location: "North Farm Road, Unit 12",
                rating: 4.8,
                availability: "On-Call"
            };
        case 'Pet':
        default:
            return {
                name: "Dr. Ellie Sattler",
                clinic: "Metro Pet Hospital & ICU",
                phone: "+1 (555) 221-7800",
                distance: "1.8 km",
                location: "Downtown Medical Plaza",
                rating: 5.0,
                availability: "Emergency Ready"
            };
    }
};
