print('it was a dark but not stormy night')
print('left or right?')
user_input = input()

if(user_input) == 'left':
    print('you went left, you see a house')
    print('basement or attic?')
    user_input = input()
    if(user_input) == 'basement':
        print('you went to the basement')
    else:
        print('you went to the attic')
elif(user_input) == 'right':
    print('you went right')
else:
    print('please choose left or right')