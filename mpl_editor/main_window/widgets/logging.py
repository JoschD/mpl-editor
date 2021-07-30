import logging

from PyQt5 import QtWidgets, QtCore

LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
DATE_FORMAT = '%d/%m/%Y %H:%M:%S'


class LogDialog(QtWidgets.QDialog, logging.StreamHandler):
    """ Logging dialog window, created by Jaime """

    _update_signal = QtCore.pyqtSignal(str)

    def __init__(self, fmt=LOG_FORMAT, datefmt=DATE_FORMAT, parent=None):
        QtWidgets.QDialog.__init__(self, parent=parent)
        logging.Handler.__init__(self)

        self.resize(855, 655)
        layout = QtWidgets.QVBoxLayout()
        self._log_text = QtWidgets.QPlainTextEdit(parent)
        self._log_text.setReadOnly(True)
        layout.addWidget(self._log_text)
        self.setLayout(layout)

        self.setFormatter(logging.Formatter(fmt, datefmt))
        self.setLevel(logging.DEBUG)

        self._update_signal.connect(self._update_log, QtCore.Qt.QueuedConnection)

    def _update_log(self, msg):
        self._log_text.appendPlainText(msg)

    def emit(self, record):
        msg = self.format(record)
        self._update_signal.emit(msg)


class LogStatusBar(QtWidgets.QStatusBar, logging.StreamHandler):
    """ Logging dialog window, created by Jaime """

    _update_signal = QtCore.pyqtSignal(str)

    def __init__(self, fmt=LOG_FORMAT, datefmt=DATE_FORMAT, parent=None):
        QtWidgets.QStatusBar.__init__(self, parent=parent)
        logging.StreamHandler.__init__(self)

        self._status_text = QtWidgets.QLabel()
        self.addWidget(self._status_text, 1)

        self.setFormatter(logging.Formatter(fmt, datefmt))
        self.setLevel(logging.INFO)

        self._update_signal.connect(self.showMessage, QtCore.Qt.QueuedConnection)

    def emit(self, record):
        msg = self.format(record)
        self._update_signal.emit(msg)
