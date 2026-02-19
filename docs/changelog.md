[Project home page](../) > Changelog

------------------------------------------------------------------------

## Changelog


### Version 0.18.6 

- Added numpad key bindings for Linux.

API: 5.52
Based on novelibre 5.52.1


### Version 0.18.5

- No longer minimizing the novelibre main window under Linux (#7).

API: 5.52
Based on novelibre 5.52.1


### Version 0.18.4 

- Improved operation under Linux by focusing the editor after loading a section. 

API: 5.52
Based on novelibre 5.52.1


### Version 0.18.3 

- Fixed a bug where an exception is raised if the project has no title. 
- Do not start the editor if a newly created project is not yet saved. 
- Do not start the editor if the project has no sections. 

API: 5.52
Based on novelibre 5.52.1


### Version 0.18.2

- Fixed a bug where the options dialog cannot be opened due to missing icons.

API: 5.52
Based on novelibre 5.52.1


### Version 0.18.1

- Changed keyboard shortcut for starting the writing mode to `F11`.
- Revised and renamed the color sets.

API: 5.52
Based on novelibre 5.52.1


### Version 0.17.4

- Adjusted the "Turquoise" theme to match the original EGA color.

API: 5.52
Based on novelibre 5.52.1


### Version 0.17.3

- Adjusted the "Amber" theme to match the original phosphor color.

API: 5.52
Based on novelibre 5.52.1


### Version 0.17.2

- Making sure that the current font settings are applied.

API: 5.52
Based on novelibre 5.52.1


### Version 0.17.1

- New feature: Apply changes and save the project on demand.
- Adjusted the default font size.
- Updated the footer bar entries.


#### Changed the key bindings.

- `Ctrl`-`S` applies changes and saves the project. 
- `Ctrl`-`L` splits the section at the cursor position.

API: 5.52
Based on novelibre 5.52.1



### Version 0.16.0 (Experimental Beta release)

#### Changed the key bindings.

- `F3` toggles the menu.
- `Esc` is another option to end the distraction-free writing mode.

--- 

- Scaling the header and footer bars.
- Major revision of the color setting.
- Protecting changes from being lost when closing the editor from the task
switcher.

API: 5.52
Based on novelibre 5.52.1


### Version 0.15.1 (Experimental Beta release)

- Changed "Blue" color set's foreground color.

API: 5.52
Based on novelibre 5.52.1


### Version 0.15.0 (Experimental Beta release)

- Added "Turquoise" color set.
- Changed "Blue" color set's foreground color.

API: 5.52
Based on novelibre 5.52.1


### Version 0.14.0 (Experimental Beta release)

- Made the editor window resizable via hotkeys.
- Updated colors for the "Blue" and "White" modes.

API: 5.52
Based on novelibre 5.52.1


### Version 0.13.2 (Experimental Beta release)

- Emphasized text is displayed slanted, strongly emphasized text is displayed in bold. 
- Changed the comment look to inverted (less obtrusive).
- The editor window geometry is defined in pixels.
- Setting the geometry to defaults, if a value in the configuration is beyond the limits.
- Making sure the default font is available.
- Setting the editor font to default, if it is misconfigured.
- Applying the default configuration, if the ini file is outdated.

API: 5.52
Based on novelibre 5.52.1


### Version 0.12.2 (Experimental Beta release)

- Fixed the `SectionContentValidator` class to consider footnotes/endnotes.
- Refactored the parsers.

API: 5.52
Based on novelibre 5.52.1


### Version 0.12.1 (Experimental Beta release)

- Handling headings including a comment.
- Handling paragraphs with attributes starting with a comment.

API: 5.52
Based on novelibre 5.52.1


### Version 0.12.0 (Experimental Beta release)

Aborting the distraction-free mode if a section cannot be processed properly. 

#### To do:

- Fix handling of headings including a comment.
- Fix handling of paragraphs with attributes starting with a comment.

API: 5.52
Based on novelibre 5.52.1


### Version 0.11.1 (Experimental Beta release)

Almost finished with fixing #5. 

#### To do:

- Fix handling of headings or paragraphs with attributes starting with a comment.

API: 5.52
Based on novelibre 5.52.0


### Version 0.11.0 (Experimental Beta release)

- No longer allow manually applying changes.
- Changed the key bindings:
   - `Ctrl`-`N` creates a new section.
   - `Ctrl`-`S` splits the section.
- Revised the footer bar menu.
- Highlighting the status bar while the menu is visible.
- Renamed color set: "Black" --> "Paper".
- Disabled the formatting shortcuts (emphasis, strong emphasis, plain).

API: 5.52
Based on novelibre 5.52.0

### Version 0.10.0 (Experimental Beta release)

- Preserving footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0

### Version 0.9.2 (Experimental Alpha release)

- Changed "Options" dialog text.
- Updated colors for the "Blue" mode.

#### To do:

- Support footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0

### Version 0.9.1 (Experimental Alpha release)

- Handling lines ending with spaces.
- Aborting the distraction-free mode if a footnote or endnote is detected.
- Refactored and commented the parsers.

#### To do: 

- Support footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0


### Version 0.8.0 (Experimental Alpha release)

- Preserving H5...H9 formats.

#### To do: 

- Support footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0


### Version 0.7.0 (Experimental Alpha release)

- Added a "Cancel" option to the confirmation dialog.

#### To do: 

- Support H5...H9 formats.
- Support footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0


### Version 0.6.0 (Experimental Alpha release)

- Providing color optins. 
- Inverted scrollbar colors.

#### To do: 

- Add a "Cancel" option to the confirmation dialog.
- Support H5...H9 formats.
- Support footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0


### Version 0.5.0 (Experimental Alpha release)

- Providing context-sensitive help.
- Providing an Options dialog.
   - Checkbox for confirmation.
   - Checkbox for live word count.

#### To do: 

- Support H5...H9 formats.
- Support footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0


### Version 0.4.0 (Experimental Alpha release)

#### To do: 

- Support H5...H9 formats.
- Support footnotes and endnotes.

API: 5.52
Based on novelibre 5.52.0