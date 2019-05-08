import setuptools

setuptools.setup(
    name="set_up_grasp_models",
    version="0.1.0",
    author="Marta Matos",
    author_email="mrama@biosustain.dtu.dk",
    description="A package to set up and check GRASP input files",
    long_description_content_type="text/markdown",
    url="https://github.com/martamatos/set_up_grasp_models",
    packages=['pandas', 'numpy'],
    python_requires='=3.6+',
    classifiers=[
        "Programming Language :: Python :: 3.6+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
)
