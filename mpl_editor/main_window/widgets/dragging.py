import time


class DragHandler(object):
    """ Handles the dragging of objects around the screen """
    time_tol = 0.1  # time between drag'n'drop to be registered (in sec)

    def __init__(self, artist, mouseevent):
        self.artist = artist
        self.time = time.time()
        self.pick_pos_data = [mouseevent.xdata, mouseevent.ydata]
        self.pick_pos_disp = [mouseevent.x, mouseevent.y]
        self.artist_pos_data = artist.get_position()
        self.artist_pos_disp = artist._get_xy_display()

    def move(self, mouseevent):
        # if (time.time() - self.time) < self.time_tol:
        #     return

        mouse_pos_disp = [mouseevent.x, mouseevent.y]
        mouse_pos_data = [mouseevent.xdata, mouseevent.ydata]

        if any(pos is None for pos in self.pick_pos_data + mouse_pos_data):
            # something was outside of the plotting area -> use figure coodinates
            return  # TODO: DOES NOT WORK AS EXPECTED
            to_pos = self._get_new_position(self.artist_pos_disp,
                                            mouse_pos_disp,
                                            self.pick_pos_disp)
            self.artist.transform = self.artist.figure.transFigure
            to_pos = self.artist.transform.inverted().transform(to_pos)
        else:
            # keep everything inside the plotting area
            to_pos = self._get_new_position(self.artist_pos_data,
                                            mouse_pos_data,
                                            self.pick_pos_data)

        self.artist.set_position(to_pos)

    def _get_new_position(self, from_pos, mouse_pos, pick_pos):
        return [fp + mp - pp for fp, mp, pp in zip(from_pos, mouse_pos, pick_pos)]