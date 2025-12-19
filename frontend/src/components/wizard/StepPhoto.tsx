'use client';

/**
 * Step 2: Photo Upload
 */

import { useCallback, useState } from 'react';
import { useWizardStore } from '@/lib/wizard-store';
import { generateCharacterPreview } from '@/lib/api';

export default function StepPhoto() {
    const {
        childName,
        childGender,
        childPhotoPreview,
        generatedPortraitUrl,
        setChildPhoto,
        setGeneratedPortrait,
        nextStep
    } = useWizardStore();

    const [isDragging, setIsDragging] = useState(false);
    const [isGenerating, setIsGenerating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleFileSelect = useCallback(async (file: File) => {
        if (file && file.type.startsWith('image/')) {
            // Local preview first
            const reader = new FileReader();
            reader.onloadend = () => {
                setChildPhoto(file, reader.result as string);
            };
            reader.readAsDataURL(file);

            // Trigger Generation IMMEDIATELY
            setIsGenerating(true);
            setError(null);

            try {
                // Call API
                console.log("🚀 Starting magic generation...");
                const result = await generateCharacterPreview(file, childGender, childName || 'Kind');

                // Save result
                console.log("✅ Magic complete:", result);
                setGeneratedPortrait(result.generated_url, result.original_url);

            } catch (err: any) {
                console.error("Magic failed:", err);
                const msg = err?.message || JSON.stringify(err);
                if (msg.includes("500") || msg.includes("Failed")) {
                    setError("Hoppla! Unsere KI ist gerade überlastet (Model Error). Bitte versuche es noch einmal.");
                } else {
                    setError("Das hat leider nicht geklappt. Bitte versuche ein anderes Foto.");
                }
                // We allow continuing with just the photo if needed, or force retry
            } finally {
                setIsGenerating(false);
            }
        }
    }, [setChildPhoto, setGeneratedPortrait, childGender, childName]);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        if (file) handleFileSelect(file);
    }, [handleFileSelect]);

    const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) handleFileSelect(file);
    }, [handleFileSelect]);

    const handleReset = () => {
        setChildPhoto(null, null);
        setGeneratedPortrait(null, null);
        setError(null);
    };

    const handleContinue = () => {
        if (childPhotoPreview) {
            nextStep();
        }
    };

    return (
        <div className="space-y-6">
            <div>
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                    Lade ein Foto von {childName || 'deinem Kind'} hoch
                </h3>
                <p className="text-gray-500 mb-6">
                    Wir verwandeln es sofort in eine 3D-Pixar-Figur! ✨
                </p>
            </div>

            {/* ERROR STATE */}
            {error && (
                <div className="bg-red-50 text-red-600 p-4 rounded-xl text-center mb-4">
                    {error}
                    <button onClick={() => setError(null)} className="ml-2 underline">Okay</button>
                </div>
            )}

            {/* PREVIEW AREA */}
            {childPhotoPreview ? (
                <div className="relative animate-in fade-in zoom-in duration-300">

                    <div className="flex flex-col md:flex-row gap-8 justify-center items-center mb-8">

                        {/* 1. Original Photo */}
                        <div className="relative w-48 h-48 md:w-56 md:h-56 rounded-3xl overflow-hidden shadow-lg border-4 border-white bg-gray-100 opacity-80 scale-90">
                            <img
                                src={childPhotoPreview}
                                alt="Original"
                                className="w-full h-full object-cover"
                            />
                            <div className="absolute bottom-0 inset-x-0 bg-black/50 p-2 text-white text-center text-xs">
                                Original
                            </div>
                        </div>

                        {/* Arrow */}
                        <div className="text-4xl text-purple-300 animate-pulse">
                            {isGenerating ? '✨' : '➜'}
                        </div>

                        {/* 2. Generated Magic */}
                        <div className="relative w-64 h-64 md:w-72 md:h-72 rounded-3xl overflow-hidden shadow-2xl border-4 border-white bg-purple-50 ring-4 ring-purple-100">
                            {isGenerating ? (
                                <div className="absolute inset-0 flex flex-col items-center justify-center bg-white/80 backdrop-blur-sm z-10">
                                    <div className="animate-spin text-4xl mb-2">✨</div>
                                    <p className="font-bold text-purple-600 animate-pulse">Zaubere...</p>
                                </div>
                            ) : null}

                            {generatedPortraitUrl ? (
                                <img
                                    src={generatedPortraitUrl}
                                    alt="Magic Portrait"
                                    className="w-full h-full object-cover animate-in fade-in duration-700"
                                />
                            ) : (
                                <div className="w-full h-full flex items-center justify-center text-gray-300">
                                    <span className="text-6xl opacity-20">👤</span>
                                </div>
                            )}

                            {generatedPortraitUrl && (
                                <div className="absolute bottom-0 inset-x-0 bg-gradient-to-t from-purple-900/80 to-transparent p-4 text-white text-center">
                                    <span className="font-bold text-lg">Dein Charakter! ✨</span>
                                </div>
                            )}
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-col gap-3 mt-4 max-w-xs mx-auto">
                        <button
                            onClick={handleContinue}
                            disabled={isGenerating || (!generatedPortraitUrl && !error)}
                            // If generating, disable. If done, enable. If error, enable (to skip or retry).
                            className={`
                                btn-primary w-full py-4 text-lg shadow-xl shadow-purple-200 transform transition-all
                                ${isGenerating ? 'opacity-50 cursor-wait' : 'hover:scale-105'}
                            `}
                        >
                            {isGenerating ? 'Bitte warten...' : 'Gefällt mir! Weiter ➜'}
                        </button>

                        <button
                            onClick={handleReset}
                            className="text-gray-400 text-sm hover:text-gray-600 underline"
                        >
                            Anderes Foto wählen
                        </button>
                    </div>
                </div>
            ) : (
                <div
                    onDrop={handleDrop}
                    onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                    onDragLeave={() => setIsDragging(false)}
                    className={`
            upload-zone relative cursor-pointer p-12 text-center touch-none
            ${isDragging ? 'dragging' : ''}
          `}
                >
                    <input
                        type="file"
                        accept="image/*"
                        onChange={handleFileInput}
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />

                    <div className="w-20 h-20 mx-auto mb-6 rounded-full bg-gradient-to-br from-purple-400 to-pink-400 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                        <span className="text-4xl">📸</span>
                    </div>

                    <p className="text-xl font-semibold text-gray-700 mb-2">
                        Foto hierher ziehen
                    </p>
                    <p className="text-gray-500 mb-4">
                        oder <span className="text-[var(--color-primary)] font-medium">klicken</span>
                    </p>
                </div>
            )}

            {/* Tips */}
            {!childPhotoPreview && (
                <div className="bg-amber-50 rounded-2xl p-4 border border-amber-200">
                    <h4 className="font-semibold text-amber-800 mb-2">💡 Tipps für das beste Ergebnis:</h4>
                    <ul className="text-sm text-amber-700 space-y-1">
                        <li>• Gesicht gut sichtbar und frontal</li>
                        <li>• Gute Beleuchtung, keine Schatten</li>
                        <li>• Neutraler Hintergrund ist hilfreich</li>
                    </ul>
                </div>
            )}
        </div>
    );
}
