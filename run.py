# import mido
from mido import MidiFile
mid = MidiFile('input.mid', clip=True)

notes, times = [], []
outputCommands = []
totalTime = 0
repeaterDelay = 1 # 1 for 150bpm, 2 for 75bpm (3 for 50bpm, 4 for 37.5bpm)

# Instruments and blocks for each octave
OCTBLOCK = ["stone", "sand", "oak_planks", "white_wool", "diamond_block", "clay", "gold_block", "gold_block", "gold_block"]
OCTINST = ["basedrum", "snare", "bass", "guitar", "harp", "flute", "bell", "bell", "bell"]


commandCount = 1 # first command always incl in count
for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        if msg.is_meta:
            print(msg) # midi metainfo
        elif msg.type == 'note_on' and msg.velocity != 0:
            # extract all notes that have sound
            # and add them to lists (notes and times)
            notes.append(msg.note)
            times.append((msg.time//6.25)/10)
            # 0.4 seconds per quarter note => 150bpm


#total length of redstone wire
redLength = int(round(sum(times), 5)*20)
outputCommands.append(f"forceload add ~ ~ ~{redLength+20} ~") # 20 to be on the safe side
outputCommands.append(f"fill ~10 ~-2 ~ ~{redLength+10} ~-2 ~ redstone_wire") # 10 to calibrate
for i in range(redLength):
    if i%2 == 0:
        outputCommands.append(f"setblock ~{i+11} ~-2 ~ repeater[delay={repeaterDelay}, facing=west]") # 10 to calibrate, then 1 to make odd numbers


for i in range(len(notes)):
    # rounding to nearest five digits to prevent floating point errors
    totalTime = round(totalTime+times[i], 5)
    print(i, notes[i], times[i], totalTime)

    octave = (notes[i]//12)-1 # middle C is the start of the 4th octave (i.e. C4)
    xPos = int((totalTime*20)+10) # determine x-position using the total time passed (including the calibration val)
    note = notes[i]

    # calibrate the notes to be between 6-17 (C-B)
    while note >= 12:
        note -= 12
    note += 6

    xOffset, zOffset, rep = 0, 0, 0

    # determine offsets to place the blocks depending on number of simultaneous notes
    if times[i] != 0 or i == 0: print("single"); pass
    elif times[i-1] != 0: print("double"); xOffset = -2; zOffset = 2; rep = -1
    elif times[i-2] != 0: print("triple"); xOffset = -2; zOffset = -2; rep = 1
    elif times[i-3] != 0: print("quadruple"); xOffset = -2; zOffset = 3
    elif times[i-4] != 0: print("quintuple"); xOffset = -2; zOffset = -3
    else: print("ERROR: TOO MANY SIMULTANEOUS NOTES"); break

    # if double or triple note, add repeater extending from previous note
    if rep != 0:
        if zOffset > 0: repDir = "north"
        else: repDir = "south"

        # repeater into note block
        outputCommands.append(f"setblock ~{xPos+xOffset} ~-2 ~{zOffset+rep} repeater[delay={repeaterDelay}, facing={repDir}]")
        # outputCommands.append("setblock ~{} ~-2 ~{} repeater[delay={}, facing={}]".format(xPos+xOffset, zOffset+rep, repeaterDelay, repDir))

    # place note block
    outputCommands.append(f"setblock ~{xPos+xOffset} ~-2 ~{zOffset} note_block[note={note}, instrument={OCTINST[octave]}]")
    # outputCommands.append("setblock ~{} ~-2 ~{} note_block[note={}, instrument={}]".format(xPos+xOffset, zOffset, note, OCTINST[octave]))

    # place underneath block
    outputCommands.append(f"setblock ~{xPos+xOffset} ~-3 ~{zOffset} {OCTBLOCK[octave]}")
    # outputCommands.append("setblock ~{} ~-3 ~{} {}".format(xPos+xOffset, zOffset, OCTBLOCK[octave]))


# output MC commmand(s) to text file
def outputCommandChunk(f, commandList):
    # Taken from https://minecraft.fandom.com/wiki/Tutorials/Falling_blocks#Example_uses
    f.write("""summon falling_block ~ ~1 ~ {Time:1,BlockState:{Name:redstone_block},Passengers:[
{id:armor_stand,Health:0,Passengers:[
{id:falling_block,Time:1,BlockState:{Name:activator_rail},Passengers:[
{id:command_block_minecart,Command:'gamerule commandBlockOutput false'},
""")
    for command in commandList:
        f.write("\n{id:command_block_minecart,Command:'")
        f.write(command)
        f.write("'},")

    f.write("""\n
{id:command_block_minecart,Command:'setblock ~ ~1 ~ command_block{auto:1,Command:"fill ~ ~ ~ ~ ~-3 ~ air"}'},
{id:command_block_minecart,Command:'kill @e[type=command_block_minecart,distance=..1]'}]}]}]}
\n--------------------------------------------------------------------------------\n
""")


with open("output.txt", mode="w", encoding='utf-8') as outputFile:
    # note that max command length is 32500, so we will need to split it up
    while len(outputCommands) > 340:
        tempCommands = outputCommands[0:339]; del outputCommands[0:339]
        outputCommandChunk(outputFile, tempCommands)
        commandCount += 1
    outputCommandChunk(outputFile, outputCommands)

# notify client upon completion
print("\nDone\nTotal Commands:", commandCount)