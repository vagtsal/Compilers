#Tsalesis Evangelos
#AM: 1779
#username: cs091779

#compile: python3 compiler.py <filename>.ci

#  ------------------------Complete Compiler----------------------------
#  Input: 	Ciscal source code (<filename>.ci)
#  Performs lexical, syntax and semantic analysis, generates symbol table
#  Outputs:	Intermediate code (<filename>.int)
#			Intermediate C code (<filename>.c)
#			Final Code in MIPS assembly (<filename>.asm)

# A 2 test files of a dummy ciscal program are used to test compiler's performance. ("test_form.ci", "test_function.ci")


import sys

# -------------------------States (lex)----------------------------
FIRST_ST		=	0
ID_STN 			=	1
NUMBER_STN		=	2
LESSTHAN_ST1	=	3
GREATERTHAN_ST1	=	4
COLON_ST1		=	5
OP_COMMENTS_ST1	=	6
OP_COMMENTS_ST2	=	7
OP_COMMENTS_ST3	=	8

# ----------------------Final States (lex)-------------------------
PLUS_ST			= 	20
MINUS_ST		=	21
EQUAL_ST		=	22
SEMICOLON_ST	= 	23
COMMA_ST		=	24
COLON_ST 		= 	25
OP_BRACE_ST		=	26
CL_BRACE_ST		=	27
OP_PAR_ST		=	28
CL_PAR_ST		=	29
OP_BRACKET_ST	=	30
CL_BRACKET_ST	=	31
ID_ST 			=	32
NUMBER_ST 		=	33
MUL_ST 			=	34
DIV_ST 			=	35
LESSTHAN_ST 	=	36
GREATERTHAN_ST	=	37
LGT_ST			=	38
LT_EQUAL_ST		=	39
GT_EQUAL_ST		=	40
ASSIGN_ST		=	41

EOF_ST			=	-1
ERROR_ST		=	-2

AND_ST			=	50
DECLARE_ST		=	51
DO_ST			=	52
ELSE_ST			=	53
ENDDECLARE_ST	=	54
EXIT_ST			=	55
PROCEDURE_ST	=	56
FUNCTION_ST		=	57
PRINT_ST		=	58
CALL_ST			=	59
IF_ST			=	60
IN_ST			=	61
INOUT_ST		=	62
NOT_ST			=	63
SELECT_ST		=	64
PROGRAM_ST		=	65
OR_ST 			=	66
RETURN_ST		=	67
WHILE_ST		=	68
DEFAULT_ST		=	69
#---------------------------------------------------------------


#----------------------global variables-------------------------
token = 0
word = ''
line_number = 1
#---------------------------------------------------------------


#------------------------Error handling-------------------------
def error(error_str):
	print("Error in line: ", line_number)
	#print("        -->",word,"<--")
	print("Error:", error_str)
	sys.exit(0)
#----------------------------------------------------------------


#-----------------------Lexical Analysis-------------------------
def lex():
	global word
	global line_number

	word = ''
	state = 0

	symbols = {
	'+':3, 
	'-':4, 
	'*':5, 
	'/':6,
	'\\':7, 
	'<':8, 
	'>':9, 
	'=':10, 
	':':11, 
	';':12, 
	',':13,
	'{':14, 
	'}':15, 
	'(':16, 
	')':17, 
	'[':18, 
	']':19,
	'':20}

	reserved_words = {
	'and':AND_ST, 
	'declare':DECLARE_ST, 
	'do':DO_ST, 
	'else':ELSE_ST, 
	'enddeclare':ENDDECLARE_ST, 
	'exit':EXIT_ST, 
	'procedure':PROCEDURE_ST, 
	'function':FUNCTION_ST,
	'print':PRINT_ST, 
	'call':CALL_ST, 
	'if':IF_ST, 
	'in':IN_ST, 
	'inout':INOUT_ST, 
	'not':NOT_ST, 
	'select':SELECT_ST, 
	'program':PROGRAM_ST, 
	'or':OR_ST, 
	'return':RETURN_ST, 
	'while':WHILE_ST, 
	'default':DEFAULT_ST}
	
	stateMatrix = [[FIRST_ST,ID_STN,NUMBER_STN,PLUS_ST,MINUS_ST,MUL_ST,DIV_ST,OP_COMMENTS_ST1,LESSTHAN_ST1,GREATERTHAN_ST1,EQUAL_ST,COLON_ST1,SEMICOLON_ST,COMMA_ST,OP_BRACE_ST,CL_BRACE_ST,OP_PAR_ST,CL_PAR_ST,OP_BRACKET_ST,CL_BRACKET_ST,EOF_ST,ERROR_ST],
	[ID_ST,ID_STN,ID_STN,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST,ID_ST],
	[NUMBER_ST,ERROR_ST,NUMBER_STN,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST,NUMBER_ST],
	[LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LGT_ST,LT_EQUAL_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST,LESSTHAN_ST],
	[GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GT_EQUAL_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST,GREATERTHAN_ST],
	[COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,ASSIGN_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST,COLON_ST],
	[ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,OP_COMMENTS_ST2,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST,ERROR_ST],
	[OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST3,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,ERROR_ST,OP_COMMENTS_ST2],
	[OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST3,OP_COMMENTS_ST2,FIRST_ST,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,OP_COMMENTS_ST2,ERROR_ST,OP_COMMENTS_ST2]]

	while state <= 8 and state >= 0: 
		c = fid.read(1)

		if '\n' in c:
			line_number = line_number + 1
		if c.isspace():
			input_char = 0
		elif c.isalpha():
			input_char = 1
		elif c.isdigit():
			input_char = 2
		elif c in symbols:
			input_char = symbols[c]
		else: 
			input_char = 21

		word = word + c
		state = stateMatrix[state][input_char]
		if state == FIRST_ST:
			word = ''

	if (c != '' and (state == COLON_ST or state == ID_ST  or state == NUMBER_ST or state == LESSTHAN_ST or state == GREATERTHAN_ST)):
		back = fid.tell() -1
		fid.seek(back)
		if '\n' in word[-1:]:
			line_number = line_number - 1
		word = word[:-1]

	if (state == NUMBER_ST and int(word) > 32768):
		state = ERROR_ST
	if (state == ID_ST and len(word) > 30):
		word = word[:30]
	if (state == ID_ST and word in reserved_words):
		state = reserved_words[word]
	
	#print(word, state)		#debugging
	return state
