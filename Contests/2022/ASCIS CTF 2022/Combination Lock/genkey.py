for n1 in range(1, 9):
    for n2 in range(1, 9):
        for n3 in range(1, 9):
            for n4 in range(1, 9):
                for n5 in range(1, 9):
                    for n6 in range(1, 9):
                        for n7 in range(1, 9):
                            for n8 in range(1, 9):
                                r1 = n1*n2 + n3*n4 + n5*n6 + n7*n8
                                r2 = (n1 + n2)*(n3 + n4)*(n5 + n6)*(n7 + n8)
                                if r1 == 88 and r2 == 8800:
                                    print("[+] Key:", n1, n2, n3, n4, n5, n6, n7, n8)
                                    exit()