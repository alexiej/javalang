from setuptools import setup


setup(
    name="javalang",
    packages=["javalang"],
    version="0.14.0",
    author="Arkadiusz Klemenko",
    author_email="alexiej@wp.pl",
    url="https://github.com/alexiej/javalang",
    description="Pure Python Java parser and tools",
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    long_description="""\
========
Javalang Source
========

Based on the https://github.com/c2nes/javalang 
new version that added get_source, and end_position of the Node.

javalang is a pure Python library for working with Java source
code. javalang provies a lexer and parser targeting Java 8. The
implementation is based on the Java language spec available at
http://docs.oracle.com/javase/specs/jls/se8/html/.

""",
    zip_safe=False,
    install_requires=[
        "six",
    ],
    tests_require=[
        "nose",
    ],
    test_suite="nose.collector",
)
