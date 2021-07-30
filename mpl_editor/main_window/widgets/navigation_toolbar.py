from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT

from mpl_editor.options_view import figure as ofigure
from mpl_editor.tools.gui_utils import get_icon


class NavigationToolbar(NavigationToolbar2QT):
    """ Customized Navigation Toolbar """

    ICON_SIZE = 24

    def __init__(self, canvas,
                 save_fun=None, load_fun=None, export_fun=None, import_fun=None, parent=None):
        self.load_data = load_fun
        self.export_plot = export_fun
        self.import_plot = import_fun

        self.toolitems = list(self.toolitems)

        if hasattr(canvas, "move_legend") and hasattr(canvas, "update_legend"):
            self.update_legend = canvas.update_legend
            self.move_legend = canvas.move_legend

            self.toolitems.insert(7, (None, None, None, None))

            self.toolitems.insert(8, (
                "Move Legend", "Move the legend location to predefined settings.",
                "arrows", "move_legend"
            ))

            self.toolitems.insert(9, (
                "Update Legend", "Update the legend.",
                "refresh", "update_legend"
            ))

        if save_fun is not None:
            self.save_figure = save_fun  # otherwise defined by super-class

        if self.load_data is not None:
            self.toolitems.append((
                    "Load Data", "Plot data from tfs files.",
                    "folder_open", "load_data"
                ))

        if self.export_plot is not None:
            self.toolitems.append((
                    "Export Plot", "Export plot to .dly file format.",
                    "export", "export_plot"
                ))

        if self.import_plot is not None:
            self.toolitems.append((
                    "Import Plot", "Import plot from .dly file format.",
                    "import", "import_plot"
                ))

        super(NavigationToolbar, self).__init__(canvas, parent)

    def _icon(self, name):
        """ Overwrite _icon() as called in super.__init__ to check for
        local icons first. '.png' will already be added to name. """
        try:
            return get_icon(name)
        except IOError:
            return super(NavigationToolbar, self)._icon(name)

    def edit_parameters(self):
        allaxes = self.canvas.figure.get_axes()
        if not allaxes:
            QtWidgets.QMessageBox.warning(
                self.parent, "Error", "There are no axes to edit.")
            return
        elif len(allaxes) == 1:
            axes, = allaxes
        else:
            titles = []
            for axes in allaxes:
                name = (axes.get_title() or
                        " - ".join(filter(None, [axes.get_xlabel(),
                                                 axes.get_ylabel()])) or
                        "<anonymous {} (id: {:#x})>".format(
                            type(axes).__name__, id(axes)))
                titles.append(name)
            item, ok = QtWidgets.QInputDialog.getItem(
                self.parent, 'Customize', 'Select axes:', titles, 0, False)
            if ok:
                axes = allaxes[titles.index(str(item))]
            else:
                return

        ofigure.figure_edit(axes, self)

    def _init_toolbar(self):
        # Called in one of the super.__init__'s but we don't want to do anything
        pass
