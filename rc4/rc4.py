#!/usr/bin/env python3
import argparse
import curses

#Codigo copiado hasta: getch = _Getch()
#https://stackoverflow.com/questions/510357/how-to-read-a-single-character-from-the-user 
#Esta parte del codigo sirve para leer caracter a caracter
#Ignora ese codigo hasta la funcion init_s()

class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def init_s():
	aux = []
	for i in range(256):
		aux.append(i.to_bytes(1,'little'))
	return aux

def init_t(input_key):
	aux = []
	for i in range(256):
		aux.append(input_key[i % len(input_key)])
	return aux

def str_to_bytes(string):
	i = int(string)
	if i < 0 or i > 255:
		raise Exception(string + " should be a value between 0 and 255.")
	return i.to_bytes(1,'little')

def get_key(input_key):
	aux = list(map(str_to_bytes, input_key.split(',')))
	return aux

def swap(v, i, j):
	v[i],v[j] = v[j],v[i]

def initial_permutation_of_s(s, t):
	j = 0
	for i in range(256):
		j = ( ( j + int.from_bytes(s[i], byteorder='little') + int.from_bytes(t[i], byteorder='little') ) % 256 )
		swap(s, i, j)

def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--key", help="key used to cipher/decipher input text, must be a csv of numbers between 0 and 255")
	parser.add_argument("-d", "--decipher", help="bytes to decipher, must be a csv of numbers between 0 and 255", required=False)
	return parser.parse_args()

def print_s(s, stdscr, swapped1=-1, swapped2=-1):
	aux = list(map(lambda b:int.from_bytes(b, byteorder='little'), s))
	for i in range(8):
		val_list = aux[i*32:(i+1)*32]
		stdscr.addstr("(")
		for val in val_list:
			if val == swapped1 or val == swapped2:
				stdscr.addstr("{:4d}".format(val), curses.color_pair(1))
			else:
				stdscr.addstr("{:4d}".format(val))
			stdscr.addstr(",")
		stdscr.addstr(")\n")
	stdscr.refresh()


def main():
	args = get_arguments()
	screen = curses.initscr()
	curses.start_color()
	curses.noecho()
	stdscr = curses.initscr()
	curses.init_color(curses.COLOR_CYAN, 730, 1000, 750)
	curses.init_pair(1, curses.COLOR_RED, curses.COLOR_CYAN)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
	curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
	curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
	if not args.decipher:
		mainenc(args, stdscr)
	else:
		maindec(args, stdscr)

def mainenc(args, stdscr):

	##### Initialization #####
	if args.key:
		k = get_key(args.key)
	else:
		curses.nocbreak()
		curses.echo()
		curses.endwin()
		raise Exception("Introduce a key, please.")
	s = init_s()
	t = init_t(k)

	stdscr.addstr("##### Initial state of vector S #####\n", curses.color_pair(2))
	print_s(s, stdscr)

	##### Initial permutation of S #####
	initial_permutation_of_s(s, t)

	stdscr.addstr("##### Initial permutation vector of S (using introduced key) #####\n", curses.color_pair(2))
	print_s(s, stdscr)

	i = 0
	j = 0
	exit_val = 3
	while(True):

		stdscr.addstr("Press key to input the byte which will be encrypted\n", curses.color_pair(3))
		stdscr.refresh()
		ch = getch()
		stdscr.clear()
		#getch() lee un char de stdin, en windows devuelve bytes y en linux devuleve una string
		#si devuelve una string lo transformamos en los bytes correspondientes
		if isinstance(ch, str):
			ch = bytes(ch, "utf8")
		if (ch==exit_val.to_bytes(1,"little")):
			curses.nocbreak()
			curses.echo()
			curses.endwin()
		#	print("\n*****   Program terminated   *****")
			return;


		#vamos a encriptar cada byte
		for input_byte in ch:
			#escojes las posiciones a intercambiar
			i = ( i + 1 ) % 256
			j = ( j + int.from_bytes(s[i], byteorder='little') ) % 256

			stdscr.addstr("Swapping positions ", curses.color_pair(2))
			stdscr.addstr(str(i), curses.color_pair(4))
			stdscr.addstr(" and ", curses.color_pair(2))
			stdscr.addstr(str(j), curses.color_pair(4))
			stdscr.addstr("...\n", curses.color_pair(2))
			swap(s, i, j)

			#sumas los valores de las posiciones para encontrar la nueva posicion final
			final_position = ( int.from_bytes(s[i], byteorder='little') + int.from_bytes(s[j], byteorder='little') ) % 256
			
			#el valor en esa posicion es el byte que usaras como keystring
			keystring = ( s[final_position] )

			# keystring XOR input_byte
			out = int.from_bytes(keystring, byteorder='little') ^ input_byte

			print_s(s, stdscr, swapped1=int.from_bytes(s[i], byteorder='little'), swapped2=int.from_bytes(s[j], byteorder='little'))
			stdscr.addstr("I(", curses.color_pair(2))
			stdscr.addstr(str(input_byte), curses.color_pair(4))
			stdscr.addstr(") XOR K(", curses.color_pair(2))
			stdscr.addstr(str(int.from_bytes(keystring, byteorder='little')), curses.color_pair(4))
			stdscr.addstr(") -> O(", curses.color_pair(2))
			stdscr.addstr(str(out), curses.color_pair(4))
			stdscr.addstr(")\n", curses.color_pair(2))
			stdscr.refresh()

