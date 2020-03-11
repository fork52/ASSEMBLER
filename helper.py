import os
import pprint as pr

def readfile(filename):
    ''' reads the file and returns it as list of dictionaries'''
    if os.path.exists(filename):
        f = open(filename,"r")
        lines = f.readlines()
        data = []

        #first line is headers
        headers = lines[0].strip()
        headers = headers.split(';')

        for line in lines[1:]:
            line1 = line.strip()
            temp = line1.split(';')
            data.append( { headers[i]: temp[i] for i in range(len(headers)) } )

        return data

if __name__ == '__main__':
    pr.pprint(readfile('MOT.txt'))
    print('\n\n\n')
    pr.pprint(readfile('POT.txt'))
