line1, line2 = input().split(), input().split()
x1, y1, r1, r2 = int(line1[0]), int(line1[1]), int(line1[2]), int(line1[3])
x2, y2, r3, r4 = int(line2[0]), int(line2[1]), int(line2[2]), int(line2[3])
xA = [x1, r1]
xB = [x2, r3]
yA = [y1, r2]
yB = [y2, r4]
if max(xA) < min(xB) or max(yA) < min(yB) or min(yA) > max(yB):
    print('NO')

elif max(xA) > min(xB) > min(xA):
    dx = max(xA) - min(xB)
    print('YES')
else:
    print('YES')

