"""
Setup configuration for PDF Invoice Combiner
"""
from setuptools import setup, find_packages
from pathlib import Path

# 读取 README 用作长描述
here = Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="pdf-invoice-combiner",
    version="1.0.0",
    description="Intelligently combine multiple PDF pages into A4 pages (2-per-page layout)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/pdf-invoice-combiner",
    author="Your Name",
    author_email="your.email@example.com",
    license="MIT",
    keywords="pdf invoice merge combine a4",
    project_urls={
        "Bug Reports": "https://github.com/your-username/pdf-invoice-combiner/issues",
        "Source": "https://github.com/your-username/pdf-invoice-combiner",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business",
        "Topic :: Multimedia :: Graphics",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pymupdf>=1.26.0",
    ],
    extras_require={
        "dev": ["pyinstaller>=5.0"],
    },
    entry_points={
        "console_scripts": [
            "combine_pdfs=combine_pdfs_two_per_a4:main",
        ],
    },
)
