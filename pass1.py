from helper import *
import pprint as pr

MOT = readfile("MOT.txt")
POT = readfile("POT.txt")
print(POT[0].keys())
pr.pprint(MOT)
pr.pprint(POT)

if os.path.exists("sourcecode.txt"):
    f = open("sourcecode.txt","r")
    lines = f.readlines()
    for instr in lines:
        instr = instr.strip()
        words = instr.split(" ")
        if words[0] in [ entry["PsuedoOp"] for entry in POT]:
            print("POT")
        elif words[0] in [ entry["Mnemonic"] for entry in MOT]:
            print("MOT")
        else:
            print("label")