#Used to align two sequences
import numpy


#The two sequences
#seq1 = "GKVFLTNAFSINMLKEFPTTITIDKLDEEDFCLKLELRLEDGTLINAIGHDSTINLVNTL"
#seq2 = "VQGAGVVGETPTIPPNTAYQYTSGTVLDTPFGIMYGTYGMVSESGEHFNAIIKPFRLATP"
seq1 = "MEDICINE"
seq2 = "MICHIGAN"
#seq1 = ""
#seq2 = ""
#output =  open("output.txt", "w")

#numbering for BLOSUM62 matrix
blosum62numb = {
    "A": 1,  "R": 2,  "N": 3,  "D": 4,  "C": 5,  "Q": 6,  "E": 7,  "G": 8,  "H": 9,  "I": 10,  "L": 11,  "K": 12,  "M": 13,  "F": 14,
    "P": 15,  "S": 16,  "T": 17,  "W": 18,  "Y": 19,  "V": 20,  "B": 21,  "Z": 22,  "X": 23
}


with open("Blosum62.txt", "r") as BlosumValues:
    BlosumArray = [[str(digit) for digit in line.split()] for line in BlosumValues]

#returns value of blosum matrix
def get_Blosum_value(L1, L2):
    for letterA in blosum62numb:
        for letterB in blosum62numb:
            if (letterA == L1) & (letterB == L2):
                return int(BlosumArray[blosum62numb[L1]][blosum62numb[L2]])



