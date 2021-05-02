import io
import os
import setuptools

os.environ["DISTUTILS_DEBUG"] = "1"

Version = io.open("VERSION").read().strip().split(".")

Path = os.path.abspath(os.path.dirname(__file__))
Installer = setuptools.setup
Packages = setuptools.find_packages

URLs = {}

Requirements = []

Dependencies = []

Databases = []

Classifiers = []

setuptools.setup(
    name="MFC API",
    version=".".join(Version),
    author="Price Hiller",
    author_email="philler3138@gmail.com",
    download_url="https://gitlab.cloud-technology.io/MFC/MFC-ELO",
    description="",
    project_urls=URLs,
    long_description="",
    long_description_content_type="text/markdown",
    url="https://gitlab.cloud-technology.io/MFC/MFC-ELO",
    packages=Packages(),
    classifiers=Classifiers,
    package_data={
        ".": [
            "setup.*",
            "*.cfg",
            "*.md",
            "requirements.txt",
            "VERSION"
        ], "API": [
            "log_config.yaml"
        ]
    },
    python_requires=">=3.9",
    include_package_data=True,
    zip_safe=False,
    requires=Requirements,
    install_requires=Dependencies,
    py_modules=[],
    include_dirs=True,
)
