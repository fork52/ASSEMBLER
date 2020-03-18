import helper,re
import pprint as pr
import os.path
from sys import exit



#TODO : ADD LOGIC OF LOCATION COUNTER
#TODO : GENERATE A LIST OF UNDEFINED SYMBOLS TO BE SEARCHED IN PASS2
#TODO : CREATION OF RELATIVE ADDRESS W.R.T location counter

keywords = [i for i in 'ABCDEF']
keywords += ['ADD','MUL','SUB', 'MOV', 'START', 'END', 'DC', 'EQU', ]

global MOT, POT ,list_of_RR_instr,list_of_RM_instr,list_of_RI_instr,list_of_POT_instr,instr_list,locations,ST,ST_headers

MOT = helper.readfile("MOT.txt")
POT = helper.readfile("POT.txt")
list_of_RR_instr =  [entry for entry in MOT if entry['Format']=='01']
list_of_RM_instr = [ entry for entry in MOT if entry['Format']=='03']
list_of_RI_instr =  [ entry for entry in MOT if entry['Format']=='02']
list_of_POT_instr = [ entry for entry in POT ]
start_instr = [ entry for entry in MOT if entry['Mnemonic']=='START'][0]
end_instr = [ entry for entry in MOT if entry['Mnemonic']=='END'] [0]
instr_list = []
locations = []
ST=[]
ST_headers = ["Symbol","Value","Length","Relocation"]


def check_RR_instr(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS matched-instr IF 'instr' IS A Reg-Reg INSTR Otherwise False
	'''
	# CREATE A LIST OF RR INSTRUCTIONS (format = 01)
	for entry in list_of_RR_instr:
		if instr in entry['Mnemonic']:   return entry
	return False

def check_RI_instr(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS matched-instr IF 'instr' IS A Reg-Immediate INSTR Otherwise False
	'''
	# CREATE A LIST OF IMMEDIATE INSTRUCTIONS (format = 02)
	hex_no = re.compile('[a-fA-F0-9][a-fA-F0-9][hH]')
	try:
		for entry in list_of_RI_instr:
			if entry['Mnemonic'][:entry['Mnemonic'].index(',')] in instr:
				if hex_no.search(instr[instr.index(',')+1:]):
					return entry
		return False
	except: return False
	

def check_RI_mem(instr,MOT):
	'''
	INPUT : SINGLE LINE OF INSTR and MOT
	OUTPUT: RETURNS TRUE IF INSTR IS A Reg-Memory INSTR Otherwise False
	'''
	words = instr.split(",")
	identifier = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)
	try:
		for entry in list_of_RM_instr:
			if entry['Mnemonic'][:entry['Mnemonic'].index(',')] in instr and words[1] not in keywords:
				if identifier.search(instr[instr.index(',')+1:]):
					return entry
		return False
	except: return False

# def check_RI_mem(instr,MOT):
# 	'''
# 	INPUT : SINGLE LINE OF INSTR and MOT
# 	OUTPUT: RETURNS TRUE IF INSTR IS A Reg-Memory INSTR Otherwise False
# 	'''
# 	try:
# 		words = instr.split(",")
# 		reg = "A"
# 		if words[0][-1]=="A":
# 			reg = "B"
# 		if check_RR_instr(words[0]+","+reg, MOT):
# 			if words[1] not in keywords:
# 				for i in list_of_RM_instr:
# 					if i['Mnemonic'].split(",")[0] == words[0]:
# 						return i
# 			return False
# 		else:
# 			return False
# 	except:
# 		return False
			
def to_hex(string):
	# return string

	n = int(string, 16)
	bin = ''
	while n > 0:
		bin = str(n % 2) + bin
		n = n >> 1

	while len(bin)<6:
		bin = '0' + bin

	return bin


