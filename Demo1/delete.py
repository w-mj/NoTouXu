import os


def dele():
    f = open('file_diffdelete.txt','r')
    getlin = f.readlines()
    f.close()
    for line in getlin:
        temp = line.strip('\n')
        temp = temp.split('|')
        filename = temp[0]
        filename = os.path.abspath(filename)
        try:
            os.remove(filename)
        except:
            try:
                os.rmdir(filename)
            except:
                pass
