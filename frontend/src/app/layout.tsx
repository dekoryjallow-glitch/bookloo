import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import "./globals.css";

const nunito = Nunito({
  subsets: ["latin"],
  variable: '--font-nunito',
  display: 'swap',
});

export const metadata: Metadata = {
  title: "bookloo - Dein Kind als Buch-Held",
  description: "Erstelle magische, personalisierte Kinderbücher mit deinem Kind als Helden. KI-gestützte Geschichten und wunderschöne Illustrationen.",
  keywords: ["Kinderbuch", "personalisiert", "KI Buch", "bookloo"],
  icons: {
    icon: "/favicon.png",
    shortcut: "/favicon.png",
    apple: "/favicon.png",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="de" suppressHydrationWarning>
      <body
        className={`${nunito.variable} font-sans antialiased bg-[#FAFAFA] min-h-screen selection:bg-blue-100 selection:text-blue-600`}
        suppressHydrationWarning
      >
        {children}
      </body>
    </html>
  );
}
