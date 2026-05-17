import { Github, Linkedin, Mail, Heart } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-white/5 py-10 px-6">
      <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center text-black font-display font-bold text-xs">
            RK
          </div>
          <span className="text-[#4a6080] text-sm font-body">
            Rajkumar Kalapala — Freelance Developer
          </span>
        </div>

        <div className="flex items-center gap-4">
          {[
            { icon: Github, href: "https://github.com/RajkumarKalapala" },
            { icon: Linkedin, href: "https://linkedin.com/in/rajkumarkalapala" },
            { icon: Mail, href: "mailto:rajkumarkalapala@gmail.com" },
          ].map(({ icon: Icon, href }) => (
            <a
              key={href}
              href={href}
              target={href.startsWith("http") ? "_blank" : undefined}
              rel="noreferrer"
              className="w-8 h-8 rounded-lg border border-white/6 flex items-center justify-center text-[#4a6080] hover:text-[#00d4ff] hover:border-[#00d4ff]/25 transition-all"
            >
              <Icon size={14} />
            </a>
          ))}
        </div>

        <p className="text-[#4a6080] text-xs font-body flex items-center gap-1.5">
          Built with <Heart size={11} className="text-[#00d4ff]" /> · {new Date().getFullYear()}
        </p>
      </div>
    </footer>
  );
}
