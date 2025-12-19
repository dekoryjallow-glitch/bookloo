'use client';

/**
 * Storybook.ai - Dashboard Page
 * Shows list of books and progress for paid books.
 */

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import confetti from 'canvas-confetti';
import { getMyBooks, getBookStatus, BookDetails } from '@/lib/api';

function DashboardContent() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const paymentSuccess = searchParams.get('payment_success') === 'true';
    const highlightBookId = searchParams.get('book_id');

    const [books, setBooks] = useState<BookDetails[]>([]);
    const [loading, setLoading] = useState(true);
    const [userId, setUserId] = useState<string | null>(null);

    // Initial load
    useEffect(() => {
        // Simple mock user_id or get from local storage if implemented
        const storedUserId = localStorage.getItem('bookloo_user_id') || 'demo-user';
        setUserId(storedUserId);

        const fetchBooks = async () => {
            try {
                const data = await getMyBooks(storedUserId);
                setBooks(data);
            } catch (error) {
                console.error('Error fetching books:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchBooks();

        // Confetti if just paid
        if (paymentSuccess) {
            confetti({
                particleCount: 150,
                spread: 70,
                origin: { y: 0.6 },
                colors: ['#6C5CE7', '#FF7675', '#FDCB6E', '#00CEC9']
            });

            // Clean URL after 5 seconds
            const timer = setTimeout(() => {
                router.replace('/dashboard');
            }, 5000);
            return () => clearTimeout(timer);
        }
    }, [paymentSuccess, router]);

    // Polling for processing books
    useEffect(() => {
        const processingBooks = books.filter(b =>
            b.status === 'paid_processing_full' || b.status === 'generating_preview' || b.status === 'creating_character'
        );

        if (processingBooks.length === 0) return;

        const interval = setInterval(async () => {
            const updatedBooks = await Promise.all(books.map(async (book) => {
                if (book.status === 'paid_processing_full' || book.status === 'generating_preview' || book.status === 'creating_character') {
                    try {
                        const status = await getBookStatus(book.id);
                        return { ...book, status: status.status, progress: status.progress, message: status.message };
                    } catch (e) {
                        return book;
                    }
                }
                return book;
            }));

            // Only update if something changed
            if (JSON.stringify(updatedBooks) !== JSON.stringify(books)) {
                setBooks(updatedBooks);
            }
        }, 3000);

        return () => clearInterval(interval);
    }, [books]);

    if (loading) {
        return (
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
                <div className="magic-orb w-16 h-16 mb-4"></div>
                <p className="text-gray-500 font-medium">Lade deine Abenteuer...</p>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto py-12 px-6">
            <header className="flex justify-between items-center mb-12">
                <div>
                    <h1 className="text-4xl font-black text-gray-900 mb-2">Meine Bücher</h1>
                    <p className="text-gray-500 font-medium">Alle deine magischen Geschichten an einem Ort.</p>
                </div>
                <Link href="/create" className="btn-primary px-8 py-3">
                    + Neues Buch
                </Link>
            </header>

            {books.length === 0 ? (
                <div className="text-center py-20 bg-white rounded-[3rem] border border-dashed border-gray-200">
                    <span className="text-6xl block mb-6">🏜️</span>
                    <h3 className="text-xl font-bold text-gray-800 mb-2">Noch keine Bücher</h3>
                    <p className="text-gray-500 mb-8 max-w-sm mx-auto">
                        Dein erstes Abenteuer wartet schon! Erstelle jetzt eine personalisierte Geschichte.
                    </p>
                    <Link href="/create" className="btn-primary">
                        Jetzt loslegen
                    </Link>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {books.map((book) => (
                        <div key={book.id} className={`card-magical p-6 flex flex-col h-full transition-all duration-500 ${highlightBookId === book.id && paymentSuccess ? 'ring-4 ring-purple-400 scale-[1.02]' : ''}`}>
                            {/* Book Preview Image */}
                            <div className="aspect-[4/5] rounded-2xl bg-gray-50 mb-6 overflow-hidden relative group">
                                {book.preview_images && book.preview_images.length > 0 ? (
                                    <img
                                        src={book.preview_images[0]}
                                        alt={book.child_name}
                                        className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                                    />
                                ) : (
                                    <div className="w-full h-full flex items-center justify-center text-gray-300">
                                        <span className="text-5xl">📖</span>
                                    </div>
                                )}

                                {/* Status Badge */}
                                <div className="absolute top-4 left-4">
                                    <StatusBadge status={book.status} />
                                </div>
                            </div>

                            <div className="flex-1">
                                <h3 className="text-xl font-black text-gray-900 mb-1">{book.child_name}s Abenteuer</h3>
                                <p className="text-sm text-gray-400 font-bold uppercase tracking-widest mb-4">Thema: {book.theme}</p>

                                {book.status === 'paid_processing_full' ? (
                                    <div className="bg-purple-50 p-4 rounded-2xl border border-purple-100 mb-4 animate-pulse">
                                        <div className="flex items-center gap-3 mb-2">
                                            <span className="text-xl">🛠️</span>
                                            <span className="text-sm font-bold text-purple-700">Wird vollendet...</span>
                                        </div>
                                        <div className="w-full bg-purple-100 h-2 rounded-full overflow-hidden">
                                            <div
                                                className="bg-purple-600 h-full transition-all duration-500"
                                                style={{ width: `${book.progress || 10}%` }}
                                            ></div>
                                        </div>
                                        <p className="text-[10px] text-purple-400 mt-2 font-bold uppercase tracking-tight">
                                            Dauert ca. 2-3 Min • Wir mailen dir!
                                        </p>
                                    </div>
                                ) : book.status === 'completed' ? (
                                    <div className="flex gap-2 mt-auto">
                                        <Link
                                            href={`/book/${book.id}`}
                                            className="flex-1 bg-gray-900 text-white text-center py-3 rounded-xl font-bold hover:bg-black transition-colors"
                                        >
                                            Ansehen
                                        </Link>
                                        <a
                                            href={book.pdf_url}
                                            download
                                            className="w-12 h-12 flex items-center justify-center bg-purple-50 text-purple-600 rounded-xl hover:bg-purple-100 transition-colors"
                                        >
                                            📥
                                        </a>
                                    </div>
                                ) : book.status === 'ready_for_purchase' ? (
                                    <Link
                                        href={`/preview/${book.id}`}
                                        className="block w-full btn-primary py-3 text-center"
                                    >
                                        Freischalten (24,90€)
                                    </Link>
                                ) : (
                                    <Link
                                        href={`/preview/${book.id}`}
                                        className="block w-full bg-gray-100 text-gray-500 py-3 text-center rounded-xl font-bold hover:bg-gray-200 transition-colors"
                                    >
                                        Status prüfen
                                    </Link>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}

function StatusBadge({ status }: { status: string }) {
    const map: Record<string, { label: string, color: string }> = {
        'completed': { label: 'Fertig', color: 'bg-emerald-100 text-emerald-700' },
        'paid_processing_full': { label: 'Wird erstellt', color: 'bg-purple-100 text-purple-700' },
        'ready_for_purchase': { label: 'Bereit', color: 'bg-orange-100 text-orange-700' },
        'waiting_for_approval': { label: 'Prüfen', color: 'bg-blue-100 text-blue-700' },
        'failed': { label: 'Fehler', color: 'bg-red-100 text-red-700' },
    };

    const config = map[status] || { label: status, color: 'bg-gray-100 text-gray-700' };

    return (
        <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase tracking-wider ${config.color} shadow-sm border border-white/50 backdrop-blur-sm`}>
            {config.label}
        </span>
    );
}

export default function DashboardPage() {
    return (
        <main className="min-h-screen bg-[#FAFAFA]">
            <Suspense fallback={
                <div className="flex flex-col items-center justify-center min-h-screen">
                    <div className="magic-orb w-16 h-16 mb-4"></div>
                    <p className="text-gray-500 font-medium">Lade Dashboard...</p>
                </div>
            }>
                <DashboardContent />
            </Suspense>
        </main>
    );
}
