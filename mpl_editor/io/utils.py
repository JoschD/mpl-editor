import os
from pathlib import Path

import matplotlib
import logging

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

from mpl_editor.io.widgets import ColumnSelectorDialog
import tfs
from tfs.handler import TfsFormatError

LOG = logging.getLogger(__name__)


# Public Methods #############################################################


def load_tfs():
    """ Plots a tfs-file.

    TODO:
        * check all tfs files for common columns -> make user choose which column
        * changemarkers tickbox
    """
    LOG.debug("Load Tfs clicked.")
    paths = QFileDialog().getOpenFileNames(None, 'Load file(s)', '')[0]
    fig = None
    if paths:
        LOG.info("Files chosen: {:s}".format(", ".join(paths)))
        if len(paths) > 1:
            # load all files and check for common columns
            df_list, common_cols = _get_all_tfs_and_common_columns(paths)
            column_selector = ColumnSelectorDialog(common_cols, single_line=True)
        elif len(paths) == 1:
            # load only one tfs
            LOG.debug("Loading only one file")
            try:
                df = tfs.read_tfs(paths[0])
            except TfsFormatError:
                LOG.error("File '{}' is not of TFS format!".format(paths[0]))
            else:
                column_selector = ColumnSelectorDialog(df.columns.tolist())
                selected = column_selector.get_selected_columns()
                if selected:
                    NotImplemented("Plotting not yet implemented")
                    # fig = plot_tfs.plot_single_file(
                    #     files=paths,
                    #     x_cols=[s["x"] for s in selected],
                    #     y_cols=[s["y"] for s in selected],
                    #     e_cols=[s["e"] for s in selected],
                    #     labels=[s["l"] for s in selected],
                    #     no_show=True,
                    # )
        return fig
    LOG.debug("No files chosen.")
    return None


def load_dly():
    """ Load data and layout from .dly file """
    path = QFileDialog().getOpenFileName(None, 'Load Figure', '', '*.dly')[0]
    if path:
        LOG.info("Importing file '{}'".format(path))
        with open(path, "rb") as f:
            pass # TODO
    return None


def save_dly(fig):
    """ Save data and layout into .dly file """
    path = QFileDialog().getSaveFileName(None, "Save Figure", "", "*.dly")[0]
    if path:
        with open(path, "wb") as f:
            pass  #TODO

def save_layout(figure):
    """ Saves the current state of the layout.

    Into ini-file
    * Save labels
    * Save Title
    * Save x_lim
    * Save y_lim
    * Gridstatus
    * axis-scaling
    * the subplot parameters


    Returns:

    """
    pass


def load_layout(figure):
    """ Load ini-file with layout properties

    """


def save_figure(figure):
    """ Save figure

     From backend_qt5.NavigationToolbar2QT
     """
    filetypes = figure.canvas.get_supported_filetypes_grouped()
    sorted_filetypes = sorted(filetypes.items())
    default_filetype = figure.canvas.get_default_filetype()

    saved_directory = Path(matplotlib.rcParams['savefig.directory']).expanduser()
    output_suggestion = saved_directory / figure.canvas.get_default_filename()
    filters = []
    selected_filter = None

    for name, exts in sorted_filetypes:
        exts_list = " ".join(['*.%s' % ext for ext in exts])
        filter = '%s (%s)' % (name, exts_list)
        if default_filetype in exts:
            selected_filter = filter
        filters.append(filter)
    filters = ';;'.join(filters)

    fname, filter = QtWidgets.QFileDialog.getSaveFileName(
        caption="Choose a filename to save to",
        directory=str(output_suggestion),
        filter=filters,
        initialFilter=selected_filter,
    )

    if fname:
        fname = Path(fname)

        # Save dir for next time, unless empty (i.e., use cwd).
        if saved_directory != Path():
            matplotlib.rcParams['savefig.directory'] = fname.parent
        try:
            figure.savefig(fname)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None, "Error saving file", str(e),
                QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.NoButton)




# Private Methods #############################################################


def _get_all_tfs_and_common_columns(paths):
    tfs_list = [tfs.read_tfs(p) for p in paths]
    cols = tfs_list[0].columns
    for t in tfs_list[1:]:
        cols = cols.intersection(t.columns)
    return tfs_list, cols
