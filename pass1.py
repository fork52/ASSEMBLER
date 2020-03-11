from helper import *
import pprint as pr

MOT = readfile("MOT.txt")
POT = readfile("POT.txt")
ST_headers = ["Symbol","Value","Length","Relocation"]
ST=[]
print(POT[0].keys())
pr.pprint(MOT)
pr.pprint(POT)

if os.path.exists("sourcecode.txt"):
	f = open("sourcecode.txt","r")
	lines = f.readlines()
	for instr in lines:
		instr = instr.strip()
		#words = instr.split(" ")
		
		if instr in [ entry["Mnemonic"] for entry in MOT]:
			print("MOT")
		else:
			words = instr.split(" ")
			if words[0] in [ entry["PsuedoOp"] for entry in POT ]:
				print("POT")
			if words[0]=="DC":
				symbol,value=words[1].split(",")
				ST.append({"Symbol":symbol,"Value":value,"Length":"4","Relocation":"R"})    										
			else :
				ST.append({"Symbol":words[0],"Value":words[2],"Length":"4","Relocation":"R"})    		
				
	f.close()
	f = open("ST.txt","w")
	f.write(":".join(ST_headers) + "\n")		
	for S in ST:
		f.write(S["Symbol"]+":"+S["Value"]+":"+S["Length"] + ":" + S["Relocation"] +"\n")
			
	pr.pprint(ST)