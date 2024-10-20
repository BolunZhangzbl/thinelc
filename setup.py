from setuptools import setup, Extension
import os
import sys

include_path = os.path.abspath(os.path.dirname(__file__))

# Modify extra_compile_args based on platform
if sys.platform == 'win32':
    extra_compile_args = ["/std:c++11", "/W3", "/O2"]  # MSVC compatible flags
    extra_link_args = ["/DEBUG"]
else:
    extra_compile_args = ["-std=c++11", "-Wall", "-Wextra", "-O3"]
    extra_link_args = ["-g"]

extensions = [
    Extension(
        name="thinelc.thinelc",
        sources=["thinelc/thinelc.pyx"],
        language="c++",   
        extra_compile_args=extra_compile_args,
        extra_link_args=extra_link_args,
    )
]

def extensions_func():
    from Cython.Build import cythonize
    extensions = [
        Extension(
            name="thinelc.thinelc",
            sources=["thinelc/thinelc.pyx"],
            language="c++",
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        )
    ]

    return cythonize(extensions, compiler_directives={"language_level": "3"}, gdb_debug=True, force=True)

setup(
    version="0.01",
    name="thinelc",
    author="Bolun Zhang",
    author_email="bolun_zhangzbl@outlook.com",
    description="A thin ELC Wrapper for Python",
    url="https://github.com/BolunZhangzbl/thinelc",
    packages=["thinelc"],
    ext_modules=extensions_func(),
    setup_requires=["Cython"],
    install_requires=["Cython"],
)   