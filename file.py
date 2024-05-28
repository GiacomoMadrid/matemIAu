from datetime import datetime
now = datetime.now()
print(now.strftime("%Y/%m/%d %H:%M:%S"))


f = open("demofile2.txt", "a")

f.write(now.strftime("%Y/%m/%d %H:%M:%S"))
f.close()


#open and read the file after the appending:
"""
f = open("demofile2.txt", "r")
won_count = 0
lost_count = 0
for line in f:
    line_split = line.split(',')
    if line_split[0] == "Won":
        won_count = won_count+1
    elif line_split[0] == "Lost":
        lost_count = lost_count+1
print("Won:", won_count)
print("Lost:", lost_count)
f.close()
"""