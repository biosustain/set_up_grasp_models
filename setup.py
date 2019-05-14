import setuptools

setuptools.setup(
    name="set_up_models",
    version="0.1.0",
    author="Marta Matos",
    author_email="marta.ra.matos@gmail.com",
    description="A package to set up and check GRASP input files",
    url="https://github.com/martamatos/set_up_grasp_models",
    packages=setuptools.find_packages(),
    install_requires=["numpy", "pandas", "xlrd"],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3.6+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
