const categories = [
  {
    label: "Frontend",
    color: "#00d4ff",
    skills: ["React", "Next.js", "Tailwind CSS", "HTML5", "CSS3", "JavaScript"],
  },
  {
    label: "Backend",
    color: "#7dd3fc",
    skills: ["Node.js", "Express", "Flask", "FastAPI", "REST APIs", "Python"],
  },
  {
    label: "AI & Automation",
    color: "#a78bfa",
    skills: ["LangChain", "OpenAI API", "RAG Systems", "OpenCV", "Pandas", "Scikit-learn"],
  },
  {
    label: "Databases",
    color: "#34d399",
    skills: ["MongoDB", "SQLite", "PostgreSQL", "ChromaDB"],
  },
  {
    label: "DevOps & Tools",
    color: "#f59e0b",
    skills: ["Git", "Docker", "Linux", "Bash", "GitHub Actions", "Vite"],
  },
  {
    label: "Languages",
    color: "#fb7185",
    skills: ["Python", "JavaScript", "Java", "Bash", "SQL"],
  },
];

export default function Skills() {
  return (
    <section id="skills" className="relative py-28">
      <div className="absolute inset-0 bg-grid opacity-40" />
      <div className="relative max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="section-tag mb-4">// tech stack</div>
          <h2 className="section-title text-4xl md:text-5xl">
            Tools I Work With
          </h2>
          <p className="mt-4 text-[#8fa8c8] font-body max-w-lg mx-auto text-sm leading-relaxed">
            A curated toolkit built over years of real project work across web development,
            AI, automation, and security.
          </p>
        </div>

        {/* Category grid */}
        <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {categories.map(({ label, color, skills }) => (
            <div key={label} className="glass-card rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-5">
                <div
                  className="w-2 h-2 rounded-full"
                  style={{ background: color, boxShadow: `0 0 8px ${color}` }}
                />
                <span
                  className="font-display font-600 text-sm"
                  style={{ color }}
                >
                  {label}
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {skills.map((s) => (
                  <span
                    key={s}
                    className="px-2.5 py-1 rounded-md text-xs font-mono-custom text-[#8fa8c8] border border-white/6 bg-white/3 hover:border-white/15 hover:text-white transition-colors duration-150 cursor-default"
                  >
                    {s}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
