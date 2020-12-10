import string
import argparse
import operator
from math import gcd

ACCEPTED_CHARS = set(string.ascii_uppercase)
ALPHABET_LENGTH = len(ACCEPTED_CHARS)
EXTRA_ASCII = 65 #min ASCII code of the alphabet

# Lee un archivo de texto y devuelve una string con sus contenidos
def read_text_file(filename):
	f = open(filename)
	return f.read()

# Encuentra los trigramas que aparecen al menos dos veces en una string y
# devuelve sus posiciones en un diccionario con clave=trigrama y valor=posiciones
def trigram_analysis(text):
	trigram_dict = {}
	searched_trigrams = []
	for posA in range(len(text)):
		trigram = text[posA:posA+3]
		if len(trigram)!=3:
			break
		if trigram in searched_trigrams:
			continue
		searched_trigrams.append(trigram)
		position_list = []
		for posB in range(len(text)):
			trigram_compare = text[posB:posB+3]
			if len(trigram_compare)!=3:
				break
			if trigram == trigram_compare:
				position_list.append(posB)
		if len(position_list)>1:
			trigram_dict[trigram]=position_list
	return trigram_dict
	
# Convierte el diccionario de trigramas devuelto por trigram_analysis a
# uno con posiciones relativas a partir de la primera aparición de un trigrama
def get_relative_positions(trigram_dict):
	relative_positions=[]
	for trigram in trigram_dict:
		for positionA in trigram_dict[trigram]:
			for positionB in trigram_dict[trigram]:
				distance = positionA-positionB
				if distance<=0:
					continue
				else:
					relative_positions.append(distance)
	return relative_positions

# Factoriza todos los números de una lista y devuelve un diccionario con los
# factores más comunes
def get_divisors(relative_positions):
    divisors_list={}
    for number in relative_positions:
        for i in range(2, number+1):
            if number % i == 0:
                if i not in divisors_list:
                    divisors_list[i]=0
                divisors_list[i]=divisors_list[i]+1
    return divisors_list
	
# Obtiene la proporción de cada factor sobre el total
def divisor_analysis(divisors_list):
    total_divisors = 0
    for number in divisors_list:
        total_divisors = total_divisors + divisors_list[number]
    relative_occurrence = {}
    for number in divisors_list:
        relative_occurrence[number] = round(( divisors_list[number] / total_divisors ) * 100,3)
    return dict(sorted(relative_occurrence.items(), key=lambda x: x[1], reverse=True)[:10])

# Muestra las longitudes más probables de la clave (los factores más comunes)
# y pide al usuario que introduzca el valor que quiere usar
def length_input(percentage_divisors):
    print("Most likely key lengths are: ")
    for element in percentage_divisors:
        print("{:4d}: {:05.2f}%".format(element,percentage_divisors[element]))
    i = 0
    while i <= 1:
        i = int(input("Input the key length that will be used: "))
    return i

def init_dictionary():
	my_dict = {}
	for ch in ACCEPTED_CHARS:
		my_dict[ch] = 0
	return my_dict 

def check_string(str_to_check):
        for ch in str_to_check:
            if ch not in ACCEPTED_CHARS:
                raise Exception('CHARACTER {} NOT IN ACCEPTED CHARS( {} )'.format(ch,ACCEPTED_CHARS))

def analiza_frecuencias(cypher):

	upper_cypher = cypher.upper()

	instances = init_dictionary()
	count_chars = 0

	for ch in upper_cypher:
		if ch in ACCEPTED_CHARS:
			count_chars = count_chars + 1
			instances[ch] = instances[ch] + 1


	tuple_list = []

	for ch in ACCEPTED_CHARS:
		tuple_list.append( (ch, 100 * instances[ch]/count_chars) )

	tuple_list.sort(key=lambda tup: - tup[1])


	return tuple_list


def split_by_key_length(length, text):

	alphabets = []
	for i in range(length):
		alphabets.append("")

	for ch in range(len(text)):
		alphabets[ch % length] = alphabets[ch % length] + text[ch]

	return alphabets


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="Text to be cryptoanalyzed")
    parser.add_argument("-i", "--iterative", help="Allows u to choose key length and key letters", action="store_true")
    return parser.parse_args()

def get_index(l):
    index = 0
    while index < 1 or index > l:
    	index = int(input( "Introduce sub-text to analyze between 1 to " + str(l) + " --> "))
    return index - 1

def get_action():
	action = ""
	while action != 'c' and action != 'e':
		action = input("Introduce action 'c' to continue, 'e' to exit --> ")
	return action

def show_key(key_array):
	text = ''
	for ch in key_array:
		text = text + ch
	print(text)

def calc_disp(p, c):
	return ( ord(c) - ord(p) ) % ALPHABET_LENGTH

def init_dict(tuple_list):
	my_dict = {}
	for tup in tuple_list:
		my_dict[tup[0]] = tup[1]
	return my_dict

