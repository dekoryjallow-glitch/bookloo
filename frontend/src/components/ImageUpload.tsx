'use client';

/**
 * Storybook.ai - Image Upload Component
 * Drag & drop or click to upload child's photo
 */

import { useCallback, useState } from 'react';

interface ImageUploadProps {
    onFileSelect: (file: File) => void;
    preview?: string;
    className?: string;
}

export default function ImageUpload({ onFileSelect, preview, className = '' }: ImageUploadProps) {
    const [isDragging, setIsDragging] = useState(false);

    const handleDrop = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            onFileSelect(file);
        }
    }, [onFileSelect]);

    const handleDragOver = useCallback((e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    }, []);

    const handleDragLeave = useCallback(() => {
        setIsDragging(false);
    }, []);

    const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            onFileSelect(file);
        }
    }, [onFileSelect]);

    return (
        <div
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            className={`
        relative group cursor-pointer
        border-2 border-dashed rounded-2xl
        transition-all duration-300 ease-out
        ${isDragging
                    ? 'border-purple-500 bg-purple-50 scale-[1.02]'
                    : 'border-gray-300 hover:border-purple-400 hover:bg-purple-50/50'
                }
        ${className}
      `}
        >
            <input
                type="file"
                accept="image/*"
                onChange={handleFileInput}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />

            {preview ? (
                <div className="relative w-full h-full">
                    <img
                        src={preview}
                        alt="Child preview"
                        className="w-full h-full object-cover rounded-xl"
                    />
                    <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center rounded-xl">
                        <span className="text-white font-medium">Change Photo</span>
                    </div>
                </div>
            ) : (
                <div className="flex flex-col items-center justify-center p-8 text-center">
                    {/* Upload Icon */}
                    <div className="w-16 h-16 mb-4 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform">
                        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                    </div>

                    <p className="text-lg font-semibold text-gray-700 mb-1">
                        Upload a Photo
                    </p>
                    <p className="text-sm text-gray-500">
                        Drag & drop or click to browse
                    </p>
                    <p className="text-xs text-gray-400 mt-2">
                        JPG, PNG, or WebP (max 10MB)
                    </p>
                </div>
            )}
        </div>
    );
}
