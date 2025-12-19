'use client';

/**
 * Storybook.ai - Book Preview Component
 * Shows generation progress and final download
 */

import { useEffect, useState } from 'react';
import { getBookStatus, getDownloadUrl, type BookStatus } from '@/lib/api';

interface BookPreviewProps {
    bookId: string;
}

export default function BookPreview({ bookId }: BookPreviewProps) {
    const [status, setStatus] = useState<BookStatus | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        let intervalId: NodeJS.Timeout;

        const fetchStatus = async () => {
            try {
                const bookStatus = await getBookStatus(bookId);
                setStatus(bookStatus);

                // Stop polling once completed or failed
                if (bookStatus.status === 'completed' || bookStatus.status === 'failed') {
                    clearInterval(intervalId);
                }
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to fetch status');
                clearInterval(intervalId);
            }
        };

        // Initial fetch
        fetchStatus();

        // Poll every 3 seconds
        intervalId = setInterval(fetchStatus, 3000);

        return () => clearInterval(intervalId);
    }, [bookId]);

    const handleDownload = async () => {
        try {
            const { download_url, filename } = await getDownloadUrl(bookId);

            // Open in new tab for download
            const link = document.createElement('a');
            link.href = download_url;
            link.download = filename;
            link.target = '_blank';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to download');
        }
    };

    if (error) {
        return (
            <div className="text-center p-8 bg-red-50 rounded-2xl border border-red-200">
                <div className="text-6xl mb-4">😢</div>
                <h2 className="text-xl font-bold text-red-600 mb-2">Oops!</h2>
                <p className="text-red-500">{error}</p>
            </div>
        );
    }

    if (!status) {
        return (
            <div className="text-center p-12">
                <div className="animate-spin w-12 h-12 border-4 border-purple-500 border-t-transparent rounded-full mx-auto mb-4" />
                <p className="text-gray-500">Loading...</p>
            </div>
        );
    }

    const statusIcons: Record<string, string> = {
        pending: '⏳',
        generating_story: '📝',
        generating_images: '🎨',
        creating_pdf: '📚',
        completed: '🎉',
        failed: '😢',
    };

    return (
        <div className="text-center p-8">
            {/* Status Icon */}
            <div className="text-7xl mb-6 animate-bounce">
                {statusIcons[status.status] || '⏳'}
            </div>

            {/* Progress Bar */}
            <div className="w-full bg-gray-200 rounded-full h-4 mb-4 overflow-hidden">
                <div
                    className="h-full bg-gradient-to-r from-purple-500 to-pink-500 transition-all duration-500 ease-out"
                    style={{ width: `${status.progress}%` }}
                />
            </div>

            {/* Progress Percentage */}
            <p className="text-3xl font-bold text-gray-700 mb-2">
                {status.progress}%
            </p>

            {/* Status Message */}
            <p className="text-lg text-gray-500 mb-8">
                {status.message}
            </p>

            {/* Download Button (when completed) */}
            {status.status === 'completed' && (
                <button
                    onClick={handleDownload}
                    className="
            inline-flex items-center gap-3
            px-8 py-4 rounded-2xl font-bold text-xl text-white
            bg-gradient-to-r from-green-500 to-emerald-600
            hover:from-green-600 hover:to-emerald-700
            shadow-xl hover:shadow-2xl hover:scale-[1.02]
            transition-all duration-300
          "
                >
                    <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                    </svg>
                    Download Your Book
                </button>
            )}

            {/* Retry Button (when failed) */}
            {status.status === 'failed' && (
                <a
                    href="/create"
                    className="
            inline-block
            px-8 py-4 rounded-2xl font-bold text-xl text-white
            bg-gradient-to-r from-purple-600 to-pink-600
            hover:from-purple-700 hover:to-pink-700
            shadow-xl hover:shadow-2xl
            transition-all duration-300
          "
                >
                    Try Again
                </a>
            )}
        </div>
    );
}
