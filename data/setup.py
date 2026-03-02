from setuptools import setup, find_packages

setup(
    name="detect-towers",
    version="0.1.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "ultralytics>=8.1.0",
        "opencv-python-headless>=4.7.0",
        "numpy>=1.25.0",
        "Pillow>=10.0.0",
        "matplotlib>=3.8.0",
        "folium>=0.18.0",
    ],
    entry_points={
        "console_scripts": [
            "detect-towers=detect_towers.cli:main",
        ],
    },
)
