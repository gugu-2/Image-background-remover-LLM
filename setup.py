from setuptools import setup, find_packages

setup(
    name="bg_remover",
    version="1.0.0",
    description="A CLI and API tool for removing image backgrounds.",
    packages=find_packages(),
    install_requires=[
        "rembg[cpu]",
        "fastapi",
        "uvicorn",
        "python-multipart"
    ],
    entry_points={
        "console_scripts": [
            "bg-remover=bg_remover.cli:main",
        ]
    }
)
