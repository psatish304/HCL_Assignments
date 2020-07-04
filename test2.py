s = 'aaabccddd'
def reduceString(s):
    l = []
    for i in s:
        # list shouldn't be empty and last elemnt should equal to i
        if l and i == l[-1]:
            l.pop()
        else:
            l.append(i)
    return ''.join(l)

if __name__ == '__main__':    
	print(reduceString(s))