def assembler_pass1(filename):
	'''
	PERFORMS PASS1 OF ASSEMEBLER ON 'filename' which is the src code
	Generates ST.txt files
	'''



	# 01 = 2 bytes, 10 = 4 bytes, 11 = 6 bytes

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
	if lines[0] != 'START': print('START DIRECTIVE MISSING..'); exit()
	if lines[-1] !='END'  : print('END DIRECTIVE MISSING..') ; exit()

	# Add start address of the program - START instr is 4 bytes
	locations.append(tuple([2]))

	# REMOVE START AND END FROM THE LIST
	lines = lines[1:-1]
	# print(lines)

	loccounter = 0  # Keep track of relative address



	print()
	for instr in lines:
		# print('\nlocations=',locations,'loccounter=',loccounter)
		print(instr, locations[loccounter], end = '  ', sep='  ')
		instr = instr.strip().upper()
		loccounter+=1
		
		MOT_entry = check_RR_instr(instr , MOT)
		if MOT_entry: 
			instr_list.append(MOT_entry)
			locations.append( tuple( [locations[-1][0] + 2]) )
			print("MOT RR instr")
			continue
		
		MOT_entry = check_RI_instr(instr , MOT)
		if MOT_entry:
			instr_list.append(MOT_entry)
			locations.append(tuple([locations[-1][0] + 4]))
			print("MOT RI instr")
			continue

		MOT_entry = check_RI_mem(instr, MOT)
		if MOT_entry:
			instr_list.append(MOT_entry)
			locations.append(tuple([locations[-1][0] + 4]))
			print("MOT RM instr")
			continue
			 	
		#CASE WHEN WE HAVE DC OR EQU
		words = instr.split(" ")
		# if words[0] in [ entry["PsuedoOp"] for entry in POT ]:
		# 	locations.append(tuple([locations[-1][0] + 4]))
		# 	print("POT instr")
		if words[0]=="DC":
			symbol,value=words[1].split(",")
			ST.append({"Symbol":symbol,"Value":value, "Length":"4","Relocation":"R"})
			locations.append(tuple([locations[-1][0] + 4]))
			instr_list.append(list_of_POT_instr[1])
			print("DC instruction")
		elif words[1]=="EQU" :
			ST.append({"Symbol":words[0],"Value":words[2],"Length":"4","Relocation":"A"})
			locations.append(tuple([locations[-1][0] + 4]))
			instr_list.append(list_of_POT_instr[0])
			print("EQU instruction")

	print()
	pr.pprint(instr_list)	


	f.close()
	f = open("ST.txt","w")
	f.write(":".join(ST_headers) + "\n")		
	for S in ST:
		f.write(S["Symbol"]+":"+S["Value"]+":"+S["Length"] + ":" + S["Relocation"] +"\n")
	print()

	pr.pprint(ST)


def assembler_pass2(filename):

	with open(filename, "r") as f:
		lines = [line.strip() for line in f if line.strip()]

	lines = lines[1:-1] #striping start and end
	counter = 0

	objectcode = open("objectcode.txt", "w")
	objectcode.write(to_hex(start_instr["BinaryOp"]))
	objectcode.write("\n")

	for instr in instr_list:
		try:
			if instr["Format"]=="01":
				objectcode.write(to_hex(instr["BinaryOp"]))
				objectcode.write("\n")
			elif instr["Format"]=="02":
				objectcode.write(to_hex(instr["BinaryOp"]) + " " + to_hex(lines[counter].split(",")[-1][:-1]) )
				objectcode.write("\n")
			elif instr["Format"]=="03":
				mem = [ i for i in ST if lines[counter].split(",")[-1].upper()==i["Symbol"] ][0]
				objectcode.write(to_hex(instr["BinaryOp"]) + " " + to_hex(mem["Value"][:-1]) )
				objectcode.write("\n")
		except Exception as e:
			print(e)
		finally:
			counter+=1

	objectcode.write(to_hex(end_instr["BinaryOp"]))
	objectcode.close()


if __name__ == '__main__':
	assembler_pass1('sourcecode.txt')
	assembler_pass2('sourcecode.txt')