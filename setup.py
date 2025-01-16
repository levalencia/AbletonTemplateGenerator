from setuptools import setup, find_packages

setup(
    name="ableton_template_generator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pydantic>=2.0.0",
        "click>=8.0.0",
        "rich>=13.0.0",
        "pytest>=7.0.0",
        "pyyaml>=6.0.0",
        "requests>=2.0.0",
        "notebook>=6.0.0",
        "python-dotenv>=0.19.0",
        "pandas",
        "plotly",
        "pyyaml"
    ],
    author="Luis Valencia",
    author_email="levm38@outlook.com",
    description="A tool for generating Ableton Live templates based on musical genres"
)