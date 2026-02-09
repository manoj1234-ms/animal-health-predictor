import React, { createContext, useContext, useEffect, useState } from 'react';

type Theme = 'light' | 'dark' | 'system';
type Language = 'English (US)' | 'Spanish' | 'French';
type Timezone = 'UTC' | 'EST' | 'PST';

interface SettingsContextType {
    theme: Theme;
    setTheme: (theme: Theme) => void;
    language: Language;
    setLanguage: (lang: Language) => void;
    timezone: Timezone;
    setTimezone: (tz: Timezone) => void;
    t: (key: string) => string;
}

const translations: Record<Language, Record<string, string>> = {
    'English (US)': {
        'dashboard': 'Herd Dashboard',
        'diagnostics': 'AI Diagnosis',
        'telemetry': 'Live Telemetry',
        'map': 'Map View',
        'reports': 'Precinct Reports',
        'settings': 'Settings',
        'critical': 'CRITICAL',
        'warning': 'WARNING',
        'healthy': 'HEALTHY'
    },
    'Spanish': {
        'dashboard': 'Panel de Control',
        'diagnostics': 'Diagnóstico IA',
        'telemetry': 'Telemetría',
        'map': 'Mapa',
        'reports': 'Informes',
        'settings': 'Ajustes',
        'critical': 'CRÍTICO',
        'warning': 'ADVERTENCIA',
        'healthy': 'SALUDABLE'
    },
    'French': {
        'dashboard': 'Tableau de Bord',
        'diagnostics': 'Diagnostic IA',
        'telemetry': 'Télémétrie',
        'map': 'Carte',
        'reports': 'Rapports',
        'settings': 'Paramètres',
        'critical': 'CRITIQUE',
        'warning': 'AVERTISSEMENT',
        'healthy': 'SAIN'
    }
};

const SettingsContext = createContext<SettingsContextType | undefined>(undefined);

export const SettingsProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [theme, setTheme] = useState<Theme>(() => (localStorage.getItem('vetnet-theme') as Theme) || 'dark');
    const [language, setLanguage] = useState<Language>(() => (localStorage.getItem('vetnet-lang') as Language) || 'English (US)');
    const [timezone, setTimezone] = useState<Timezone>(() => (localStorage.getItem('vetnet-tz') as Timezone) || 'UTC');

    const t = (key: string) => {
        return translations[language][key] || key;
    };

    useEffect(() => {
        localStorage.setItem('vetnet-theme', theme);
        applyTheme(theme);
    }, [theme]);

    useEffect(() => {
        localStorage.setItem('vetnet-lang', language);
    }, [language]);

    useEffect(() => {
        localStorage.setItem('vetnet-tz', timezone);
    }, [timezone]);

    const applyTheme = (selectedTheme: Theme) => {
        const root = window.document.documentElement;
        root.classList.remove('light', 'dark');

        let effectiveTheme = selectedTheme;
        if (selectedTheme === 'system') {
            effectiveTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }

        root.classList.add(effectiveTheme);

        // Update meta theme color if needed
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', effectiveTheme === 'dark' ? '#0b0c15' : '#ffffff');
        }
    };

    // Listen for system theme changes
    useEffect(() => {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        const handleChange = () => {
            if (theme === 'system') {
                applyTheme('system');
            }
        };

        mediaQuery.addEventListener('change', handleChange);
        return () => mediaQuery.removeEventListener('change', handleChange);
    }, [theme]);

    return (
        <SettingsContext.Provider value={{ theme, setTheme, language, setLanguage, timezone, setTimezone, t }}>
            {children}
        </SettingsContext.Provider>
    );
};

export const useSettings = () => {
    const context = useContext(SettingsContext);
    if (!context) {
        throw new Error('useSettings must be used within a SettingsProvider');
    }
    return context;
};
