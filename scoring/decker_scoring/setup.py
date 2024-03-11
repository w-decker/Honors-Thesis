from setuptools import setup, find_packages

setup(
    name="decker_scoring",
    version="1.0.0",
    author="Will Decker",
    author_email="deckerwill7@gmail.com",
    description="Scoring behvarioal data for Will Decker's honors thesis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering"
    ],
    python_requires='>=3.8',
    install_requires=['pandas', 
                      'matplotlib',
                      'numpy']
)