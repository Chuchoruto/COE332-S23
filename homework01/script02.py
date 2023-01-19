import names

nombres = []
while(len(nombres) < 5):
    name = names.get_full_name()
    if(len(name)== 9):
        nombres.append(name)

print(nombres)