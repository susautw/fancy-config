from pathlib import Path

from setuptools import setup, find_namespace_packages

package_dir = Path(__file__).parent
readme_file = package_dir / "README.md"
requirements_file = package_dir.parent.parent / "requirements.txt"

with readme_file.open() as fp:
    long_description = fp.read()

with requirements_file.open() as fp:
    requirements = [r.strip() for r in fp.readlines()]


setup(
    name="fancy-config",
    version="0.13.4",
    packages=find_namespace_packages("src"),
    package_dir={"": "src"},
    package_data={
        "": ["*.md", "*.txt", "*.pyi"],
    },

    # metadata to display on PyPI
    author="su-rin",
    author_email="susautw@gmail.com",
    description="config",
    license="MIT",
    keywords="config",
    project_urls={
        "Source Code": "https://github.com/susautw/fancy-config",
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements
)
