my_list=[1,3,4,5,6,7,8,9]
sum=10
for i in my_list:
    if (sum-i) in my_list:
        print ("{0}:{1}".format(my_list.index(i),my_list.index(sum-i)))
        break
        