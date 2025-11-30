import sys, os

def findLCS( p, q ):

    emptyFlag = -1

    def calcLCS(i,j):

        if table[i][j] == emptyFlag:
            
            if p[i] == q[j]:
                table[i][j] = 1 + calcLCS(i-1,j-1)
            else:
                table[i][j] = max( calcLCS(i-1,j), calcLCS(i,j-1) )

        return table[i][j]

    # init

    p = [''] + list(p)   # include a first item at index 0 to store base-case edit distance
    q = [''] + list(q)

    n = len(p)-1
    m = len(q)-1

    # results
    #
    # table[i][j] corresponds to p[i] and q[j]

    table = [ [emptyFlag for j in range(m+1)] for i in range(n+1) ]

    # base cases

    for i in range(n+1):
        table[i][0] = 0

    for j in range(m+1):
        table[0][j] = 0

    # fill in edit distance table

    calcLCS(n,m)

    # Debugging: output the table
    
    if True:
        print()
        for i in range(n+1):
            for j in range(m+1):
                if table[i][j] == -1:
                    sys.stdout.write( '   ' )
                else:
                    sys.stdout.write( ' %2d' % table[i][j] )
            sys.stdout.write( '\n' )

    lcs = []

    while table[n][m] != 0: #base case
        if p[n] == q[m]: #in this case, we use the character (add indeces to the list)
            lcs.append((n-1, m-1)) #-1 due to table offset
            n -= 1 #move diagonally 
            m -= 1

        elif table[n-1][m] >= table[n][m-1]: #we move up if its value is greater than the left
            n -= 1

        else: #otherwise we go to the left
            m -=1
    
    #since we append from the end to the start we must reverse the list to match the desired output
    lcs.reverse()

    return lcs

# ----------------------------------------------------------------

# Check command-line arguments
#
# Can be either <string1> <string2> or <file1> <file2>

if len(sys.argv) < 3:
    print( 'Usage: %s <string1> <string2> or %s <file1> <file2>' % (sys.argv[0],sys.argv[0]) )
    sys.exit(1)

if not os.path.isfile( sys.argv[1] ) and not os.path.isfile( sys.argv[2] ):

    # neither arg is a filename, so assume strings
    
    p = list( sys.argv[1] )
    q = list( sys.argv[2] )

    elementName = 'char'
    
else:

    # Check that *both* args are filenames
    
    if not os.path.isfile( sys.argv[1] ):
        print( 'File %s not found' % sys.argv[1] )
        sys.exit(1)

    if not os.path.isfile( sys.argv[2] ):
        print( 'File %s not found' % sys.argv[2] )
        sys.exit(1)

    # Read files into lists p and q, with one string for each line

    with open( sys.argv[1], 'r', encoding='UTF-8' ) as pFile:
        p = [ line.rstrip() for line in pFile ]

    with open( sys.argv[2], 'r', encoding='UTF-8' ) as qFile:
        q = [ line.rstrip() for line in qFile ]

    elementName = 'line'
    
# Find the edits from p to q

if elementName == 'char':  # doing strings
    
    lcs = findLCS( p, q )
    
else:  # doing files
    
    pHashed = [ hash(elem) for elem in p ]  # use a hash for each element to
    qHashed = [ hash(elem) for elem in q ]  # avoid long string comparisons
    lcs = findLCS( pHashed, qHashed )

# Debugging: Output the LCS

if True:
    print()
    print( 'LCS:' )
    for pair in lcs:
        pIndex = pair[0]
        qIndex = pair[1]
        print( '  ', pair, p[pIndex] if pIndex < len(p) else '', q[qIndex] if qIndex < len(q) else '' )

# Add matches before and after.  This makes the display code (below)
# cleaner.

lcs = [ (-1,-1) ] + lcs + [ (len(p),len(q)) ]

pStart, qStart = lcs[0] #we start at (-1,-1) to simplify the loop 


#between each common lcs pair, we iterate through and print the differences in the two strings/files
for pEnd, qEnd in lcs[1:]: 
    
    for i in range (pStart +1, pEnd): #if there are any elements between the lcs pair indeces for p
        print("<< ", p[i]) 

    for i in range (qStart + 1, qEnd): #if there are any elements between the lcs pair indeces for q
        print(" >>", q[i])

    if pEnd < len(p) and qEnd < len(q): #print the common character/line if its not the last (len(p),len(q))
        print("===", p[pEnd])

    pStart = pEnd #move to the next common lcs pair
    qStart = qEnd

