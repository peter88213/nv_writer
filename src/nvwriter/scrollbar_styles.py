"""Provide a helper function to customize the scrollbars.

    Credit goes to user Peter on stackoverflow
    https://stackoverflow.com/a/74877760
"""
from tkinter import ttk


def make_scrollbar_styles(
    troughcolor='black',
    background='grey',
    arrowcolor='white',
):
    """
    Style the scrollbars.  Usage:
        parent_frame = ... # tk.Frame(...) or tk.Tk() or whatever you're using for the parent
        hstyle, vstyle = make_scrollbar_styles()
        self._vbar = ttk.Scrollbar(
            parent_frame, 
            orient='vertical', 
            style=vstyle,
        )
        self._hbar = ttk.Scrollbar(
            parent_frame, 
            orient='horizontal', 
            style=hstyle,
        )
    """
    style = ttk.Style()

    for is_hori in (True, False):
        v = "Horizontal" if is_hori else "Vertical"
        style.element_create(
            f'CustomScrollbarStyle.{v}.Scrollbar.trough',
            'from',
            'default',
        )
        style.element_create(
            f'CustomScrollbarStyle.{v}.Scrollbar.thumb',
            'from',
            'default',
        )
        style.element_create(
            f'CustomScrollbarStyle.{v}.Scrollbar.leftarrow',
            'from',
            'default',
        )
        style.element_create(
            f'CustomScrollbarStyle.{v}.Scrollbar.rightarrow',
            'from',
            'default',
        )
        style.element_create(
            f'CustomScrollbarStyle.{v}.Scrollbar.grip',
            'from',
            'default',
        )
        style.layout(
            f'CustomScrollbarStyle.{v}.TScrollbar',
            [(f'CustomScrollbarStyle.{v}.Scrollbar.trough', {
                'children': [
                    (f'CustomScrollbarStyle.{v}.Scrollbar.thumb', {
                        'unit': '1',
                        'children': [(
                            f'CustomScrollbarStyle.{v}.Scrollbar.grip',
                            {'sticky': ''}
                        )],
                        'sticky': 'nswe'}
                     )
                ],
                'sticky': 'we' if is_hori else 'ns'}),
             ])
        style.configure(
            f'CustomScrollbarStyle.{v}.TScrollbar',
            troughcolor=troughcolor,
            background=background,
            arrowcolor=arrowcolor,
        )
    return (
        "CustomScrollbarStyle.Horizontal.TScrollbar",
        "CustomScrollbarStyle.Vertical.TScrollbar"
    )

