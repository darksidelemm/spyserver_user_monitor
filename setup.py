import os
import pathlib
import re
import sys
from setuptools import setup, find_packages

assert sys.version_info >= (3, 6, 0), "spyserver_user_monitor requires Python 3.6+"

THIS_DIR = pathlib.Path(__file__).parent


def get_version() -> str:
    init_file = THIS_DIR / "src" / "spyserver_user_monitor" / "__init__.py"
    version_re = re.compile(r".*__version__\s=\s+[\'\"](?P<version>.*?)[\'\"]")
    with open(init_file, "r", encoding="utf8") as init_fd:
        match = version_re.search(init_fd.read())
        if match:
            version = match.group("version")
        else:
            raise RuntimeError(f"Cannot find __version__ in {init_file}")
        return version


def get_long_description() -> str:
    readme_file = THIS_DIR / "README.md"
    with open(readme_file, encoding="utf8") as fd:
        readme = fd.read()
    return readme


if __name__ == "__main__":
    setup(
        name="spyserver_user_monitor",
        description="spyserver_user_monitor provides utilities for monitoring usage of a spyserver",
        long_description=get_long_description(),
        long_description_content_type="text/markdown",
        version=get_version(),
        author="Mark Jessop",
        python_requires=">=3.6",
        install_requires=[
            "flask",
            "flask_socketio"

        ],
        dependency_links=[
        ],
        package_dir={"": "src"},
        packages=find_packages("src"),
        extras_require={
            "develop": ["black", "pylint", "wheel"],
        },
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Developers",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
        keywords=["spyserver", "network", "monitor"],
        # entry_points = {
        #     'console_scripts': [
        #         'spyserver-monitor = spyserver_user_monitor.monitor:main',
        #     ]
        # },
    )
