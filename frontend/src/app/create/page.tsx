'use client';

/**
 * Storybook.ai - Creator Wizard Page
 * Step-by-step book creation flow
 */

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useWizardStore } from '@/lib/wizard-store';
import { initBook, uploadImage } from '@/lib/api';

import StepName from '@/components/wizard/StepName';
import StepPhoto from '@/components/wizard/StepPhoto';
import StepTheme from '@/components/wizard/StepTheme';
// import StepStyle from '@/components/wizard/StepStyle'; // Removed to simplify to Pixar style only

const steps = [
    { id: 1, title: 'Name', icon: '👶' },
    { id: 2, title: 'Foto', icon: '📸' },
    { id: 3, title: 'Thema', icon: '🚀' },
];

export default function CreatePage() {
    const router = useRouter();
    const {
        currentStep,
        nextStep,
        prevStep,
        isStepValid,
        childName,
        childPhotoFile,
        generatedPortraitUrl, // Get from store
        selectedTheme,
        customTheme,
        selectedStyle,
        userId,
        setBookId,
        reset,
    } = useWizardStore();

    // Reset wizard when page loads (fresh start)
    useEffect(() => {
        reset();
    }, [reset]);

    const [isSubmitting, setIsSubmitting] = useState(false);
    const [uploadProgress, setUploadProgress] = useState(0);

    const handleNext = async () => {
        if (currentStep === steps.length) {
            // Final step - create the book
            setIsSubmitting(true);
            try {
                // 1. Upload Photo if exists
                let photoUrl = "";
                if (childPhotoFile) {
                    console.log("📤 Uploading photo...");
                    setUploadProgress(10);
                    photoUrl = await uploadImage(childPhotoFile);
                    setUploadProgress(40);
                    console.log("✅ Upload complete:", photoUrl);
                } else {
                    // Ideally we require a photo, but handle edge case
                    console.warn("⚠️ No photo file in store!");
                }

                const theme = selectedTheme === 'custom' ? customTheme : selectedTheme;
                const style = 'pixar_3d';

                console.log('🎬 Initializing book with:', { childName, theme, style, userId });
                setUploadProgress(50);

                // 2. Init Book
                const result = await initBook({
                    child_name: childName,
                    theme: theme,
                    child_photo_url: photoUrl,
                    approved_character_url: generatedPortraitUrl || undefined, // Pass if available
                    user_id: userId,
                    style: style,
                    custom_theme: selectedTheme === 'custom' ? customTheme : undefined,
                });

                setUploadProgress(100);
                setBookId(result.id);

                // 3. Redirect
                router.push(`/magic/${result.id}`);

            } catch (error) {
                console.error('Error creating book:', error);
                alert('Fehler beim Erstellen des Buches. Bitte versuche es erneut.');
                setIsSubmitting(false);
                setUploadProgress(0);
            }
        } else {
            nextStep();
        }
    };

    const renderStep = () => {
        switch (currentStep) {
            case 1: return <StepName />;
            case 2: return <StepPhoto />;
            case 3: return <StepTheme />;
            default: return <StepName />;
        }
    };

    return (
        <main className="min-h-screen py-8 px-4 md:px-6">
            <div className="max-w-2xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <Link
                        href="/"
                        className="flex items-center gap-2 text-gray-500 hover:text-gray-700 transition-colors"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        <span>Zurück</span>
                    </Link>

                    <div className="flex items-center gap-2">
                        <span className="text-2xl">📚</span>
                        <span className="font-bold gradient-text text-xl">bookloo</span>
                    </div>
                </div>

                {/* Progress Steps */}
                <div className="flex justify-center gap-3 mb-10">
                    {steps.map((step) => (
                        <div
                            key={step.id}
                            className="flex items-center gap-2"
                        >
                            <div className={`
                step-dot
                ${currentStep === step.id ? 'active' : ''}
                ${currentStep > step.id ? 'completed' : ''}
              `} />
                            {step.id < steps.length && (
                                <div className={`
                  w-8 h-0.5 
                  ${currentStep > step.id ? 'bg-[var(--color-accent)]' : 'bg-gray-200'}
                `} />
                            )}
                        </div>
                    ))}
                </div>

                {/* Step Header */}
                <div className="text-center mb-8">
                    <span className="text-5xl mb-4 block">{steps[currentStep - 1].icon}</span>
                    <h1 className="text-2xl font-bold text-gray-800">
                        Schritt {currentStep}: {steps[currentStep - 1].title}
                    </h1>
                </div>

                {/* Step Content */}
                <div className="card-magical p-8 mb-8">
                    {renderStep()}
                </div>

                {/* Navigation Buttons - Hide on Step 2 (Photo) as it has internal navigation */}
                {currentStep !== 2 && (
                    <div className="flex justify-between gap-4">
                        {currentStep > 1 ? (
                            <button
                                onClick={prevStep}
                                disabled={isSubmitting}
                                className="btn-secondary group/nav"
                            >
                                <svg className="w-5 h-5 transition-transform duration-300 group-hover/nav:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M15 19l-7-7 7-7" />
                                </svg>
                                <span>Zurück</span>
                            </button>
                        ) : (
                            <div />
                        )}

                        <button
                            onClick={handleNext}
                            disabled={!isStepValid(currentStep) || isSubmitting}
                            className={`
                                btn-primary group/nav
                                ${(!isStepValid(currentStep) || isSubmitting) ? 'opacity-50 cursor-not-allowed !shadow-none' : ''}
                            `}
                        >
                            {currentStep === steps.length ? (
                                <>
                                    {isSubmitting ? (
                                        <span>⏳ Generiere...</span>
                                    ) : (
                                        <>
                                            <span>✨ Magie starten</span>
                                            <svg className="w-5 h-5 transition-transform duration-300 group-hover/nav:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                            </svg>
                                        </>
                                    )}
                                </>
                            ) : (
                                <>
                                    <span>Weiter</span>
                                    <svg className="w-5 h-5 transition-transform duration-300 group-hover/nav:translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                                    </svg>
                                </>
                            )}
                        </button>
                    </div>
                )}
            </div>
        </main>
    );
}
