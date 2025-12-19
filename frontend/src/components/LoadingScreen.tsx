'use client';

import { useEffect, useState } from 'react';
import { BookStatus, PreviewScene } from '@/lib/api';
import { motion, AnimatePresence } from 'framer-motion';

interface LoadingScreenProps {
    status: BookStatus | null;
}

const STEPS = [
    { id: 'analyze', icon: '🧠', label: 'Analyse' },
    { id: 'story', icon: '✍️', label: 'Story' },
    { id: 'illustration', icon: '🎨', label: 'Illustration' },
    { id: 'final', icon: '✨', label: 'Finale' },
];

const FACTS = [
    "Wusstest du? Dein Buch ist ein absolutes Unikat.",
    "Die KI berechnet gerade die Position von 1.000 Sternen...",
    "Jedes Abenteuer wird passgenau für dein Kind geschrieben.",
    "Unsere Illustratoren-KI schärft gerade die Bleistifte...",
    "Gleich geht die Reise los!",
    "Fast geschafft..."
];

export default function LoadingScreen({ status }: LoadingScreenProps) {
    const [factIndex, setFactIndex] = useState(0);

    // Rotate facts
    useEffect(() => {
        const interval = setInterval(() => {
            setFactIndex((prev) => (prev + 1) % FACTS.length);
        }, 5000);
        return () => clearInterval(interval);
    }, []);

    // Calculate Active Step based on Progress/Status
    const getActiveStepIndex = () => {
        if (!status) return 0;
        const p = status.progress;
        if (p < 20) return 0; // Analyse
        if (p < 45) return 1; // Story
        if (p < 90) return 2; // Illustration
        return 3;             // Finale
    };

    const activeStepIndex = getActiveStepIndex();
    // Use raw progress or 0, clamped to 0-100
    const progress = Math.min(100, Math.max(0, status?.progress || 0));

    // Headlines mapping
    const getHeadline = () => {
        switch (activeStepIndex) {
            case 0: return "Die KI lernt deinen Charakter kennen...";
            case 1: return "Eine einzigartige Geschichte entsteht...";
            case 2: return "Die Welt wird bunt gemalt...";
            case 3: return "Wir binden das Buch...";
            default: return "Magie passiert...";
        }
    };

    // Preview Cards: 0 (Cover), 1, 7
    const previewIndices = [0, 1, 7];

    return (
        <div className="min-h-screen w-full bg-gradient-to-b from-white to-blue-50 flex items-center justify-center p-4">

            {/* Main Card */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
                className="bg-white rounded-[2rem] shadow-2xl w-full max-w-3xl p-8 md:p-12 relative overflow-hidden border border-white/60 backdrop-blur-xl"
            >

                {/* Header Section with AnimatePresence for text swap */}
                <div className="text-center mb-16 h-28">
                    <AnimatePresence mode="wait">
                        <motion.h1
                            key={activeStepIndex} // Change key when step changes
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -10 }}
                            transition={{ duration: 0.4 }}
                            className="text-3xl md:text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 mb-4"
                        >
                            {getHeadline()}
                        </motion.h1>
                    </AnimatePresence>

                    <AnimatePresence mode="wait">
                        <motion.p
                            key={factIndex}
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            transition={{ duration: 0.5 }}
                            className="text-gray-500 font-medium"
                        >
                            {FACTS[factIndex]}
                        </motion.p>
                    </AnimatePresence>
                </div>

                {/* Timeline Section */}
                <div className="relative mb-20 mx-4 md:mx-12">
                    {/* Background Line */}
                    <div className="absolute top-1/2 left-0 w-full h-1.5 bg-gray-100 -translate-y-1/2 rounded-full z-0 overflow-hidden">
                        <div className="absolute inset-0 bg-gray-200/50"></div>
                    </div>

                    {/* Active Progress Bar */}
                    <motion.div
                        className="absolute top-1/2 left-0 h-1.5 bg-gradient-to-r from-blue-500 to-purple-500 -translate-y-1/2 rounded-full z-0"
                        initial={{ width: '0%' }}
                        animate={{ width: `${progress}%` }}
                        transition={{ type: 'spring', stiffness: 50, damping: 20 }}
                    >
                        {/* Waiting Bear Mascot */}
                        {/* Position relative to the *end* of the progress bar */}
                        <div className="absolute right-0 top-1/2 -translate-y-1/2 translate-x-1/2 z-20">
                            <motion.div
                                className="relative -top-9 w-20 h-20"
                                animate={{
                                    y: [0, -8, 0],
                                    rotate: [0, -2, 2, 0]
                                }}
                                transition={{
                                    duration: 0.8,
                                    repeat: Infinity,
                                    ease: "easeInOut"
                                }}
                            >
                                <img
                                    src="/assets/mascot/bear_walking.png"
                                    alt="Loading Bear"
                                    className="w-full h-full object-contain filter drop-shadow-xl transform scale-x-[-1]"
                                />
                            </motion.div>
                        </div>
                    </motion.div>

                    {/* Steps Points */}
                    <div className="relative z-10 flex justify-between">
                        {STEPS.map((step, idx) => {
                            const isActive = idx === activeStepIndex;
                            const isCompleted = idx < activeStepIndex;

                            return (
                                <div key={step.id} className="flex flex-col items-center gap-3 relative group">
                                    <motion.div
                                        initial={false}
                                        animate={{
                                            scale: isActive ? 1.3 : 1,
                                            backgroundColor: isCompleted ? '#22c55e' : isActive ? '#ffffff' : '#f9fafb',
                                            borderColor: isCompleted ? '#22c55e' : isActive ? '#fb923c' : '#f3f4f6',
                                            color: isCompleted ? '#ffffff' : isActive ? '#000000' : '#d1d5db'
                                        }}
                                        className={`
                                            w-10 h-10 rounded-full flex items-center justify-center text-lg border-4 shadow-sm z-10
                                        `}
                                    >
                                        {isCompleted ? (
                                            <motion.span initial={{ scale: 0 }} animate={{ scale: 1 }}>✓</motion.span>
                                        ) : (
                                            <span>{step.icon}</span>
                                        )}
                                    </motion.div>

                                    <motion.span
                                        animate={{
                                            color: isActive ? '#f97316' : isCompleted ? '#16a34a' : '#9ca3af',
                                            fontWeight: isActive ? 600 : 400,
                                            y: isActive ? 0 : 0
                                        }}
                                        className="text-xs uppercase tracking-wider absolute top-12 whitespace-nowrap"
                                    >
                                        {step.label}
                                    </motion.span>
                                </div>
                            );
                        })}
                    </div>
                </div>

                {/* Magic Preview Cards */}
                <div className="grid grid-cols-3 gap-6 mt-8">
                    {previewIndices.map((sceneId, idx) => {
                        const sceneData = status?.preview_scenes?.find(s => s.scene_id === sceneId);
                        const isReady = sceneData?.image_url && sceneData.status !== 'generating'; // Use status from backend

                        return (
                            <div key={sceneId} className="relative aspect-[3/4] w-full max-w-[160px] mx-auto perspective-1000">
                                <motion.div
                                    className="w-full h-full relative preserve-3d"
                                    initial={false}
                                    animate={{ rotateY: isReady ? 180 : 0 }}
                                    transition={{ type: "spring", stiffness: 60, damping: 12 }}
                                    style={{ transformStyle: 'preserve-3d' }}
                                >
                                    {/* FRONT (Skeleton) */}
                                    <div className="absolute inset-0 backface-hidden bg-gray-50 rounded-2xl border-2 border-gray-100 overflow-hidden">
                                        <div className="absolute inset-0 shimmer opacity-60"></div>
                                        <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-300 gap-2">
                                            <span className="text-3xl opacity-50">
                                                {idx === 0 ? '📕' : '🎨'}
                                            </span>
                                            <span className="text-[10px] font-bold uppercase tracking-widest opacity-40">
                                                {idx === 0 ? 'Cover' : `Szene ${idx}`}
                                            </span>
                                        </div>
                                        <div className="absolute bottom-3 left-3 right-3 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                            <div className="h-full w-full progress-shimmer opacity-40"></div>
                                        </div>
                                    </div>

                                    {/* BACK (Image) */}
                                    <div
                                        className="absolute inset-0 backface-hidden bg-white rounded-2xl overflow-hidden shadow-lg border-4 border-white ring-1 ring-black/5"
                                        style={{ transform: 'rotateY(180deg)', backfaceVisibility: 'hidden' }}
                                    >
                                        {isReady && (
                                            <img
                                                src={sceneData?.image_url!}
                                                alt={`Preview ${sceneId}`}
                                                className="w-full h-full object-cover"
                                            />
                                        )}
                                        {/* Success Badge */}
                                        <div className="absolute bottom-0 inset-x-0 p-3 bg-gradient-to-t from-black/50 to-transparent flex justify-center">
                                            <motion.div
                                                initial={{ scale: 0 }}
                                                animate={{ scale: 1 }}
                                                transition={{ delay: 0.2 }}
                                                className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center text-white text-xs border-2 border-white shadow-sm"
                                            >
                                                ✓
                                            </motion.div>
                                        </div>
                                    </div>
                                </motion.div>
                            </div>
                        );
                    })}
                </div>

                {/* Footer Message */}
                <div className="mt-12 text-center">
                    <motion.p
                        key={status?.message}
                        initial={{ opacity: 0, y: 5 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-sm text-gray-400 font-medium"
                    >
                        {status?.message || "Lade..."}
                    </motion.p>
                </div>
            </motion.div>
        </div>
    );
}
