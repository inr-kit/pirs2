import matplotlib.colors as mplcols
import numpy as np


class myNormalize(mplcols.Normalize):
    """
    Nromalization with the center of the original colormap shifted to `vmid`.
    """
    def __init__(self, *args, **kwargs):
        self.vmid = kwargs.pop('vmid', None)  # TODO: apply _sanitize_extrema
        mplcols.Normalize.__init__(self, *args, **kwargs)
        return

    def __call__(self, value, *args, **kwargs):
        # The original Normalize works properly with masked values. Here I try
        # to split the whole value array into parts containing values below and
        # above self.vmid, and process them similar to the original Normalize.

        # First, use the original implementation to get the linear
        # normalization
        rh = mplcols.Normalize.__call__(self, value, *args, **kwargs)

        # Short names:
        a = 0.0                                                # self.vmin
        b = (self.vmid - self.vmin) / (self.vmax - self.vmin)  # self.vmid
        c = 1.0                                                # self.vmax
        # Split r1 into two parts, above and below t:
        r1 = np.ma.masked_array(rh, mask=rh > b)   # values below b
        r2 = np.ma.masked_array(rh, mask=rh <= b)  # values above b
        # Apply different normalizations to each part
        r1 = r1 * (c - a) / (b - a) * 0.5
        r2 = r2 + (b - (c+a)*0.5)*(r2 - c) / (c - a) / (c - b)
        # Put modified r1 and r2 into single array:
        r = np.ma.where(rh <= b, r1, r2)
        return r

    def autoscale_None(self, A):
        mplcols.Normalize.autoscale_None(self, A)
        d = max(self.vmid, self.vmax) - min(self.vmin, self.vmid)
        d *= 0.1
        self.vmax = max(self.vmax, self.vmid + d)
        self.vmin = min(self.vmin, self.vmid - d)

