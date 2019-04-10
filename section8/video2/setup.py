import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="oware-client-server",

    version="0.0.1",

    author="Daniel Arbuckle",
    author_email="daniel@arbuckle-everything.com",

    description="Oware game client and server",
    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/fake/use_your_real_project_homepage",

    packages=setuptools.find_packages(),

    package_data={
        'oware.client': ['data/*'],
    },

    # A list of valid classifies is at https://pypi.org/classifiers/
    # We should always include Python version, license, and operating
    # system classifiers, but there are others that we can add as well
    # to help people find our software
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[
        'Kivy>=1.10.1',
    ],

    python_requires='>=3.7',
)
