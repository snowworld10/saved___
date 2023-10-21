groups = [] 
with open("chats.txt") as f: 
    [groups.append(line) for line in f.read().splitlines() if line not 
    in groups]
print(groups)
with open("chats.txt", "w") as f:
    [f.write(group + "\n") for group in  groups]
