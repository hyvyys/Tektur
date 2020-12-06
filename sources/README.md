# Tektur sources

The preferred modification format is FontLab 7 `.vfj`.
The `UFO/*.designspace` files are not as exported from FontLab and should not be overwritten.

## Exporting FontLab sources to UFO

1. Export `DesignSpace+UFO` from FontLab (Destination: Source, Subfolders by: none).
2. For each master, build `mark/mkmk` features in FontLab and export them using the `exportFeatures.py` script from within FontLab. This is preferred because FontLab cannot export correct `mark/mkmk` for each master on its own and only exports these features as created, duplicating one master’s features in all masters. (Google Fonts is no better and strips mark attachment features from the webfonts altogether, but whatever).
3. Move the `masters` directory from `/sources/FontLab/` to `/sources/UFO/`.

## Building the fonts

Make sure you have Python 3 installed. Create a `virtualenv` if you like. Install prerequisites from `/requirements.txt`.

1. Open terminal in `/sources`. Run `./build.sh`.