'use client';

/**
 * Storybook.ai - Wizard Store
 * Client-side state management for the book creation wizard
 */

import { create } from 'zustand';
import { v4 as uuidv4 } from 'uuid';

export type Gender = 'boy' | 'girl' | 'neutral';
export type Theme = 'space' | 'dinos' | 'princess' | 'pirates' | 'underwater' | 'magic' | 'custom';
export type Style = 'pixar_3d';

export interface WizardState {
    // Session
    userId: string;

    // Step 1: Name & Gender
    childName: string;
    childGender: Gender;

    // Step 2: Photo
    childPhotoFile: File | null;
    childPhotoPreview: string | null;
    generatedPortraitUrl: string | null; // Restored
    originalPhotoUrl: string | null;     // Restored

    // Step 3: Theme
    selectedTheme: Theme;
    customTheme: string;

    // Step 4: Style
    selectedStyle: Style;

    // Wizard navigation
    currentStep: number;
    bookId: string | null;

    // Actions
    setChildName: (name: string) => void;
    setChildGender: (gender: Gender) => void;
    setChildPhoto: (file: File | null, preview: string | null) => void;
    setGeneratedPortrait: (url: string | null, originalUrl: string | null) => void; // Restored
    setSelectedTheme: (theme: Theme) => void;
    setCustomTheme: (theme: string) => void;
    setSelectedStyle: (style: Style) => void;
    setCurrentStep: (step: number) => void;
    setBookId: (id: string) => void;
    nextStep: () => void;
    prevStep: () => void;
    reset: () => void;
    isStepValid: (step: number) => boolean;
}

const getInitialUserId = () => {
    // In a real app, from auth or localStorage
    if (typeof window !== 'undefined') {
        const stored = localStorage.getItem('sb_user_id');
        if (stored) return stored;
        const newId = uuidv4();
        localStorage.setItem('sb_user_id', newId);
        return newId;
    }
    return 'temp-user-id'; // Server-side fallback or wait for mount
};

const initialState = {
    userId: '', // Will be set on hydrate/init
    childName: '',
    childGender: 'neutral' as Gender,
    childPhotoFile: null,
    childPhotoPreview: null,
    generatedPortraitUrl: null, // Restored
    originalPhotoUrl: null,     // Restored
    selectedTheme: 'space' as Theme,
    customTheme: '',
    selectedStyle: 'pixar_3d' as Style,
    currentStep: 1,
    bookId: null,
};

export const useWizardStore = create<WizardState>()((set, get) => ({
    ...initialState,

    // Initialize userId on first use if needed (hacky, better in useEffect)
    // But we can just set it:
    userId: getInitialUserId(),

    setChildName: (name) => set({ childName: name }),
    setChildGender: (gender) => set({ childGender: gender }),

    setChildPhoto: (file, preview) => set({
        childPhotoFile: file,
        childPhotoPreview: preview,
        // Reset generated portrait if photo changes
        generatedPortraitUrl: null,
        originalPhotoUrl: null
    }),

    setGeneratedPortrait: (url, originalUrl) => set({
        generatedPortraitUrl: url,
        originalPhotoUrl: originalUrl
    }),

    setSelectedTheme: (theme) => set({ selectedTheme: theme }),
    setCustomTheme: (theme) => set({ customTheme: theme }),
    setSelectedStyle: (style) => set({ selectedStyle: style }),

    setCurrentStep: (step) => set({ currentStep: step }),
    setBookId: (id) => set({ bookId: id }),

    nextStep: () => {
        const { currentStep, isStepValid } = get();
        if (isStepValid(currentStep) && currentStep < 3) {
            set({ currentStep: currentStep + 1 });
        }
    },

    prevStep: () => {
        const { currentStep } = get();
        if (currentStep > 1) {
            set({ currentStep: currentStep - 1 });
        }
    },

    reset: () => {
        set({
            ...initialState,
            userId: get().userId // Keep user ID
        });
    },

    isStepValid: (step) => {
        const state = get();
        switch (step) {
            case 1:
                return state.childName.trim().length >= 2;
            case 2:
                // Photo is optional? Or required for new flow?
                // New Phase 1 requires photo for character gen.
                // Let's make it required for now to ensure good results.
                // UPDATED logic: Ideally we want a generated portrait, but for validity just the file is enough
                // to proceed IF we are skipping generation (but we want to FORCE generation).
                // But the user might want to skip if it fails. 
                // Let's keep it simple: file needed.
                return !!state.childPhotoFile || !!state.childPhotoPreview;
            case 3:
                return !!state.selectedTheme;
            default:
                return false;
        }
    },
}));
