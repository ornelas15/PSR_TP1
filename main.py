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
from time import time, sleep, ctime
#####################################




#Função começar teste:
#Caso utilizador pretenda começar o teste pressiona uma tecla
#Caso utilizador pretenda sair, pressiona X
def can_start_test():

    print(Fore.RED + Style.BRIGHT + 'Typing test: ' +  Style.RESET_ALL + Fore.BLUE + Style.BRIGHT +  '\nPress a key to start the test' +  Style.RESET_ALL + '(Space to Leave)'  +  Style.RESET_ALL)
    pressed_key = ord(getch())
    # Space key == 32 in ascii table

    if pressed_key == 32:
        pressed_key = ('Space Bar')      
        print( 'You typed ' + Fore.CYAN + Style.BRIGHT + pressed_key + Style.RESET_ALL + Fore.RED + Style.BRIGHT +'\nTerminating...')
        sleep(1)
        return False
    else:
        print(Fore.GREEN + Style.BRIGHT + 'Starting test... ' + Style.RESET_ALL)
        sleep(1)
        return True


######## Funcao para obter caracter aleatorio ########
def generate_rkey():
    lc = string.ascii_lowercase     #todas as letras minusculas em string
    rkey = random.choice(lc)        #escolhe valor aleatório da string
    
    return rkey 
    

######## Funcao que trata o key press ########
def key_pressing(g_stats):
    generated_key=generate_rkey()
    init_time=time()
    print("Type letter "+generated_key)
    pressed_key = readchar.readkey()
    after_press_time=time()
    g_stats['test_start']=init_time
    g_stats['test_end']=after_press_time

    press_time=after_press_time-init_time
    
    Input = namedtuple('Input', ['requested' , 'received' , 'duration'])

    press_stats = Input(generated_key, pressed_key, press_time)
    g_stats['inputs'].append(press_stats)
    g_stats['number_of_types']+=1
    if pressed_key == generated_key:
        g_stats['number_of_hits']+=1
        g_stats['type_hit_average_duration']=(g_stats['type_hit_average_duration']*(g_stats['number_of_hits']-1)+press_time)/g_stats['number_of_types']

        print('You typed letter ' + Fore.GREEN + Style.BRIGHT + pressed_key + Style.RESET_ALL)
    else:
        g_stats['type_miss_average_duration']=(g_stats['type_miss_average_duration']*(g_stats['number_of_types']-1-g_stats['number_of_hits'])+press_time)/g_stats['number_of_types']
        
        print('You typed letter ' + Fore.RED + Style.BRIGHT + pressed_key + Style.RESET_ALL)
    
    g_stats['type_average_duration']=((g_stats['number_of_types']-1)*g_stats['type_average_duration']+press_time)/g_stats['number_of_types']
    g_stats['accuracy']=g_stats['number_of_hits']/g_stats['number_of_types']
    return generated_key


def show_stats(stats):
    print(stats)

#result example
# {'accuracy': 0.0,
#  'inputs': [Input(requested='v', received='s', duration=0.11265206336975098),
#             Input(requested='w', received='d', duration=0.07883906364440918),
#             Input(requested='d', received='a', duration=0.0720210075378418),
#             Input(requested='a', received='s', duration=0.0968179702758789),
#             Input(requested='b', received='d', duration=0.039067983627319336)],
#  'number_of_hits': 0,
#  'number_of_types': 5,
#  'test_duration': 0.3997969627380371,
#  'test_end': 'Thu Sep 10 16:36:20 2020',
#  'test_start': 'Thu Sep 10 16:36:20 2020',
#  'type_average_duration': 0.07987945793212418,
#  'type_hit_average_duration': 0.0,
#  'type_miss_average_duration': 0.07987945793212418}

######## if it is based on time ########
def timed_mode(max_time):
    stats = {
        'inputs':[],
        'number_of_hits':0,
        'number_of_misses':0,
        'number_of_types':0,
        'type_miss_average_duration':0,
        'type_hit_average_duration':0,
        'type_average_duration':0
    }
    print(Fore.GREEN + Style.BRIGHT + 'Test started' + Style.RESET_ALL)
    start_time=time()
    while max_time+start_time>time():
       key_pressing(stats)
    stats['test_duration']=time()-start_time
    print(Fore.RED+"Time is over"+Style.RESET_ALL)
    show_stats(stats)
    print(Fore.RED + Style.BRIGHT + 'Test finished' + Style.RESET_ALL)

######## if it is based on character inputs ########
def max_key_mode(num_chars): 
    stats = {
        'inputs':[],
        'number_of_hits':0,
        'number_of_misses':0,
        'number_of_types':0,
        'type_miss_average_duration':0,
        'type_hit_average_duration':0,
        'type_average_duration':0
    }
    print(Fore.GREEN + Style.BRIGHT + 'Test started' + Style.RESET_ALL)
    for i in range(num_chars):
        key_pressing(stats)
    stats['test_duration']=time()-start_time
    show_stats(stats)
    print(Fore.RED + Style.BRIGHT + 'Test finished' + Style.RESET_ALL)


#Main:
def main():
    parser = argparse.ArgumentParser(description='Typing test')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mn', '--max_number', type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
    args = vars(parser.parse_args())

    if can_start_test():
        if args['use_time_mode']:
            print('Using time mode. test will run up to ' + str(args['max_number']) + ' seconds')
            timed_mode(args['max_number'])
            print
        else:
            print('Not using time mode. Test will ask for ' + str(args['max_number']) + ' responses')
            max_key_mode(args['max_number'])

    else:
        
        print(Fore.RED + Style.BRIGHT + 'Test canceled' + Style.RESET_ALL)
    

if __name__ == "__main__":
    main()
