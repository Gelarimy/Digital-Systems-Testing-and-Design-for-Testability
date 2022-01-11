#lab 7

def RAM():
    matrix = [1024][1024]

def walking_0_1(mx): #три цикла - первый записывает в базовую ячейку 1, второй и третий остальное зануляет
    matrix = [1024][1024]
    read_matrix = []

    for base in range(1024*1024):
        for mx_col in range(1024):
            for ms_row in range(1024):
                matrix[mx_col][ms_row] = 0
        matrix[base] = 1

        for m in matrix:
            read_matrix.append(m)




def decoder(adr):
    inputs = [i for i in range(10)]  #входы в дек системе

    outputs = [i for i in range(1024)] #выходов 1024

    adr_colunm = int(adr/32)
    adr_row = divmod(adr, 32)

    print(adr_colunm, adr_row)


if __name__ == '__main__':
    decoder(1023)