#-----------------------------------------------------------------------	


#------------------------Syntax Analysis--------------------------------
doWhileFlag = 0			#checks whether parser is inside a "do_while" loop
funcFlag = 0			#checks whether parser is inside a function
returnFlag = False		#checks whether there is a 'return' inside a function

def program():
	global token
	global word

	token = lex()
	if token == PROGRAM_ST:
		token = lex()
		if token == ID_ST:
			newScope()
			blockName = word
			genquad("begin_block",blockName,"_","_")
			block()
			deleteScope()
			genquad("halt","_","_","_")
			genquad("end_block",blockName,"_","_")
			token = lex()
			if token != EOF_ST:
				error("code after program block")
		else:
			error("valid program name expected")
	else:
		error("'program' keyword expected")


def block():
	global token
	global word

	global symbolTable
	global mainStart

	token = lex()
	if token == OP_BRACE_ST:
		token = lex()
		if (token == DECLARE_ST):
			declarations()
			token = lex()
		subprograms()

		# update startQuad
		if len(symbolTable) > 1:
			symbolTable[-2][subprogName[-1]][1] = nextquad()
		elif len(symbolTable) == 1:
			mainStart = nextquad() 
		
		sequence()
		if token != CL_BRACE_ST:
			error("'}' expected")
	else:
		error("'{' expected")


def declarations():
	global token
	global word

	token = lex()
	if token == ID_ST:
		insertEntity(word, "var")
		varlist()
	if token != ENDDECLARE_ST:
		error("'enddeclare' keyword expected")


def varlist():
	global token
	global word

	token = lex()
	while token == COMMA_ST:
		token = lex()
		if token == ID_ST:
			insertEntity(word, "var")
		else:
			error("valid variable name expected")
		token = lex()


def subprograms():
	global token
	global word
	global funcFlag
	global returnFlag
	global subprogName

	isFunction = False

	while token == PROCEDURE_ST or token == FUNCTION_ST:
		if (token == FUNCTION_ST):
			isFunction = True
			funcFlag += 1
		token = lex()
		if token == ID_ST:			
			if isFunction == True:
				insertEntity(word, "func")
			else:
				insertEntity(word, "proc")
			newScope()
			blockName = word
			genquad("begin_block",blockName,"_","_")
			funcbody()
			deleteScope()
			genquad("end_block",blockName,"_","_")
		else:
			error("valid procedure/function name expected")
		token = lex()
		if isFunction == True:
			if returnFlag == True:
				returnFlag = False
				isFunction = False
				funcFlag -= 1
			else:
				error("no 'return' statement in the function '" + blockName + "'")


def funcbody():
	global token
	global word

	formalpars()
	block()


def formalpars():
	global token
	global word

	token = lex()
	if (token == OP_PAR_ST):
		formalparlist()
		if (token != CL_PAR_ST):
			error("')' expected")
	else:
		error ("'(' expected")


def formalparlist():
	global token
	global word

	formalparitem()
	while token == COMMA_ST:
			formalparitem()


def formalparitem():
	global token
	global word
	global SymbolTable
	global subprogName

	token = lex()
	if  token == IN_ST or token == INOUT_ST:
		if word == "in":
			parMode = "cv"
		else:
			parMode = "ref"
		token = lex()
		if token == ID_ST:
			insertEntity(word, parMode)
			token = lex()
		else:
			error("valid variable name expected")


def sequence():
	global token
	global word

	statement()
	while token == SEMICOLON_ST:
		token = lex()
		statement()


def brackets_seq():
	global token
	global word

	sequence()
	if (token != CL_BRACE_ST):
		error("'}' expected")


