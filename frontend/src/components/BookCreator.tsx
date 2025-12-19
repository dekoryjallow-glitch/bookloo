'use client';

/**
 * Storybook.ai - Book Creator Component
 * Main form for creating a personalized children's book
 */

import { useState, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import ImageUpload from './ImageUpload';
import { createBook } from '@/lib/api';

const THEMES = [
    { id: 'adventure', label: '🚀 Adventure', color: 'from-orange-400 to-red-500' },
    { id: 'friendship', label: '🤝 Friendship', color: 'from-pink-400 to-purple-500' },
    { id: 'magic', label: '✨ Magic', color: 'from-purple-400 to-indigo-500' },
    { id: 'nature', label: '🌳 Nature', color: 'from-green-400 to-emerald-500' },
    { id: 'space', label: '🌌 Space', color: 'from-indigo-400 to-blue-500' },
    { id: 'underwater', label: '🐠 Underwater', color: 'from-cyan-400 to-blue-500' },
];

export default function BookCreator() {
    const router = useRouter();
    const [childName, setChildName] = useState('');
    const [selectedTheme, setSelectedTheme] = useState('adventure');
    const [customTheme, setCustomTheme] = useState('');
    const [childPhoto, setChildPhoto] = useState<File | null>(null);
    const [photoPreview, setPhotoPreview] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handlePhotoSelect = useCallback((file: File) => {
        setChildPhoto(file);
        const reader = new FileReader();
        reader.onloadend = () => {
            setPhotoPreview(reader.result as string);
        };
        reader.readAsDataURL(file);
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!childName.trim()) {
            setError('Please enter your child\'s name');
            return;
        }

        setIsLoading(true);
        setError(null);

        try {
            const result = await createBook(
                childName,
                selectedTheme,
                childPhoto || undefined,
                selectedTheme === 'custom' ? customTheme : undefined,
            );

            // Redirect to book status page
            router.push(`/book/${result.id}`);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Something went wrong');
            setIsLoading(false);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="space-y-8">
            {/* Child's Name */}
            <div>
                <label htmlFor="childName" className="block text-lg font-semibold text-gray-700 mb-2">
                    What's your child's name?
                </label>
                <input
                    type="text"
                    id="childName"
                    value={childName}
                    onChange={(e) => setChildName(e.target.value)}
                    placeholder="Enter name..."
                    className="w-full px-6 py-4 text-xl border-2 border-gray-200 rounded-2xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all outline-none"
                />
            </div>

            {/* Photo Upload */}
            <div>
                <label className="block text-lg font-semibold text-gray-700 mb-2">
                    Upload a photo (optional)
                </label>
                <ImageUpload
                    onFileSelect={handlePhotoSelect}
                    preview={photoPreview || undefined}
                    className="h-64"
                />
            </div>

            {/* Theme Selection */}
            <div>
                <label className="block text-lg font-semibold text-gray-700 mb-4">
                    Choose a story theme
                </label>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                    {THEMES.map((theme) => (
                        <button
                            key={theme.id}
                            type="button"
                            onClick={() => setSelectedTheme(theme.id)}
                            className={`
                relative p-4 rounded-2xl border-2 transition-all duration-300
                ${selectedTheme === theme.id
                                    ? 'border-purple-500 ring-4 ring-purple-100 scale-[1.02]'
                                    : 'border-gray-200 hover:border-purple-300'
                                }
              `}
                        >
                            <div className={`h-12 rounded-xl bg-gradient-to-br ${theme.color} mb-3`} />
                            <span className="font-semibold text-gray-700">{theme.label}</span>

                            {selectedTheme === theme.id && (
                                <div className="absolute top-2 right-2 w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center">
                                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                </div>
                            )}
                        </button>
                    ))}
                </div>
            </div>

            {/* Error Message */}
            {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-600">
                    {error}
                </div>
            )}

            {/* Submit Button */}
            <button
                type="submit"
                disabled={isLoading}
                className={`
          w-full py-5 rounded-2xl font-bold text-xl text-white
          bg-gradient-to-r from-purple-600 to-pink-600
          hover:from-purple-700 hover:to-pink-700
          focus:ring-4 focus:ring-purple-200
          transition-all duration-300
          disabled:opacity-50 disabled:cursor-not-allowed
          shadow-xl hover:shadow-2xl hover:scale-[1.02]
        `}
            >
                {isLoading ? (
                    <span className="flex items-center justify-center gap-3">
                        <svg className="animate-spin h-6 w-6" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                        </svg>
                        Creating Magic...
                    </span>
                ) : (
                    '✨ Create My Book'
                )}
            </button>
        </form>
    );
}
