"use client";

import Link from "next/link";
import { useState } from "react";
import Image from "next/image";
import ComparisonSlider from "@/components/ComparisonSlider";

// Theme Data
const themes = [
  { id: "space", title: "Weltraum Mission", color: "bg-blue-50" },
  { id: "dino", title: "Dino-Forscher", color: "bg-green-50" },
  { id: "pirate", title: "Piraten-Schatzsuche", color: "bg-orange-50" },
  { id: "forest", title: "Zauberwald & Feen", color: "bg-purple-50" },
  { id: "underwater", title: "Unterwasser-Zauber", color: "bg-cyan-50" },
  { id: "princess", title: "Zauber-Königreich", color: "bg-pink-50" },
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
            <span>4.9 • 500+ glückliche Familien</span>
          </div>

          {/* Slider Container */}
          <div className="relative w-full max-w-md mx-auto animate-fade-in-up delay-500">
            {/* Slider Frame */}
            <div className="relative aspect-[3/4] w-full shadow-2xl shadow-blue-900/10 rounded-[2.5rem] overflow-hidden border-8 border-white bg-white">
              <ComparisonSlider
                imageBefore="/assets/hero/hero-comparison-real.jpg"
                imageAfter="/assets/hero/hero-comparison-pixar.jpg"
                labelBefore="Original"
                labelAfter="Zauberhaft"
                orientation="horizontal"
                objectPosition="top"
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


          </div>

        </div>

      </section>

      {/* --- Trust Stats Section --- */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-2xl md:text-3xl font-bold text-slate-800 mb-2 flex items-center justify-center gap-3">
              Vertraut von Eltern in ganz Deutschland
              <span className="text-2xl">🇩🇪</span>
            </h2>
          </div>

          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center mb-16 border-b border-slate-100 pb-12">
            <div className="space-y-2">
              <div className="text-4xl md:text-5xl font-extrabold text-blue-600">500+</div>
              <div className="text-2xl">📚</div>
              <p className="text-slate-600 font-medium">Bücher erstellt</p>
            </div>

            <div className="space-y-2">
              <div className="text-4xl md:text-5xl font-extrabold text-slate-800 flex items-center justify-center gap-2">
                4.9 <span className="text-yellow-400 text-3xl">★</span>
              </div>
              <div className="flex justify-center text-yellow-400 gap-1 text-sm">
                <span>★</span><span>★</span><span>★</span><span>★</span><span>★</span>
              </div>
              <p className="text-slate-600 font-medium">Eltern-Bewertung</p>
            </div>

            <div className="space-y-2">
              <div className="text-4xl md:text-5xl font-extrabold text-orange-500">3-5</div>
              <div className="text-2xl">🚚</div>
              <p className="text-slate-600 font-medium">Tage Lieferzeit</p>
            </div>

            <div className="space-y-2">
              <div className="text-4xl md:text-5xl font-extrabold text-slate-800">100%</div>
              <div className="text-2xl">🇩🇪</div>
              <p className="text-slate-600 font-medium">Made in Germany</p>
            </div>
          </div>

          {/* Trust Badges */}
          <div className="flex flex-wrap justify-center items-center gap-8 md:gap-16 opacity-70 grayscale hover:grayscale-0 transition-all duration-500">


            <div className="flex items-center gap-2 px-4 py-2 bg-slate-100 rounded-lg text-slate-700 font-bold border border-slate-200">
              <span className="text-xl">🔒</span> SSL SECURED
            </div>

            <div className="flex items-center gap-2 font-bold text-slate-800">
              <span className="text-3xl">🌱</span>
              <div className="leading-tight">Klimaneutral<br /><span className="text-[10px] text-slate-500 font-normal">Durch Kompensation</span></div>
            </div>

            <div className="flex items-center gap-2 font-bold text-slate-800">
              <span className="text-xl">🔒</span>
              <div className="leading-tight">Sichere Zahlung<br />
                <span className="flex gap-1 mt-1">
                  <span className="text-[10px] px-1 bg-slate-200 text-slate-600 rounded">VISA</span>
                  <span className="text-[10px] px-1 bg-slate-200 text-slate-600 rounded">PayPal</span>
                  <span className="text-[10px] px-1 bg-slate-200 text-slate-600 rounded">Klarna</span>
                </span>
              </div>
            </div>

            <div className="flex items-center gap-2 font-bold text-slate-800">
              <div className="w-8 h-8 border-2 border-slate-800 rounded-full flex items-center justify-center">✓</div>
              <div className="leading-tight">30 Tage<br /><span className="text-xs font-normal">Geld-zurück-Garantie</span></div>
            </div>
          </div>

        </div>
      </section>
      <section id="how-it-works" className="py-24 bg-white relative overflow-hidden">
        {/* Background Decoration */}
        <div className="absolute top-1/2 right-0 w-[600px] h-[600px] bg-blue-50/50 rounded-full blur-[120px] translate-x-1/2 -translate-y-1/2 -z-10"></div>

        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-16">
            <span className="text-brand-blue font-bold tracking-wider uppercase text-sm mb-2 block">Einzigartige Erinnerungen</span>
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6">So einfach entsteht dein Buch</h2>
            <p className="text-xl text-slate-500 max-w-2xl mx-auto">
              In nur wenigen Minuten erstellst du ein unvergessliches Geschenk, das dein Kind zum Strahlen bringt.
            </p>
          </div>

          <div className="grid lg:grid-cols-2 gap-16 items-center">
            {/* Left Column: Visuals */}
            <div className="relative order-2 lg:order-1">
              <div className="relative aspect-square max-w-[500px] mx-auto">
                {/* Main Circle BG */}
                <div className="absolute inset-0 bg-blue-50 rounded-full animate-pulse-slow"></div>

                {/* Elements */}
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[90%]">
                  <Image
                    src="/assets/landing/hero-book.png"
                    alt="Book Preview"
                    width={600}
                    height={600}
                    className="object-contain drop-shadow-2xl hover:scale-105 transition-transform duration-700"
                  />
                </div>

                {/* Floating Badge */}
                <div className="absolute top-10 right-10 bg-white p-4 rounded-2xl shadow-xl animate-float">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center text-2xl">📸</div>
                    <div>
                      <div className="text-xs text-slate-400 font-bold uppercase">Schritt 1</div>
                      <div className="font-bold text-slate-800">Foto hochladen</div>
                    </div>
                  </div>
                </div>

                {/* Bear element */}
                <div className="absolute -bottom-10 -left-10 w-48 animate-bounce-slow">
                  <Image
                    src="/assets/mascot/bear_walking.png"
                    alt="Bear"
                    width={200}
                    height={200}
                    className="object-contain"
                  />
                </div>
              </div>
            </div>

            {/* Right Column: Steps */}
            <div className="space-y-12 order-1 lg:order-2">
              {[
                {
                  step: 1,
                  title: "Foto hochladen",
                  desc: "Lade ein einfaches Foto deines Kindes hoch. Unsere sichere KI analysiert es in Sekunden – völlig privat & DSGVO-konform.",
                  icon: "📸",
                  color: "bg-blue-100 text-blue-600"
                },
                {
                  step: 2,
                  title: "Abenteuer wählen",
                  desc: "Ob Weltraum, Dinos oder Feen – wähle aus 6 magischen Welten. Dein Kind wird zur Hauptfigur in seinem eigenen Pixar-Style Film.",
                  icon: "🪄",
                  color: "bg-orange-100 text-orange-600"
                },
                {
                  step: 3,
                  title: "Buch erhalten",
                  desc: "Bestelle dein Premium-Hardcover. Wir drucken in Deutschland auf hochwertigem Papier und liefern in 3-5 Tagen.",
                  icon: "🎁",
                  color: "bg-green-100 text-green-600"
                }
              ].map((item, idx) => (
                <div key={idx} className="flex gap-6 group">
                  <div className="flex flex-col items-center">
                    <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-bold ${item.color} shadow-sm group-hover:scale-110 transition-transform`}>
                      {item.icon}
                    </div>
                    {idx !== 2 && <div className="w-0.5 h-full bg-slate-100 my-2"></div>}
                  </div>
                  <div className="pb-8">
                    <h3 className="text-xl font-bold text-slate-900 mb-2">{item.title}</h3>
                    <p className="text-slate-500 leading-relaxed text-lg">{item.desc}</p>
                  </div>
                </div>
              ))}

              <div className="pt-4 pl-20">
                <Link href="/create" className="btn-primary inline-flex gap-2 items-center">
                  Jetzt ausprobieren <span className="text-xl">→</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* --- Theme Selector --- */}
      <section id="themes" className="py-24 px-6 bg-slate-50">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center gap-3 mb-4">
              <span className="text-4xl">📚</span>
              <span className="font-bold gradient-text text-2xl">bookloo</span>
            </div>
            <h2 className="text-4xl font-bold text-slate-900 mb-4">Wähle dein magisches Abenteuer</h2>
            <p className="text-xl text-slate-500">6 handgezeichnete Welten voller Magie und Abenteuer</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
            {themes.map((theme) => (
              <div
                key={theme.id}
                onClick={() => setSelectedTheme(theme.id)}
                className={`relative group cursor-pointer transition-all duration-300 rounded-2xl overflow-hidden border-4 shadow-lg hover:shadow-xl ${selectedTheme === theme.id ? 'border-brand-blue shadow-2xl scale-[1.02]' : 'border-white hover:border-blue-200'}`}
              >
                {/* Theme Preview Image */}
                <div className="aspect-[4/3] relative overflow-hidden">
                  <img
                    src={`/assets/themes/${theme.id}.png`}
                    alt={theme.title}
                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                  />

                  {/* Selected Checkmark */}
                  {selectedTheme === theme.id && (
                    <div className="absolute top-3 right-3 w-10 h-10 bg-brand-blue text-white rounded-full flex items-center justify-center text-xl shadow-lg animate-in zoom-in">
                      ✓
                    </div>
                  )}
                </div>

                {/* Theme Title */}
                <div className="p-4 bg-white">
                  <h3 className="font-bold text-lg text-slate-800">{theme.title}</h3>
                </div>
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
      {/* --- Pricing Section (Redesigned) --- */}
      <section id="pricing" className="py-24 px-6 bg-gradient-to-b from-white to-blue-50 overflow-hidden">
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-16">
            <span className="inline-block px-4 py-1.5 rounded-full bg-brand-orange/10 text-brand-orange font-bold text-sm mb-4 border border-brand-orange/20">✨ Einführungspreis</span>
            <h2 className="text-4xl font-bold text-slate-900">Ein Geschenk für die Ewigkeit</h2>
          </div>

          <div className="bg-white rounded-[2.5rem] shadow-2xl shadow-blue-900/10 border border-slate-100 overflow-hidden flex flex-col md:flex-row">
            {/* Left Column: Product Image */}
            <div className="md:w-1/2 bg-blue-50 relative p-12 flex items-center justify-center overflow-hidden group">
              <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-white/50 to-transparent"></div>
              <Image
                src="/assets/landing/hero-book.png"
                alt="Book Cover"
                width={500}
                height={500}
                className="relative z-10 drop-shadow-2xl transition-transform duration-500 group-hover:scale-105 group-hover:rotate-1"
              />
              {/* Floating Price Tag */}
              <div className="absolute bottom-8 right-8 bg-white px-6 py-4 rounded-2xl shadow-xl z-20 animate-bounce-slow">
                <div className="text-xs text-slate-400 line-through font-bold">39,99 €</div>
                <div className="text-3xl font-extrabold text-brand-blue">24,90 €</div>
              </div>
            </div>

            {/* Right Column: Details */}
            <div className="md:w-1/2 p-8 md:p-12 flex flex-col justify-center">
              <h3 className="text-2xl font-bold text-slate-900 mb-2">Premium Hardcover</h3>
              <p className="text-slate-500 mb-8">Personalisiert mit deinem Kind</p>

              <div className="space-y-4 mb-10">
                {[
                  "21x21cm Format",
                  "30 personalisierte Seiten",
                  "Pixar-Qualität Illustrationen",
                  "Dein Kind als Hauptfigur",
                  "6 Abenteuer zur Auswahl",
                  "Versand in 3-5 Tagen"
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-3">
                    <div className="w-5 h-5 rounded-full bg-blue-100 text-brand-blue flex items-center justify-center text-xs font-bold">✓</div>
                    <span className="text-slate-700 font-medium">{item}</span>
                  </div>
                ))}
              </div>

              <Link href="/create" className="btn-primary w-full py-4 text-center text-lg shadow-lg hover:shadow-blue-300/50">
                Jetzt erstellen →
              </Link>
              <div className="mt-4 text-center">
                <span className="text-xs text-slate-400">Kostenlose Vorschau • Kein Risiko</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* --- Testimonials Section (Redesigned) --- */}
      <section className="py-24 px-6 bg-white">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-slate-900 mb-4">Über 500 glückliche Familien</h2>
            <div className="flex items-center justify-center gap-2 text-2xl font-bold text-slate-800">
              <div className="flex text-yellow-400 text-3xl">★★★★★</div>
              4.9/5
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                name: "Sarah M.",
                loc: "München",
                text: "Meine Tochter war so begeistert! Sie hat sich sofort erkannt und das Buch nie mehr aus der Hand gelegt.",
                img: "bg-pink-100 text-pink-600"
              },
              {
                name: "Thomas K.",
                loc: "Berlin",
                text: "Das perfekte Geschenk! Die Qualität ist fantastisch und der Versand war super schnell.",
                img: "bg-blue-100 text-blue-600"
              },
              {
                name: "Lisa W.",
                loc: "Hamburg",
                text: "Wir haben schon 3 Bücher bestellt - für jeden Geburtstag ein neues Abenteuer!",
                img: "bg-green-100 text-green-600"
              },
            ].map((t, i) => (
              <div key={i} className="bg-white p-8 rounded-3xl shadow-[0_10px_40px_-10px_rgba(0,0,0,0.08)] border border-slate-100 hover:-translate-y-1 transition-transform duration-300">
                <div className="flex items-center gap-4 mb-6">
                  <div className={`w-14 h-14 rounded-full ${t.img} flex items-center justify-center font-bold text-xl`}>
                    {t.name[0]}
                  </div>
                  <div>
                    <h4 className="font-bold text-slate-900">{t.name}</h4>
                    <p className="text-sm text-slate-500">{t.loc}</p>
                  </div>
                  <div className="ml-auto flex text-yellow-400 text-sm">★★★★★</div>
                </div>

                <div className="relative">
                  <span className="absolute -top-4 -left-2 text-6xl text-brand-orange/20 font-serif leading-none">“</span>
                  <p className="text-slate-600 font-medium leading-relaxed relative z-10">
                    {t.text}
                  </p>
                  <span className="absolute -bottom-8 right-0 text-6xl text-brand-orange/20 font-serif leading-none rotate-180">“</span>
                </div>
              </div>
            ))}
          </div>

          <div className="mt-16 flex flex-wrap justify-center gap-8 md:gap-12 grayscale opacity-60">
            {/* Simple placeholders for footer trust icons if needed, or leave empty space */}
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

    </main >
  );
}