def brack_or_stat():
	global token
	global word

	token = lex()
	if (token == OP_BRACE_ST):
		token = lex()
		brackets_seq()
	else:
		statement()
		if token != SEMICOLON_ST:
			error("';' expected")


def statement():
	global token
	global word

	if token == ID_ST:
		assignment_stat(word)
	elif token == IF_ST:
		if_stat()
	elif token == DO_ST:
		do_while_stat()
		token = lex()
	elif token == WHILE_ST:
		while_stat()
		token = lex()
	elif token == SELECT_ST:
		select_stat()
		token = lex()
	elif token == EXIT_ST:
		exit_stat()
		token = lex()
	elif token == RETURN_ST:
		return_stat()
		token = lex()
	elif token == PRINT_ST:
		print_stat()
		token = lex()
	elif token == CALL_ST:
		call_stat()
		token = lex()
	elif token == SEMICOLON_ST:
		error("Invalid use of semicolon")


def assignment_stat(z):
	global token
	global word
	global w

	findEntity(z, ["var","cv","ref"])
	token = lex()
	if token == ASSIGN_ST:
		token = lex()
		expression()
		genquad(":=",w,"_",z)
	else:
		error("assignment symbol ':=' expected")


def if_stat():
	global token
	global word

	token = lex()
	if token == OP_PAR_ST:
		condQuadList = [[],[]]
		condition(condQuadList)
		if token == CL_PAR_ST:
			backpatch(condQuadList[1],nextquad())
			brack_or_stat()
			token = lex()
			if token == ELSE_ST:
				jumpElseQuad = [nextquad()]
				genquad("jump","_","_","_")
				backpatch(condQuadList[0],nextquad())
				brack_or_stat()
				backpatch(jumpElseQuad,nextquad())
				token = lex()
			else:
				backpatch(condQuadList[0],nextquad())
		else:
			error("')' expected")
	else:
		error("'(' expected")


def while_stat():
	global token
	global word

	token = lex()
	if token == OP_PAR_ST:
		jumpLoop = nextquad()
		condQuadList = [[],[]]
		condition(condQuadList)
		backpatch(condQuadList[1],nextquad())
		if token == CL_PAR_ST:
			brack_or_stat()
			genquad("jump","_","_",str(jumpLoop))
			backpatch(condQuadList[0],nextquad())
		else:
			error("')' expected")
	else:
		error("'(' expected")


def select_stat():
	global token
	global word

	endSelection = []

	token = lex()
	if token == OP_PAR_ST:
		token = lex()
		if token == ID_ST:
			x = word
			token = lex()
			if token == CL_PAR_ST:
				token = lex()
				counter = 1
				while token == NUMBER_ST:
					if counter == int(word):
						genquad("=",x,word,str(nextquad()+2))
						counter = counter + 1
					else:
						error("not valid constants in 'select' statement")
					token = lex()
					if token == COLON_ST:
						jumpSelection = [nextquad()]
						genquad("jump","_","_","_")
						brack_or_stat()
						endSelection = endSelection + [nextquad()] 
						genquad("jump","_","_","_")
						backpatch(jumpSelection, nextquad())
					else:
						error("':' expected")
					token = lex()
				if token == DEFAULT_ST:
					token = lex()
					if token == COLON_ST:
						brack_or_stat()
						backpatch(endSelection,nextquad())
					else:
						error("':' expected")
				else:
					error("'default' keyword expected")
			else:
				error("')' expected")
		else:
			error("valid variable name expected")
	else:
		error("'(' expected")


def do_while_stat():
	global token
	global word
	global exitQuad
	global doWhileFlag

	doWhileFlag += 1

	jumpLoop = nextquad()
	brack_or_stat()
	token = lex()
	if token == WHILE_ST:
		token = lex()
		if token == OP_PAR_ST:	
			condQuadList = [[],[]]
			condition(condQuadList)
			if (exitQuad != []):
				backpatch(exitQuad, nextquad())
				exitQuad = []
			backpatch(condQuadList[0],nextquad())
			backpatch(condQuadList[1],jumpLoop)
			if token != CL_PAR_ST:
				error("')' expected")
		else:
			error("'(' expected")
	else:
		error("'while' keyword expected")

	doWhileFlag -= 1


def exit_stat():
	global token
	global word
	global exitQuad

	if (doWhileFlag == 0):
		error("'exit' outside a do_while loop")
	exitQuad = exitQuad + [nextquad()]
	genquad("jump","_","_","_")



def return_stat():
	global token
	global word
	global funcFlag
	global returnFlag

	if (funcFlag == 0):
		error("'return' outside a function")

	returnFlag = True

	token = lex()
	if token == OP_PAR_ST:
		token = lex()
		expression()
		genquad("retv", w, "_", "_")
		if token != CL_PAR_ST:
			error("')' expected")
	else:
		error("'(' expected")


def print_stat():
	global token
	global word

	token = lex()
	if token == OP_PAR_ST:
		token = lex()
		expression()
		genquad("out", w, "_", "_")
		if token != CL_PAR_ST:
			error("')' expected")
	else:
		error("'(' expected")


