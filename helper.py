import os


def readfile(filename):
    ''' reads the file and returns it as list of dictionaries'''
    if os.path.exists(filename):
        f = open(filename,"r")
        lines = f.readlines()
        data = []

        #first line is headers
        headers = lines[0].split(',')
        
        for line in lines[1:]:
            temp = line.split(',')
            data.append( { headers[i]: temp[i] for i in len(headers) } )

        return data