#class for matrix
class New_mat(object):
    #initializing 3D matrix with all values at 0 AND
    #sets the Gap opening vs Extension penalty
    def __init__(self, mat, lst1, lst2, opening, extension):
        self.lst1 = list(lst1)
        self.lst2 = list(lst2)
        self.opening = opening #gap opening
        self.extension = extension #gap extension
        self.mat = numpy.zeros(((len(self.lst1)+1), (len(self.lst2)+1), 4))
        #3D matrix. 2D for values in scoring. 3D[1] for direction: 1= diag, 2 = vertical, 3 = horizontal.
        #3D[2] for the amount of jumps vertical. 3d[3] for the amount of jumps horizontal
        self.output1 = []
        self.output3 = []
        self.output2 = []

    #definition to print matrix
    def print_mat(self):
        for i in range(0, len(self.lst1) + 1):
            for j in range(0, len(self.lst2) + 1):
                if j == (len(self.lst2)):
                    print "%10s" % (str(self.mat[i][j][0])) + "\n"
                else:
                    print " %10s " % (self.mat[i][j][0]),

    #sets the initiation of the matrix
    def initiate_row(self):
        for row in range(1, len(self.lst1)+1):
                self.mat[row][0][0] = self.mat[row-1][0][0] + self.extension

    #sets the initiation of the column matrix
    def initiate_col(self):
        for col in range(1, len(self.lst2)+1):
                self.mat[0][col][0] = self.mat[0][col - 1][0] + self.extension
    #checks to see if the seq matches at row and col

    def check_match(self, row, col):
        if self.lst1[row] == self.lst2[col]:
            return True
        else:
            return False
    #returns value of matrix

    def return_value(self, row, col):
        return self.mat[row][col][0]

    def return_horizontal(self, row, col):
        horizontal = self.return_value(row, col - 1)
        if self.mat[row][col - 1][3] != 0:
            horizontal += self.extension
        else:
            horizontal += self.opening
        for i in range(1, col-1, 1):
            horizontal_jump = self.mat[row][col - 1 - i][0] + self.opening + (i*self.extension)
            if horizontal <= horizontal_jump:
                horizontal = horizontal_jump
                self.mat[row][col][3] = i
        return horizontal

    def return_vertical(self, row, col):
        vertical = self.return_value(row - 1, col)
        if self.mat[row-1][col][2] != 0:
            vertical += self.extension
            temp = self.mat[row - 1][col][2]
            vertical_jump = self.mat[row - temp][col][0] + self.opening + (temp*self.extension)
            if vertical < vertical_jump:

        else:
            vertical += self.opening
            return vertical

        #returns the value of the square from the calculation of the squares around it.
        #also saves the direction of return
    def set_value(self, row, col):
        rows = row - 1
        cols = col - 1
        blosumv = get_Blosum_value(self.lst1[rows], self.lst2[cols])
        diag = self.return_value(row-1, col-1) + blosumv
        if (diag >= vertical) and (diag >= horizontal):
            self.mat[row][col][0] = diag
            self.mat[row][col][1] += 1
        elif (vertical > diag) and (vertical > horizontal):
            self.mat[row][col][0] = vertical
            if vertical_count == 1:
                self.mat[row][col][1] = 0
            else:
                self.mat[row][col][1] = vertical_count
            self.mat[row][col][1] += 2
        elif (horizontal > diag) and (horizontal >= vertical):
            self.mat[row][col][0] = horizontal
            if horizontal_count == 1:
                self.mat[row][col][1] = 0
            else:
                self.mat[row][col][1] = horizontal_count
            self.mat[row][col][1] += 3

    def fill_matrix(self):
        for x in range(1, len(self.lst1) + 1):
            for y in range(1, len(self.lst2) + 1):
                self.set_value(x, y)
    
    def reduce_dir(self, row, col):
        count = 0
        s = self.mat[row][col][1]
        self.mat[row][col][1] %= 10
        while s > 3:
            count += 1
            s /= 10
        return count

    def traceback(self):
        xx = len(self.lst1)-1
        yy = len(self.lst2)-1
        while (xx >= 0) and (yy >= 0):
            count = self.reduce_dir(xx, yy)
            if (self.mat[xx][yy][1]) == 1:
                self.output1.append(self.lst1[xx])
                self.output2.append(self.lst2[yy])
                xx -= 1
                yy -= 1
            elif (self.mat[xx][yy][1]) == 2:
                self.output1.append(self.lst1[xx])
                self.output2.append("-")
                if count == 0:
                    xx -= 1
                else:
                    xx -= count
            elif (self.mat[xx][yy][1]) == 3:
                self.output2.append(self.lst2[yy])
                self.output1.append("-")
                if count == 0:
                    yy -= 1
                else:
                    yy -= count
            elif (xx == 0) or (yy == 0):
                if xx == 0:
                    for y in range(yy, -1, -1):
                        self.output2.append(self.lst2[y])
                        self.output1.append("-")
                        yy -= 1
                if yy == 0:
                    for x in range(xx, -1, -1):
                        self.output1.append(self.lst1[x])
                        self.output2.append("-")
                        xx -= 1
    
                if (xx == -1) or (yy == -1):
                    if xx == -1:
                        self.output2.append(self.lst2[0])
                        self.output1.append("-")
                    elif yy == -1:
                        self.output2.append("-")
                        self.output1.append(self.lst1[0])
                xx = -1
                yy = -1
        seqcount = 0
        for dist in range(0, len(self.output1)):
            if self.output1[dist] == self.output2[dist]:
                self.output3.append(":")
                seqcount += 1
            else:
                self.output3.append(" ")
        al = float(len(self.output1)) - float(seqcount) - 1
        si = float(seqcount)/float(len(self.lst1))
        print "Aligned Length: " + str(al)
        print "Identical Length: " + str(seqcount)
        print "Sequence Identity: " + str(si)
        print "".join(self.output1)[::-1]
        print "".join(self.output3)[::-1]
        print "".join(self.output2)[::-1]
















mat = New_mat("mat", seq1, seq2, -11, -1)
mat.initiate_row()
mat.initiate_col()
print mat.return_horizontal(1, 1)
#mat.print_mat()
#mat.fill_matrix()
mat.print_mat()
#mat.traceback()
#print mat.mat

BlosumValues.close()