def maindec(args, stdscr):

	##### Initialization #####
	if args.key:
		k = get_key(args.key)
	else:
		raise Exception("Introduce a key, please.")
	s = init_s()
	t = init_t(k)

	if args.decipher:
		#valores decimales a bytes
		ch =  list(map(str_to_bytes, args.decipher.split(',')))
	else:
		Exception("Introduce bytes to decipher, please.")
	stdscr.clear()
	stdscr.addstr("##### Initial state of vector S #####\n", curses.color_pair(2))
	print_s(s, stdscr)

	##### Initial permutation of S #####
	initial_permutation_of_s(s, t)

	stdscr.addstr("##### Initial permutation of vector S (using introduced key) #####\n", curses.color_pair(2))
	print_s(s, stdscr)

	i = 0
	j = 0
	exit_val = 3
	for input_byte in ch:
		input_byte = int.from_bytes(input_byte, byteorder='little')
		stdscr.addstr("Press any key for next iteration\n", curses.color_pair(3))
		stdscr.refresh()
		
		#stdscr.addstr("Press any key for next iteration!I(" + str(input_byte) + ")\n")
		#stdscr.refresh()
		ch = getch()
		stdscr.clear()
		stdscr.addstr("Deciphering I(" + str(input_byte) + ")\n", curses.color_pair(4))
		if isinstance(ch, str):
			ch = bytes(ch, "utf8")
		if (ch==exit_val.to_bytes(1,"little")):
			curses.nocbreak()
			curses.echo()
			curses.endwin()
		#	print("\n*****   Program terminated   *****")
			return;
		#escojes las posiciones a intercambiar
		i = ( i + 1 ) % 256
		j = ( j + int.from_bytes(s[i], byteorder='little') ) % 256

		stdscr.addstr("Swapping positions ", curses.color_pair(2))
		stdscr.addstr(str(i), curses.color_pair(4))
		stdscr.addstr(" and ", curses.color_pair(2))
		stdscr.addstr(str(j), curses.color_pair(4))
		stdscr.addstr("...\n", curses.color_pair(2))
		swap(s, i, j)

		#sumas los valores de las posiciones para encontrar la nueva posicion final
		final_position = ( int.from_bytes(s[i], byteorder='little') + int.from_bytes(s[j], byteorder='little') ) % 256
			
		#el valor en esa posicion es el byte que usaras como keystring
		keystring = ( s[final_position] )

		# keystring XOR input_byte
		out = int.from_bytes(keystring, byteorder='little') ^ input_byte

		print_s(s, stdscr, swapped1=int.from_bytes(s[i], byteorder='little'), swapped2=int.from_bytes(s[j], byteorder='little'))
		stdscr.addstr("I(", curses.color_pair(2))
		stdscr.addstr(str(input_byte), curses.color_pair(4))
		stdscr.addstr(") XOR K(", curses.color_pair(2))
		stdscr.addstr(str(int.from_bytes(keystring, byteorder='little')), curses.color_pair(4))
		stdscr.addstr(") -> O(", curses.color_pair(2))
		stdscr.addstr(str(out), curses.color_pair(4))
		stdscr.addstr(")\n", curses.color_pair(2))
		stdscr.refresh()
	stdscr.addstr("Press any key to quit\n", curses.color_pair(3))
	stdscr.refresh()	
	ch = getch()
	curses.nocbreak()
	curses.echo()
	curses.endwin()
		


if __name__ == "__main__":
	main()
