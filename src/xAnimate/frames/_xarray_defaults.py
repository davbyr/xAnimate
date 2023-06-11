'''
Set of frame function classes, which call the xarray basic plots.
'''

from .frame_function import FrameFunction

class Plot( FrameFunction ):

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def __call__(self, data_ii):
        f = data_ii.squeeze().plot(**self.kwargs).figure
        return f