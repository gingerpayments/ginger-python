import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ginger-sdk",
    version="2.0.0",
    author="Ginger Payments",
    author_email="dev@gingerpayments.com",
    description="The official Ginger Payments Python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gingerpayments/ginger-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.6',
)