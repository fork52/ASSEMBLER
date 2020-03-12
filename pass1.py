import helper,re
import pprint as pr
import os.path
from sys import exit

#TODO : ADD LOGIC OF LOCATION COUNTER
#TODO : GENERATE A LIST OF UNDEFINED SYMBOLS TO BE SEARCHED IN PASS2
#TODO : CREATION OF RELATIVE ADDRESS W.R.T location counter


def check_RR_instr(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS TRUE IF INSTR IS A Reg-Reg INSTR Otherwise False
	'''
	# CREATE A LIST OF RR INSTRUCTIONS (format = 01)

	list_of_RR_instr =  [entry['Mnemonic'] for entry in MOT if entry['Format']=='01']
	return instr in list_of_RR_instr

def check_RI_instr(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS TRUE IF INSTR IS A Reg-Immediate INSTR Otherwise False
	'''
	# CREATE A LIST OF IMMEDIATE INSTRUCTIONS (format = 02)
	hex_no = re.compile('[a-fA-F0-9][a-fA-F0-9][hH]')
	list_of_RI_instr =  [ entry['Mnemonic'] for entry in MOT if entry['Format']=='02']
	try:
		for entry in list_of_RI_instr:
			if entry[:entry.index(',')] in instr:
				if hex_no.search(instr[instr.index(',')+1:]):
					return True
	except: pass
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
	# print(lines)

	# CHECK FOR START AND END IN THE BEGINNING AND END OF THE src code
	if lines[0] != 'START': print('START DIRECTIVE MISSING..') 
	if lines[-1] !='END'  : print('END DIRECTIVE MISSING..') 

	# REMOVE START AND END FROM THE LIST
	lines = lines[1:-1]
	# print(lines)

	for instr in lines:
		print(instr,'  ',end='')
		instr = instr.strip().upper()
		#words = instr.split(" ")
		
		if check_RR_instr(instr,MOT):
			print("MOT RR instr")
		elif check_RI_instr(instr,MOT):
			print("MOT RI instr")
			 	
		else: #CASE WHEN WE HAVE DC OR EQU
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
	print()
	pr.pprint(ST)

if __name__ == '__main__':
	assembler_pass1('sourcecode.txt')