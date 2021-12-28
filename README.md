# Autocraftic Notes

Moses Yu Chong Hei, CS50x 2021

#### [Video Demo](https://youtu.be/zwn23R2TJg4)

#### Description:

###### Abstract
This program automates the creation of Minecraft note block maps from musical sheet music.

I have a YouTube channel, [Apl3ater](https://www.youtube.com/c/Apl3ater), where I make these note block maps from scratch and then play them. They take around 12-20 hours to make each, so I hope that this program will shorten the time to around one hour.

###### Note Block Basics

In Minecraft, note blocks are blocks that emit a musical note whenever they receive a redstone (read: electrical) signal. Clicking on the note blocks will change its pitch in a two octave range, where it will them loop back around.
![note block colors](https://i.imgur.com/BOXl9X2.png)

Also, you can change the instruments by switching the note below the note block. I use the bass drum, snare drum, bass guitar, acoustic guitar, piano, flute, and bell in my builds.
![note block instruments](https://i.pinimg.com/736x/82/de/7d/82de7d00610b2cfbc5db12f16c932bd0.jpg)

The note blocks are timed using redstone repeaters, which are somewhat similar to transistors in real life. Most of the notes are laid out in a straight line, which the player can fly along to listen to. A button is used to activate the whole contraption which then plays the entirety of the song.


###### input.mid
This file contains the raw MIDI (musical instrument digital interface) of my personal transcription of the [CS50 Theme](https://www.youtube.com/watch?v=OYDVxOKbbaE) by Jacob Lurye. MIDI files (.mid and .midi) contain all the relevant information of a musical piece, such as the note pitches, rhythms, instruments, tempo, and so on. They will be our primary input for

`input.mid` is a single-track, polyphonic rendering of the CS50 Theme, where the bass drum part has been entered in as C1 notes (i.e. three octaves below middle C). A representation of this MIDI track can be seen in `This_is_CS50_midified.pdf`. Notice how everything has been squished up into a single staff; this is a necessity and will be explained more in the next section. Furthermore, there are no dynamic markings or any slurs or accents in the music. This is because they are simply not necessary - `run.py` will filter through them as Minecraft note blocks do not have variable volume or dynamics.

Minecraft's redstone repeaters can only be set to delay for 1-4 ticks (a tick is 0.1 seconds). Therefore, the tempo (in bpm, beats per minute) of the input file must be 150 (0.1 second semiquavers = 0.4 second beats = 150 beats per minute) or 75 (0.2 second semiquavers = 0.8 second beats = 75 beats per minute).

###### run.py
We will be going through the important sections of the code from top to bottom.

**Ln 2-3:** [mido](https://mido.readthedocs.io/en/latest/), a python library that extracts data from MIDI files, is imported.

**Ln 11-12:** the instruments and their corresponding blocks are defined - each element in the list corresponds to that octave's instrument or block (e.g. `OCTINST[4]` is the note block instrument to be used for octave 4, which is the octave at middle C).

**Ln 15-26:** mido is used to go through the entire track and export all the pitch and rhythm data into `notes[]` and `times[]`, as well as printing metainfo into the console

**Ln 29-35:** `outputCommands[]` is used as a temporary variable to store all the commands that are to be sent to the game. This means that the user will be inputting multiple commands at a time into a [command block](https://docs.microsoft.com/en-us/minecraft/creator/documents/commandblocks) in the Minecraft map, which is essentially the terminal of Minecraft. I decided to use Minecraft commands as the link between the program and game, as I have tested other options, including [schematic](https://www.minecraft-schematics.com/) and creating a map completely from scratch, but those options had their own bugs and I wasn't able to get them up and running. Testing was also extremely difficult with those other options as I could not see what was wrong with my code.

`redLength` is an integer used to define how long the entire Minecraft map has to be, and the subsequent lines create a line of alternating redstone dust (read: wire) and repeaters (read: transistors/digital delay line). `forceload` is a Minecraft command to force the loading of all the chunks on and surrounding the redstone line to make sure that no in-game glitches occur.

**Ln 38:** repeat `for` loop for each note in the MIDI file.

**Ln 39-60:** note blocks are placed in a location which is a function of the current time and amount of simultaneous notes in that moment.

**Ln 62-77:** if there are simultaneous notes, a redstone repeater may need to be added; this segment of code goes through all the possible orientations and locations of those repeaters.

*NOTE: I was having trouble with format strings so I used* `.format()` *but later figured out how to use the cleaner* `f"{variable}"` *method which I then used. The old method is still in the code, commented out.*

**Ln 80-97:** `outputCommandChunk()` is defined which creates a long ["one-block-command"](https://minecraft.fandom.com/wiki/Tutorials/Falling_blocks#Example_uses) that boxes and multiple commands together into a text file, `output.txt`.

**Ln 100-106:** calls `outputCommandChunk()` in 340-command chunks. The reason for the number 340 is because Minecraft has a maximum command length of 32500 characters when placed into a command block (when typed in chat, this number is even less). As my longest possible commands are 95 characters long, I divide 32500 by 95 and round off the ones digit (floor to be on the safe side) to get 340.

`run.py` takes `input.mid` and the variable `repeaterDelay` as input and outputs `output.txt` for the user to put into their Minecraft world.

###### output.txt
This file has been tested to work from Minecraft versions 1.13 up to 1.18 (latest to date). As there was a [large change in command syntax](https://minecraft.fandom.com/wiki/Java_Edition_17w45a#Changes) between Minecraft 1.12 and 1.13, I do not believe my program will work for 1.12 and below.

How to use:
1. In Minecraft, mark a coordinate on solid, flat ground where the music is to be spawned at.
2. Copy and paste each command (separated by many horizontal dashes) sequentially into a Minecraft command block (spawned in via `/give @p minecraft:command_block`).
3. Activate the redstone using a button.
4. Enjoy the CS50 theme!

###### CS50_Theme.zip
This is a Minecraft world/save file of the map created through the process outlined above. Unzip the file, and then put the output folder into your saves file (`.minecraft/saves/`) to be able to access the file from Minecraft.

#### Issues

Although I have tried my best to minimize the amount of bugs, there are still some issues that are either very hard or impossible to fix:
- Notes cannot exceed 5 at a time (i.e. chords larger than 5 notes cannot be rendered)
- I need to combine all my music to one staff for mido to work
- The first note must be a single note or else the program will crash prematurely
- Songs longer than five minutes (at 150 BPM) may exceed the `forceload` limit and crash Minecraft


## Thank you for reading, and this was CS50x!
