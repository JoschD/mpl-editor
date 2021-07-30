from typing import Tuple, Union, Dict

import matplotlib as mpl
import logging

LOG = logging.getLogger(__name__)


NOLEGEND = '_nolegend_'


def get_linestyles() -> Dict[str, str]:
    """ Return a mapping from linestyle shorthands to linestyles as shown in GUI."""
    return {
        'solid': 'Solid',
        '-': 'Solid',
        'dashed': 'Dashed',
        '--': 'Dashed',
        'dashdot': 'DashDot',
        '-.': 'DashDot',
        'dotted': 'Dotted',
        ':': 'Dotted',
        None: 'None',
        'none': 'None',
        'None': 'None',
    }


def convert_linestyle_to_approximate_str(ls: Union[str, Tuple[int, Tuple[int]]]) -> str:
    """ Convert linestyle to approximate string, i.e.
     also from tuple-form into string.
    see: https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
    """
    if ls is None:
        return "none"

    if isinstance(ls, str):
        try:
            return get_linestyles()[ls]
        except KeyError:
            return ls

    if len(ls) == 2 and ls[0] == 0:
        pattern = ls[1]
        if pattern is None or not len(pattern):
            return "solid"


        try:
            return {1: "dotted", 3: "dashdot", 5: "dashed"}[pattern[0]]
        except KeyError:
            pass

    raise IOError(f"Unknown linestyle {ls!s}")


def get_drawstyles():
    return {
        'default': 'Default',
        'steps-pre': 'Steps (Pre)',
        'steps': 'Steps',
        'steps-mid': 'Steps (Mid)',
        'steps-post': 'Steps (Post)'}


def get_ticks_directions():
    return ["in", "out", "inout"]


def get_scales():
    return ['linear', 'log', 'symlog', 'logit']


def regenerate_legend(axes, force_new=False):
    """ Update legend but keep style and position """
    old_legend = axes.get_legend()
    if old_legend is None and not force_new:
        return

    draggable = None
    loc = None
    ncol = 1
    # save old properties
    if old_legend is not None:
        draggable = old_legend._draggable is not None
        ncol = old_legend._ncol
        loc = old_legend._get_loc()

    # create new legend
    new_legend = axes.legend(ncol=ncol)
    if new_legend:
        new_legend.set_draggable(draggable)
        if loc:
            new_legend._set_loc(loc)
        new_legend.set_picker(True)
    return new_legend


def get_markers():
    return mpl.markers.MarkerStyle.markers


def is_errorbar(o):
    return isinstance(o, mpl.container.ErrorbarContainer)


def apply_to_ebar(func, ebar,  value, line=True, caps=True, bars=True):
    """ Do function `func` with input `line, value` to all lines of the errorbar ebar """

    if line:
        if isinstance(func, str):
            ebar[0].__getattribute__(func)(value)
        else:
            func(ebar[0], value)

    if caps:
        for cap in ebar[1]:
            if isinstance(func, str):
                cap.__getattribute__(func)(value)
            else:
                func(cap, value)

    if bars:
        for bar in ebar[2]:
            if isinstance(func, str):
                bar.__getattribute__(func)(value)
            else:
                func(bar, value)


def get_errorbar_from_line(line):
    """ Returns first container of type errorbar if line is in there, otherwise index errror. """
    return [cont for cont in line.axes.containers if is_errorbar(cont) and line in cont][0]


def prepare_formdata(style_choice_map: dict, selected_choice: str):
    """Prepare an entry for FormLayout.

    `style_choices_map` is a mapping of shorthands to style names (a single style may
    have multiple shorthands, in particular the shorthands `None`,
    `"None"`, `"none"` and `""` are synonyms);

    This function returns a tuple of the initial value and the choices of the formdata:
    `initial_name, [(shorthand, style_name), (shorthand, style_name), ...]`.
    """
    # Drop duplicate shorthands from dict (by overwriting them during
    # the dict comprehension).
    name2short = {name: short for short, name in style_choice_map.items()}
    # Convert back to {shorthand: name}.
    short2name = {short: name for name, short in name2short.items()}
    # Find the kept shorthand for the style specified by init.
    try:
        short_selected = name2short[style_choice_map[selected_choice]]
    except KeyError:
        LOG.debug("Unkown style found. Possibly tuple-style. This is not supported for now.")
        short_selected = None
    # Sort by representation and prepend the initial value.
    return short_selected, sorted(short2name.items(), key=lambda short_and_name: short_and_name[1])
