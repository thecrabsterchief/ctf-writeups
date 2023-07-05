from secret import flag

def cal_flag(flag):
	output=[]
	for i in range(len(flag)):
	    temp = ord(flag[i])**17%3233
	    output.append(temp)
	print(output)

if __name__ == '__main__':
	cal_flag(flag)

#[604, 2170, 3179, 884, 1313, 3000, 1632, 884, 855, 3179, 119, 1632, 2271, 119, 612, 2412, 2185, 2923, 2412, 1632, 2271, 2271, 1313, 2412, 119, 3179, 119, 2170, 1632, 2578, 1313, 119, 2235, 2185, 119, 745, 3179, 1369, 1313, 1516]