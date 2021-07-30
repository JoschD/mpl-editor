from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from mpl_editor.options_view import utils as outils


class FigureCanvasExt(FigureCanvas):
    """ Extended FigureCanvas.

    TODO: Multiaxes
    - Legend positions can be easily saved and restored

    """

    LEGEND_LOCATIONS = [0, 1, 2, 3, 4, None]

    def __init__(self, figure):
        super(FigureCanvasExt, self).__init__(figure)
        self._legend_location_index = 0
        self._legend_locations = list(FigureCanvasExt.LEGEND_LOCATIONS)

    def move_legend(self):
        self._legend_location_index = (
                                              self._legend_location_index + 1
                                      ) % len(self._legend_locations)
        self._set_legend_loc()

    def update_legend(self):
        axes = self.figure.gca()
        outils.regenerate_legend(axes, force_new=True)
        self._save_legend_loc()
        self.draw()

    def _set_legend_loc(self):
        legend = self.figure.gca().get_legend()
        if legend is not None:
            loc = self._legend_locations[
                self._legend_location_index
            ]
            if loc is None:
                legend.set_visible(False)
            else:
                legend.set_visible(True)
                legend._set_loc(loc)

            self.draw()

    def _save_legend_loc(self):
        legend = self.figure.gca().get_legend()
        if legend:
            self._legend_location_index = 0
            self._legend_locations = ([legend._get_loc()] +
                                      list(FigureCanvasExt.LEGEND_LOCATIONS))

    def update_figure(self, figure):
        """ Change Figure for this canvas """
        figure.canvas = self
        self.figure = figure
        self._save_legend_loc()
        self._set_legend_loc()
        self.draw()

    def set_pickers(self, tol=0.5):
        """ Set all artists to send pick events when they are clicked """
        axes = self.figure.get_axes()
        for ax in axes:
            for l in ax.lines:
                width = max(1.1*l.get_markersize(), 1.5*l.get_linewidth())
                l.set_picker(width)

            for a in [ax.xaxis, ax.yaxis]:
                a.set_picker(tol)
                for c in a.get_children():
                    c.set_picker(True)

            for t in ax.texts:
                t.set_picker(True)

            legend = ax.get_legend()
            if legend is not None:
                legend.set_picker(True)

            ax.title.set_picker(True)
            # ax.set_picker(True)

    def unset_pickers(self):
        for c in self.figure.get_children():
            try:
                c.set_picker(False)
                c.set_draggable(False)
            except AttributeError:
                pass