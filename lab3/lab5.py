import mpi4py
import typing
import random
from mpi4py import MPI
 
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
dice_values_sum3 = 0
#defines a function returing a random int from the [1,6] interval.
def throw_dice(n=1, prnt=False) -> list:
    dice_values = []
    for i in range(n):
        dice_value = random.randint(1,9)
        dice_values.append(dice_value)
    if prnt:
        print(dice_values)
    return dice_values
 
match rank:
    case 0: # 0 - print -> send to 3
        dice_values = throw_dice(1, True)
        comm.send(sum(dice_values), 1)
        data = comm.recv()
        print(f"{rank} - {data}")
    case 1: # 1 - throw 2 dices, print each time, sum, send to 3
        dice_values = throw_dice(1,True)
        data = comm.recv()
        dice_values_sum = 10 * sum(dice_values) + data
        comm.send(dice_values_sum, 2)
        print(f"{rank} - {dice_values_sum}")
    case 2: # 2 - throw 3 dices, print each time, sum, send to 3
        dice_values = throw_dice(1, True)
        data = comm.recv()
        dice_values_sum = 100 * sum(dice_values) + data
        comm.send(dice_values_sum, 3)
        print(f"{rank} - {dice_values_sum}")
    case 3: # 3 - sum of all received
        dice_values = throw_dice(1, True)
        data = comm.recv()
        dice_values_sum = 1000 * sum(dice_values) + data
        comm.send(dice_values_sum, 0)
        print(f"{rank} - {dice_values_sum}")