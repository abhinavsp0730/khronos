import setuptools

with open(r'README.md', "r") as file:
  long_desc = file.read()

setuptools.setup(
    name="django-khronos",
    version="0.1.1",
    description="Khronos is a Python library that benchmarks the duration of Django tests. It helps identify slow-running tests in your test suite, allowing you to optimize their performance.",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    author="Abhinav Prakash",
    author_email="abhinavsp0730@gmail.com",
    license="MIT License",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    zip_safe=False,
    install_requires=["rich>=13.3.5", "gspread>=5.9.0"],
    python_requires=">=3.9",
    url="https://github.com/abhinavsp0730/khronos/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
