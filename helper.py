import os

def readfile(filename):
    ''' reads the file and returns it as list of dictionaries'''
    if os.path.exists(filename):
        f = open(filename,"r")
        lines = f.readlines()
        lines = [ i.strip() for i in lines]
        data = []

        #first line is headers
        headers = lines[0].split(',')
        
        for line in lines[1:]:
            temp = line.split(',')
            data.append( { headers[i]: temp[i] for i in range(len(headers)) } )

        return data
