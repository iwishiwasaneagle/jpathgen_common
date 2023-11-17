import fnmatch
import glob
import os
import shutil
import subprocess
import sys

from setuptools import setup, find_packages
from setuptools.command.build_py import build_py as _build_py

if "PROTOC" in os.environ and os.path.exists(os.environ["PROTOC"]):
    protoc = os.environ["PROTOC"]
else:
    protoc = shutil.which("protoc")


class BuildPyCmd(_build_py):
    def run(self):
        for proto in glob.glob("**/*.proto"):
            protoc_command = [protoc, "-Isrc", "--python_out=.", proto]
            if subprocess.call(protoc_command) != 0:
                sys.exit(-1)
        _build_py.run(self)


if __name__ == "__main__":
    setup(
        name="jpathgen_common",
        packages=find_packages(where="src"),
        cmdclass={
            "build_py": BuildPyCmd,
        },
        install_requires=["protobuf"],
        python_requires=">=3.8",
    )
