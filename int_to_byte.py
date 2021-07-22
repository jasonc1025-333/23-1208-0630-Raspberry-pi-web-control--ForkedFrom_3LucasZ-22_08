#! /usr/bin/env python
from textwrap import wrap
def int_to_byte_array(num):
   if num < 0:
      hexStr = hex((1<<32) + num)
   else:
      hexStr = hex(num)
   hexStr = hexStr.rstrip("L")      #sometimes the hex conversion adds a 'L' to the end. Remove it

   padded = str.format('{:08X}',int(hexStr,16))   #pad out to 8 hex characters
   padded = wrap(padded,2)                     #split into pairs of hex chars ie bytes

   array = [0,0,0,0]
   for x in range(4):
      array[x] = int(padded[x],16)

   array.reverse()      #reverse the list. We will send LSB first

   return array

if __name__ == 'main':
    print(int_to_byte_array(-100))