from setuptools import setup, find_packages

setup(
    name="food-tetris",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.5.2",
    ],
    entry_points={
        'console_scripts': [
            'food-tetris=food_tetris:main',
        ],
    },
    author="Gabriel Baldwin",
    description="A food-themed Tetris game",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/food-tetris",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        "": ["images/*"],
    },
) 