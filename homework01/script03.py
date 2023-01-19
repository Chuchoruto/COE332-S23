import names

def lenname (nombre):
    return len(nombre) - 1

losnames = []
for i in range(5):
    losnames.append(names.get_full_name())
    print(losnames[i] + ' ' + str(lenname(losnames[i])))