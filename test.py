string = 'banana'

w = []
z = len(string)-1
for i in range(len(string)):
    if not string[i] == string[z]:
        w.append(string[i])
    z -= 1

print(w)