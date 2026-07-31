# Image Background Remover Pro

A complete ecosystem for removing backgrounds from images using state-of-the-art AI. 
This project features a **Windows Desktop Application**, a **Developer CLI**, and an **API Service** that you can host on your own server.

## 📥 Download the Desktop App

The easiest way to use the Background Remover is via our fully packaged Windows software! It features a stunning High-Fidelity UI, an AI auto-remover, and manual touch-up tools (Brush and Eraser).

👉 **[Download Background Remover Pro Setup.exe](desktop-app/dist-electron/Background%20Remover%20Pro%20Setup%200.0.0.exe)**

*Simply download the `Setup.exe` file and double-click to install. No Python installation required!*

---

## 📚 Documentation Index

If you are a developer looking to use the CLI, API, or modify the source code, we have comprehensive documentation covering every aspect of the project in the `docs/` folder:

1. **[Setup Guide](docs/setup.md)**: How to set up your local environment and install the Python package.
2. **[CLI Usage Guide](docs/cli_usage.md)**: How to use the `bg-remover` terminal commands for single and batch processing.
3. **[API Usage Guide](docs/api_usage.md)**: How to run the local web server and integrate the background removal API into your own apps (with cURL, Python, and JS examples).
4. **[Deployment Guide](docs/deployment.md)**: How to deploy your API to production using Docker or Gunicorn.
5. **[System Architecture](docs/architecture.md)**: A technical overview and data-flow diagram explaining how the system components interact.

---

## 🛠️ Developer Quick Start (CLI & API)

If you want to use the python tools directly instead of the desktop app:

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate  # (Windows: .\venv\Scripts\activate)

# 2. Install the package
pip install -e .

# 3. Process an image via CLI!
bg-remover --input photo.jpg --output clean.png

# 4. Or start the API server!
bg-remover-api
```

## 🏗️ Desktop App Development

To work on the Electron/React desktop application:

```bash
cd desktop-app
npm install

# Run in development mode (starts Vite and Electron)
npm run dev

# Package for Windows
npm run electron:build
```
