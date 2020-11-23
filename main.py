import os
import json
from random import random


# Il vantaggio dell'utilizzo di with è che non è necessario chiudere esplicitamente
# i file o preoccuparsi dei casi in cui è presente un'eccezione.
def crea_10files():
    for item in range(1, 10):
        with open("/mnt/file{}.txt".format(item), "w") as file:
            file.write("This is file {}\n".format(item))
    print("\n*** Sto creando i 10 file ***")


def crea_2files():
    for item in range(1, 3):
        with open("/mnt/dir1/file{}.txt".format(item), "w") as file:
            file.write("This is file {}\n".format(item))
    print("\n*** Sto creando i 2 file ***")


def crea_directory(path):
    print("\n *** Sto creando la directory *** ")
    os.mkdir(path)


def elimina_file():
    for item in range(1, 10):
        with open("/mnt/file{}.txt".format(item), "r"):
            os.remove("/mnt/file{}.txt".format(item))
    print("\n*** Ho rimosso i file ***")


def rimuovi_directory(path_directory):
    print("\n *** Sto rimuovendo la directory")
    os.system("rm -rf " + path_directory)


def mostra_contenuto(path_directory):
    print("\n *** Sto mostrando il conenuto della directory")
    os.system("ls -l " + path_directory)

def mostra_contenuto_file():
    for item in range(1, 3):
        with open("/mnt/dir1/file{}.txt".format(item), "r") as file:
            print(file.read().format(item))


def smontaggio(partizione):
    print("\n*** Sto smontando la partizione ***")
    os.system("umount " + partizione)


def montaggio(partizione, parent_dir):
    print("\n*** Sto montando la partizione in " + parent_dir + " ***")
    os.system("mount " + partizione + " " + parent_dir)


def formattazione(partizione):
    print("\n*** Sto formattando la partizione ***")
    os.system("mkfs.ext4 " + partizione)


def iniezione_superblocco(partizione):
    print("\n*** Sto procedendo con l'iniezione ***")
    os.system("dd if=/dev/zero of=" + partizione + " count=1 bs=1024 seek=1")


def filesystem_check(partizione):
    os.system("e2fsck " + partizione)


partizione = "/dev/sdb1"
parent_dir = "/mnt"
directory = "dir1"
path = os.path.join(parent_dir, directory)  # /mnt/dir1
lost_found = "lost+found"
path_lost = os.path.join(parent_dir, lost_found)  # /mnt/lost+found


# read file
myjsonfile = open('config.json', 'r')
data = myjsonfile.read()
obj = json.loads(data)
list = obj['faults']


# 1
def corruzione_superblocco(list):
    smontaggio(partizione)
    formattazione(partizione)
    montaggio(partizione, parent_dir)
    crea_10files()
    # print(list[0])
    rand = random()
    # print(rand)
    if list[2].get("value") == 0:
        if rand < list[0].get("value"):
            print("\n***** Sto iniettando il fault con probabilità " + str(list[0].get("value")) + " *****")
            iniezione_superblocco(partizione)
        else:
            print("\n***** Iniezione non andata a buon fine ***** ")
    smontaggio(partizione)
    montaggio(partizione, parent_dir)  # dovrebbe fallire se rand > probabilità
    risp = input("\n***** Il montaggio è fallito? {s,n} ")
    if (risp == "s"):
        print("\n***** Sto avviando e2fsck per la riparazione")
        filesystem_check(partizione)


# 2
def corruzione_inode():
    smontaggio(partizione)
    formattazione(partizione)
    montaggio(partizione, parent_dir)
    rimuovi_directory(path_lost)
    rimuovi_directory(path)
    crea_directory(path)
    inode_dir = os.stat(path).st_ino
    # print(str(inode_dir))
    # os.system("ls -i /mnt")
    crea_2files()
    # os.system("cat /mnt/dir1/file1.txt /mnt/dir1/file2.txt")
    os.system("debugfs -R 'clri <" + str(inode_dir) + ">' " + partizione + " -w")
    smontaggio(partizione)
    montaggio(partizione, parent_dir)
    mostra_contenuto(path)  # dovrebbe fallire e chiedere di fare pulizia
    smontaggio(partizione)
    filesystem_check(partizione)
    montaggio(partizione, parent_dir)
    mostra_contenuto(path_lost)
    # os.system("rm -rf /mnt/lost+found")


# 3
def corruzione_blocco():
    smontaggio(partizione)
    formattazione(partizione)
    montaggio(partizione, parent_dir)
    crea_10files()
    os.system("cat /mnt/file1.txt /mnt/file2.txt")
    os.system("debugfs -R 'stat <12>' " + partizione + "|grep '(0)'")
    os.system("debugfs -R 'mi <12>' " + partizione + " -w")
    smontaggio(partizione)
    montaggio(partizione, parent_dir)
    os.system("cat /mnt/file1.txt /mnt/file2.txt")
    smontaggio(partizione)
    filesystem_check(partizione)


while True:
    try:
        n = int((input("\nDove vuoi iniettare il fault?\n1. Superblocco\n2. I-node\n3. Blocco\n")))
        break
    except ValueError:
        print("\nScelta non valida")

if n == 1:
    corruzione_superblocco(list)
elif n == 2:
    corruzione_inode()
elif n == 3:
    corruzione_blocco()
else:
    print("\nScelta non valida")
