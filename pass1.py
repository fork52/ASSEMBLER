import helper,re
import pprint as pr
import os.path
from sys import exit

#TODO : ADD LOGIC OF LOCATION COUNTER
#TODO : GENERATE A LIST OF UNDEFINED SYMBOLS TO BE SEARCHED IN PASS2
#TODO : CREATION OF RELATIVE ADDRESS W.R.T location counter

keywords = [i for i in 'ABCDEF']
keywords += ['ADD','MUL','SUB', 'MOV', 'START', 'END', 'DC', 'EQU', ]

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
	list_of_RI_instr =  [ entry['Mnemonic'] for entry in MOT if entry['Format']=='03']
	try:
		for entry in list_of_RI_instr:
			if entry[:entry.index(',')] in instr:
				if hex_no.search(instr[instr.index(',')+1:]):
					return True
	except: pass
	return False

def check_RI_mem(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS TRUE IF INSTR IS A Reg-Memory INSTR Otherwise False
	'''

	list_of_RM_instr = [ entry for entry in MOT if entry['Format']=='02']
	try:
		words = instr.split(",")
		reg = "A"
		if words[0][-1]=="A":
			reg = "B"
		if check_RR_instr(words[0]+","+reg, MOT):
			if words[1] not in keywords:
				for i in list_of_RM_instr:
					if i['Mnemonic'].split(",")[0] == words[0]:
						return i
				return
			return False
		else:
			return False
	except:
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
		elif check_RI_mem(instr, MOT):
			print("MOT RM instr")
			locations.append(tuple([locations[-1][0] + 4]))
			 	
		else: #CASE WHEN WE HAVE DC OR EQU
			words = instr.split(" ")
			if words[0] in [ entry["PsuedoOp"] for entry in POT ]:
				locations.append(tuple([locations[-1][0] + 4]))
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