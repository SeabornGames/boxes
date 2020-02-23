Model House
===========

This layout generates the input file to create a model of a home based on an
ascii text files.  It is expected to take the users some effort in laying out
their design for the model house, but it shouldn't take special expertise or
any programming skills.  This layout creates and updates the following two
files:


Diagram File
============
The diagram file will be used by the generator to create the floor SVG tiles.

Using the characters below the user can specify walls, virtual walls, windows,
doors, and objects.

Door Characters:          ▤ (horizontal) █ (vertical)
Wall Characters:          ═ ╬ ╔ ╦ ╗ ╚ ╩ ╝ ╠ ║ ╣
Window Characters:        ─ ┼ ╟ ╤     ╧   ╟ │ ╢
Virtual Wall Characters:  ┈ ⟊ ┌ ╤ ┐ └ ╧ ┘ ╟ ┆ ╢
Object Characters:        ━ ╋ ┏ ┳ ┓ ┗ ┻ ┛ ┣ ┃ ┫

In addition to these characters Names can be given to rooms with characters:
A-Z [ ] _ -

Names can be given to objects with a-z.

Example:
```
 ╔┈┈┈┈┈┈┈┈┈┈┈┈╦═════════════════════════════╦═▤▤▤▤▤▤▤▤▤▤▤═╦═════════════════╗
 ║            ║                             ┆             ┆                 ║
 ║   refrig   ║            couch            ┆             ┆                 ║
 ║            ║                             ┆             ┆                 ║
 ║            ║                             ┆             ┆                 ║
 ╠════════════╩┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┘             │       BAR       ║
 ║                       MEDIA ROOM                       │                 ║
 ║                                                        │                 ║
 ║              ┌┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┐             │                 ║
 ║              ┆                           ┆             ╠═════════════════╣
 ║              ┆                           ┆             ║                 █
 ║              ┆         love seat         ┆             ║                 █
 ║              ┆                           ┆             ║                 █
 ║              ┆                           ┆             ║                 █
 ║              ┆                           ┆             ║                 █
 ║              └┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┘             ║  HALF BATHROOM  █
 ║                                                        ║                 ║
 ║                                                        ║                 ║
 ║                                                        ║                 ║
 ║     ┌┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┈┐      ║                 ║
 ║     ┆                     tv                    ┆      ║                 ║
 ╚═════╩═══════════════════════════════════════════╩══════╩═════════════════╝
```

Each character represents 3" by 6", so the example below represents 2 foot by
2 foot room with a 1.5 feet window and a 1 foot door.

Example:
```
╔──────╗
║      █
║      █
╚══════╝

```

Diagram Helper functions:
-------------------------

1. Creation: If the input diagram file does not exist then the layout script
             will generate it with the dimensions --width --height

2. Cleanup: It is tedious to put corners and intersects walls, so the layout
            script will update the diagram file to clean it up.

3. Ruler:   The --ruler option will add ruler numbers to the top and left side
            of the diagram file.

4. Checker: The --checker option will add background checker board so you can
            see the feet and ten feet marks.

5. Debug:   The command --highlight-room, --remove-objects, --remove-names are
            generally done for debug purposes.

6. Backup:  Since the layout will be modify your existing diagram file a backup
            will be generated with the same name *.bck

7. Output:  The diagram file will automatically be converted to a ``Wall File``
            to be sent to the generator.


Wall File
=========

The diagram file is only a 2D representation of the layout, so the generator
still need details of height to be provided.  Most walls, doors, and windows
will be the same height and therefore the default will suffice, but if that is
not the case then custom values can be used to override those values in this
table (csv/md) like file.

When the generator creates a wall, the doors and windows are included and then
cut out of the wall.


The columns within this table are:
- horizontal:
    (True, False)
    read-only
    describes if the wall is horizontal or vertical

- status:
    (new, used, missing)
    read-only
    if this object is new it may need its parameters specified
    if this object is missing it means the script couldn't find it any more.
    Note, rooms are found by their name and walls are found by the names of
    the rooms they touch

- height_1
    (float of the number of feet)
    If blank this will equal the default.
    This represents the height of the wall at the left or top side.

- height_2
    (float of the number of feet)
    If blank this will equal the default.
    This represents the height of the wall at the right or bottom side.

- window_1
    (float of the number of feet)
    If blank this will equal the default.
    This represents the height at the bottom of the window.

- window_2
    (float of the window height)
    If blank this will equal the default.
    This represents the height at the top of the window.

- door
    (float of the door height)
    If blank this will equal the default.
    This represents the height at the top of the door.

- color
    (black, red, green, blue, purple)
    This represents the color of the wall within the SVG.

- room_0, room_1, room_2, room_3
    (name of the rooms the wall touches)
    read-only

- x, y
    (integer)
    read-only
    This represents the X and Y location of the first character of the wall.

- symbols
    (characters)
    read-only
    This represents the wall as seen in the diagram file.


Stairs:
-------
The room name STAIRS is reserved for specifying stairs.


