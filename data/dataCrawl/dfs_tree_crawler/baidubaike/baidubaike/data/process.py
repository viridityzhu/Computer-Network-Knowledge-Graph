with open('leaf_from_baidu.csv', 'r')as f:
    words = f.readlines()

words = set(words)
print(len(words))
with open('leaf_from_baidu.csv', 'w')as f:
    f.writelines(words)
