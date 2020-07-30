with open('metadata.csv', 'r') as f, open('t-metadata.csv', 'w') as t:
    for line in f.readlines():
        splits = line.split('|')
        l = splits[0] + "|" + splits[1].strip() + "|0"
        if not any(char.isdigit() for char in splits[1]):
            t.write(l + "\n")
print("done.")
