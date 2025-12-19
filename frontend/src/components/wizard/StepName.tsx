'use client';

/**
 * Step 1: Name & Gender
 */

import { useWizardStore, Gender } from '@/lib/wizard-store';

const genderOptions: { value: Gender; label: string; emoji: string }[] = [
    { value: 'boy', label: 'Junge', emoji: '👦' },
    { value: 'girl', label: 'Mädchen', emoji: '👧' },
    { value: 'neutral', label: 'Neutral', emoji: '🧒' },
];

const ageOptions = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

export default function StepName() {
    const {
        childName,
        setChildName,
        childGender,
        setChildGender,
    } = useWizardStore();

    return (
        <div className="space-y-8">
            {/* Name Input */}
            <div>
                <label htmlFor="childName" className="block text-lg font-semibold text-gray-700 mb-3">
                    Wie heißt dein Kind?
                </label>
                <input
                    type="text"
                    id="childName"
                    value={childName}
                    onChange={(e) => setChildName(e.target.value)}
                    placeholder="z.B. Emma, Max, Luna..."
                    className="w-full px-6 py-4 text-xl border-2 border-gray-200 rounded-2xl 
            focus:border-[var(--color-primary)] focus:ring-4 focus:ring-purple-100 
            transition-all outline-none bg-white"
                    autoFocus
                    suppressHydrationWarning
                />
                <p className="mt-2 text-sm text-gray-500">
                    Dieser Name wird der Held/die Heldin der Geschichte sein.
                </p>
            </div>

            {/* Gender Selection */}
            <div>
                <label className="block text-lg font-semibold text-gray-700 mb-3">
                    Geschlecht des Kindes
                </label>
                <div className="grid grid-cols-3 gap-4">
                    {genderOptions.map((option) => (
                        <button
                            key={option.value}
                            type="button"
                            onClick={() => setChildGender(option.value)}
                            className={`
                p-4 rounded-2xl border-2 transition-all duration-300 text-center
                ${childGender === option.value
                                    ? 'border-[var(--color-primary)] bg-[var(--color-bg-lavender)] shadow-lg scale-[1.02]'
                                    : 'border-gray-200 bg-white hover:border-purple-200 hover:bg-purple-50/50'
                                }
              `}
                        >
                            <span className="text-4xl block mb-2">{option.emoji}</span>
                            <span className="font-medium text-gray-700">{option.label}</span>
                        </button>
                    ))}
                </div>
            </div>

            {/* Age Selection Removed - Optimized Flow */}
        </div>
    );
}
