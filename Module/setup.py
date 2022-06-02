import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Projet_ADEME",
    version="0.0.1",
    author="Group_2",
    author_email="ray-hann06@hotmail.fr",
    description="Small Project used to determine an next to optimal delivery road ",
    long_description="A delivery road optimisation is needed to limit the dioxide carbon release in the atmosphere for that we created an algoritm letting the ability to determine a next to optimal road",
    long_description_content_type="text/markdown",
    url="https://github.com/rayray06/AlgoAv/tree/master/Module/AlgoAV",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "AlgoAV"},
    packages=setuptools.find_packages(where="AlgoAV"),
    python_requires=">=3.8",
)