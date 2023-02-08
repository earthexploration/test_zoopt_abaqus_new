# A python script to extract data from neper generated files
from re import search
# read neper generated file
with open("./n100-id1.inp","r") as neper_file:
    lines = neper_file.readlines()
# neper_file = open("./n1000-id1.inp","r")
# print(lines)
# for line in lines:
#     #print(line)
#     if line[:-1] == "*Node":
#         print(line)
    # read the following information
# print(len(lines))
# for i in range(len(lines)):
#     if lines[i][:-1] == "*Node":
#         print(lines[i])
#     if lines[i][:-1] == "*End Part":
#         print(lines[i])
# test elsetName
# for line in lines:
#     if line[:-1] == "*Elset, elset=poly1":
#         print(line)
#         print(line.strip("*Elset, elset="))
#         break

# loop each lines
for i in range(len(lines)):
    # to identify whether this is the key word
    # *Node
    if "*Node" in lines[i]:
        # if true, the current i-th line is the
        # *Node, the next step is to store the
        # index i and continue to read until we
        # find the end symbol ""
        #
        # store the start of Node segment
        nodeStartIndex = i
        #print(nodeStartIndex)
        nodeFile = open("nodeInfo.txt","w")
        # start the loop
        for j in range(nodeStartIndex, len(lines)):
            nodeFile.write(lines[j])
            # we know from the neper generated file that
            # each part, e.g., Node information, Element
            # set information, Node set information are divided
            # by an empty line, therefore:
            if lines[j+1][:-1] == "":
                break #the end of Node information
        # close the fime
        nodeFile.close()
        # update the index i
        i = j

    # *Element
    if "*Element" in lines[i]:
        # if true, the current i-th line is the
        # *Node, the next step is to store the
        # index i and continue to read until we
        # find the end symbol ""
        #
        # store the start of Node segment
        elementStartIndex = i
        #print(nodeStartIndex)
        elementFile = open("elementInfo.txt","w")
        # start the loop
        for j in range(elementStartIndex, len(lines)):
            #
            # to add "instance"
            #
            # if j == elementStartIndex:
            #     elementFile.write(lines[j][:-1]+", instance=Part-1-1")
            # else:
            #     elementFile.write(lines[j])
            elementFile.write(lines[j])
            # we know from the neper generated file that
            # each part, e.g., Node information, Element
            # set information, Node set information are divided
            # by an empty line, therefore:
            if lines[j+1][:-1] == "":
                break #the end of Node information
        # close the file
        elementFile.close()
        # update the index i
        i = j
        #print(i)
        #break
    #
    # *Elset
    if "*Elset" in lines[i]:
        # if true, the current i-th line is the
        # *Node, the next step is to store the
        # index i and continue to read until we
        # find the end symbol ""
        #
        # store the start of Node segment
        elsetStartIndex = i
        #print(nodeStartIndex)
        # to get the name of the elset
        elsetName = lines[i][:-1].strip("*Elset, elset=")
        elsetFileName = "elset_" + elsetName + ".txt"
        elsetFile = open(elsetFileName,"w")
        # start the loop
        for j in range(elsetStartIndex, len(lines)):
            #
            # to write instance
            #
            # if j == elsetStartIndex:
            #     elsetFile.write(lines[j][:-1] + ", instance=Part-1-1 \n")
            # else:
            #     elsetFile.write(lines[j])
            elsetFile.write(lines[j])
            # we know from the neper generated file that
            # each part, e.g., Node information, Element
            # set information, Node set information are divided
            # by an empty line, therefore:
            if lines[j+1][:-1] == "":
                break #the end of Node information
        # close the file
        elsetFile.close()
        # update the index i
        i = j
        #print(i)
        #break
    #
    # *Nset
    if "*Nset" in lines[i]:
        # if true, the current i-th line is the
        # *Node, the next step is to store the
        # index i and continue to read until we
        # find the end symbol ""
        #
        # store the start of Node segment
        nsetStartIndex = i
        #print(nodeStartIndex)
        # to get the name of the elset
        nsetName = lines[i][:-1].strip("*Nset, nset=")
        nsetFileName = "nset_" + nsetName + ".txt"
        nsetFile = open(nsetFileName,"w")
        # start the loop
        for j in range(nsetStartIndex, len(lines)):
            #
            # write instance
            #
            if j == nsetStartIndex:
                nsetFile.write(lines[j][:-1] + ", instance=Part-1-1 \n")
            else:
                nsetFile.write(lines[j])
            # we know from the neper generated file that
            # each part, e.g., Node information, Element
            # set information, Node set information are divided
            # by an empty line, therefore:
            if lines[j+1][:-1] == "":
                break #the end of Node information
        # close the file
        nsetFile.close()
        # update the index i
        i = j
        #print(i)
        #break 
# end loop and close file
neper_file.close()
