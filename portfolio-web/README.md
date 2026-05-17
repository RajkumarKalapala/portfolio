# Rajkumar Kalapala — Freelance Developer Portfolio

A professional freelancer portfolio built with **React + Vite + Tailwind CSS**.

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev
# → Open http://localhost:5173

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📁 Project Structure

```
src/
├── components/
│   ├── Navbar.jsx       # Sticky nav with mobile menu
│   ├── Hero.jsx         # Hero section with typewriter
│   ├── About.jsx        # About / positioning section
│   ├── Skills.jsx       # Tech stack grid
│   ├── Services.jsx     # Service cards (client-focused)
│   ├── Projects.jsx     # Featured project cards
│   ├── Contact.jsx      # Contact form + social links
│   └── Footer.jsx       # Footer
├── App.jsx
├── main.jsx
└── index.css            # Tailwind + custom CSS
```

## ✏️ Customisation Checklist

### Update Your Info
- [ ] `src/components/Hero.jsx` — Update name, GitHub/LinkedIn/email URLs
- [ ] `src/components/About.jsx` — Edit bio text
- [ ] `src/components/Projects.jsx` — Update GitHub links and add live demo URLs
- [ ] `src/components/Contact.jsx` — Update email, LinkedIn, Fiverr link
- [ ] `src/components/Footer.jsx` — Update links

### Contact Form
The form currently shows a success message but doesn't send emails.
To make it functional, integrate one of:
- **EmailJS** (free tier, no backend needed)
- **Formspree** (drop-in form API)
- **Web3Forms**

Example with EmailJS:
```js
import emailjs from '@emailjs/browser';
emailjs.send('SERVICE_ID', 'TEMPLATE_ID', form, 'PUBLIC_KEY');
```

### Add Project Screenshots
Replace the icon placeholders in `Projects.jsx` by adding:
```jsx
<img src="/screenshots/cctv-monitor.png" alt="CCTV Monitor" className="w-full h-full object-cover" />
```
Place images in `public/screenshots/`.

## 🌐 Deployment

### Vercel (Recommended — Free)
```bash
npm install -g vercel
vercel
```

### Netlify
```bash
npm run build
# Upload the `dist/` folder to app.netlify.com
```

### GitHub Pages
```bash
npm install -D gh-pages
# Add to package.json: "homepage": "https://RajkumarKalapala.github.io/portfolio"
npm run build && gh-pages -d dist
```

## 🎨 Design System

| Token | Value |
|-------|-------|
| Background | `#080c14` |
| Card | `rgba(15,24,41,0.9)` |
| Accent Cyan | `#00d4ff` |
| Text Primary | `#e8f0fe` |
| Text Secondary | `#8fa8c8` |
| Font Display | Syne |
| Font Body | Outfit |
| Font Mono | JetBrains Mono |

## 📦 Tech Stack
- React 18
- Vite 8
- Tailwind CSS 3
- Lucide React (icons)
- Google Fonts (Syne, Outfit, JetBrains Mono)
