import { Globe, Bot, Shield, Zap, CheckCircle } from "lucide-react";

const services = [
  {
    icon: Globe,
    title: "Web Development",
    tagline: "Responsive, modern web applications",
    color: "#00d4ff",
    items: [
      "Custom business websites & landing pages",
      "Admin dashboards & internal tools",
      "E-commerce platforms",
      "API integration & backend setup",
    ],
    tech: ["React", "Node.js", "MongoDB", "Tailwind"],
  },
  {
    icon: Zap,
    title: "Automation Solutions",
    tagline: "Save time with smart automation",
    color: "#f59e0b",
    items: [
      "Python workflow automation scripts",
      "Data scraping & reporting pipelines",
      "Scheduled task automation",
      "System monitoring & alerting",
    ],
    tech: ["Python", "Bash", "Linux", "Cron"],
  },
  {
    icon: Bot,
    title: "AI-Powered Applications",
    tagline: "Intelligent tools for modern businesses",
    color: "#a78bfa",
    items: [
      "AI chatbots with document understanding",
      "RAG systems for private knowledge bases",
      "AI-powered data analysis tools",
      "LLM API integrations",
    ],
    tech: ["LangChain", "OpenAI", "ChromaDB", "FastAPI"],
    featured: true,
  },
  {
    icon: Shield,
    title: "Security & Monitoring",
    tagline: "Eyes on your systems, 24/7",
    color: "#34d399",
    items: [
      "CCTV monitoring platform development",
      "Employee & asset monitoring systems",
      "Security audit scripts",
      "Log parsing & intrusion detection",
    ],
    tech: ["OpenCV", "Python", "Flask", "SQLite"],
  },
];

export default function Services() {
  return (
    <section id="services" className="relative py-28">
      <div className="absolute inset-0" style={{background:'radial-gradient(ellipse 70% 50% at 50% 50%, rgba(0,212,255,0.04) 0%, transparent 70%)'}} />
      <div className="relative max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="section-tag mb-4">// what i offer</div>
          <h2 className="section-title text-4xl md:text-5xl">
            Services & Solutions
          </h2>
          <p className="mt-4 text-[#8fa8c8] font-body max-w-xl mx-auto text-sm leading-relaxed">
            Every service is delivered with clean code, clear documentation,
            and a focus on what actually matters to your business.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-5">
          {services.map(({ icon: Icon, title, tagline, color, items, tech, featured }) => (
            <div
              key={title}
              className={`glass-card rounded-2xl p-7 relative overflow-hidden ${featured ? "ring-1 ring-inset" : ""}`}
              style={featured ? { ringColor: `${color}30` } : {}}
            >
              {featured && (
                <div className="absolute top-4 right-4 px-2.5 py-1 rounded-full text-xs font-mono-custom" style={{background:`${color}15`, color, border:`1px solid ${color}30`}}>
                  Most Popular
                </div>
              )}

              {/* Icon */}
              <div
                className="w-12 h-12 rounded-xl flex items-center justify-center mb-5"
                style={{ background: `${color}12`, border: `1px solid ${color}20` }}
              >
                <Icon size={22} style={{ color }} />
              </div>

              <h3 className="font-display font-700 text-white text-xl mb-1">{title}</h3>
              <p className="text-[#4a6080] text-sm mb-5 font-body">{tagline}</p>

              <ul className="space-y-2.5 mb-6">
                {items.map((item) => (
                  <li key={item} className="flex items-start gap-2.5 text-sm text-[#8fa8c8] font-body">
                    <CheckCircle size={14} className="mt-0.5 shrink-0" style={{ color }} />
                    {item}
                  </li>
                ))}
              </ul>

              {/* Tech pills */}
              <div className="flex flex-wrap gap-2">
                {tech.map((t) => (
                  <span
                    key={t}
                    className="px-2.5 py-1 rounded text-xs font-mono-custom"
                    style={{ background: `${color}08`, color: color + "cc", border: `1px solid ${color}15` }}
                  >
                    {t}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* CTA strip */}
        <div className="mt-12 glass-card rounded-2xl p-8 text-center">
          <p className="font-display text-white text-lg mb-2">Have a custom project in mind?</p>
          <p className="text-[#8fa8c8] text-sm mb-6 font-body">
            I'm open to freelance work, short contracts, and long-term collaborations.
          </p>
          <a href="#contact" className="btn-primary px-8 py-3 rounded-xl text-sm inline-block">
            Let's Talk
          </a>
        </div>
      </div>
    </section>
  );
}
