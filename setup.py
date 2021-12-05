from setuptools import setup

setup(
        name="imgsort",
        version="1.1",
        description="A program that lets you easily sort images into different folders.",

        author="Matthias Quintern",
        author_email="matthiasqui@protonmail.com",

        url="https://github.com/MatthiasQuintern/imgsort.git",

        license="GPLv3",

        packages=["imgsort"], #, "imgsort.sorter", "imgsort.config"],
        # packages=setuptools.find_packages(),
        install_requires=["ueberzug"],

        classifiers=[
            "Operating System :: POSIX :: Linux",
            "Environment :: Console :: Curses",
            "Programming Language :: Python :: 3",
            "Topic :: Multimedia :: Graphics",
            "Topic :: Utilities",
            ],

        # scripts=["bin/imgsort"],
        entry_points={
            "console_scripts": [ "imgsort=imgsort.sorter:main" ],
            },
)


