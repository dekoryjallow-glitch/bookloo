import BookPreview from '@/components/BookPreview';
import Link from 'next/link';

interface BookPageProps {
    params: Promise<{ id: string }>;
}

export default async function BookPage({ params }: BookPageProps) {
    const { id } = await params;

    return (
        <main className="min-h-screen py-12 px-6">
            <div className="max-w-2xl mx-auto">
                {/* Header */}
                <div className="text-center mb-12">
                    <Link
                        href="/"
                        className="inline-flex items-center gap-2 text-purple-600 hover:text-purple-700 mb-6 transition-colors"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                        </svg>
                        Back to Home
                    </Link>

                    <h1 className="text-4xl md:text-5xl font-extrabold mb-4">
                        <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                            Your Book
                        </span>
                    </h1>
                    <p className="text-xl text-gray-600">
                        Watch the magic happen ✨
                    </p>
                </div>

                {/* Book Preview */}
                <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-2xl p-8 md:p-10">
                    <BookPreview bookId={id} />
                </div>

                {/* Create Another */}
                <div className="text-center mt-8">
                    <Link
                        href="/create"
                        className="text-purple-600 hover:text-purple-700 font-medium transition-colors"
                    >
                        Create Another Book →
                    </Link>
                </div>
            </div>
        </main>
    );
}
