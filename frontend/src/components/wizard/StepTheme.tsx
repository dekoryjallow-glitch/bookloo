'use client';

/**
 * Step 3: Theme Selection
 */

import { useWizardStore, Theme } from '@/lib/wizard-store';

const themes: { value: Theme; label: string; emoji: string; description: string; color: string }[] = [
    {
        value: 'space',
        label: 'Weltraum Mission',
        emoji: '🚀',
        description: 'Abenteuer zwischen den Sternen',
        color: 'from-indigo-400 to-purple-600'
    },
    {
        value: 'dinos',
        label: 'Dino-Forscher',
        emoji: '🦕',
        description: 'Abenteuer im Dschungel',
        color: 'from-green-400 to-emerald-600'
    },
    {
        value: 'pirates',
        label: 'Piraten-Schatzsuche',
        emoji: '🏴‍☠️',
        description: 'Inseln & Schiffe',
        color: 'from-amber-400 to-orange-600'
    },
    {
        value: 'princess',
        label: 'Prinzessin / Königreich',
        emoji: '👸',
        description: 'Schloss & Magie',
        color: 'from-pink-400 to-rose-500'
    },
    {
        value: 'magic',
        label: 'Zauberwald & Feen',
        emoji: '🧚',
        description: 'Tiere & Glitzer',
        color: 'from-violet-400 to-purple-600'
    },
    {
        value: 'underwater',
        label: 'Meerjungfrau / Unterwasserzauber',
        emoji: '🧜‍♀️',
        description: 'Korallenriff & Delfine',
        color: 'from-cyan-400 to-blue-600'
    },
];

export default function StepTheme() {
    const {
        selectedTheme,
        setSelectedTheme,
        customTheme,
        setCustomTheme,
        childName
    } = useWizardStore();

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                    Welches Abenteuer soll {childName || 'dein Kind'} erleben?
                </h3>
                <p className="text-gray-500 mb-6">
                    Wähle ein Thema für die Geschichte
                </p>
            </div>

            {/* Theme Grid */}
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {themes.map((theme) => (
                    <button
                        key={theme.value}
                        type="button"
                        onClick={() => setSelectedTheme(theme.value)}
                        className={`
              theme-card relative overflow-hidden
              ${selectedTheme === theme.value ? 'selected' : ''}
            `}
                    >
                        <div className={`
              absolute inset-0 bg-gradient-to-br ${theme.color} opacity-10
            `} />

                        <div className="relative z-10">
                            <span className="text-4xl block mb-3">{theme.emoji}</span>
                            <span className="font-bold text-gray-800 block">{theme.label}</span>
                            <span className="text-sm text-gray-500">{theme.description}</span>
                        </div>

                        {selectedTheme === theme.value && (
                            <div className="absolute top-3 right-3 w-6 h-6 bg-[var(--color-primary)] rounded-full flex items-center justify-center">
                                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                            </div>
                        )}
                    </button>
                ))}
            </div>

        </div>
    );
}
