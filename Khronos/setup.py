import setuptools

setuptools.setup(
    name="django-khronos",
    version="0.1.0",
    description="Python package to benchmark django test time",
    long_description="",
    author="Abhinav Prakash",
    author_email="abhinavsp0730@gmail.com",
    license="MIT License",
    package_dir={"": "src"},
    packages=setuptools.find_namespace_packages(where="src"),
    zip_safe=False,
    install_requires=["rich>=13.3.5", "gspread>=5.9.0"],
    python_requires=">=3.9",
)
