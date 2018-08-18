from hashlib import sha256 
import os
import sys 
import argparse

parser = argparse.ArgumentParser(description='this script to give best hashs of text')

parser.add_argument("-t", "--text", dest="text", help="text to hash")
parser.add_argument("-c", "--count", dest="count", help="count of tries")

args = parser.parse_args()

text = ""
if args.text:
    text = args.text
else:
    raise Exception("you should set the text to hash ex.:'-t yourtext'")  

text_hash = sha256(text.encode()).hexdigest()

print(text_hash)