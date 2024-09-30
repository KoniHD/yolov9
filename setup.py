from setuptools import setup, find_packages

setup(
    name="yolov9",
    version="0.1",
    packages=find_packages(),
    author="KoniHD",
    author_email="konstantin.zeck+github@gmail.com",
    install_requires=[
        # Base ------------------------------------------------------------------------
        "gitpython",
        "ipython",
        "matplotlib>=3.2.2",
        "numpy>=1.18.5",
        "opencv-python>=4.1.1",
        "Pillow>=7.1.2, <10.0.0",
        "psutil",
        "PyYAML>=5.3.1",
        "requests>=2.23.0",
        "scipy>=1.4.1",
        "thop>=0.1.1",
        "torch>=1.7.0",
        "torchvision>=0.8.1",
        "tqdm>=4.64.0",

        # Logging ---------------------------------------------------------------------
        "tensorboard>=2.4.1",

        # Plotting --------------------------------------------------------------------
        "pandas>=1.1.4",
        "seaborn>=0.11.0",

        # Extras ----------------------------------------------------------------------
        "albumentations>=1.0.3",
        "pycocotools>=2.0",

    ],
    description="YOLOv9 package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KoniHD/yolov9",
)