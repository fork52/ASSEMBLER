import helper
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
	list_of_RI_instr =  [ entry['Mnemonic'] for entry in MOT if entry['Format']=='02']
	for entry in list_of_RI_instr:
		if entry[:-3] in instr: return True
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

	# 01 = 2 bytes, 10 = 4 bytes, 11 = 6 bytes
	locations = [] 					#Location counter

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

	# Add start address,
	locations.append(tuple([2]))

	# REMOVE START AND END FROM THE LIST
	lines = lines[1:-1]
	# print(lines)

	loccounter = 0
	for instr in lines:
		print(instr,locations[loccounter],end = '  ',sep='  ')
		instr = instr.strip().upper()
		loccounter+=1
		#words = instr.split(" ")
		
		if check_RR_instr(instr,MOT):
			print("MOT RR instr")
			locations.append(tuple( [locations[-1][0] + 2]))
		elif check_RI_instr(instr,MOT):
			print("MOT RI instr")
			locations.append(tuple([locations[-1][0] + 4]))
			 	
		else: #CASE WHEN WE HAVE DC OR EQU
			words = instr.split(" ")
			if words[0] in [ entry["PsuedoOp"] for entry in POT ]:
				locations.append(tuple([locations[-1][0] + 12]))
				print("POT instr")

			elif words[0]=="DC":
				symbol,value=words[1].split(",")
				ST.append({"Symbol":symbol,"Value":value,"Length":"4","Relocation":"R"})
				locations.append(tuple([locations[-1][0] + 6]))
				print("DC instructions")
			else :
				ST.append({"Symbol":words[0],"Value":words[2],"Length":"4","Relocation":"R"})
				locations.append(tuple([locations[-1][0] + 6]))
				print("EQU instructions")
				
	f.close()
	f = open("ST.txt","w")
	f.write(":".join(ST_headers) + "\n")		
	for S in ST:
		f.write(S["Symbol"]+":"+S["Value"]+":"+S["Length"] + ":" + S["Relocation"] +"\n")
	print()

if __name__ == '__main__':
	assembler_pass1('sourcecode.txt')