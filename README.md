# Dicom Art

Misc helpers for creating visualizations using DICOM images and matplotlib.
Anything related to creating visualizations using DICOMS could find a home here.

## `DicomPlotter` and `CINEPlotter`

These classes provide similar interfaces for easy visualization of points on
a DICOM/CINE data set. `DicomPlotter` expects a dicom image (from pydicom) and
`CINEPlotter` expects "cine data" (a dict of dicom objects) that can be read
using `dicom_utils.read_cine_dir`.

## Examples

A concrete example of the use of `DicomPlotter` can be found in
`cathy/cli.scatter` where it is used to draw catheter coordinates on top of a
dicom image.