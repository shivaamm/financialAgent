from setuptools import setup, find_namespace_packages

setup(
    name="emergentintegrations-llm",
    version="0.1.1",
    description="LLM service integrations for the emergentintegrations library",
    author="Developer",
    author_email="developer@example.com",
    packages=find_namespace_packages(include=["emergentintegrations.llm", "emergentintegrations.llm.*"]),
    install_requires=[
        "requests>=2.25.0",
        "openai>=1.0.0",
        "litellm>=1.0.0",
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "aiohttp>=3.8.0",
        "google-generativeai>=0.3.0",
        "Pillow>=10.0.0",
        "google-genai"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)