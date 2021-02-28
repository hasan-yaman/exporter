#  image-export-start
def function_1():
    print("Hello World!")
#  image-export-end

#  image-export-start
def function_2(x):
    print(x)
    if x == 3:
        y = 2
    else:
        y = 4
    print(y)
# image-export-end


#  image-export-start
def function_3(x: int):
    #  This is a comment
    print(f"x: {x}")
    total = 0
    for i in range(x):
        total += i * x
    return total
# image-export-end
