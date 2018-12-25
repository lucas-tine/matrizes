# initializer: M = matrix (lines, columns)
M = matrix (2,2)
# Easy ways to place numbers in it:  

M.fill (1, 2,  3 ,4)

the result:
| 1  2 |
| 3  4 |

other possibilities to the same result:

# M.setline (line , [*values])
M.setline(1, [1,2])
M.setline(2, [3,4])

# M.setcolumn (column, [*values])
M.setcolumn (1, [1,3])
M.setcolumn (2, [2,4])

# M.setterm (line, column, value)
M.setterm (1,1 ,1)
M.setterm (1,2 ,2)
M.setterm (2,1 ,3)
M.setterm (2,2 ,4)

Operations:
add       C = A + B
multiply  C = A * B
mult-num  C = 3*A
div-num   C = A/3
transpose C = A.transpose()
inverse   C = A.inverse()

