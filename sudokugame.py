# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 10:35:19 2018

@author: ashsih k dubey
program is to validate Sudoku puzzle
Step 1: Taking input for sudoku at it's respective places - done
Step 2: Prinitng same in form of Sudoku puzzle on scrren using "=" - done
Step 3: validating inputs for rows - NA
Step 4: validating inputs for cols - NA
Step 5: validating inputs for box  - NA 
Step 6: Start solving
    6a: using single position & single candidate technique - done
    6b: candidate line  - done
    6c: double pair     -done
    6d: multi line      -done
    6e: naked pairs     - done
    6f: hidden pairs
"""
import datetime

def print_sudoku(puzzle):
# function used to print puzzle in sudoku format 9x9 tabuler format 
# with seperater to show 9 boxes of 3x3 size

    print ("=========================================") 
    print ("=========================================")     
    for i in range(w):
        #for j in range(h):
        if (i== 3 or i==6):
            print ("=========================================")
            print ("=========================================")
        print("||", puzzle[i][0:3], "|*|", puzzle[i][3:6], "|*|", puzzle[i][6:9],"||")
    print ("=========================================") 
    print ("=========================================")   
    print("\n")

def pop_n(x,y,n):
# when get solution for one cell, this function helps removing 
# occurance of solved number from related rows, cols and box

    j=0
    for j in range(w):
        if (puzzle_comb[j][y]!=0 and puzzle_comb[j][y].count(n)==1):
            puzzle_comb[j][y].remove(n)
            if(len(puzzle_comb[j][y])==0):
                puzzle_comb[j][y]=0 

        if (puzzle_comb[x][j]!=0 and puzzle_comb[x][j].count(n)==1):
            puzzle_comb[x][j].remove(n)
            if(len(puzzle_comb[x][j])==0):
                puzzle_comb[x][j]=0 

    box_x=(int(x/3)*3)
    box_y=(int(y/3)*3)
    for j in range(box_x,box_x+3):
        for k in range(box_y,box_y+3):
            if (puzzle_comb[j][k]!=0 and puzzle_comb[j][k].count(n)==1):
                puzzle_comb[j][k].remove(n)
                if(puzzle_comb[j][k]!=0 and len(puzzle_comb[j][k])==0):
                    puzzle_comb[j][k]=0
            

def input_n(puzzle,x,y,n):
# function to insert one number in cell
# additionly this also removing number from suggested solutions using pop_n function
    global sudoku_cnt
    sudoku_cnt=sudoku_cnt-1
    puzzle[x][y]=n
    puzzle_comb[x][y]=0
    pop_n(x,y,n)
    

def input_sudoku(puzzle):
# function to provide input to sudoku puzzle
# uncomment to activate puzzle for console input
    x,y,n,sudoku_size=0,0,0,0

    s_inputs=     [216,277,294
              ,324,352,367,383
              ,425,438,451,464,472
              ,521,534,553,579,585
              ,639,642,657,674,688
              ,722,748,756,784
              ,811,836,898]

    sudoku_size= len(s_inputs)
    #sudoku_size=int(input("Sudoku puzzle size > "))
    print("Inputs for puzzle as (x,y) position starting (1,1)")
    for i in range(0,sudoku_size):
        n=s_inputs[i]
        #n= int(input("3 digit value for position (x,y) and value n  in format xyn > ")) 
        x=int((n/100))-1
        y=int((n%100)/10)-1
        n=n%10
        input_n(puzzle,x,y,n)              
    print("INPUT SUDOKU COMPLETED...")
    return puzzle



def solve_sudoku(puzzle):
# function checks if there is single suggestion for any cell and consider it as solution          
    x,y,=0,0
    w,h=9,9
    flg=0
    for x in range(w):
        for y in range(h):
            if(puzzle_comb[x][y]!=0 and len(puzzle_comb[x][y])==1):
                n=puzzle_comb[x][y][0]
                input_n(puzzle,x,y,n)
                flg=1
    return flg


def naked_pair():
# function to check if there is same pair of suggestion at two places 
# elements of pair can not be solution for any other place       

    w,h=9,9
    for x in range(w):
        s=-1
        for y in range(h):
            if s==-1 and puzzle_comb[x][y]!=0 and len(puzzle_comb[x][y])==2:
                s=y
            else:
                if s!=-1 and puzzle_comb[x][y]!=0 and len(puzzle_comb[x][y])==2 and puzzle_comb[x][y]== puzzle_comb[x][s]:
                    for item in puzzle_comb[x][y]:
                        for z in range(9):
                            if z!=y and z!=s and puzzle_comb[x][z]!=0 and puzzle_comb[x][z].count(item)>0:
                                puzzle_comb[x][z].remove(item)
                    break
    for x in range(w):
        s=-1
        for y in range(h):
            if s==-1 and puzzle_comb[y][x]!=0 and len(puzzle_comb[y][x])==2:
                s=y
            else:
                if s!=-1 and puzzle_comb[y][x]!=0 and len(puzzle_comb[y][x])==2 and puzzle_comb[y][x]== puzzle_comb[s][x]:
                    for item in puzzle_comb[y][x]:
                        for z in range(9):
                            if z!=y and z!=s and puzzle_comb[z][x]!=0 and puzzle_comb[z][x].count(item)>0:
                                puzzle_comb[z][x].remove(item)
                    break
    
    return
                


def solve_sudoku_pos():
# function to check if suggestion is only in row or col of box but not in row 
#    or col of other associated boxes, it will be conidered as unique solution 
#    for row or col of box and should be removed from others       
    x,y,=0,0
    w,h=9,9
    flg=0
    for x in range(w):
        for y in range(h):
            #if x!=1 or y!=3:
            #    continue
            if(puzzle_comb[x][y]!=0 and len(puzzle_comb[x][y])>=1):
                for item in puzzle_comb[x][y]:
                    flg=0
                    for r in range(9):
                        if(r>=int(y/3)*3 and r<(int(y/3)*3)+3):
                            continue
                        else:
                            if (puzzle_comb[x][r]!=0 and puzzle_comb[x][r].count(item)>0):
                                flg=1
                                break
                    if flg==0:
                        for a in range(int(x/3)*3,(int(x/3)*3)+3):
                            if a==x:
                                continue
                            for b in range(int(y/3)*3,(int(y/3)*3)+3):
                                if (puzzle_comb[a][b]!=0 and puzzle_comb[a][b].count(item)>0):
                                    print("check row", item,x,y)
                                    puzzle_comb[a][b].remove(item)
    
                    flg=0
                    for c in range(9):
                        if(c>=int(x/3)*3 and c<(int(x/3)*3)+3):
                            continue
                        else:
                            if (puzzle_comb[c][y]!=0 and puzzle_comb[c][y].count(item)>0):
                                flg=1
                                break
                    if flg==0:
                        for a in range(int(x/3)*3,(int(x/3)*3)+3):
                            for b in range(int(y/3)*3,(int(y/3)*3)+3):
                                if b==y:
                                    continue
                                if (puzzle_comb[a][b]!=0 and puzzle_comb[a][b].count(item)>0):
                                    print("check col", item,x,y)
                                    puzzle_comb[a][b].remove(item)
                            
    return

def find_unique_box(puzzle):
# function checks if a number present only once as suggested solution in box
# to consider it as solution

    box=[[0 for x in range(3)] for y in range(3)]
    srtd_box=[[0 for x in range(3)] for y in range(3)]
    flg=0
    for x in range(0,w,3):
        box[0]=[]
        srtd_box[0]=[]
        box[1]=[]
        srtd_box[1]=[]
        box[2]=[]
        srtd_box[2]=[]
        
        for y in range(w):
            if(puzzle_comb[x][y]!=0):
                box[int(y/3)] = box[int(y/3)]+puzzle_comb[x][y]
            if(puzzle_comb[x+1][y]!=0 ):
                box[int(y/3)] = box[int(y/3)]+puzzle_comb[x+1][y]
            if(puzzle_comb[x+2][y]!=0 ):
                box[int(y/3)] = box[int(y/3)]+puzzle_comb[x+2][y]            
        for y in range(3):
            srtd_box[y]= sorted(set([i for i in box[y] if box[y].count(i)==1]))
            if(len(srtd_box[y])>0):
                for item in srtd_box[y]:
                    for z in range(y*3,(y*3)+3):
                        if(puzzle_comb[x][z]!=0 and puzzle_comb[x][z].count(item)==1):
                            input_n(puzzle,x,z,item)
                            flg=1
                            break
                        if(puzzle_comb[x+1][z]!=0 and puzzle_comb[x+1][z].count(item)==1):
                            input_n(puzzle,x+1,z,item)
                            flg=1
                            break
                        if(puzzle_comb[x+2][z]!=0 and puzzle_comb[x+2][z].count(item)==1):
                            input_n(puzzle,x+2,z,item)
                            flg=1
                            break
    return flg
    
def solve_candidate_line():
# function checks if a number present only row or column as solution in a box
# such number should be dropped from other cells of related row or column 
# of other boxes 

    box=[[0 for x in range(3)] for y in range(3)]
    srtd_box=[[0 for x in range(3)] for y in range(3)]
    #flg=0
    for x in range(0,w,3):
        box[0]=[]
        srtd_box[0]=[]
        box[1]=[]
        srtd_box[1]=[]
        box[2]=[]
        srtd_box[2]=[]
        
        for y in range(w):
        # loop to find possible numers in box 1-3 and so on 
            if(puzzle_comb[x][y]!=0):
                box[int(y/3)] = box[int(y/3)]+puzzle_comb[x][y]
            if(puzzle_comb[x+1][y]!=0 ):
                box[int(y/3)] = box[int(y/3)]+puzzle_comb[x+1][y]
            if(puzzle_comb[x+2][y]!=0 ):
                box[int(y/3)] = box[int(y/3)]+puzzle_comb[x+2][y]            
        
        for y in range(3):
            srtd_box[y]= sorted(set([i for i in box[y] if box[y].count(i)>=1]))
            if(len(srtd_box[y])>0):
                for item in srtd_box[y]:
                    for z in range(y*3,(y*3)+3):
                        if(puzzle_comb[x][z]!=0 
                           and puzzle_comb[x][z].count(item)==1
                           and (unique_in_row(item,x,z)==1 
                                or unique_in_col(item,x,z)==1)):
                            1 #do nothing
                        if(puzzle_comb[x+1][z]!=0 
                           and puzzle_comb[x+1][z].count(item)==1
                           and (unique_in_row(item,x+1,z)==1 
                                or unique_in_col(item,x+1,z)==1)):
                            1 #do_nothing
                        if(puzzle_comb[x+2][z]!=0 
                           and puzzle_comb[x+2][z].count(item)==1
                           and (unique_in_row(item,x+2,z)==1 
                                or unique_in_col(item,x+2,z)==1)):
                            1 #do_nothing

#    flg=solve_sudoku(puzzle)
    return 

def unique_in_row(num, row_no, col_no):
    r=int(row_no/3)*3
    c=int(col_no/3)*3
    for a in range(r,r+3):
        if a==row_no:
            continue
        for b in range(c,c+3):
            if (puzzle_comb[a][b]!=0 and puzzle_comb[a][b].count(num)>0):
                return 0
    
    for b in range(9):
        if b>=c and b<c+3:
            continue
        else:
            if (puzzle_comb[row_no][b]!=0 and puzzle_comb[row_no][b].count(num)>0):
                puzzle_comb[row_no][b].remove(num)
    return 1
        
def unique_in_col(num, row_no, col_no):
    if row_no<6 or col_no<6:
        return 0
    r=int(row_no/3)*3
    c=int(col_no/3)*3
    for a in range(r,r+3):
        for b in range(c,c+3):
            if b==col_no:
                continue
            if (puzzle_comb[a][b]!=0 and puzzle_comb[a][b].count(num)>0):
                return 0
    for b in range(9):
        if b>=r and b<r+3:
            continue
        else:
            if (puzzle_comb[b][col_no]!=0 and puzzle_comb[b][col_no].count(num)>0):      
                puzzle_comb[b][col_no].remove(num)
    return 1            
    
def find_unique(puzzle):
# function checks if a number present only once as suggested solution in 
# any row or column
# to consider it as solution for corresponding cell

    lst_row=[]   #row possible solutions
    srtd_row=[]  #row unique solution/s
    lst_col=[]   #col possible solution 
    srtd_col=[]  #col unique solution/s
    flg=0
    for x in range(0,w):
        lst_row=[]
        srtd_row=[]
        lst_col=[]
        srtd_col=[]
        for y in range(0,w):
            if(puzzle_comb[x][y]!=0):
                lst_row = lst_row+puzzle_comb[x][y]
            if(puzzle_comb[y][x]!=0):
                lst_col = lst_col+puzzle_comb[y][x]
               
        srtd_row= sorted(set([i for i in lst_row if lst_row.count(i)==1]))
        srtd_col= sorted(set([i for i in lst_col if lst_col.count(i)==1]))
        
        if(len(srtd_row)>0):
            for item in srtd_row:
                for y in range(w):
                    if(puzzle_comb[x][y]!=0 and puzzle_comb[x][y].count(item)==1):
                        input_n(puzzle,x,y,item)
                        flg=1
                        break
        
        if(len(srtd_col)>0):
            for item in srtd_col:
                for y in range(w):
                    if(puzzle_comb[y][x]!=0 and puzzle_comb[y][x].count(item)==1):
                        input_n(puzzle,y,x,item)
                        flg=1
                        break
    return flg

## MAIN FUNCTION 
## Starting point

w, h, z= 9, 9, 9 
i=0 
sudoku_cnt=81  
puzzle=[[0 for x in range(w)] for y in range(h)]
puzzle_comb=[[[x+1 for x in range(w)] for y in range(h)] for z in range(w)]
flag=1

print("Blank Sudoku sheet")
print_sudoku(puzzle)
puzzle=input_sudoku(puzzle)
print("Sudoku sheet")
print_sudoku(puzzle)
#print(sudoku_cnt)

print("Start Solving....")
st_time=datetime.datetime.now()
while (flag>0 and sudoku_cnt>0):
    flag=0
    print("attempt",i+1)
    flag=solve_sudoku(puzzle)
    flag=flag+find_unique(puzzle)
    flag=flag+find_unique_box(puzzle)
    i=i+1

flag=1
print("Candidate Line approach")
while (flag>0 and sudoku_cnt>0):
    flag=0
    print("attempt",i+1)
    solve_candidate_line()
    solve_sudoku_pos()
    naked_pair()
    flag=solve_sudoku(puzzle)
    flag=flag+find_unique(puzzle)
    flag=flag+find_unique_box(puzzle)
    i=i+1


if(sudoku_cnt>0):
    print_sudoku(puzzle)
    print_sudoku(puzzle_comb)
    print("Does this has one solution??")
    
else:
   print("Solved..")
   print_sudoku(puzzle)
end_time=datetime.datetime.now()
print("Elapsed Time ",end_time-st_time)
