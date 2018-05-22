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

    s_inputs=[216,277,294
              ,324,352,367,383
              ,425,438,451,464,472
              ,521,534,553,579,585
              ,639,642,657,674,688
              ,722,748,756,784
              ,811,836,898]

    sudoku_size=29 
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
#                print(x,y," Sorted BOX ",srtd_box[y])
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
    
    
def find_unique(puzzle):
# function checks if a number present only once as suggested solution in any row or column
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

if(sudoku_cnt>0):
    print_sudoku(puzzle)
    print_sudoku(puzzle_comb)
    print("Does this has one solution??")
    
else:
   print("Solved..")
   print_sudoku(puzzle)
end_time=datetime.datetime.now()
print("Elapsed Time ",end_time-st_time)
