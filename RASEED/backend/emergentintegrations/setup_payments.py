from setuptools import setup, find_namespace_packages

setup(
    name="emergentintegrations-payments",
    version="0.1.0",
    description="Payment integrations for the emergentintegrations library",
    author="Developer",
    author_email="developer@example.com",
    packages=find_namespace_packages(include=["emergentintegrations.payments", "emergentintegrations.payments.*"]),
    install_requires=[
        "requests>=2.25.0",
        "stripe>=4.0.0",
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