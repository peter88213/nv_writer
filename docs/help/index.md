[Project homepage](https://github.com/peter88213/nv_writer) > [Index](../) > User guide

---

# User guide

This page refers to the latest 
[nv_writer](https://github.com/peter88213/nv_writer/) release.

The plugin adds an **Write in distraction free mode** entry to both 
the *novelibre* **Section** menu and the section context menu. 

---

## Operation

- Select the section to start with (optional). If no section is selected in the project tree, the first section will be opened.
- To enter the distraction free editing mode, either 
   - hit `Ctrl`-`W`, or
   - right-click the selected section and select **Write in distraction free mode**, or 
   - click **Section > Write in distraction free mode**.
- Hit `Alt`-`F4` (Windows) or `Ctrl`-`Q` (Linux) to finish the editing session.

> **Important**
>
> In order to avoid confusion, the distraction-free editor will not start, if either 
> - an editable manuscript exists, or
> - the project is locked. 
>
> So if yo have a regular manuscript or a manuscript for third-pary word processing, 
> you may want to discard it after updating your *novelibre* project.

## Select text

-  `Ctrl`-`A` selects the whole text.
-  Select a word via double-clicking.
-  Select a paragraph via triple-clicking.
-  Extend the selection via `Shift`-`Arrow`.
-  Extend the selection to the next word via `Ctrl`-`Shift`-`Arrow`.
 
## Copy/Paste text

-  `Ctrl`-`C` copies the selected text to the clipboard.
-  `Ctrl`-`X` cuts the selected text and moves it to the clipboard.
-  `Ctrl`-`V` pastes the clipboard text content to the cursor position.

## Format text

-  `Ctrl`-`I` emphasizes the selected text.
   If the selection is already emphasized, the command removes the markup.
-  `Ctrl`-`B` strongly emphasizes the selected text.
   If the selection is already strong, the command removes the markup.
-  `Ctrl`-`M` removes "emphasized" and "strong" formatting from the selection.

## Undo/Redo

-  `Ctrl`-`Z` undoes the last editing. Multiple undo is possible.
-  `Ctrl`-`Y` redoes the last undo. Multiple redo is possible.

---

## Switch between sections

- `Ctrl`-`PgUp` loads the previous section, if any.
- `Ctrl`-`PgDn`, loads the next section, if any.
-  When loading another section, you may be asked for applying changes.


## Create a new section

With `Ctrl`-`Alt`-`N`, you can create a new section.

-  The new section is placed after the currently edited section.
-  The new section is of the same type as the currently edited section.
-  The editor loads the newly created section.


## Split a section

With `Ctrl`-`Alt`-`S`, you can split the section at the cursor position.

-  All the text from the cursor position is cut and pasted into a newly created section.
-  The new section is placed after the currently edited section.
-  The new section is appended to the currently edited section.
-  The new section has the same status as the currently edited section.
-  The new section is of the same type as the currently edited section.
-  The new section has the same viewpoint character as the currently edited section.
-  The editor loads the newly created section.

---

## Word count

-  The section word count is displayed at the status bar at the top of the window.
-  By default, word count is updated manually by pressing the `F5` key.
-  The word count can be updated "live", i.e. just while entering text.
   This is enabled or disabled via ... .

> **Note**
>
> Live updating the word count is resource intensive and may slow down
> the program when editing big sections. This is why it’s disabled by default.

---

## Apply changes

With `Ctrl`-`S`, you can apply changes to the section.
Then "Modified" status is displayed in *novelibre*.

> **Hint**
>
> Unlike *Writer*, the distraction-free editor does not automatically replace quotation marks, dashes, etc.
> Typographical adjustments must therefore be made in a proofreading process on the regular manuscript using *Writer*.
> I recommend one of the [curly](https://github.com/peter88213/curly) extensions for this purpose.




## Close the editor window

-  Under Windows you can exit with `Alt`-`F4`.
-  Otherwise you can exit with `Ctrl`-`Q`.
-  When closing the editor window, you may be asked for applying changes.
-  You can temporarily leave the distraction-free mode using your desktop's task switcher (e.g. via `Win`-`Tab` under Windows).  


---

Copyright (c) by Peter Triesberger. All rights reserved.
