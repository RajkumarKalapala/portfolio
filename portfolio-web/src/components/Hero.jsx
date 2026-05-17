import { Github, Linkedin, Mail, ArrowDown, ExternalLink } from "lucide-react";
import { useEffect, useRef, useState } from "react";

const ROLES = [
  "Full Stack Developer",
  "Automation Engineer",
  "AI Application Builder",
  "Security & Monitoring Dev",
];

function TypeWriter({ words }) {
  const [displayed, setDisplayed] = useState("");
  const [wordIdx, setWordIdx] = useState(0);
  const [charIdx, setCharIdx] = useState(0);
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    const word = words[wordIdx];
    const speed = deleting ? 40 : 80;
    const timeout = setTimeout(() => {
      if (!deleting && charIdx < word.length) {
        setDisplayed(word.slice(0, charIdx + 1));
        setCharIdx(charIdx + 1);
      } else if (!deleting && charIdx === word.length) {
        setTimeout(() => setDeleting(true), 1800);
      } else if (deleting && charIdx > 0) {
        setDisplayed(word.slice(0, charIdx - 1));
        setCharIdx(charIdx - 1);
      } else {
        setDeleting(false);
        setWordIdx((wordIdx + 1) % words.length);
      }
    }, speed);
    return () => clearTimeout(timeout);
  }, [charIdx, deleting, wordIdx, words]);

  return (
    <span>
      {displayed}
      <span className="cursor-blink text-[#00d4ff]">|</span>
    </span>
  );
}

export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-grid opacity-100" />
      <div className="absolute inset-0 bg-glow-top" />
      {/* Ambient orbs */}
      <div className="absolute top-1/3 left-1/4 w-96 h-96 rounded-full bg-cyan-500/5 blur-3xl pointer-events-none" />
      <div className="absolute bottom-1/4 right-1/4 w-64 h-64 rounded-full bg-blue-500/5 blur-3xl pointer-events-none" />

      <div className="relative z-10 max-w-6xl mx-auto px-6 pt-28 pb-16 text-center">
        {/* Status badge */}
        <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-[#00d4ff]/20 bg-[#00d4ff]/5 mb-8">
          <span className="w-2 h-2 rounded-full bg-emerald-400 glow-dot animate-pulse" style={{boxShadow:'0 0 6px #34d399, 0 0 12px #34d399'}}/>
          <span className="section-tag" style={{fontSize:'0.7rem'}}>Available for Projects</span>
        </div>

        {/* Main headline */}
        <h1 className="section-title text-5xl md:text-7xl lg:text-8xl mb-6 tracking-tight leading-none">
          Automation &<br />
          <span className="text-gradient">Full Stack</span> Dev
        </h1>

        {/* Typewriter */}
        <div className="text-xl md:text-2xl text-[#8fa8c8] mb-6 font-mono-custom font-medium h-8">
          <TypeWriter words={ROLES} />
        </div>

        {/* Value prop */}
        <p className="max-w-2xl mx-auto text-[#8fa8c8] text-base md:text-lg leading-relaxed mb-10 font-body">
          I build modern web applications, AI-powered tools, monitoring systems,
          and automation solutions — helping businesses work smarter and move faster.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <a href="#projects" className="btn-primary px-8 py-3.5 rounded-xl text-sm inline-flex items-center gap-2 justify-center">
            View Projects
            <ExternalLink size={15} />
          </a>
          <a href="#contact" className="btn-ghost px-8 py-3.5 rounded-xl text-sm inline-flex items-center gap-2 justify-center">
            Get In Touch
            <Mail size={15} />
          </a>
        </div>

        {/* Social links */}
        <div className="flex items-center gap-4 justify-center mb-16">
          {[
            { icon: Github, href: "https://github.com/RajkumarKalapala", label: "GitHub" },
            { icon: Linkedin, href: "https://linkedin.com/in/rajkumarkalapala", label: "LinkedIn" },
            { icon: Mail, href: "mailto:rajkumarkalapala@gmail.com", label: "Email" },
          ].map(({ icon: Icon, href, label }) => (
            <a
              key={label}
              href={href}
              target={href.startsWith("http") ? "_blank" : undefined}
              rel="noreferrer"
              aria-label={label}
              className="w-10 h-10 rounded-xl border border-white/8 bg-white/3 flex items-center justify-center text-[#8fa8c8] hover:text-[#00d4ff] hover:border-[#00d4ff]/30 hover:bg-[#00d4ff]/8 transition-all duration-200"
            >
              <Icon size={17} />
            </a>
          ))}
        </div>

        {/* Stats */}
        <div className="flex flex-wrap gap-6 justify-center">
          {[
            { value: "5+", label: "Live Projects" },
            { value: "3+", label: "Years Building" },
            { value: "4", label: "Tech Domains" },
          ].map(({ value, label }) => (
            <div key={label} className="text-center">
              <div className="font-display text-2xl font-800 text-gradient">{value}</div>
              <div className="text-[#4a6080] text-xs mt-0.5 font-body">{label}</div>
            </div>
          ))}
        </div>

        {/* Scroll cue */}
        <div className="mt-16 flex justify-center">
          <a href="#about" className="flex flex-col items-center gap-2 text-[#4a6080] hover:text-[#00d4ff] transition-colors group">
            <span className="text-xs font-mono-custom tracking-widest">SCROLL</span>
            <ArrowDown size={16} className="animate-bounce" />
          </a>
        </div>
      </div>
    </section>
  );
}
