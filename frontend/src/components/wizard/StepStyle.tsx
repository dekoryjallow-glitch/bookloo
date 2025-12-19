'use client';

/**
 * Step 4: Style Selection
 */

import { useWizardStore, Style } from '@/lib/wizard-store';

const styles: { value: Style; label: string; description: string; preview: string }[] = [
    {
        value: 'watercolor',
        label: 'Aquarell',
        description: 'Weiche, traumhafte Wasserfarben',
        preview: '🎨'
    },
    {
        value: 'pixar_3d',
        label: 'Pixar 3D',
        description: 'Lebendiger 3D-Animationsstil',
        preview: '🎬'
    },
    {
        value: 'pencil',
        label: 'Buntstift',
        description: 'Klassischer, handgezeichneter Look',
        preview: '✏️'
    },
];

// Placeholder images for style preview (in production, use real previews)
const styleGradients: Record<Style, string> = {
    watercolor: 'from-blue-200 via-purple-200 to-pink-200',
    pixar_3d: 'from-orange-300 via-red-300 to-purple-300',
    pencil: 'from-amber-100 via-orange-100 to-yellow-100',
};

export default function StepStyle() {
    const { selectedStyle, setSelectedStyle, childName } = useWizardStore();

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                    Welchen Illustrationsstil magst du?
                </h3>
                <p className="text-gray-500 mb-6">
                    Wähle den Look für {childName || 'dein'} Buch
                </p>
            </div>

            {/* Style Options */}
            <div className="space-y-4">
                {styles.map((style) => (
                    <button
                        key={style.value}
                        type="button"
                        onClick={() => setSelectedStyle(style.value)}
                        className={`
              style-option w-full flex items-center gap-4 p-4 bg-white rounded-2xl border-2 text-left
              transition-all duration-300
              ${selectedStyle === style.value
                                ? 'border-[var(--color-primary)] ring-4 ring-purple-100'
                                : 'border-gray-100 hover:border-gray-200'
                            }
            `}
                    >
                        {/* Style Preview */}
                        <div className={`
              w-24 h-24 rounded-xl bg-gradient-to-br ${styleGradients[style.value]}
              flex items-center justify-center text-4xl
              shadow-inner
            `}>
                            {style.preview}
                        </div>

                        {/* Style Info */}
                        <div className="flex-1">
                            <span className="font-bold text-lg text-gray-800 block">{style.label}</span>
                            <span className="text-gray-500">{style.description}</span>
                        </div>

                        {/* Selection Indicator */}
                        <div className={`
              w-6 h-6 rounded-full border-2 flex items-center justify-center
              transition-all duration-200
              ${selectedStyle === style.value
                                ? 'border-[var(--color-primary)] bg-[var(--color-primary)]'
                                : 'border-gray-300'
                            }
            `}>
                            {selectedStyle === style.value && (
                                <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                </svg>
                            )}
                        </div>
                    </button>
                ))}
            </div>

            {/* Summary */}
            <div className="bg-[var(--color-bg-lavender)] rounded-2xl p-5 mt-8">
                <h4 className="font-semibold text-gray-700 mb-3">📖 Dein Buch wird erstellt:</h4>
                <ul className="text-sm text-gray-600 space-y-2">
                    <li>• 20 personalisierte Seiten</li>
                    <li>• Heldenreise-Struktur</li>
                    <li>• {childName || 'Dein Kind'} als Hauptfigur</li>
                    <li>• Druckfertige PDF (21×21 cm)</li>
                </ul>
            </div>
        </div>
    );
}
