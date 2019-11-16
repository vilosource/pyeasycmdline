from setuptools import setup, find_packages

setup(
    name="pyeasycmdline",
    version="0.1.0",
    description="A YAML-driven command-line interface framework",
    author="JV",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyyaml",
        "colorlog",  # For colored console logging (optional)
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    entry_points={
        "console_scripts": [
            "easycmdline=easycmdline.cli:run",
        ],
    },
    python_requires=">=3.9",
)
