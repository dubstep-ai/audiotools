f = open('transcriptions.txt', 'r')
o = open('characterset.txt', 'w')

characterset = {}
for line in f.readlines():
    for character in line:
        characterset[character] = 1
o.write(''.join(sorted(characterset.keys())).strip())