def call_stat():
	global token
	global word

	token = lex()
	if token == ID_ST:
		name = word
		findEntity(name,["proc"])
		token = lex()
		actualpars()
		genquad("call", name, "_","_")
	else:
		error("valid function name expected")


def actualpars():
	global token
	global word
	global parList

	if token == OP_PAR_ST:
		actualparlist()
		if token != CL_PAR_ST:
			error("')' expected")
	else:
		error("'(' expected")
	if len(parList) != 0:
				error("Too few arguments")


def actualparlist():
	global token
	global word

	actualparitem()
	while token == COMMA_ST:
		actualparitem()


def actualparitem():
	global token
	global word
	global parList

	token = lex()
	if token == IN_ST:
		if len(parList) != 0:
			token = lex()
			expression()
			if parList[0][1] == "cv":
				genquad("par",w,"cv","_")
			else:
				error("Argument type mismatch in '" + w + "': 'in' instead of 'inout'")
		else:
			error("Too many arguments")
		parList = parList[1:]
	elif token == INOUT_ST:
		if len(parList) != 0:
			token = lex()
			if token == ID_ST:
				findEntity(word,["var","cv","ref"])
				if parList[0][1] == "ref":
					genquad("par",word,"ref","_")
				else:
					error("Argument type mismatch in '" + word + "': 'inout' instead of 'in'")
				token = lex()
			else:
				error("valid variable name expected")
		else:
			error("Too many arguments")
		parList = parList[1:]
	


def condition(condQuadList):
	global token
	global word

	condQuadList2 = [[],[]]			#list of two lists, condQuadList[0]:Q.false, condQuadList[1]:Q.true

	boolterm(condQuadList2)
	condQuadList[1] = condQuadList2[1]
	condQuadList[0] = condQuadList2[0]
	while token == OR_ST:
		backpatch(condQuadList2[0],nextquad())
		boolterm(condQuadList2)
		condQuadList[1] = condQuadList[1] + condQuadList2[1]
		condQuadList[0] = condQuadList2[0]


def boolterm(condQuadList2):
	global token
	global word

	condQuadList3 = [[],[]]

	boolfactor(condQuadList3)
	condQuadList2[1] = condQuadList3[1]
	condQuadList2[0] = condQuadList3[0]
	while token == AND_ST:
		backpatch(condQuadList2[1],nextquad())
		boolfactor(condQuadList3)
		condQuadList2[0] = condQuadList2[0] + condQuadList3[0]
		condQuadList2[1] = condQuadList3[1]


def boolfactor(condQuadList3):
	global token
	global word

	token = lex()
	if token == NOT_ST:
		token = lex()
		if token == OP_BRACKET_ST:
			condQuadList = [[],[]]
			condition(condQuadList)
			condQuadList3[1] = condQuadList[0]
			condQuadList3[0] = condQuadList[1]
			if token != CL_BRACKET_ST:
				error("']' expected")
			token = lex()
		else:
			error("'[' expected")
	elif token == OP_BRACKET_ST:		
		condQuadList = [[],[]]
		condition(condQuadList)
		condQuadList3[1] = condQuadList[1]
		condQuadList3[0] = condQuadList[0]
		if token != CL_BRACKET_ST:
			error("']' expected")
		token = lex()
	else:
		expression()
		T1 = w
		relational_oper()
		relOper = word
		token = lex()
		expression()
		T2 = w
		condQuadList3[1] = [nextquad()]
		genquad(relOper,T1,T2,"_")
		condQuadList3[0] = [nextquad()]
		genquad("jump","_","_","_")


def expression():
	global token
	global word
	global w

	if token == PLUS_ST or token == MINUS_ST:
		oper = word
		token = lex()
		T2 = term()
		w = newtemp()
		genquad(oper,"0",T2,w)
		T1 = w
	else:
		T1 = term()
		w = T1
	while token == PLUS_ST or token == MINUS_ST:
		oper = word
		token = lex()
		T2 = term()
		w = newtemp()
		genquad(oper, T1, T2, w)
		T1 = w


def term():
	global token
	global word
	global w

	T1 = factor()
	while token == MUL_ST or token == DIV_ST:
		oper = word
		token = lex()
		T2 = factor()
		w = newtemp()
		genquad(oper, T1, T2, w)
		T1 = w
	return T1

def factor():
	global token
	global word
	global w
	global parList

	if token == NUMBER_ST:
		fact = word
		token = lex()
		return fact
	elif token == OP_PAR_ST:
		token = lex()
		expression()
		if token != CL_PAR_ST:
			error("')' expected")
		token = lex()
		return w
	elif token == ID_ST:
		fact = word
		token = lex()
		if token == OP_PAR_ST:			#id_tail
			findEntity(fact, ["func"])
			actualpars()
			w = newtemp()
			genquad("par",w,"ret","_")
			genquad("call",fact,"_","_")
			token = lex()
			return w
		findEntity(fact, ["var","cv","ref"])
		return fact
	else:
		error("a valid factor expected")


def relational_oper():
	global token
	global word

	if token != EQUAL_ST and token != LESSTHAN_ST and  token != LT_EQUAL_ST and token != LGT_ST and token != GT_EQUAL_ST and token != GREATERTHAN_ST:
		error("relational operator expected")


