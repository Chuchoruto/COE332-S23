import names

def lenname (nombre):
    return len(nombre) - 1

losnombres = []
for i in range(5):
    losnombres.append(names.get_full_name())
    print(losnombres[i] + ' ' + str(lenname(losnombres[i])))