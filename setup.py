from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name="exporter",
    version="0.0.4",
    author="Hasan Yaman",
    author_email="hasannyaman@gmail.com",
    description="exporter helps to export Jupyter notebooks as a Python script.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hasan-yaman/Exporter",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        'nbformat',
        'imgkit',
        'Pygments'
    ],
    entry_points={
        'console_scripts': [
            'exporter=exporter.console_script:run_export_console_script',
            'image-exporter=exporter.console_script:run_image_export_console_script'
        ]
    }
)