def show_eaosr(disp, tuple_dict):
	cipher_e = chr( ( (ord('E')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII ) 
	cipher_a = chr( ( (ord('A')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	cipher_o = chr( ( (ord('O')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	cipher_s = chr( ( (ord('S')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	cipher_r = chr( ( (ord('R')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	print("E(13,68%)-->" + cipher_e + "(" + "{:.2f}".format(tuple_dict[cipher_e]) + "%) ||| A(12,53%)-->" + cipher_a + "(" + "{:.2f}".format(tuple_dict[cipher_a]) + "%) ||| O(8,68%)-->" + cipher_o + "(" + "{:.2f}".format(tuple_dict[cipher_o]) + "%) ||| S(7,98%)-->" + cipher_s + "(" + "{:.2f}".format(tuple_dict[cipher_s]) + "%) ||| R(6,87%)-->" + cipher_r + "(" + "{:.2f}".format(tuple_dict[cipher_r]) + "%)")

#Calculate the diference between the real frecuencies and guess cipher's effective frecuency
#We use power of 2 because we want all values to be possitive
def calc_aeosr(disp, tuple_dict):
	cipher_e = chr( ( (ord('E')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII ) 
	cipher_a = chr( ( (ord('A')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	cipher_o = chr( ( (ord('O')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	cipher_s = chr( ( (ord('S')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	cipher_r = chr( ( (ord('R')- EXTRA_ASCII + disp) % ALPHABET_LENGTH ) + EXTRA_ASCII )
	return (13.68 - tuple_dict[cipher_e])**2 + (12.53 - tuple_dict[cipher_a])**2 + (8.68 - tuple_dict[cipher_o])**2 + (7.98 - tuple_dict[cipher_s])**2 +(6.87 - tuple_dict[cipher_r])**2


def get_key(tuple_list):

	tuple_dict = init_dict(tuple_list)
	ans = "n"
	while ans != 'y':
		print(tuple_list[0][0] + ": " + str(tuple_list[0][1]) + ", 	" + tuple_list[1][0] + ": " + str(tuple_list[1][1]) + ", 	" + tuple_list[2][0] + ": " + str(tuple_list[2][1]) + ", 	" + tuple_list[3][0] + ": " + str(tuple_list[3][1]) + ", 	" + tuple_list[4][0] + ": " + str(tuple_list[4][1]) )
		p = ""
		c = ""
		while p not in ACCEPTED_CHARS:
			p = input("Character on plaintext: --> ")
		while c not in ACCEPTED_CHARS:
			c =input("Character on cyphertext: --> ")
		disp = calc_disp(p, c)
		show_eaosr(disp, tuple_dict)
		ans = input("Does this solution fit?(y/n): ")
	return chr( ord('A') + disp )

#supose either 'A' or 'E' is top 5 frecuencies
#get the supposition with less difference with standard probabilities
def get_key_no_iterative(tuple_list):

	tuple_dict = init_dict(tuple_list)
	best_disp = 0
	best_disp_metric = 100000.0
	for tup in tuple_list[0:5]:
		disp=calc_disp('E', tup[0])
		disp_metric=calc_aeosr(disp, tuple_dict)
		if disp_metric < best_disp_metric:
			best_disp_metric = disp_metric
			best_disp = disp
	for tup in tuple_list[0:5]:
		disp=calc_disp('A', tup[0])
		disp_metric=calc_aeosr(disp, tuple_dict)
		if disp_metric < best_disp_metric:
			best_disp_metric = disp_metric
			best_disp = disp
	return chr( ord('A') + best_disp )

def main():

    args = get_arguments()

    if args.iterative:
    	pass#keep the initial aproach
    else:
    	main_no_iterativo(args)
    	return

    cyphertext = read_text_file(args.text)

    #make sure all characters are allowed
    check_string(cyphertext)

    #get the most probable key lengths based on trigram positions
    trigrams = trigram_analysis(cyphertext)
    relative_positions = get_relative_positions(trigrams)
    divisors=get_divisors(relative_positions) 
    percentage_divisors=divisor_analysis(divisors)
         
    #ask for the key length to be used
    key_length = length_input(percentage_divisors)

    print("Key length: "+str(key_length))

    #get sub-ciphered-messages
    alphabets = split_by_key_length(key_length, cyphertext)

    key_array = []

    #analyze frecuencies for each sub-message and ask the user for displacement
    for i in range(key_length):
    	key_array.append('_')
    while(True):
    	show_key(key_array)
    	action = get_action()
    	if action == 'c':
    		index = get_index(len(alphabets))
    		tuple_list = analiza_frecuencias(alphabets[index])
    		key = get_key(tuple_list)
    		key_array[index] = key
    	elif action == 'e':
    		return
    	else:
    		print("Unknown action!")


def main_no_iterativo(args):

    cyphertext = read_text_file(args.text)

    #make sure all characters are allowed
    check_string(cyphertext)

    #get the most probable key length based on trigram positions
    trigrams = trigram_analysis(cyphertext)
    relative_positions = get_relative_positions(trigrams)
    divisors=get_divisors(relative_positions)  
    percentage_divisors=divisor_analysis(divisors)

    #on no iterative version get the most likely     
    key_length = max(percentage_divisors.items(), key=operator.itemgetter(1))[0]

    #get sub-ciphered-messages
    alphabets = split_by_key_length(key_length, cyphertext)

    key_array = []
    #analyze frecuencies for each sub-message and get the most likely displacement
    for i in range(key_length):
    	tuple_list = analiza_frecuencias(alphabets[i])
    	key = get_key_no_iterative(tuple_list)
    	key_array.append(key)

    for ch in key_array:
    	print(ch, end='')

if __name__ == '__main__':
	main()