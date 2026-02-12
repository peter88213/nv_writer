"""Provide a helper function to customize the vertical scrollbar.

    Credit goes to user Peter on stackoverflow
    https://stackoverflow.com/a/74877760
"""
from tkinter import ttk


def make_scrollbar_style(
    troughcolor='black',
    background='grey',
):
    style = ttk.Style()
    style.element_create(
        'CustomScrollbarStyle.Vertical.Scrollbar.trough',
        'from',
        'default',
    )
    style.element_create(
        'CustomScrollbarStyle.Vertical.Scrollbar.thumb',
        'from',
        'default',
    )
    style.element_create(
        'CustomScrollbarStyle.Vertical.Scrollbar.grip',
        'from',
        'default',
    )
    style.layout(
        'CustomScrollbarStyle.Vertical.TScrollbar',
        [(
            'CustomScrollbarStyle.Vertical.Scrollbar.trough',
            {
                'children': [
                    ('CustomScrollbarStyle.Vertical.Scrollbar.thumb',
                        {
                            'unit': '1',
                            'children': [(
                                'CustomScrollbarStyle.Vertical.Scrollbar.grip',
                                {'sticky': ''}
                            )],
                            'sticky': 'nswe'
                        }
                    )
                ],
                'sticky': 'ns'
            }
        )]
    )
    style.configure(
        'CustomScrollbarStyle.Vertical.TScrollbar',
        troughcolor=troughcolor,
        background=background,
    )

