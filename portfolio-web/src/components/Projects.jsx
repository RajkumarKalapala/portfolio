import { Github, ExternalLink, Camera, Bot, ShoppingCart, Shield, Monitor, Code2 } from "lucide-react";

const projects = [
  {
    id: 1,
    icon: Bot,
    title: "AI Document Chatbot",
    category: "AI / RAG System",
    color: "#a78bfa",
    description:
      "A private, local AI chatbot that lets users upload any document and ask questions — no data leaves the machine. Built for businesses that need document intelligence without cloud dependency.",
    impact: "Eliminates hours of manual document reading; works entirely offline.",
    tech: ["Python", "LangChain", "ChromaDB", "FastAPI", "Docker", "Ollama"],
    github: "https://github.com/RajkumarKalapala/portfolio",
    demo: null,
  },
  {
    id: 2,
    icon: Camera,
    title: "CCTV Unified Monitoring Platform",
    category: "Monitoring / Dashboard",
    color: "#00d4ff",
    description:
      "Centralised web platform for monitoring city-wide SIM-based CCTV cameras with real-time online/offline status, geo-map visualisation, ticketing system, and role-based access control.",
    impact: "Reduced camera downtime response time by giving IT teams a single pane of glass.",
    tech: ["Python", "Flask", "SQLite", "HTML5", "JavaScript", "Chart.js"],
    github: "https://github.com/RajkumarKalapala/portfolio",
    demo: "cctv-monitoring-system-wheat.vercel.app",
    featured: true,
  },
  {
    id: 3,
    icon: Monitor,
    title: "Employee Webcam Monitor",
    category: "Workplace Automation",
    color: "#34d399",
    description:
      "Automated employee activity tracking system using computer vision. Detects presence, motion, and attendance patterns — designed for remote team oversight without complex hardware.",
    impact: "Automates manual attendance logging and provides activity analytics.",
    tech: ["Python", "OpenCV", "Flask", "SQLite"],
    github: "https://github.com/RajkumarKalapala/portfolio",
    demo: null,
  },
  {
    id: 4,
    icon: ShoppingCart,
    title: "Full-Stack E-Commerce Platform",
    category: "Web Application",
    color: "#f59e0b",
    description:
      "Production-grade e-commerce platform with product management, cart, orders, wishlists, reviews, JWT authentication, and a full REST API backend.",
    impact: "Deployable out of the box — covers 90% of a standard online store's feature set.",
    tech: ["React", "Node.js", "Express", "MongoDB", "JWT", "Tailwind CSS"],
    github: "https://github.com/RajkumarKalapala/portfolio",
    demo: "ecommerce-frontend-five-lyart.vercel.app",
    featured: false,
  },
  {
    id: 5,
    icon: Shield,
    title: "Security Bash Toolkit",
    category: "Security / Automation",
    color: "#fb7185",
    description:
      "A suite of Linux security scripts: firewall panic mode, system info grabber, IP log parser, and an all-in-one super-tool for rapid incident response on Linux servers.",
    impact: "Cuts incident response setup time from minutes to seconds on any Linux host.",
    tech: ["Bash", "Linux", "iptables", "grep/awk"],
    github: "https://github.com/RajkumarKalapala/portfolio",
    demo: null,
  },
  {
    id: 6,
    icon: Code2,
    title: "USB Device Monitor",
    category: "Security Monitoring",
    color: "#60a5fa",
    description:
      "Real-time USB device detection and logging tool that alerts administrators when unauthorised storage devices are connected — useful for endpoint security in corporate environments.",
    impact: "Provides a lightweight layer of data exfiltration protection with zero infrastructure.",
    tech: ["Python", "Linux", "udev", "SQLite"],
    github: "https://github.com/RajkumarKalapala/portfolio",
    demo: null,
  },
];

