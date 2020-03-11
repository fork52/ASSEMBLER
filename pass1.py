import helper
import pprint as pr
import os.path
from sys import exit

def check_RR_instr(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS TRUE IF INSTR IS A Reg-Reg INSTR Otherwise False
	'''
	list_of_RR_instr = []
	for entry in MOT:
		if entry['Format'] == '02': list_of_RR_instr.append(entry)
	return instr in list_of_RR_instr

def check_RI_instr(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS TRUE IF INSTR IS A Reg-Immediate INSTR Otherwise False
	'''
	# CREATE A LIST OF IMMEDIATE INSTRUCTIONS (format = 02)
	list_of_RI_instr = []
	for entry in MOT: 
		if entry['Format'] == '02': list_of_RI_instr.append(entry)

	for entry in list_of_RI_instr:
		if entry['Mnemonic'][:-3] in instr: return True
	return False
			

def assembler_pass1(filename):
	'''
	PERFORMS PASS1 OF ASSEMEBLER ON 'filename' which is the src code
	Generates ST.txt files
	'''
	MOT = helper.readfile("MOT.txt")
	POT = helper.readfile("POT.txt")
	ST_headers = ["Symbol","Value","Length","Relocation"]
	ST=[]                        #ST - Symbol Table

	# print(POT[0].keys())
	# pr.pprint(MOT)
	# pr.pprint(POT)

	if not os.path.exists(filename): 
		print('File Not Found...')
		exit()
	
	# Ignore all the whitespaces in the src code
	with open(filename, "r") as f:
		lines = [line.strip() for line in f if line.strip() ]
	print(lines)

	for instr in lines:
		instr = instr.strip().upper()
		#words = instr.split(" ")
		
		if check_RR_instr(instr,MOT):
			print("MOT RR instr")
		elif check_RI_instr(instr,MOT):
			print("MOT RI instr")
			 	
		else:
			words = instr.split(" ")
			if words[0] in [ entry["PsuedoOp"] for entry in POT ]:
				print("POT instr")

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

if __name__ == '__main__':
	assembler_pass1('sourcecode.txt')