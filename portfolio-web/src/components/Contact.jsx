import { useState } from "react";
import { Github, Linkedin, Mail, ExternalLink, Send, MapPin } from "lucide-react";
import emailjs from '@emailjs/browser';

const socials = [
  {
    icon: Github,
    label: "GitHub",
    value: "RajkumarKalapala",
    href: "https://github.com/RajkumarKalapala",
    color: "#e8f0fe",
  },
  {
    icon: Linkedin,
    label: "LinkedIn",
    value: "Connect with me",
    href: "https://www.linkedin.com/in/rajkumar-kalapala-54927a37a",
    color: "#0a66c2",
  },
  {
    icon: Mail,
    label: "Email",
    value: "rajkumarkalapala@gmail.com",
    href: "mailto:rajkumarkalapala@gmail.com",
    color: "#00d4ff",
  },
  {
    icon: ExternalLink,
    label: "Fiverr",
    value: "Rajkumar",
    href: "https://www.fiverr.com/s/Eg8XXBq",
    color: "#1dbf73",
  },
];

export default function Contact() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [sent, setSent] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Placeholder - wire up to EmailJS or Formspree
    setSent(true);
    setTimeout(() => setSent(false), 4000);
    setForm({ name: "", email: "", message: "" });
  };

  return (
    <section id="contact" className="relative py-28">
      <div className="absolute inset-0" style={{background:'radial-gradient(ellipse 60% 50% at 50% 100%, rgba(0,212,255,0.06) 0%, transparent 70%)'}} />
      <div className="relative max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="section-tag mb-4">// get in touch</div>
          <h2 className="section-title text-4xl md:text-5xl">
            Let's Build Together
          </h2>
          <p className="mt-4 text-[#8fa8c8] font-body max-w-xl mx-auto text-sm leading-relaxed">
            Have a project in mind? I'm currently available for freelance work.
            Reach out and let's discuss what you need.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-10">
          {/* Left — socials & info */}
          <div className="space-y-5">
            <div className="flex items-center gap-2 text-[#8fa8c8] text-sm font-body mb-6">
              <MapPin size={14} className="text-[#00d4ff]" />
              Vijayawada, Andhra Pradesh, India · Remote Worldwide
            </div>

            {socials.map(({ icon: Icon, label, value, href, color }) => (
              <a
                key={label}
                href={href}
                target={href.startsWith("http") ? "_blank" : undefined}
                rel="noreferrer"
                className="glass-card rounded-xl p-4 flex items-center gap-4 group no-underline"
              >
                <div
                  className="w-10 h-10 rounded-lg flex items-center justify-center shrink-0"
                  style={{ background: `${color}15`, border: `1px solid ${color}20` }}
                >
                  <Icon size={17} style={{ color }} />
                </div>
                <div>
                  <div className="text-[#4a6080] text-xs font-mono-custom">{label}</div>
                  <div className="text-white text-sm font-body group-hover:text-[#00d4ff] transition-colors">
                    {value}
                  </div>
                </div>
                <ExternalLink size={13} className="ml-auto text-[#4a6080] group-hover:text-[#00d4ff] transition-colors" />
              </a>
            ))}

            {/* Availability badge */}
            <div className="glass-card rounded-xl p-4 mt-4">
              <div className="flex items-center gap-3">
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-400" style={{boxShadow:'0 0 8px #34d399'}} />
                <div>
                  <div className="text-white text-sm font-display font-600">Open to Work</div>
                  <div className="text-[#4a6080] text-xs font-body mt-0.5">
                    Freelance · Contract · Part-time
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right — form */}
          <form onSubmit={sendEmail} className="glass-card rounded-2xl p-7 space-y-5">
            <div>
              <label className="section-tag block mb-2">Your Name</label>
              <input
                type="text"
                name="from_name"
                required
                value={form.name}
                onChange={(e) => setForm({ ...form, name: e.target.value })}
                placeholder="John Smith"
                className="w-full bg-white/3 border border-white/8 rounded-xl px-4 py-3 text-white text-sm font-body placeholder-[#4a6080] focus:outline-none focus:border-[#00d4ff]/40 focus:bg-white/5 transition-all"
              />
            </div>
            <div>
              <label className="section-tag block mb-2">Email</label>
              <input
                type="email"
                name="from_email"
                required
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="john@company.com"
                className="w-full bg-white/3 border border-white/8 rounded-xl px-4 py-3 text-white text-sm font-body placeholder-[#4a6080] focus:outline-none focus:border-[#00d4ff]/40 focus:bg-white/5 transition-all"
              />
            </div>
            <div>
              <label className="section-tag block mb-2">Project Details</label>
              <textarea
                rows={5}
                name="message"
                required
                value={form.message}
                onChange={(e) => setForm({ ...form, message: e.target.value })}
                placeholder="Tell me about your project, timeline, and budget..."
                className="w-full bg-white/3 border border-white/8 rounded-xl px-4 py-3 text-white text-sm font-body placeholder-[#4a6080] focus:outline-none focus:border-[#00d4ff]/40 focus:bg-white/5 transition-all resize-none"
              />
            </div>
            <button
              type="submit"
              className="btn-primary w-full py-3.5 rounded-xl text-sm flex items-center justify-center gap-2"
            >
              {sent ? "Message Sent ✓" : (
                <>Send Message <Send size={14} /></>
              )}
            </button>
            {sent && (
              <p className="text-emerald-400 text-xs font-body text-center">
                Thanks! I'll get back to you within 24 hours.
              </p>
            )}
          </form>
        </div>
      </div>
    </section>
  );
}

const sendEmail = (e) => {
  e.preventDefault();

  emailjs
    .sendForm(
      'service_a00rn7h',
      'template_a6j3c61',
      e.target,
      'j3ijbCyYRKcQBkfTE'
    )
    .then(
      () => {
        alert('Message sent successfully!');
      },
      (error) => {
        alert('Failed to send message.');
        console.log(error);
      }
    );

  e.target.reset();
};