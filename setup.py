from distutils.core import setup

PACKAGE = "Chern"
NAME = "Chern"
DESCRIPTION = "A data analysis framework for High Energy Physics"
AUTHOR = "Mingrui Zhao"
AUTHOR_EMAIL = "mingrui.zhao@mail.labz0.org"
URL = "https://github.com/zhaomr13/Chern"
VERSION = __import__(PACKAGE).__version__

setup(
    name = NAME,
    version = VERSION,
    description = DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="Apache License, Version 2.0",
    url = URL,
    packages=["Chern"],
    classifiers = [

    ],
    zip_safe=False
)
