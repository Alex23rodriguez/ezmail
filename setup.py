import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ezmail",
    version="1.0.3",
    author="Alex Rodriguez",
    author_email="alex.rodriguez.oro@gmail.com",
    description="easily send out emails via SMTP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Alex23rodriguez/ezmail",
    packages=setuptools.find_packages(),
    keywords=["python", "mail", "smtp", "cli"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["python-dotenv"],
    python_requires=">=3.7",
)
