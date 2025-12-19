"use client";

import { useState, useEffect, useRef } from "react";

interface ComparisonSliderProps {
    imageBefore: string;
    imageAfter: string;
    labelBefore?: string;
    labelAfter?: string;
    className?: string;
    orientation?: "horizontal" | "vertical";
    objectPosition?: string;
}

export default function ComparisonSlider({
    imageBefore,
    imageAfter,
    labelBefore = "Original",
    labelAfter = "Generated",
    className = "",
    orientation = "vertical", // Match the vertical card design
    objectPosition = "center",
}: ComparisonSliderProps) {
    const [sliderPosition, setSliderPosition] = useState(100);
    const [isDragging, setIsDragging] = useState(false);
    const containerRef = useRef<HTMLDivElement>(null);

    const handleMove = (event: React.MouseEvent | React.TouchEvent | MouseEvent | TouchEvent) => {
        if (!containerRef.current) return;

        const rect = containerRef.current.getBoundingClientRect();
        let clientPos, size, start;

        if (orientation === "horizontal") {
            size = rect.width;
            start = rect.left;
            clientPos = "touches" in event ? event.touches[0].clientX : (event as MouseEvent).clientX;
        } else {
            size = rect.height;
            start = rect.top;
            clientPos = "touches" in event ? event.touches[0].clientY : (event as MouseEvent).clientY;
        }

        const position = ((clientPos - start) / size) * 100;
        setSliderPosition(Math.min(100, Math.max(0, position)));
    };

    const handleMouseDown = () => setIsDragging(true);
    const handleMouseUp = () => setIsDragging(false);

    useEffect(() => {
        if (isDragging) {
            window.addEventListener("mousemove", handleMove);
            window.addEventListener("mouseup", handleMouseUp);
            window.addEventListener("touchmove", handleMove);
            window.addEventListener("touchend", handleMouseUp);
        }

        return () => {
            window.removeEventListener("mousemove", handleMove);
            window.removeEventListener("mouseup", handleMouseUp);
            window.removeEventListener("touchmove", handleMove);
            window.removeEventListener("touchend", handleMouseUp);
        };
    }, [isDragging]);

    const isVertical = orientation === "vertical";

    return (
        <div
            className={`relative w-full h-full overflow-hidden rounded-3xl shadow-2xl select-none ${isVertical ? 'cursor-row-resize' : 'cursor-col-resize'} ${className}`}
            ref={containerRef}
            onMouseDown={handleMouseDown}
            onTouchStart={handleMouseDown}
        >
            {/* Background Image (After - Generated) */}
            <img
                src={imageAfter}
                alt="After"
                className="absolute inset-0 w-full h-full object-cover"
                style={{ objectPosition }}
                draggable={false}
            />

            {/* Label After (Bottom/Right) */}
            {labelAfter && (
                <div className={`absolute bg-black/50 backdrop-blur-md text-white px-3 py-1 rounded-full text-xs font-medium z-10 pointer-events-none ${isVertical ? 'bottom-4 right-4' : 'top-4 right-4'}`}>
                    {labelAfter}
                </div>
            )}

            {/* Foreground Image (Before - Original) - Clipped */}
            <div
                className="absolute inset-0 w-full h-full overflow-hidden"
                style={{
                    clipPath: isVertical
                        ? `inset(0 0 ${100 - sliderPosition}% 0)` // Clip from bottom up
                        : `inset(0 ${100 - sliderPosition}% 0 0)` // Clip from right to left
                }}
            >
                <img
                    src={imageBefore}
                    alt="Before"
                    className="absolute inset-0 w-full h-full object-cover"
                    style={{ objectPosition }}
                    draggable={false}
                />

                {/* Label Before (Top/Left) */}
                {labelBefore && (
                    <div className="absolute top-4 left-4 bg-white/80 backdrop-blur-md text-slate-800 px-3 py-1 rounded-full text-xs font-bold z-10 pointer-events-none">
                        {labelBefore}
                    </div>
                )}
            </div>

            {/* Slider Handle */}
            <div
                className={`absolute z-20 flex items-center justify-center ${isVertical ? 'w-full h-1' : 'h-full w-1'} bg-white/80`}
                style={{
                    left: isVertical ? '0' : `${sliderPosition}%`,
                    top: isVertical ? `${sliderPosition}%` : '0',
                }}
            >
                <div className="w-12 h-12 bg-white rounded-full shadow-lg flex items-center justify-center transform hover:scale-110 transition-transform">
                    <div className="w-8 h-8 rounded-full bg-indigo-600 flex items-center justify-center text-white">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className={`w-4 h-4 ${isVertical ? 'rotate-0' : 'rotate-90'}`}>
                            <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 15L12 18.75 15.75 15m-7.5-6L12 5.25 15.75 9" />
                        </svg>
                    </div>
                </div>
            </div>
        </div>
    );
}
