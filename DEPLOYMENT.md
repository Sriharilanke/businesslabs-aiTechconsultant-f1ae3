# 🚀 Deployment Guide: Vercel & Netlify

This repository is **pre-configured for zero-configuration, 1-click deployments** to both **Vercel** and **Netlify**.

The frontend dashboard includes **intelligent dual-mode architecture**:
- **Cloud Mode (Vercel / Netlify):** Zero server setup required. Complete client-side simulation with instant grounding, multi-source citations, screenshot inspection modals, prompt guardrail escalation, customer inbox drafts, diff engine, and Jira/Linear synchronization.
- **Local Dev Mode:** Automatically connects to live backend services on ports `8001` (Task 1 Knowledge Brain), `8002` (Task 2 Inbox Agent), and `8003` (Task 3 Meeting to Scope).

---

## ⚡ Option 1: Deploy to Vercel (1-Click)

The repository includes a ready-to-use [`vercel.json`](./vercel.json) root configuration.

### Method A: Via GitHub Web Dashboard (Recommended)
1. Go to [vercel.com/new](https://vercel.com/new) and log in with your GitHub account.
2. Select your repository: **`Sriharilanke/businesslabs-aiTechconsultant`**.
3. In the configuration screen:
   - **Framework Preset:** Leave as `Other` or `None`.
   - **Root Directory:** `./` (Leave default — `vercel.json` automatically maps `outputDirectory: "frontend-dashboard"`).
   - **Build Command:** Leave empty.
   - **Output Directory:** Leave default (managed by `vercel.json`).
4. Click **Deploy**.
5. Your dashboard will be live at `https://businesslabs-aitechconsultant.vercel.app` in under 30 seconds!

### Method B: Via Vercel CLI
```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## 🌐 Option 2: Deploy to Netlify (1-Click)

The repository includes a ready-to-use [`netlify.toml`](./netlify.toml) root configuration.

### Method A: Via GitHub Web Dashboard (Recommended)
1. Go to [app.netlify.com/start](https://app.netlify.com/start) and connect your GitHub account.
2. Choose your repository: **`Sriharilanke/businesslabs-aiTechconsultant`**.
3. Netlify will **automatically detect `netlify.toml`**:
   - **Publish directory:** `frontend-dashboard` (auto-detected).
   - **Build command:** (none needed).
4. Click **Deploy site**.
5. Your dashboard will be live at `https://businesslabs-aitechconsultant.netlify.app` instantly!

### Method B: Via Netlify CLI
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir=frontend-dashboard
```

---

## 🛠️ Configuration Files Reference

| File | Purpose | Location |
| :--- | :--- | :--- |
| [`vercel.json`](./vercel.json) | Vercel routing, static directory mapping, and HTTP security headers | Repository Root |
| [`frontend-dashboard/vercel.json`](./frontend-dashboard/vercel.json) | Fallback Vercel config if imported with `frontend-dashboard` root | `frontend-dashboard/` |
| [`netlify.toml`](./netlify.toml) | Netlify publish directory, 200 rewrites, and security headers | Repository Root |
| [`index.html`](./index.html) | Fail-safe landing and immediate redirect to `/frontend-dashboard/` | Repository Root |

---

## 🔒 Security Headers Included
Both `vercel.json` and `netlify.toml` automatically enforce enterprise HTTP security headers:
- `X-Frame-Options: DENY` (Clickjacking mitigation)
- `X-Content-Type-Options: nosniff` (MIME sniffing prevention)
- `X-XSS-Protection: 1; mode=block` (Cross-site scripting protection)
- `Referrer-Policy: strict-origin-when-cross-origin` (Privacy enforcement)

---

## 🧪 Local Verification Before Deployment
To preview the static build locally just like Vercel or Netlify would serve it:
```bash
# Serve frontend directly
python -m http.server 8000 --directory frontend-dashboard
```
Open [http://localhost:8000](http://localhost:8000) in your browser. All interactive features, animations, audio synthesizer, and scenarios run immediately!
