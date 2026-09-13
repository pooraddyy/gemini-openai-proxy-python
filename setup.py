from setuptools import setup, find_packages

setup(
    name="gemixy",
    version="1.0.0",
    description="Python SDK for Gemini OpenAI Proxy",
    author="pooraddyy",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
