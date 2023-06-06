# Tektur sources

The preferred modification format is FontLab 7 `.vfj`. TypeRig is recommended for exporting features.
The `UFO/*.designspace` files are not as exported from FontLab and should not be overwritten.


## Exporting FontLab sources to UFO

1. Export `DesignSpace+UFO` from FontLab (Destination: Source, Subfolders by: none).
2. For each master, build `mark/mkmk` features in FontLab and export them from FontLab using the `exportFeatures.py` script (which uses TypeRig). This is preferred because FontLab cannot export correct `mark/mkmk` for each master on its own and only exports these features as created, duplicating one master’s features in all masters.
3. Move the `masters` directory from `/sources/FontLab/` to `/sources/UFO/`.


## Setting up a build environment

A macOS/ Linux system is recommended. Under Windows, you can use a Linux Subsystem for Windows.
Make sure you have Python 3 installed and create a `virtualenv`.

### Set up Python and venv on Linux/WSL:

```bash
sudo apt-get update
sudo apt install python3-virtualenv
virtualenv --python=/usr/bin/python3 ./build
python3 -m venv ./build
```

or

### Set up Python and venv on macOS:

Install [brew](https://brew.sh/index_pl), then:

```bash
brew install python3
python3 -m venv ./build
```

### Activate the `virtualenv`:

```bash
source ./build/bin/activate
```

### Install prerequisites from `/requirements.txt`:

```bash
pip install -r ./requirements.txt
```

## Building the fonts

Open terminal in `/sources`. Run `./build.sh`. If needed, set execution permissions for the build and test scripts first:

```bash
sudo chmod 777 ./build.sh
sudo chmod 777 ./test.sh
```