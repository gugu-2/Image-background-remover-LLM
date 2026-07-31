# Setup Guide

This document explains how to set up the Image Background Remover project on your local machine for development or personal use.

## Prerequisites

- **Python 3.8+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).
- **Git** (Optional): If you plan to clone the repository, ensure Git is installed.

## 1. Create a Virtual Environment

It is highly recommended to install the dependencies in a virtual environment to avoid conflicts with other Python packages on your system.

**On Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**On macOS and Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

## 2. Install the Package

With your virtual environment activated, install the `bg_remover` package and its dependencies. Running the following command in the root directory (where `setup.py` is located) will install the tool in "editable" mode:

```bash
pip install -e .
```

This command will install:
- `rembg` (The core AI model for background removal)
- `fastapi` & `uvicorn` (For the API web server)
- All required dependencies.

> [!NOTE]
> The first time you process an image, `rembg` will download the pre-trained AI model weights (~170MB). This happens automatically and will only occur once.

## 3. Verify Installation

To ensure everything was installed correctly, run the CLI help command:

```bash
bg-remover --help
```

You should see the help text explaining the usage of the tool!

Next, check out how to use the CLI in [CLI Usage](cli_usage.md) or how to start the API in [API Usage](api_usage.md).
