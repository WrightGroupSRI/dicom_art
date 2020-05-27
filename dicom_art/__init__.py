import numpy
import matplotlib.pyplot as plt
import dicom_utils


def _get_nearest_key(d, k):
    return d[min(d.keys(), key=lambda u: abs(u - k))]


def _minmax(vec):
    return numpy.min(vec), numpy.max(vec)


class CinePlotter(object):
    def __init__(self, cine_data):
        self.cine_data = cine_data
        self._exemplar = list(list(cine_data.values())[0].values())[0]
        # transpose because we act on row vectors not column vectors.
        self._w2p = numpy.transpose(dicom_utils.world_to_pixel(self._exemplar))

    def plot(self, points, ax=None, plot_args=None, plot_kwargs=None):
        if ax is None:
            ax = plt
        if plot_args is None:
            plot_args = ["."]
        if plot_kwargs is None:
            plot_kwargs = {}
        # Plot points in image coords, y is flipped
        points = self._local_coords(points)
        ax.plot(points[:, 0], -points[:, 1], *plot_args, **plot_kwargs)

    def imshow(self, trigger, coord, ax=None, imshow_args=None, imshow_kwargs=None):
        if ax is None:
            ax = plt
        if imshow_args is None:
            imshow_args = []
        if imshow_kwargs is None:
            imshow_kwargs = dict(cmap="gray")
        image = self._pick_image(trigger, coord)
        ax.imshow(image.pixel_array, *imshow_args, **imshow_kwargs)

    def focus_on(self, points, ax=None, margin=15):
        if ax is None:
            ax = plt
        points = self._local_coords(points)
        center = numpy.mean(points, axis=0)
        xmin, xmax = _minmax(points[:, 0])
        ymin, ymax = _minmax(-points[:, 1])
        window = max((numpy.abs(xmax - xmin), numpy.abs(ymax - ymin))) + margin
        ax.set_xlim(xmin=center[0] - window, xmax=center[0] + window)
        ax.set_ylim(ymin=window - center[1], ymax=-center[1] - window)

    def _local_coords(self, points):
        points = numpy.concatenate((points, numpy.ones((points.shape[0], 1))), axis=1)
        points = points @ self._w2p
        return points

    def _pick_image(self, trigger, coord):
        slice_data = _get_nearest_key(
            self.cine_data, dicom_utils.dicom_slice_direction(self._exemplar, coord)
        )
        image = _get_nearest_key(slice_data, trigger)
        return image


class DicomPlotter(object):
    def __init__(self, dcm):
        self._dcm = dcm
        self._w2p = numpy.transpose(dicom_utils.world_to_pixel(self._dcm))

    def plot(self, points, ax=None, plot_args=None, plot_kwargs=None):
        if ax is None:
            ax = plt
        if plot_args is None:
            plot_args = ["."]
        if plot_kwargs is None:
            plot_kwargs = {}
        # Plot points in image coords, y is flipped
        points = self._local_coords(points)
        # ax.plot(points[:, 0], -points[:, 1], *plot_args, **plot_kwargs)
        ax.plot(points[:, 0], points[:, 1], *plot_args, **plot_kwargs)

    def imshow(self, ax=None, imshow_args=None, imshow_kwargs=None):
        if ax is None:
            ax = plt
        if imshow_args is None:
            imshow_args = []
        if imshow_kwargs is None:
            imshow_kwargs = dict(cmap="gray")
        image = self._dcm
        ax.imshow(image.pixel_array, *imshow_args, **imshow_kwargs)

    def focus_on(self, points, ax=None, margin=15):
        if ax is None:
            ax = plt
        points = self._local_coords(points)
        center = numpy.mean(points, axis=0)
        xmin, xmax = _minmax(points[:, 0])
        ymin, ymax = _minmax(-points[:, 1])
        window = max((numpy.abs(xmax - xmin), numpy.abs(ymax - ymin))) + margin
        ax.set_xlim(xmin=center[0] - window, xmax=center[0] + window)
        ax.set_ylim(ymin=window - center[1], ymax=-center[1] - window)

    def _local_coords(self, points):
        points = points.reshape((-1, 3))
        points = numpy.concatenate((points, numpy.ones((points.shape[0], 1))), axis=1)
        points = points @ self._w2p
        return points
