# Purepy Documentation

This directory contains the documentation for Purepy, built with VitePress.

## Setup

1. Install dependencies:

```bash
npm install
```

2. Start development server:

```bash
npm run docs:dev
```

3. Build for production:

```bash
npm run docs:build
```

4. Preview production build:

```bash
npm run docs:preview
```

## Structure

```
docs/
├── .vitepress/
│   └── config.js          # VitePress configuration
├── public/
│   └── pure.svg           # Logo and static assets
├── guide/                 # Chinese documentation
│   ├── index.md           # What is Purepy?
│   ├── installation.md    # Installation guide
│   ├── getting-started.md # Quick start guide
│   └── basic-usage.md     # Basic usage
├── en/                    # English documentation
│   ├── index.md           # English homepage
│   └── guide/
│       └── index.md       # What is Purepy? (English)
├── api/
│   └── index.md           # API reference
├── index.md               # Homepage
└── package.json           # Dependencies
```

## Contributing

When adding new documentation:

1. Add the page to the appropriate language directory
2. Update the sidebar configuration in `.vitepress/config.js`
3. Follow the existing naming conventions
4. Include both Chinese and English versions when possible

## Deployment

The documentation can be deployed to any static hosting service like:

- GitHub Pages
- Netlify
- Vercel
- Cloudflare Pages

Build the documentation with `npm run docs:build` and deploy the `docs/.vitepress/dist` directory.
