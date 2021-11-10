#!/usr/bin/python3

#Imports:
######################################
from colorama import Fore, Style
import argparse
import readchar
from collections import namedtuple
import string
import random
from getch import getch 
from time import time, sleep, ctime
from pprint import pprint
import signal
#####################################



Input = namedtuple('Input', ['requested' , 'received' , 'duration'])

def timeout_handler(num, stack):
    raise Exception("TIME_OVER")

#Função começar teste:
#Caso utilizador pretenda começar o teste pressiona uma tecla
#Caso utilizador pretenda sair, pressiona Space
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
    print("Type letter " + Fore.YELLOW + Style.BRIGHT + generated_key + Style.RESET_ALL)
    pressed_key = readchar.readkey()
    if pressed_key==' ':
        return True
    after_press_time=time()
    press_time=after_press_time-init_time
    
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
    return False

def show_stats(stats):
    pprint(stats)

######## if it is based on time ########
def timed_mode(max_time, stats):
    print(Fore.GREEN + Style.BRIGHT + 'Test started' + Style.RESET_ALL)
    stats['test_start']=ctime()
    signal.signal(signal.SIGALRM, timeout_handler)
    start_time=time()
    signal.alarm(max_time)
    try:
        while True:
            interrupted = key_pressing(stats)
            if interrupted:
                    break
    except:
        print(Fore.YELLOW + Style.BRIGHT + "Time is over" + Style.RESET_ALL)
    finally:
        stats['test_end']=ctime()
        stats['test_duration']=time()-start_time
        if interrupted:
            print(Fore.YELLOW + Style.BRIGHT +"Test was interrupted."+Style.RESET_ALL)
        else:       
            print(Fore.RED + Style.BRIGHT + 'Test finished' + Style.RESET_ALL)
        print(Fore.YELLOW + Style.BRIGHT + 'The results were:' + Style.RESET_ALL)
    return stats

######## if it is based on character inputs ########
def max_key_mode(num_chars, stats): 
    
    print(Fore.GREEN + Style.BRIGHT + 'Test started' + Style.RESET_ALL)
    stats['test_start']=ctime()
    start_time=time()
    for i in range(num_chars):
        interrupted = key_pressing(stats)
        if interrupted:
            print(Fore.YELLOW + Style.BRIGHT +"Test was interrupted."+Style.RESET_ALL)
            break
    stats['test_end']=ctime()
    stats['test_duration']=time()-start_time
    print(Fore.RED + Style.BRIGHT + 'Test finished' + Style.RESET_ALL)
    print(Fore.YELLOW + Style.BRIGHT + 'The results were:' + Style.RESET_ALL)
    return stats


#Main:
def main():
    parser = argparse.ArgumentParser(description='Typing test')
    parser.add_argument('-utm', '--use_time_mode', action='store_true', help='Max number of secs for time mode or maximum number of inputs for number of inputs mode.')
    parser.add_argument('-mn', '--max_number', required=True, type=int, help='Max number of seconds for time mode or maximum number of inputs for number of inputs mode.')
    args = vars(parser.parse_args())
    stats = {
        'inputs':[],
        'number_of_hits':0,
        'number_of_types':0,
        'type_miss_average_duration':0,
        'type_hit_average_duration':0,
        'type_average_duration':0
    }
    if can_start_test():
        if args['use_time_mode']:
            print(Fore.CYAN + Style.BRIGHT + 'Using time mode. Test will run up to ' + str(args['max_number']) + ' seconds' + Style.RESET_ALL)
            stats = timed_mode(args['max_number'], stats)
            print
        else:
            print(Fore.CYAN + Style.BRIGHT + 'Not using time mode. Test will ask for ' + str(args['max_number']) + ' responses' + Style.RESET_ALL)
            stats = max_key_mode(args['max_number'], stats)
        show_stats(stats)
    else:
        print(Fore.RED + Style.BRIGHT + 'Test canceled' + Style.RESET_ALL)
    

if __name__ == "__main__":
    main()
