'use client';

/**
 * Storybook.ai - Magic Page
 * Shows generation progress with live updates and preview images
 */

import { useEffect, useState, use } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { getBookStatus, approveCharacter, regenerateCharacter, type BookStatus } from '@/lib/api';
import LoadingScreen from '@/components/LoadingScreen';

interface MagicPageProps {
    params: Promise<{ id: string }>;
}

const stages = [
    { key: 'pending', label: 'Bereite Magie vor...', emoji: '⏳' },
    { key: 'creating_character', label: 'Zaubere Charakter...', emoji: '✨' },
    { key: 'waiting_for_approval', label: 'Character Sheet bereit!', emoji: '👀' },
    { key: 'generating_preview', label: 'Erstelle Vorschau...', emoji: '🎨' },
    { key: 'ready_for_purchase', label: 'Vorschau bereit!', emoji: '🔓' },
    { key: 'paid_processing_full', label: 'Erstelle Buch...', emoji: '📖' },
    { key: 'completed', label: 'Fertig!', emoji: '🎉' },
];

const magicFacts = [
    "Wusstest du? Jede Geschichte ist einzigartig! 📖",
    "Die KI malt gerade wunderschöne Bilder... 🎨",
    "Dein Kind wird der Star dieser Geschichte! ⭐",
    "20 Seiten voller Abenteuer entstehen... 🚀",
    "Die beste Gute-Nacht-Geschichte wartet! 🌙",
    "Magie braucht einen Moment... ✨",
];

export default function MagicPage({ params }: MagicPageProps) {
    const { id } = use(params);
    const router = useRouter();
    const [status, setStatus] = useState<BookStatus | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [factIndex, setFactIndex] = useState(0);
    const [isApproving, setIsApproving] = useState(false);

    // Poll for status updates
    useEffect(() => {
        let intervalId: NodeJS.Timeout;

        const fetchStatus = async () => {
            try {
                const bookStatus = await getBookStatus(id);
                setStatus(bookStatus);

                // Redirect logic
                if (bookStatus.status === 'ready_for_purchase' || bookStatus.status === 'completed') {
                    clearInterval(intervalId);
                    // Redirect to preview page after short delay
                    setTimeout(() => {
                        router.push(`/preview/${id}`);
                    }, 1500);
                } else if (bookStatus.status === 'failed') {
                    clearInterval(intervalId);
                    setError('Etwas ist schiefgelaufen. Bitte versuche es erneut.');
                }
            } catch (err) {
                console.error("Status poll failed", err);
            }
        };

        fetchStatus();
        intervalId = setInterval(fetchStatus, 3000); // Polling every 3s

        return () => clearInterval(intervalId);
    }, [id, router]);

    // Rotate fun facts
    useEffect(() => {
        const factInterval = setInterval(() => {
            setFactIndex((prev) => (prev + 1) % magicFacts.length);
        }, 4000);

        return () => clearInterval(factInterval);
    }, []);

    const handleApprove = async () => {
        setIsApproving(true);
        try {
            await approveCharacter(id);
            // Status update will be caught by next poll
        } catch (e) {
            alert("Fehler beim Bestätigen. Bitte versuche es erneut.");
            setIsApproving(false);
        }
    };

    const handleRegenerate = async () => {
        if (!confirm("Bist du sicher? Das aktuelle Character Sheet wird gelöscht.")) return;
        setIsApproving(true);
        try {
            await regenerateCharacter(id);
            setIsApproving(false);
        } catch (e) {
            alert("Fehler beim Neustart.");
            setIsApproving(false);
        }
    };

    const getCurrentStageIndex = () => {
        if (!status) return 0;
        const idx = stages.findIndex(s => s.key === status.status);
        return idx >= 0 ? idx : 0;
    };

    if (error) {
        return (
            <main className="min-h-screen flex items-center justify-center px-4">
                <div className="card-magical p-10 text-center max-w-md">
                    <span className="text-6xl block mb-6">😢</span>
                    <h1 className="text-2xl font-bold text-gray-800 mb-4">Hoopla!</h1>
                    <p className="text-gray-600 mb-6">{error}</p>
                    <Link href="/create" className="btn-primary inline-block">
                        Nochmal versuchen
                    </Link>
                </div>
            </main>
        );
    }

    // === REVIEW STATE ===
    // Priority: character_image_url > preview_images
    const characterUrl = status?.character_image_url || (status?.preview_images && status.preview_images.length > 0 ? status.preview_images[0] : null);

    if (status?.status === 'waiting_for_approval' && characterUrl) {
        return (
            <main className="min-h-screen flex flex-col items-center justify-center px-4 py-8 bg-purple-50">
                <div className="max-w-4xl w-full">
                    <div className="text-center mb-8">
                        <span className="text-5xl block mb-4">👀</span>
                        <h1 className="text-3xl font-bold text-gray-800 mb-2">
                            Das ist dein Charakter!
                        </h1>
                        <p className="text-gray-600">
                            Hier ist das generierte Character Sheet. Gefällt es dir?
                            <br />Es wird die Basis für alle Szenen im Buch sein.
                        </p>
                    </div>

                    {/* Character Master Portrait */}
                    <div className="flex justify-center mb-12">
                        <div className="w-full max-w-sm aspect-[3/4] bg-white rounded-[2.5rem] shadow-2xl overflow-hidden border-4 border-white ring-1 ring-purple-100 group relative perspective-1000">
                            <img
                                src={characterUrl}
                                alt="Dein bookloo Charakter"
                                className="w-full h-full object-cover transform-gpu group-hover:scale-105 transition-transform duration-700"
                            />

                            <div className="absolute inset-0 bg-gradient-to-tr from-transparent via-white/5 to-transparent pointer-events-none"></div>

                            <div className="absolute bottom-6 left-1/2 -translate-x-1/2 px-4 py-2 bg-white/80 backdrop-blur-md rounded-full shadow-lg border border-white/50">
                                <span className="text-sm font-bold text-slate-800 uppercase tracking-widest">Master Portrait</span>
                            </div>
                        </div>
                    </div>

                    {/* Actions */}
                    <div className="flex flex-col md:flex-row justify-center gap-6">
                        <button
                            onClick={handleRegenerate}
                            disabled={isApproving}
                            className="btn-secondary group/reg"
                        >
                            <span className="group-hover/reg:rotate-180 transition-transform duration-500">🔄</span>
                            <span>Neu generieren</span>
                        </button>

                        <button
                            onClick={handleApprove}
                            disabled={isApproving}
                            className={`btn-success text-xl px-12 py-5 group/success ${isApproving ? 'opacity-70 cursor-wait' : ''}`}
                        >
                            {isApproving ? (
                                <>⏳ Verarbeite...</>
                            ) : (
                                <>
                                    <span className="scale-110 group-hover/success:animate-bounce">👍</span>
                                    <span>Sieht super aus - Buch erstellen!</span>
                                </>
                            )}
                        </button>
                    </div>
                </div>
            </main>
        );
    }

    // === LOADING STATE ===
    return (
        <LoadingScreen status={status} />
    );
}
