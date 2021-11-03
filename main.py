#!/usr/bin/python3

#Imports:
######################################
from colorama import Fore, Back, Style
import argparse
import readchar
from collections import namedtuple
import string
import random
from getch import getch 
from time import time
#####################################

#Inputs:




#Função começar teste:
#Caso utilizador pretenda começar o teste pressiona uma tecla
#Caso utilizador pretenda sair, pressiona X
def start_test():

    print(Fore.RED + Style.BRIGHT + 'Typing test: ' +  Style.RESET_ALL + Fore.BLUE + Style.BRIGHT +  '\nPress a key to start the test' +  Style.RESET_ALL + '(Space to Leave)'  +  Style.RESET_ALL)
    pressed_key = ord(getch())
    # Space key == 32 in ascii table

    if pressed_key == 32:
        pressed_key = ('Space Bar')      
        print( 'You typed ' + Fore.CYAN + Style.BRIGHT + pressed_key + Style.RESET_ALL + Fore.RED + Style.BRIGHT +'\nTerminating...')
        time.sleep(1)
        return False
    else:
        print(Fore.GREEN + Style.BRIGHT + 'Starting test... ' + Style.RESET_ALL)
        time.sleep(1)
        return True

######## Funcao para obter caracter aleatorio ########
def generate_rkey():
      
    lc = string.ascii_lowercase     #todas as letras minusculas em string
    rkey = random.choice(lc)        #escolhe valor aleatório da string
    print(rkey)
    
    
######## Funcao ler o caracter inserido ########
def read_key():
    
    pressed_keys = []
    pressed_key = readchar.readkey()
    pressed_keys.append(pressed_key)
    print (pressed_keys)

#Main:
def timed_mode(time):

def main():
    parser = argparse.ArgumentParser(description='PSR argparse example.')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='')
    parser.add_argument('-mn', '--max_number', type=int, help='')
    args = vars(parser.parse_args())
    print(args)

    if args['use_time_mode']:
        print('Using time mode. test will run up to ' + str(args['max_number']) + ' seconds')
        timed_mode(args['max_number'])
    else:
        print('Not using time mode. Test will ask for ' + str(args['max_number']) + ' responses')
    print(args['use_time_mode'])
    if args['use_time_mode'] and args['max_number'] > 0 :
        elif not args['use_time_mode'] and args['max_number'] > 0 :
        max_key_mode(args['max_number'])
    if start_test():
        print(Fore.GREEN + Style.BRIGHT + 'Test started' + Style.RESET_ALL)
        generate_rkey()
        read_key()

    else:
        
        print(Fore.RED + Style.BRIGHT + 'Test canceled' + Style.RESET_ALL)
    

if __name__ == "__main__":
    main()
