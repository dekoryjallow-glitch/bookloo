"use client";

import Link from "next/link";
import { useState } from "react";
import Image from "next/image";
import ComparisonSlider from "@/components/ComparisonSlider";

// Theme Data
const themes = [
  { id: "space", title: "Weltraum Mission", img: "/assets/landing/hero-book.png", color: "bg-blue-50" }, // Fallback img
  { id: "dinos", title: "Dino-Forscher", img: "/assets/landing/hero-book.png", color: "bg-green-50" },
  { id: "pirates", title: "Piraten-Schatzsuche", img: "/assets/landing/hero-book.png", color: "bg-orange-50" },
  { id: "magic", title: "Zauberwald & Feen", img: "/assets/landing/hero-book.png", color: "bg-purple-50" },
  { id: "underwater", title: "Unterwasser-Zauber", img: "/assets/landing/hero-book.png", color: "bg-cyan-50" },
  { id: "princess", title: "Zauber-Königreich", img: "/assets/landing/hero-book.png", color: "bg-pink-50" },
];

export default function Home() {
  const [selectedTheme, setSelectedTheme] = useState("space");

  return (
    <main className="min-h-screen bg-brand-gradient">
      {/* --- Header --- */}
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-slate-100">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-3xl">🐻</span>
            <span className="text-2xl font-bold text-slate-800">bookloo</span>
          </div>

          <nav className="hidden md:flex items-center gap-8 font-bold text-slate-600">
            <Link href="#how-it-works" className="hover:text-brand-blue transition-colors">So funktioniert's</Link>
            <Link href="#themes" className="hover:text-brand-blue transition-colors">Abenteuer</Link>
            <Link href="#pricing" className="hover:text-brand-blue transition-colors">Preise</Link>
          </nav>

          <Link href="/create" className="btn-primary">
            Jetzt starten
          </Link>
        </div>
      </header>

      {/* --- Hero Section --- */}
      <section className="relative pt-20 pb-32 px-6 overflow-hidden text-center">
        {/* Decorative Blurs */}
        <div className="absolute top-0 left-0 w-[500px] h-[500px] bg-blue-100/50 rounded-full blur-[100px] -translate-x-1/2 -translate-y-1/2 -z-10"></div>
        <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-orange-100/50 rounded-full blur-[100px] translate-x-1/2 -translate-y-1/2 -z-10"></div>

        <div className="max-w-4xl mx-auto flex flex-col items-center">

          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-6 py-2 bg-white border border-blue-100 shadow-sm text-slate-600 font-medium rounded-full text-sm mb-8 animate-fade-in-up">
            <span>🎄</span>
            <span className="text-brand-blue font-bold">Weihnachts-Special:</span>
            <span>Noch rechtzeitig lieferbar!</span>
          </div>

          {/* Headline */}
          <h1 className="text-6xl md:text-8xl font-extrabold text-slate-900 leading-tight mb-6 animate-fade-in-up delay-100 tracking-tight">
            Dein Kind wird <br />
            <span className="text-brand-blue">zum Helden</span>
          </h1>

          {/* Subheadline */}
          <p className="text-xl md:text-2xl text-slate-500 mb-10 max-w-2xl leading-relaxed animate-fade-in-up delay-200">
            Personalisierte Kinderbücher mit echter KI-Magie ✨
          </p>

          {/* Buttons */}
          <div className="flex flex-col sm:flex-row items-center gap-6 mb-8 animate-fade-in-up delay-300 z-10">
            <Link href="/create" className="btn-primary text-xl px-12 py-5 shadow-blue-300 hover:shadow-blue-400 hover:-translate-y-1 transition-all">
              Jetzt Buch erstellen →
            </Link>
            <Link href="#how-it-works" className="flex items-center gap-2 text-brand-blue font-bold hover:underline">
              <span className="w-8 h-8 rounded-full border-2 border-brand-blue flex items-center justify-center pl-1">▶</span>
              So funktioniert's
            </Link>
          </div>

          {/* Social Proof */}
          <div className="flex items-center gap-2 text-sm font-bold text-slate-500 mb-16 animate-fade-in-up delay-400">
            <div className="flex text-yellow-400 text-lg">★★★★★</div>
            <span>4.9 • 10.000+ glückliche Familien</span>
          </div>

          {/* Slider Container */}
          <div className="relative w-full max-w-4xl mx-auto animate-fade-in-up delay-500">
            {/* Slider Frame */}
            <div className="relative aspect-[16/9] md:aspect-[2/1] w-full shadow-2xl shadow-blue-900/10 rounded-[2.5rem] overflow-hidden border-8 border-white bg-white">
              <ComparisonSlider
                imageBefore="/assets/landing/slider-before.png"
                imageAfter="/assets/landing/slider-after.png"
                labelBefore="Original"
                labelAfter="Held"
                orientation="horizontal"
                className="h-full"
              />
            </div>

            {/* Mascot Peeking */}
            <div className="absolute -bottom-12 -right-8 w-40 h-40 hidden md:block rotate-12 animate-float">
              <div className="relative w-full h-full">
                <span className="text-9xl absolute bottom-0 right-0 drop-shadow-xl">🐻</span>
                {/* Small book icon */}
                <span className="text-5xl absolute bottom-0 left-0">📖</span>
              </div>
            </div>

            {/* Play Button Overlay (Optional - center of video feel) */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 pointer-events-none">
              <div className="w-20 h-20 bg-white/30 backdrop-blur-sm rounded-full flex items-center justify-center border border-white/50">
                <div className="w-0 h-0 border-t-[10px] border-t-transparent border-l-[18px] border-l-white border-b-[10px] border-b-transparent ml-1"></div>
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* --- So funktioniert's --- */}
      <section id="how-it-works" className="py-24 bg-white relative">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16 relative">
            <h2 className="text-4xl font-bold text-slate-900 mb-4">So einfach geht's</h2>
            <p className="text-xl text-slate-500">In 3 Schritten zum fertigen Buch</p>
            {/* Bear on top */}
            <div className="absolute -top-16 right-1/3 w-24 h-24 hidden md:block">
              <span className="text-6xl absolute top-0 right-0 rotate-12">🐻</span>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8 relative z-10">
            {/* Connecting Line (Desktop) */}
            <div className="hidden md:block absolute top-1/2 left-0 w-full h-1 border-t-2 border-dashed border-slate-200 -z-10"></div>

            {[
              { icon: "📸", title: "Foto hochladen", desc: "Lade ein Foto deines Kindes hoch. Unsere KI zaubert daraus einen Charakter.", color: "bg-blue-50 text-brand-blue" },
              { icon: "🪄", title: "Magie erleben", desc: "Wähle ein Abenteuer und sieh zu, wie das Buch Seite für Seite entsteht.", color: "bg-orange-50 text-brand-orange" },
              { icon: "🎁", title: "Geschenk erhalten", desc: "Bestelle dein Hardcover-Buch und mach deinem Kind eine riesige Freude.", color: "bg-blue-50 text-brand-blue" },
            ].map((step, i) => (
              <div key={i} className="bg-white p-8 rounded-3xl shadow-xl border border-slate-50 text-center">
                <div className={`w-20 h-20 mx-auto ${step.color} rounded-2xl flex items-center justify-center text-4xl mb-6 shadow-sm`}>
                  {step.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                <p className="text-slate-500 leading-relaxed">{step.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* --- Theme Selector --- */}
      <section id="themes" className="py-24 px-6 bg-brand-gradient">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-end justify-between mb-12">
            <div>
              <h2 className="text-4xl font-bold text-slate-900 mb-4">Wähle dein Abenteuer</h2>
              <p className="text-xl text-slate-500">6 magische Welten warten auf dein Kind</p>
            </div>
            {/* Bear Dreaming */}
            <div className="hidden md:block text-6xl animate-bounce">
              💭🐻
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            {themes.map((theme) => (
              <div
                key={theme.id}
                onClick={() => setSelectedTheme(theme.id)}
                className={`relative group cursor-pointer transition-all duration-300 rounded-3xl overflow-hidden border-4 ${selectedTheme === theme.id ? 'border-brand-blue shadow-2xl scale-[1.02]' : 'border-transparent hover:border-blue-200'}`}
              >
                <div className={`aspect-[4/3] ${theme.color} relative`}>
                  {/* Placeholder for Theme Image */}
                  <div className="absolute inset-0 flex items-center justify-center text-6xl grayscale group-hover:grayscale-0 transition-all opacity-50">
                    {theme.id === 'space' && '🚀'}
                    {theme.id === 'dino' && '🦖'}
                    {theme.id === 'pirate' && '🏴‍☠️'}
                    {theme.id === 'fantasy' && '🧚'}
                    {theme.id === 'underwater' && '🧜‍♀️'}
                    {theme.id === 'princess' && '👑'}
                  </div>
                </div>

                <div className="p-6 bg-white">
                  <h3 className="font-bold text-lg text-slate-800">{theme.title}</h3>
                  <p className="text-sm text-slate-400">13 magische Szenen</p>
                </div>

                {/* Checkmark Overlay */}
                {selectedTheme === theme.id && (
                  <div className="absolute inset-0 flex items-center justify-center bg-brand-blue/10 pointer-events-none">
                    <div className="w-16 h-16 bg-brand-blue text-white rounded-full flex items-center justify-center text-3xl shadow-lg animate-in zoom-in">
                      ✓
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>

          <div className="mt-12 text-center">
            <Link href={`/create?theme=${selectedTheme}`} className="btn-primary text-xl px-12 py-4 shadow-blue-200">
              Weiter mit {themes.find(t => t.id === selectedTheme)?.title}
            </Link>
          </div>
        </div>
      </section>

      {/* --- Pricing --- */}
      <section id="pricing" className="py-24 px-6 bg-white overflow-hidden">
        <div className="max-w-4xl mx-auto relative">

          {/* Bear Thumbs Up */}
          <div className="absolute -right-20 top-20 w-64 h-64 index-10 hidden lg:block">
            <span className="text-9xl rotate-12 block">👍🐻</span>
          </div>

          <div className="bg-white rounded-[3rem] shadow-2xl border border-slate-100 p-12 md:p-16 relative overflow-hidden text-center">
            {/* Badge */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 bg-brand-orange text-white px-8 py-2 rounded-b-2xl font-bold text-sm uppercase tracking-wider shadow-lg">
              ✨ Einführungspreis
            </div>

            <h2 className="text-3xl font-bold text-slate-900 mt-8 mb-2">Dein personalisiertes Hardcover</h2>
            <p className="text-slate-500 mb-8">Ein Geschenk für die Ewigkeit</p>

            <div className="flex items-center justify-center gap-4 mb-8">
              <span className="text-3xl text-slate-300 line-through font-bold">39,99€</span>
              <span className="text-6xl font-extrabold text-brand-blue">24,90€</span>
            </div>

            <div className="grid md:grid-cols-2 gap-4 text-left max-w-lg mx-auto mb-12">
              {[
                "Premium Hardcover (21x21cm)",
                "32 personalisierte Seiten",
                "Echte Fadenbindung",
                "Pixar-Qualität Druck",
                "Klimaneutraler Versand",
                "100% Zufriedenheitsgarantie"
              ].map((feat, i) => (
                <div key={i} className="flex items-center gap-3">
                  <div className="w-6 h-6 rounded-full bg-blue-100 text-brand-blue flex items-center justify-center text-xs font-bold">✓</div>
                  <span className="font-medium text-slate-700">{feat}</span>
                </div>
              ))}
            </div>

            <Link href="/create" className="btn-orange w-full md:w-auto text-xl px-16 py-4">
              Jetzt gestalten
            </Link>
            <p className="mt-6 text-sm text-slate-400">Kein Risiko • Kostenlose Vorschau vor dem Kauf</p>
          </div>
        </div>
      </section>

      {/* --- Testimonials --- */}
      <section className="py-24 px-6 bg-[#F8FAFC]">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">Über 10.000 glückliche Familien</h2>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              { name: "Sarah Müller", loc: "München", text: "Meine Tochter hat sich sofort erkannt! Sie will das Buch jeden Abend lesen.", stars: 5 },
              { name: "Thomas Klein", loc: "Hamburg", text: "Die Qualität ist der Wahnsinn. Fühlt sich an wie aus dem Buchladen, nur eben mit meinem Sohn.", stars: 5 },
              { name: "Julia Weber", loc: "Berlin", text: "Endlich ein personalisiertes Buch, das nicht billig aussieht. Die Bilder sind wunderschön.", stars: 5 },
            ].map((t, i) => (
              <div key={i} className="bg-white p-8 rounded-3xl shadow-lg border border-slate-50">
                <div className="flex text-brand-orange mb-4 gap-1">
                  {[...Array(t.stars)].map((_, si) => <span key={si}>★</span>)}
                </div>
                <p className="text-slate-600 font-medium mb-6 leading-relaxed">"{t.text}"</p>
                <div className="flex items-center gap-4">
                  <div className="w-12 h-12 bg-slate-200 rounded-full flex items-center justify-center font-bold text-slate-500">
                    {t.name[0]}
                  </div>
                  <div>
                    <div className="font-bold text-slate-900">{t.name}</div>
                    <div className="text-xs text-slate-400">{t.loc}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* --- Footer --- */}
      <footer className="py-12 bg-white border-t border-slate-100 text-center">
        <div className="flex items-center justify-center gap-2 mb-8">
          <span className="text-2xl">🐻</span>
          <span className="text-xl font-bold text-slate-800">bookloo</span>
        </div>
        <div className="flex justify-center gap-8 text-sm font-medium text-slate-500 mb-8">
          <Link href="#">Impressum</Link>
          <Link href="#">Datenschutz</Link>
          <Link href="#">AGB</Link>
          <Link href="#">Kontakt</Link>
        </div>
        <p className="text-slate-400 text-xs text-center">
          © 2024 bookloo AI • Mit ❤️ in Deutschland entwickelt
        </p>
      </footer>

    </main>
  );
}
