from helper import *
import pprint as pr

MOT = readfile("MOT.txt")
POT = readfile("POT.txt")
ST_headers = ["Symbol","Value","Length","Relocation"]
ST = readfile("ST.txt")

if os.path.exists("sourcecode.txt"):
	f = open("sourcecode.txt","r")
	lines = f.readlines()
	for instr in lines:
		instr = instr.strip()
		words = instr.split(" ")
		if instr in [ entry["Mnemonic"] for entry in MOT]:
			print("MOT")
		
	f.close()			
