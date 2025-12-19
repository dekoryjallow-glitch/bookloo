'use client';

/**
 * Storybook.ai - Preview & Purchase Page
 * Shows 4 high-quality preview images before purchase
 */

import { useEffect, useState } from 'react';
import { useRouter, useParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { getBookDetails, getBookStatus, createCheckoutSession } from '@/lib/api';

interface BookData {
    id: string;
    child_name: string;
    theme: string;
    status: string;
    preview_images?: string[];
    preview_scenes?: Array<{
        scene_id: number;
        status: 'locked' | 'unlocked' | 'generating';
        image_url?: string;
        thumbnail_url?: string;
    }>;
    pdf_url?: string;
    pages?: Array<{
        page_number: number;
        text: string;
        image_url?: string;
    }>;
}

export default function PreviewPage() {
    const router = useRouter();
    const params = useParams();
    const bookId = params.id as string;

    const [book, setBook] = useState<BookData | null>(null);
    const [loading, setLoading] = useState(true);
    const [purchasing, setPurchasing] = useState(false);
    const [selectedImage, setSelectedImage] = useState<number>(0);
    const [lightboxOpen, setLightboxOpen] = useState(false);
    const [lightboxImage, setLightboxImage] = useState<string | null>(null);

    const openLightbox = (imageUrl: string) => {
        setLightboxImage(imageUrl);
        setLightboxOpen(true);
    };

    const closeLightbox = () => {
        setLightboxOpen(false);
        setLightboxImage(null);
    };

    const openModal = () => {
        const modal = document.getElementById('cta-modal') as HTMLDialogElement;
        if (modal) modal.showModal();
    };

    const closeModal = () => {
        const modal = document.getElementById('cta-modal') as HTMLDialogElement;
        if (modal) modal.close();
    };

    useEffect(() => {
        let intervalId: NodeJS.Timeout;

        const fetchBook = async () => {
            try {
                const details = await getBookDetails(bookId);
                setBook(details);

                // Keep polling if not ready or completed
                if (details.status === 'ready_for_purchase' || details.status === 'completed') {
                    // We can stop polling if it's already in a final preview state
                    // But if some images are still missing, we might want to continue.
                    // For now, let's stop only if all preview scenes are unlocked.
                    const allUnlocked = details.preview_scenes?.every(s => s.status !== 'generating') ?? true;
                    if (allUnlocked) {
                        clearInterval(intervalId);
                    }
                }
            } catch (error) {
                console.error('Error fetching book:', error);
            } finally {
                setLoading(false);
            }
        };

        if (bookId) {
            fetchBook();
            intervalId = setInterval(fetchBook, 5000); // Poll every 5s
        }

        return () => clearInterval(intervalId);
    }, [bookId]);

    const handlePurchase = async () => {
        setPurchasing(true);
        try {
            const { checkout_url } = await createCheckoutSession(bookId);
            // Hard redirect to Stripe
            window.location.href = checkout_url;
        } catch (error) {
            console.error('Error starting checkout:', error);
            alert('Fehler beim Starten der Zahlung. Bitte versuche es erneut.');
            setPurchasing(false);
        }
    };

    if (loading) {
        return (
            <main className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <div className="magic-orb w-24 h-24 mx-auto mb-6"></div>
                    <p className="text-gray-500">Lade Vorschau...</p>
                </div>
            </main>
        );
    }

    if (!book) {
        return (
            <main className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <h1 className="text-2xl font-bold text-gray-800 mb-4">Buch nicht gefunden</h1>
                    <Link href="/" className="btn-primary">
                        Zurück zur Startseite
                    </Link>
                </div>
            </main>
        );
    }

    const previewImages = book.preview_images || [];
    const hasPreviewImages = previewImages.length > 0;

    return (
        <main className="min-h-screen py-8 px-4 md:px-6 bg-[#f8f9fa]">
            <div className="max-w-6xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <Link
                        href="/"
                        className="flex items-center gap-2 text-gray-500 hover:text-gray-700 transition-colors"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        <span>Startseite</span>
                    </Link>

                    <div className="flex items-center gap-2">
                        <span className="text-2xl">📚</span>
                        <span className="font-bold gradient-text text-xl">bookloo</span>
                    </div>
                </div>

                {/* Title */}
                <div className="text-center mb-10">
                    <span className="text-5xl mb-4 block">🎉</span>
                    <h1 className="text-3xl font-bold text-gray-800 mb-2">
                        Deine Vorschau ist bereit!
                    </h1>
                    <p className="text-gray-500">
                        {book.child_name}s personalisiertes Abenteuer
                    </p>
                </div>

                {/* Main Content - Improved Gallery Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 mb-16">
                    {/* Preview Gallery (Left 3/4) */}
                    <div className="lg:col-span-3 space-y-8">
                        {/* 4 Multi-Preview Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {[0, 1, 7, 13].map((sceneId, idx) => {
                                const sceneData = book.preview_scenes?.find(s => s.scene_id === sceneId);
                                const mapIndex = [0, 1, 7, 13].indexOf(sceneId);
                                const imageUrl = sceneData?.image_url || (mapIndex !== -1 ? previewImages[mapIndex] : null);

                                return (
                                    <div key={sceneId} className="space-y-2">
                                        <div
                                            className="bg-white p-2 rounded-2xl shadow-lg border border-gray-100 hover:shadow-2xl hover:scale-[1.02] transition-all duration-300 cursor-pointer group relative"
                                            onClick={() => {
                                                if (imageUrl) openLightbox(imageUrl);
                                            }}
                                        >
                                            <div className="aspect-[3/4] rounded-xl overflow-hidden bg-gray-50 relative">
                                                {imageUrl ? (
                                                    <img
                                                        src={imageUrl}
                                                        alt={`Preview Scene ${sceneId}`}
                                                        className="w-full h-full object-cover"
                                                    />
                                                ) : (
                                                    <div className="w-full h-full flex flex-col items-center justify-center space-y-2">
                                                        <div className="w-8 h-8 rounded-full border-4 border-purple-100 border-t-purple-600 animate-spin"></div>
                                                        <p className="text-xs text-gray-400">Wird erstellt...</p>
                                                    </div>
                                                )}

                                                {/* Zoom Overlay on Hover */}
                                                {imageUrl && (
                                                    <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300 flex items-center justify-center">
                                                        <div className="w-12 h-12 rounded-full bg-white/90 shadow-lg flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300 scale-75 group-hover:scale-100">
                                                            <svg className="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0zM10 7v3m0 0v3m0-3h3m-3 0H7" />
                                                            </svg>
                                                        </div>
                                                    </div>
                                                )}

                                                {/* Badge */}
                                                <div className="absolute top-2 left-2 px-2 py-1 bg-white/95 backdrop-blur-sm rounded-full shadow-sm text-[10px] font-bold uppercase tracking-wider text-purple-600 border border-purple-100">
                                                    {sceneId === 0 ? '📕 Buch-Cover' : `📖 Seite ${sceneId * 2}`}
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                );
                            })}
                        </div>

                        {/* Story Progress Preview / More Scenes */}
                        <div className="bg-white/50 p-6 rounded-3xl border border-dashed border-gray-300">
                            <h3 className="text-sm font-bold text-gray-500 uppercase tracking-widest mb-6 text-center">Inhaltsverzeichnis - 32 Seiten Abenteuer</h3>
                            <div className="flex flex-wrap justify-center gap-4">
                                {Array.from({ length: 14 }).map((_, index) => {
                                    const isKey = [0, 1, 7, 13].includes(index);
                                    const sceneData = book.preview_scenes?.find(s => s.scene_id === index);
                                    const isLocked = sceneData ? sceneData.status === 'locked' : !isKey;

                                    return (
                                        <div key={index} className="flex flex-col items-center gap-2">
                                            <div
                                                className={`w-14 h-14 rounded-xl flex items-center justify-center text-xl shadow-sm transition-all
                                                    ${isLocked ? 'bg-gray-100 text-gray-400 border border-gray-200' : 'bg-purple-600 text-white border-2 border-white shadow-purple-200'}
                                                `}
                                            >
                                                {isLocked ? '🔒' : '✅'}
                                            </div>
                                            <span className="text-[10px] font-medium text-gray-400">P.{index * 2}</span>
                                        </div>
                                    );
                                })}
                            </div>
                        </div>
                    </div>

                    {/* Purchase Card (Right 1/3) */}
                    <div className="lg:col-span-1">
                        <div className="card-magical p-8 sticky top-8">
                            <div className="text-center mb-6">
                                <span className="text-4xl block mb-2">✨</span>
                                <h2 className="text-2xl font-bold text-gray-800">
                                    {book.child_name}s Abenteuer
                                </h2>
                            </div>

                            <div className="space-y-4 mb-8">
                                <div className="flex items-center gap-3 text-sm text-gray-600">
                                    <span className="text-xl">📖</span> 32 Seiten Hardcover
                                </div>
                                <div className="flex items-center gap-3 text-sm text-gray-600">
                                    <span className="text-xl">🎨</span> 14 Einzigartige Illustrationen
                                </div>
                                <div className="flex items-center gap-3 text-sm text-gray-600">
                                    <span className="text-xl">⚡</span> PDF Sofort-Download
                                </div>
                            </div>

                            {/* Price */}
                            <div className="text-center mb-6 bg-orange-50 p-4 rounded-xl border border-orange-100">
                                <span className="text-4xl font-bold text-orange-600">24,90 €</span>
                                <p className="text-xs text-orange-400 mt-1 uppercase tracking-wide font-bold">Limitierter Einführungspreis</p>
                            </div>

                            <button
                                onClick={handlePurchase}
                                disabled={purchasing}
                                className={`w-full btn-primary py-4 font-bold text-lg shadow-xl hover:shadow-2xl hover:scale-[1.02] active:scale-95 transition-all ${purchasing ? 'opacity-70 cursor-wait' : ''}`}
                            >
                                {purchasing ? (
                                    <span className="flex items-center gap-2">
                                        <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                                        </svg>
                                        Leite zu Stripe weiter...
                                    </span>
                                ) : (
                                    <span className="flex items-center gap-2">
                                        🔒 Jetzt freischalten für 24,90€
                                    </span>
                                )}
                            </button>

                            <p className="text-center text-xs text-gray-400 mt-4">
                                Sichere SSL-Verschlüsselung via Stripe
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* CTA Modal */}
            <dialog id="cta-modal" className="modal p-0 rounded-3xl shadow-2xl backdrop:bg-black/50">
                <div className="p-8 max-w-md bg-white text-center">
                    <div className="text-6xl mb-4">🔐</div>
                    <h3 className="text-2xl font-bold text-gray-800 mb-2">Neugierig?</h3>
                    <p className="text-gray-600 mb-6">
                        Dies ist nur eine Vorschau! Schalte jetzt das komplette Buch frei, um zu sehen, wie {book.child_name}s Reise weitergeht.
                    </p>
                    <div className="flex gap-3 justify-center">
                        <button
                            onClick={closeModal}
                            className="px-4 py-2 text-gray-500 hover:bg-gray-100 rounded-lg transition-colors"
                        >
                            Abbrechen
                        </button>
                        <button
                            onClick={() => {
                                closeModal();
                                handlePurchase();
                            }}
                            className="px-6 py-2 bg-orange-600 text-white rounded-lg font-bold hover:bg-orange-700 transition-colors"
                        >
                            Für 24,90 € Freischalten
                        </button>
                    </div>
                </div>
            </dialog>

            {/* Lightbox Modal for Full-Size Image */}
            {lightboxOpen && lightboxImage && (
                <div
                    className="fixed inset-0 z-50 bg-black/90 flex items-center justify-center p-4 animate-fadeIn"
                    onClick={closeLightbox}
                >
                    {/* Close Button */}
                    <button
                        onClick={closeLightbox}
                        className="absolute top-6 right-6 w-12 h-12 rounded-full bg-white/10 hover:bg-white/20 flex items-center justify-center transition-colors"
                    >
                        <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>

                    {/* Full Size Image */}
                    <div
                        className="max-w-4xl max-h-[90vh] rounded-2xl overflow-hidden shadow-2xl"
                        onClick={(e) => e.stopPropagation()}
                    >
                        <img
                            src={lightboxImage}
                            alt="Full size preview"
                            className="w-full h-full object-contain"
                        />
                    </div>

                    {/* Hint */}
                    <p className="absolute bottom-6 left-1/2 -translate-x-1/2 text-white/60 text-sm">
                        Klicke irgendwo, um zu schließen
                    </p>
                </div>
            )}
        </main>
    );
}
