from setuptools import setup, find_packages

setup(
    name='preflight',
    version='0.0.1',
    description = "Preflight check system.",
    package_dir={
        '': 'src',
    },
    packages=find_packages(where="src"),
    # install_requires=[""],
    # entry_points={  # Optional
    #     "console_scripts": [
    #         "sample=sample:main",
    #     ],
    # },
)