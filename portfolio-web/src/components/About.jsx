import { Shield, Cpu, Globe, Zap } from "lucide-react";

const highlights = [
  { icon: Globe, label: "Full Stack Web", desc: "React, Node.js, MongoDB — end-to-end." },
  { icon: Cpu, label: "AI & Automation", desc: "LangChain, RAG systems, Python workflows." },
  { icon: Shield, label: "Security & Monitoring", desc: "CCTV systems, security scripts, threat monitoring." },
  { icon: Zap, label: "Fast Delivery", desc: "Clean code, documented, production-ready." },
];

export default function About() {
  return (
    <section id="about" className="relative py-28 overflow-hidden">
      <div className="absolute inset-0 bg-grid opacity-50" />
      <div className="relative max-w-6xl mx-auto px-6">
        <div className="grid lg:grid-cols-2 gap-16 items-center">
          {/* Left — text */}
          <div>
            <div className="section-tag mb-4">// who i am</div>
            <h2 className="section-title text-4xl md:text-5xl mb-6">
              I build tools that<br />
              <span className="text-gradient">actually ship.</span>
            </h2>
            <div className="space-y-4 text-[#8fa8c8] leading-relaxed font-body text-base">
              <p>
                I'm a developer who specialises in turning complex technical problems
                into clean, working software. My work spans full-stack web applications,
                AI-powered pipelines, real-time monitoring dashboards, and security
                automation — each built with production quality in mind.
              </p>
              <p>
                I've worked as a Security Analyst at Supraja Technologies and as a
                domain trainer covering Python, Java, Linux, and data science —
                which means I bring both hands-on engineering experience and the
                ability to explain what I build clearly.
              </p>
              <p>
                If you need a reliable developer who can take a brief, figure out
                the architecture, and deliver — that's where I excel.
              </p>
            </div>

            <div className="mt-8 flex flex-wrap gap-3">
              {["Remote Work", "Quick Turnaround", "Clean Code", "Well Documented"].map((t) => (
                <span
                  key={t}
                  className="px-3 py-1.5 rounded-md border border-[#00d4ff]/15 bg-[#00d4ff]/5 text-[#00d4ff] text-xs font-mono-custom"
                >
                  {t}
                </span>
              ))}
            </div>
          </div>

          {/* Right — highlight cards */}
          <div className="grid grid-cols-2 gap-4">
            {highlights.map(({ icon: Icon, label, desc }) => (
              <div key={label} className="glass-card rounded-xl p-5">
                <div className="w-10 h-10 rounded-lg bg-[#00d4ff]/10 border border-[#00d4ff]/15 flex items-center justify-center mb-4">
                  <Icon size={18} className="text-[#00d4ff]" />
                </div>
                <div className="font-display font-600 text-white text-sm mb-1">{label}</div>
                <div className="text-[#4a6080] text-xs leading-relaxed font-body">{desc}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
