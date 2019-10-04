import sys
vowels = {}
for character in 'aeiou':
    vowels[character] = 0
"""
input() 
"""
words = sys.stdin.readline().split(' ')

for word in words:
    for character in word:
        if character in 'aeiou':
            vowels[character] += 1

for character in 'aeiou':
    print(f'{character:{vowels[character]}}')
