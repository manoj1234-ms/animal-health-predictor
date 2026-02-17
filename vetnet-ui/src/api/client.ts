
import axios from 'axios';

const API_URL = 'http://localhost:8002';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface DeviceSummary {
    device_id: string;
    animal_id: string;
    species: 'Cattle' | 'Dog' | 'Horse' | 'Sheep' | 'Pig' | 'Goat' | 'Chicken';
    last_seen: number;
    seconds_ago: number;
    status: 'HEALTHY' | 'WARNING' | 'CRITICAL';
    temperature: number;
    heart_rate: number;
    activity: number;
    battery: number;
    alerts: string[];
}

export interface DashboardSummaryResponse {
    devices: DeviceSummary[];
    count: number;
}

export interface DiagnosisResponse {
    device_id: string;
    timestamp: number;
    ai_diagnosis: {
        predicted_disease: string;
        confidence: number;
        severity: string;
        treatment: {
            treatment_plan: string;
        };
    };
}


export interface PredictionRequest {
    Animal: string;
    Country?: string;
    State?: string;
    City?: string;
    Age: number;
    Gender: string;
    Breed?: string;
    WBC?: number;
    RBC?: number;
    Hemoglobin?: number;
    Platelets?: number;
    Glucose?: number;
    ALT?: number;
    AST?: number;
    Urea?: number;
    Creatinine?: number;
    Symptom_Fever?: number;
    Symptom_Lethargy?: number;
    Symptom_Vomiting?: number;
    Symptom_Diarrhea?: number;
    Symptom_WeightLoss?: number;
    Symptom_SkinLesion?: number;
    Symptom_Coughing?: number;
    Symptom_Lameness?: number;
}

export const fetchDashboardSummary = async (): Promise<DashboardSummaryResponse> => {
    const response = await apiClient.get('/iot/dashboard/summary');
    return response.data;
};

export const diagnoseDevice = async (deviceId: string): Promise<DiagnosisResponse> => {
    const response = await apiClient.post(`/iot/diagnose/${deviceId}`);
    return response.data;
};

export const uploadReport = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post('/upload-report', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });
    return response.data;
};

export const predictDisease = async (data: PredictionRequest) => {
    const response = await apiClient.post('/predict', data);
    return response.data;
};