#------------------------------------------------------------------------------------------------------------


#--------------------------------------------Intermediate Code-----------------------------------------------
quadNo = 0
quadList = []		# stores all quads
tempVarNo = 0
w = ""				# current temp variable

exitQuad = []

# returns next quad number
def nextquad():
	return quadNo

# generates a quad
def genquad(op, x, y, z):
	global quadNo
	global quadList

	quadList.append([op,x,y,z])
	quadNo += 1

# inserts z value into a list of quads
def backpatch(list, z):
	for quadListNo in list:
		quadList[quadListNo][3] = str(z)

# returns a new temp variable
def newtemp():
	global tempVarNo
	global symbolTable

	tempVarNo += 1
	tempVar = "T_" + str(tempVarNo)
	insertEntity(tempVar, "tempVar")
	return tempVar

# prints quads (debug mode)
def printquads():
	lineNo = 0
	for quad in quadList:
		print(str(lineNo) + ": (" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")")
		lineNo += 1

# writes quads into a *.int file
def intCreator():
	try:
		fidInt = open(sys.argv[1].split(".")[0] + ".int", 'w')
	except:
		sys.exit("Cannot create .int file")
	
	lineNo = 0
	for quad in quadList:
		fidInt.write(str(lineNo) + ": (" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		lineNo += 1

#----------------------------------------------------------------------------------------------------------------


#---------------------------------------------Symbol Table---------------------------------------------------

# Symbol Table Structure
#-----------------------
# Symbol Table is a List of dictionaries. Every dictionary is a scope.
# Dictionaries contain names of symbols as keys and their lists of attributes as keys' values
# Examples:
# "funcname": ["func", number of first quad, [list of arguments], framelength]
# "varname": ["var", offset]
# "argname": ["arg", "ref/cv"]


# A List (scopes) of dictionaries containing entities (key:name of symbol, value: list of attributes)
symbolTable = []
savedSymbolTable = {}	# dictionary of dictionaries, stores entities of every block (used for intermediate c and final code)					

subprogName = ['']	#function/subroutine names stack
offset = 0 	
mainFrameLength = 0
mainStart = 0
parList = []

# creates a new scope (adds a dictionary into symboltable list)
def newScope():
	global symbolTable
	global offset

	global subprogName

	if len(symbolTable) != 0:
		subprogName.append(word)

	symbolTable.append({})


# deletes last scope (and saves the current scope for final code generation)
def deleteScope():
	global symbolTable
	global savedSymbolTable
	global subprogName

	savedSymbolTable[subprogName[-1]] = symbolTable[-1]

	symbolTable = symbolTable[:-1]

	if len(subprogName) > 1:	
		subprogName = subprogName[:-1]


# inserts an entity into symbol table (checks for redeclarations)
def insertEntity(name, symType):
	global symbolTable
	global offset
	global mainFrameLength

	if name in symbolTable[0]:
		error("Redeclaration of global symbol \"" + name + "\"")

	if name not in symbolTable[-1]:
		if symType is "func" or symType is "proc":
			symbolTable[-1][name] = [symType, 0, [], 12]

		else:
			if len(subprogName) != 1:
				offset = symbolTable[-2][subprogName[-1]][3]
			else:
				offset = mainFrameLength
			symbolTable[-1][name] = [symType, offset]
			if symType is "cv" or symType is "ref":
				symbolTable[-2][subprogName[-1]][2].append([name,symType])
			if len(symbolTable) != 1:
				symbolTable[-2][subprogName[-1]][3] = symbolTable[-2][subprogName[-1]][3] + 4
			else:
				mainFrameLength = mainFrameLength + 4
	else:
		error("Redeclaration of symbol \"" + name + "\"")

	if debugSymTable == True: printTable()
	

# searches for an entity in symbol table
def findEntity(name,typeList):
	global symbolTable
	global parList

	for scope in symbolTable:
		if name in scope:
			if scope[name][0] in typeList:
				if scope[name][0] in ["proc","func"]:
					parList = scope[name][2]
				return
			else:
				error("Bad type of symbol '" + name + "'")
	error("Symbol '" + name + "' is not declared")


# prints symbol table (debug)
def printTable():
	for scope in symbolTable:
		for key in scope:
			print(key + ": [", end="")
			print(','.join(map(str, scope[key])), end="")
			print("]   ", end="")
		print("\n")
	print("--------------------------")


#---------------------------------------------------------------------------------------------------------


#------------------------------------------Intermediate C code-----------------------------------------------------

# For C int. code (see below in "deleteScope" function)


# generates *.c file
def CintCreator():
	tabNo = 0
	mainFlag = False
	callArgs = []
	returnVar = ""
	indent = 0
	indentation = "".join(indent*"\t")

	# useful lists generated from savedSymbolTable
	cVar = {}
	cArg = {}
	cProc = []
	for blockDictionary in savedSymbolTable:
		for entity in savedSymbolTable[blockDictionary]:
			if savedSymbolTable[blockDictionary][entity][0] == "var" or savedSymbolTable[blockDictionary][entity][0] == "tempVar":
				if blockDictionary not in cVar:
					cVar[blockDictionary] = []
				cVar[blockDictionary].append(entity)
			elif savedSymbolTable[blockDictionary][entity][0] == "func" or savedSymbolTable[blockDictionary][entity][0] == "proc":
				if entity not in cArg:
					cArg[entity] = []
				for argument in savedSymbolTable[blockDictionary][entity][2]:
					if argument[1] == "ref":
						cArg[entity].append("*" + argument[0])
					else:
						cArg[entity].append(argument[0])
			else:
				if blockDictionary not in cVar:
					cVar[blockDictionary] = []
			if  savedSymbolTable[blockDictionary][entity][0] == "proc":
				cProc.append(entity)

	try:
		fidC = open(sys.argv[1].split(".")[0] + ".c", 'w')
	except:
		sys.exit("Cannot create .c file")

	fidC.write("#include <stdio.h>\n\n")

	lineNo = 0
	for quad in quadList:
		if quad[0] == ":=":
			fidC.write(indentation + "L_" + str(lineNo) + ": " + quad[3] + " = " + quad[1] + ";  //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		elif quad[0] == "+" or quad[0] == "-" or quad[0] == "*" or quad[0] == "/":
			fidC.write(indentation + "L_" + str(lineNo) + ": " + quad[3] + " = " + quad[1] + " " + quad[0] + " " + quad[2] + ";  //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		elif quad[0] == "=" or quad[0] == "<" or quad[0] == ">" or quad[0] == "<>" or quad[0] == ">=" or quad[0] == "<=":
			if quad[0] == "<>":
				conditional = "!="
			elif quad[0] == "=":
				conditional = "=="
			else:
				conditional = quad[0]
			fidC.write(indentation + "L_" + str(lineNo) + ": if (" + quad[1] + " " + conditional + " " + quad[2] + ") goto L_" + quad[3] + ";  //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		elif quad[0] == "jump":
			fidC.write(indentation + "L_" + str(lineNo) + ": goto L_"  + quad[3] + ";  //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		elif quad[0] == "begin_block":
			if lineNo == 0:
				fidC.write("int main()\n{\n")
				indent += 1
				indentation = "".join(indent*"\t")
				if len(cVar[""]) > 0:
					fidC.write(indentation + "int ")
					fidC.write(",".join(cVar[""]))
					fidC.write(";\n\n")
			else:
				args = ", int ".join(cArg[quad[1]])
				if quad[1] in cProc:
					fidC.write(indentation + "void ")
				else:
					fidC.write(indentation + "int ")
				if len(cArg[quad[1]]) != 0:
					fidC.write(quad[1] + "(int " + args + ")\n")
				else:
					fidC.write(quad[1] + "()\n")
				fidC.write(indentation + "{\n")
				indent += 1
				indentation = "".join(indent*"\t")
				if len(cVar[quad[1]]) > 0:
					fidC.write(indentation + "int ")
					fidC.write(",".join(cVar[quad[1]]))
					fidC.write(";\n\n")
		elif quad[0] == "end_block":
			fidC.write(indentation + "L_" + str(lineNo) + ": ;   //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
			indent -= 1
			indentation = "".join(indent*"\t")
			fidC.write(indentation + "}\n\n")
		elif quad[0] == "par":
			fidC.write(indentation + "L_" + str(lineNo) + ": ;   //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
			if quad[2] != "ret":
				if quad[2] == "ref":
					callArgs.append("&" + quad[1])
				else:
					callArgs.append(quad[1])
			else:
				returnVar = quad[1]
		elif quad[0] == "call":
			if returnVar != "":
				fidC.write(indentation + "L_" + str(lineNo) + ": " + returnVar + " = " + quad[1] + "(") 
				returnVar = ""
			else:
				fidC.write(indentation + "L_" + str(lineNo) + ": " + quad[1] + "(") 
			fidC.write(",".join(callArgs))
			fidC.write(");   //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
			callArgs = []
		elif quad[0] == "out":
			fidC.write(indentation + "L_" + str(lineNo) + ": " + "printf " + "(\"%d\\n\"," + quad[1] + ");   //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		elif quad[0] == "halt":
			fidC.write(indentation + "L_" + str(lineNo) + ": ;   //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		elif quad[0] == "retv":
			fidC.write(indentation + "L_" + str(lineNo) + ": " + "return " + "(" + quad[1] + ");   //(" + quad[0] + ", " + quad[1] + ", " + quad[2] + ", " + quad[3] + ")\n")
		
		lineNo += 1

#------------------------------------------------------------------------------------------------------------


#------------------------------------------Final Code--------------------------------------------------------
finalCode = []

subroutineStack = [""]	#stores the current scope structure (useful in conjuction with savedSymbolTable)

# loads the address of a non local variable to $t0 register
def gnvlcode(v):
	global subroutineStack
	global finalCode
	
	print(v)
	scope = -2
	finalCode.append("lw $t0,-4($sp)")
	while v not in savedSymbolTable[subroutineStack[scope]]:
		finalCode.append("lw $t0,-4($t0)")
		scope = scope - 1	
	offset = savedSymbolTable[subroutineStack[scope]][1]
	finalCode.append("add $t0,$t0,-" + str(offset))
	return scope


# loads a variable v to $tr register
def loadvr(v, r):
	global subroutineStack
	global finalCode

	#variable is number
	if v.isdigit():
		finalCode.append("li $t" + str(r) + "," + v)
	# variable is global
	elif v in savedSymbolTable[""]:
		offset = savedSymbolTable[""][v][1]
		finalCode.append("lw $t" + str(r) + ",-" + str(offset) + "($s0)")
	# variable is local
	elif v in savedSymbolTable[subroutineStack[-1]]:
		offset = savedSymbolTable[subroutineStack[-1]][v][1]
		if savedSymbolTable[subroutineStack[-1]][v][0] != "ref":
			finalCode.append("lw $t" + str(r) + ",-" + str(offset) + "($sp)")
		else:
			finalCode.append("lw $t0,-" + str(offset) + "($sp)")
			finalCode.append("lw $t" + str(r) + ",($t0)")
	# variable is not local
	else:
		scope = gnvlcode(v)
		if savedSymbolTable[subroutineStack[scope]][v][0] != "ref":
			finalCode.append("lw $t" + str(r) + ",($t0)")
		else:
			finalCode.append("lw $t0,($t0)")
			finalCode.append("lw $t" + str(r) + ",($t0)")


# stores a $tr register into memory of variable v
def storerv(r, v):
	global subroutineStack
	global finalCode

	# variable is global
	if v in savedSymbolTable[""]:
		offset = savedSymbolTable[""][v][1]
		finalCode.append("sw $t" + str(r) + ",-" + str(offset) + "($s0)")
	# variable is local
	elif v in savedSymbolTable[subroutineStack[-1]]:
		offset = savedSymbolTable[subroutineStack[-1]][v][1]
		if savedSymbolTable[subroutineStack[-1]][v][0] != "ref":
			finalCode.append("sw $t" + str(r) + ",-" + str(offset) + "($sp)")
		else:
			finalCode.append("lw $t0,-" + str(offset) + "($sp)")
			finalCode.append("sw $t" + str(r) + ",($t0)")
	# variable is not local
	else:
		scope = gnvlcode(v)
		if savedSymbolTable[subroutineStack[scope]][v][0] != "ref":
			finalCode.append("sw $t" + str(r) + ",($t0)")
		else:
			finalCode.append("lw $t0,($t0)")
			finalCode.append("sw $t" + str(r) + ",($t0)")


# generates *.asm file
def FinalCreator():
	global subroutineStack
	global finalCode

	parameters = []
	framelength = 0

	# finds all subroutines' starting points to add (sw $ra,($sp) instruction)
	startingPoints = []
	for functions in savedSymbolTable:
		for entity in savedSymbolTable[functions]:
			if savedSymbolTable[functions][entity][0] in ["proc","func"]:
				startingPoints.append(savedSymbolTable[functions][entity][1])

	finalCode.append("add $sp,$sp," + str(mainFrameLength))
	finalCode.append("move $s0,$sp")
	finalCode.append("j L_" + str(mainStart))
	
	lineNo = 0
	for quad in quadList:
		finalCode.append("L_" + str(lineNo) + ": #(" + quad[0] + "," + quad[1] + "," + quad[2] + "," + quad[3] + ")")
		if lineNo in startingPoints:
			finalCode.append("sw $ra,($sp)")
		if quad[0] == "jump":			
			finalCode.append("j L_" + quad[3])
		elif quad[0] == "=":
			loadvr(quad[1],1)
			loadvr(quad[2],2)
			finalCode.append("beq,$t1,$t2,L_" + quad[3])
		elif quad[0] == ">":
			loadvr(quad[1],1)
			loadvr(quad[2],2)
			finalCode.append("bgt,$t1,$t2,L_" + quad[3])
		elif quad[0] == "<":
			loadvr(quad[1],1)
			loadvr(quad[2],2)
			finalCode.append("blt,$t1,$t2,L_" + quad[3])
		elif quad[0] == ">=":
			loadvr(quad[1],1)
			loadvr(quad[2],2)
			finalCode.append("bge,$t1,$t2,L_" + quad[3])
		elif quad[0] == "<=":
			loadvr(quad[1],1)
			loadvr(quad[2],2)
			finalCode.append("ble,$t1,$t2,L_" + quad[3])
		elif quad[0] == "<>":
			loadvr(quad[1],1)
			loadvr(quad[2],2)
			finalCode.append("bne,$t1,$t2,L_" + quad[3])
		elif quad[0] == ":=":
			loadvr(quad[1], 1)
			storerv(1, quad[3])
		elif quad[0] == "+":
			loadvr(quad[1], 1)
			loadvr(quad[2], 2)
			finalCode.append("add $t1,$t1,$t2")
			storerv(1,quad[3])
		elif quad[0] == "-":
			loadvr(quad[1], 1)
			loadvr(quad[2], 2)
			finalCode.append("sub $t1,$t1,$t2")
			storerv(1,quad[3])
		elif quad[0] == "*":
			loadvr(quad[1], 1)
			loadvr(quad[2], 2)
			finalCode.append("mul $t1,$t1,$t2")
			storerv(1,quad[3])
		elif quad[0] == "/":
			loadvr(quad[1], 1)
			loadvr(quad[2], 2)
			finalCode.append("div $t1,$t1,$t2")
			storerv(1,quad[3])
		elif quad[0] == "out":
			finalCode.append("li $v0,1")
			loadvr(quad[1], 1)
			finalCode.append("add $a0, $t1, $zero")
			finalCode.append("syscall")
		elif quad[0] == "par":
			parameters.append([quad[1],quad[2]])
		elif quad[0] == "call":
			i = 1
			while quad[1] not in savedSymbolTable[subroutineStack[-i]]:
				i = i - 1
			framelength = savedSymbolTable[subroutineStack[-i]][quad[1]][3]
			jumpCall = savedSymbolTable[subroutineStack[-i]][quad[1]][1]
			
			finalCode.append("add $fp,$sp," + str(framelength))
			i = 0
			for parameter in parameters:
				if parameter[1] == "cv":
					loadvr(parameter[0], 0)
					finalCode.append("sw $t0,-" + str(12+4*i) + "($fp)")

				elif parameter[1] == "ref":
					if parameter[0] in savedSymbolTable[subroutineStack[-1]]:
						offset = savedSymbolTable[subroutineStack[-1]][parameter[0]][1]
						if savedSymbolTable[subroutineStack[-1]][parameter[0]][0] in ["cv","var","tempVar"]:
							finalCode.append("add $t0,$sp,-" + str(offset))
						elif savedSymbolTable[subroutineStack[-1]][parameter[0]][0] == "ref":
							finalCode.append("lw $t0,-" + str(offset) +"($sp)")
					else:
						scope = gnvlcode(parameter[0])
						if savedSymbolTable[subroutineStack[scope]][parameter[0]][0] == "ref":
							finalCode.append("lw $t0,($t0)")
					finalCode.append("sw $t0,-" + str(12+4*i) + "($fp)")
				elif parameter[1] == "ret":	
					offset = savedSymbolTable[subroutineStack[-1]][parameter[0]][1]
					finalCode.append("add $t0,$sp,-" + str(offset))
					finalCode.append("sw $t0,-8($fp)")		
				i = i + 1
			parameters = []
			if quad[1] in savedSymbolTable[subroutineStack[-1]]:
				finalCode.append("sw $sp,-4($fp)")
			else:
				finalCode.append("lw $t0,-4($sp)")
				finalCode.append("sw $t0,-4($fp)")
			finalCode.append("add $sp,$sp," + str(framelength))
			finalCode.append("jal L_" + str(jumpCall))
			finalCode.append("add $sp, $sp,-" + str(framelength))
		elif quad[0] == "retv" or quad[0] == "end_block":
			if quad[0] == "retv":
				loadvr(quad[1], 1)
				finalCode.append("lw $t0,-8($sp)")
				finalCode.append("sw $t1,($t0)")
			finalCode.append("lw $ra,($sp)")
			finalCode.append("jr $ra")
			if quad[0] == "end_block":
				subroutineStack = subroutineStack[:-1]
		elif quad[0] == "begin_block":
			if lineNo != 0:
				subroutineStack.append(quad[1])
		elif quad[0] == "halt":
			finalCode.append("L_" + str(lineNo+1) + ":")
			finalCode.append("add $v0,$zero,10")
			finalCode.append("syscall")
			break;
		lineNo = lineNo + 1
	
	try:
		fidF = open(sys.argv[1].split(".")[0] + ".asm", 'w')
	except:
		sys.exit("Cannot create .asm file")

	for instruction in finalCode:
		if instruction[:2] == "L_":
			fidF.write(instruction + "\n")
		else:
			fidF.write("\t" + instruction + "\n")




#---------------------------------------------------------------------------------------------------------

#---------------------------------main routine--------------------------------

debugSymTable = False 		# when true, prints SymbolTable before a scope is deleted
debugCintCode = False 		# debug Cint code
debugSavedSymTable = False 	# debug savedSymbolTable

try:
	fid = open(sys.argv[1], 'r')
except:
	sys.exit("File not found")


program()
print("1)Lexical, Syntax, Semantic analysis passed.")
intCreator()
CintCreator()
print("2)Intermediate Code is generated.")
FinalCreator()
print("3)Final Code is generated.")

#---------------debug code-------------
#printquads()				# prints quads
if debugSavedSymTable == True:
	for function in savedSymbolTable:
		print(function + " " + str(savedSymbolTable[function]))
if debugCintCode == True:
	print(cVar)				#print dict of variables for every block 	|
	print(cArg)				#prints dict of arguments for every block   | Used for C int code generation
	print(cProc)			#prints list of procedures' names 		    |
#--------------------------------------

#----------------------------------------------------------------------------