function ProjectCard({ project }) {
  const Icon = project.icon;
  return (
    <div className={`glass-card rounded-2xl overflow-hidden flex flex-col ${project.featured ? "ring-1 ring-[#00d4ff]/15" : ""}`}>
      {/* Visual header */}
      <div
        className="h-44 flex items-center justify-center relative overflow-hidden"
        style={{ background: `linear-gradient(135deg, ${project.color}08 0%, ${project.color}04 100%)` }}
      >
        <div className="absolute inset-0 bg-grid opacity-60" />
        {/* Glow orb */}
        <div
          className="absolute w-32 h-32 rounded-full blur-3xl"
          style={{ background: `${project.color}15` }}
        />
        <div
          className="relative w-16 h-16 rounded-2xl flex items-center justify-center"
          style={{ background: `${project.color}15`, border: `1px solid ${project.color}25` }}
        >
          <Icon size={30} style={{ color: project.color }} />
        </div>
        {project.featured && (
          <div
            className="absolute top-3 right-3 px-2.5 py-1 rounded-full text-xs font-mono-custom"
            style={{ background: `${project.color}15`, color: project.color, border: `1px solid ${project.color}30` }}
          >
            Featured
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-6 flex flex-col flex-1">
        <div className="section-tag mb-2" style={{ color: project.color }}>{project.category}</div>
        <h3 className="font-display font-700 text-white text-lg mb-2 leading-snug">{project.title}</h3>
        <p className="text-[#8fa8c8] text-sm leading-relaxed font-body mb-3 flex-1">{project.description}</p>

        {/* Impact */}
        <div
          className="flex items-start gap-2 p-3 rounded-lg mb-4 text-xs"
          style={{ background: `${project.color}08`, border: `1px solid ${project.color}15` }}
        >
          <span style={{ color: project.color }}>↑</span>
          <span className="font-body leading-relaxed" style={{ color: project.color + "bb" }}>{project.impact}</span>
        </div>

        {/* Tech */}
        <div className="flex flex-wrap gap-1.5 mb-5">
          {project.tech.map((t) => (
            <span
              key={t}
              className="px-2 py-0.5 rounded text-xs font-mono-custom text-[#4a6080] border border-white/5 bg-white/2"
            >
              {t}
            </span>
          ))}
        </div>

        {/* Actions */}
        <div className="flex gap-3 mt-auto">
          <a
            href={project.github}
            target="_blank"
            rel="noreferrer"
            className="flex-1 btn-ghost py-2 rounded-lg text-xs flex items-center justify-center gap-1.5"
          >
            <Github size={13} /> Code
          </a>
          {project.demo ? (
            <a
              href={project.demo}
              target="_blank"
              rel="noreferrer"
              className="flex-1 btn-primary py-2 rounded-lg text-xs flex items-center justify-center gap-1.5"
            >
              <ExternalLink size={13} /> Demo
            </a>
          ) : (
            <button
              disabled
              className="flex-1 py-2 rounded-lg text-xs flex items-center justify-center gap-1.5 text-[#4a6080] border border-white/5 cursor-not-allowed"
            >
              <ExternalLink size={13} /> Demo Soon
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Projects() {
  return (
    <section id="projects" className="relative py-28">
      <div className="absolute inset-0 bg-grid opacity-40" />
      <div className="relative max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="section-tag mb-4">// portfolio</div>
          <h2 className="section-title text-4xl md:text-5xl">
            Featured Projects
          </h2>
          <p className="mt-4 text-[#8fa8c8] font-body max-w-xl mx-auto text-sm leading-relaxed">
            Real-world systems built to solve real problems — from AI tools
            to monitoring infrastructure.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-5">
          {projects.map((p) => (
            <ProjectCard key={p.id} project={p} />
          ))}
        </div>

        <div className="mt-10 text-center">
          <a
            href="https://github.com/RajkumarKalapala"
            target="_blank"
            rel="noreferrer"
            className="btn-ghost px-8 py-3 rounded-xl text-sm inline-flex items-center gap-2"
          >
            <Github size={16} /> View All on GitHub
          </a>
        </div>
      </div>
    </section>
  );
}
