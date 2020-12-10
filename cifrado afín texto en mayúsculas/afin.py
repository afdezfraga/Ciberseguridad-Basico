import string
import argparse

ACCEPTED_CHARS = set(string.ascii_uppercase)
ALPHABET_LENGTH = len(ACCEPTED_CHARS)
EXTRA = 65 #min ASCII code of the alphabet

SUM_FACTOR = 14 
MULTIPLY_FACTOR = 21 

# se que debería usar euclides extendido aquí, hemos sido vagos
def get_demultiply_factor(factor, l):

	a = factor
	b = l

	while b:
		a, b = b, a%b

	#a has the gcd
	if a != 1:
		raise Exception("MULTIPLY_FACTOR invalid for this alphabet length because they are not coprime")

	demult = 1
	while (((factor * demult) % l) != 1):
		demult = demult + 1

	return demult


DEMULTIPLY_FACTOR = get_demultiply_factor(MULTIPLY_FACTOR, ALPHABET_LENGTH)




def cipher(ch, a, b):

	#chech if the character is in our alphabet
	if ch not in ACCEPTED_CHARS:
		raise Exception("value" + ch + "not in accepted alphabet: " + string.ascii_uppercase)

	#we get values form 0(A) to 25(Z)
	val = ord(ch) - EXTRA

	#affine cipher
	cipher_val = ((a * val) + b) % ALPHABET_LENGTH

	#we get the ascii code of the cipher character 65(A) - 90(Z)
	cipher_val = cipher_val + EXTRA

	return chr(cipher_val)


def cipher_text(plain_text, a, b):

	cipher_text = ""

	for ch in plain_text:
		cipher_ch = cipher(ch, a, b)
		cipher_text = cipher_text + cipher_ch

	return cipher_text



def decipher(ch, a, b):

	#chech if the character is in our alphabet
	if ch not in ACCEPTED_CHARS:
		raise Exception("value" + ch + "not in accepted alphabet: " + string.ascii_uppercase)

	#we get values form 0(A) to 25(Z)
	val = ord(ch) - EXTRA

	#affine decipher
	decipher_val = (a * (val - b)) % ALPHABET_LENGTH

	#we get the ascii code of the plain character 65(A) - 90(Z)
	decipher_val = decipher_val + EXTRA

	return chr(decipher_val)


def decipher_text(cipher_text, a, b):

	plain_text = ""

	for ch in cipher_text:
		plain_ch = decipher(ch, a, b)
		plain_text = plain_text + plain_ch

	return plain_text

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("text", help="Text to be ciphered/deciphered")
    parser.add_argument("-d", "--decipher", help="decipher the input text, if not used then cipher is asumed ", action="store_true")
    parser.add_argument("-a", "--multfactor", help="Decimation constant, number between 1 and "  + str(ALPHABET_LENGTH - 1), type=int )
    parser.add_argument("-b", "--addfactor", help="Displacement constant, number between 0 and " + str(ALPHABET_LENGTH - 1), type=int )
    return parser.parse_args()

def main():
	args = get_arguments()

	mult = MULTIPLY_FACTOR
	demult = DEMULTIPLY_FACTOR
	add = SUM_FACTOR

	if args.multfactor:
		if (args.multfactor > ALPHABET_LENGTH - 1) or (args.multfactor < 1):
			raise Exception("mult factor out of range")
		else:
			mult = args.multfactor
			demult = get_demultiply_factor(mult, ALPHABET_LENGTH);


	if args.addfactor:
		if (args.addfactor > ALPHABET_LENGTH - 1) or (args.addfactor < 0):
			raise Exception("sum factor out of range")
		else:
			add = args.addfactor

	if args.decipher:
		print(decipher_text(args.text, demult, add))
	else:
		print(cipher_text(args.text, mult, add))



if __name__ == '__main__':
	main()
