from dataclasses import dataclass
import numpy as np


@dataclass
class PatchRef:
    annot_fname: str
    # patch origin position relative to annotation
    # for addressing the location within the padded image
    x: int
    y: int
    z: int
    """
    The image annotation may get updated by the user at any time.
    We can use the mtime to check for this.
    If the annotation has changed then we need to retrieve patch
    coords for this image again. The reason for this is that we
    only want patch coords with annotations in. The user may have added or removed
    annotation in part of an image. This could mean a different set of coords (or
    not) should be returned for this image.
    """
    mtime: int # when was the corresponding annotation modified

    # These metrics are the cached performance for this patch 
    # with previous (current best) model.
    # Initialized to None but otherwise [tp, fp, tn, fn]
    fp: int | None = None # number of false positives for patch
    tp: int | None = None # number of true positives for patch
    tn: int | None = None # number of true negatives for patch
    fn: int | None = None # number of false negatives for patch
    # FIXME: Could ignore_mask be a list of coordinates describing a cuboid rather than 
    #        a likely memory intensive exaustive list of voxels?
 
    # ignore_mask (regions to ignore because they overlap with another patch)
    # numpy array saying which voxels should be ignored when computing metrics
    # because these voxels exist in another overlapping patch.
    ignore_mask: np.ndarray 
 
    def has_metrics(self):
        return self.fp is not None
 
    def is_same_region_as(self, other: PatchRef):
        return (self.annot_fname == other.annot_fname and 
                self.x == other.x and
                self.y == other.y and
                self.z == other.z)
 
    def metrics_str(self):
        # used for debugging from time to time.
        return f"tp:{self.tp}, tn:{self.tn} fp:{self.fp}, fn:{self.fn}"
 
    def assign_metrics(tp:int, fp:int, tn:int, fn:int):
        self.tp = tp
        self.fp = fp
        self.tn = tn
        self.fn = fn
