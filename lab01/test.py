'''
TODO Complete this file by following the instructions in the lab exercise.
'''

strings = ['This', 'list', 'is', 'now', 'all', 'together']
new=''
for x in strings:
    if (x == 'together'):
        new += x
    else:
        new += x + ' '
        
print(new)
print(' '.join(strings))
