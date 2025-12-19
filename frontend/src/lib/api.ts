/**
 * Storybook.ai - API Client
 * Functions to interact with the FastAPI backend
 */

const getApiBase = () => {
    if (typeof window !== 'undefined') {
        // In browser, if env is missing, default to current origin
        return process.env.NEXT_PUBLIC_API_URL || window.location.origin;
    }
    return process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
};

const API_BASE = getApiBase();


export interface BookCreateResponse {
    id: string;
    status: string;
    progress: number;
    message: string;
    pdf_url?: string;
    preview_images?: string[];
}

export interface PreviewScene {
    scene_id: number;
    status: 'locked' | 'unlocked' | 'generating';
    image_url?: string;
    thumbnail_url?: string;
}

export interface BookStatus {
    id: string;
    status: 'pending' | 'creating_character' | 'waiting_for_approval' | 'generating_preview' | 'ready_for_purchase' | 'paid_processing_full' | 'completed' | 'failed';
    progress: number;
    message: string;
    character_image_url?: string; // NEW
    pdf_url?: string;
    preview_images?: string[];
    preview_scenes?: PreviewScene[];
}

export interface BookDetails {
    id: string;
    child_name: string;
    theme: string;
    status: string;
    progress: number;
    pages: Array<{
        page_number: number;
        text: string;
        image_url?: string;
    }>;
    pdf_url?: string;
    preview_images?: string[];
    preview_scenes?: Array<{
        scene_id: number;
        status: 'locked' | 'unlocked' | 'generating';
        image_url?: string;
        thumbnail_url?: string;
    }>;
    created_at: string;
    updated_at: string;
}

/**
 * Create a new personalized book
 */
/**
 * Generate a character preview
 */
export async function generateCharacterPreview(
    file: File,
    gender: string,
    name: string
): Promise<{ original_url: string; generated_url: string }> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('gender', gender);
    formData.append('name', name);

    const url = `${API_BASE}/api/assets/generate-character-preview`;
    console.log('ðŸš€ Generating character preview:', url);

    const response = await fetch(url, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Failed to generate preview: ${errorText}`);
    }

    return response.json();
}

export interface InitBookPayload {
    child_name: string;
    theme: string;
    child_photo_url: string; // Must be uploaded first
    user_id: string; // Session ID
    approved_character_url?: string; // Pre-generated character
    style?: string;
    custom_theme?: string;
}

export interface UploadResponse {
    url: string;
}

/**
 * Upload an image to the backend
 */
export async function uploadImage(file: File): Promise<string> {
    const formData = new FormData();
    formData.append('file', file);

    const url = `${API_BASE}/api/assets/upload`;
    const response = await fetch(url, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
    }

    const data: UploadResponse = await response.json();
    return data.url;
}

/**
 * Initialize a new book (Step 1)
 */
export async function initBook(payload: InitBookPayload): Promise<BookCreateResponse> {
    const url = `${API_BASE}/api/books/init`;
    console.log('ðŸš€ Initializing book:', payload);

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('âŒ Init failed:', errorText);
            throw new Error(`Failed to init book: ${errorText}`);
        }

        return response.json();
    } catch (error) {
        console.error('âŒ Fetch error:', error);
        throw error;
    }
}

/**
 * Get the current status of a book
 */
export async function getBookStatus(bookId: string): Promise<BookStatus> {
    const response = await fetch(`${API_BASE}/api/books/${bookId}/status`);

    if (!response.ok) {
        throw new Error(`Failed to get book status: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Get all books for a specific user
 */
export async function getMyBooks(userId: string): Promise<BookDetails[]> {
    const response = await fetch(`${API_BASE}/api/books/user/${userId}`);

    if (!response.ok) {
        // Fallback for demo or if endpoint doesn't exist yet
        console.warn('âŒ Failed to fetch user books, using empty list');
        return [];
    }

    return response.json();
}

/**
 * Get full book details including pages
 */
export async function getBookDetails(bookId: string): Promise<BookDetails> {
    const response = await fetch(`${API_BASE}/api/books/${bookId}`);

    if (!response.ok) {
        throw new Error(`Failed to get book details: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Get download URL for completed book
 */
export async function getDownloadUrl(bookId: string): Promise<{ download_url: string; filename: string }> {
    const response = await fetch(`${API_BASE}/api/books/${bookId}/download`);

    if (!response.ok) {
        throw new Error(`Failed to get download URL: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Purchase book and trigger completion
 */
export async function purchaseBook(bookId: string): Promise<{ message: string; book_id: string }> {
    const response = await fetch(`${API_BASE}/api/books/${bookId}/purchase`, {
        method: 'POST',
    });

    if (!response.ok) {
        throw new Error(`Failed to purchase book: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Approve character and start scene generation
 */
export async function approveCharacter(bookId: string): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_BASE}/api/books/${bookId}/approve`, {
        method: 'POST',
    });

    if (!response.ok) {
        throw new Error(`Failed to approve character: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Reject and regenerate character
 */
export async function regenerateCharacter(bookId: string): Promise<{ status: string; message: string }> {
    const response = await fetch(`${API_BASE}/api/books/${bookId}/regenerate`, {
        method: 'POST',
    });

    if (!response.ok) {
        throw new Error(`Failed to regenerate character: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Create Stripe Checkout Session
 */
export async function createCheckoutSession(bookId: string): Promise<{ checkout_url: string }> {
    const response = await fetch(`${API_BASE}/api/payment/create-checkout-session`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ book_id: bookId }),
    });

    if (!response.ok) {
        throw new Error(`Failed to create checkout session: ${response.statusText}`);
    }

    return response.json();
}
/**
 * Create a new book
 */
export async function createBook(
    childName: string,
    theme: string,
    photo?: File,
    customTheme?: string
): Promise<{ id: string }> {
    const formData = new FormData();
    formData.append('child_name', childName);
    formData.append('theme', theme);
    if (photo) {
        formData.append('photo', photo);
    }
    if (customTheme) {
        formData.append('custom_theme', customTheme);
    }
    const response = await fetch(API_BASE + '/api/books/create', {
        method: 'POST',
        body: formData,
    });
    if (!response.ok) {
        throw new Error('Failed to create book: ' + response.statusText);
    }
    return response.json();
}
