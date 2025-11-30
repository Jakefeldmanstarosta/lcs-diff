# "diff" utility to compare files
#
# Usage: python diff.py <string1> <string1>
#    or: python diff.py <file1> <file2>


import sys, os



# Given two lists, p and q, find the Longest Common Subsequence (LCS).
# Return a list of of index pairs, where each pair is an index from p
# and an index from q of the common subsequence.
#
# Example:  Given p = 'asdzf'  q = 'asxdf'
#           the return value is [ (0,0), (1,1), (2,3), (4,4) ]
#           which means p0=q0, p1=q1, p2=q3, p4=q4 in the LCS.

def findLCS( p, q ):

    def calcLCS(i,j):

        if table[i][j] == -1:
            
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

    table = [ [-1 for j in range(m+1)] for i in range(n+1) ]

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

    # return list of pairs of indices of matching elements
    #
    # If p[i] and q[i] are a pair of elements in the LCS, add
    # (i-1,j-1) to the list.  The -1 is necessary because the table is
    # offset by (+1,+1) due to the base-case row and column.

    lcs = []

    for i in range(5):
        lcs.append( (i,i) )

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

# Add matches before and after.  This makes the display code (below)
# cleaner.

lcs = [ (-1,-1) ] + lcs + [ (len(p),len(q)) ]

# Display the edits

# [ YOUR CODE HERE ]
