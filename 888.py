import csv
# НЕ УДАЛЯЙ ЭТО КОД КРАТК ДОРОЖ ПУТИ
with open('plantis.csv', mode='r', encoding='utf8') as f:
    reader = csv.reader(f, delimiter=';', quotechar='"')
    lst = list(reader)
cities_start = []
cities_continue = []
res = []
x_min = 0
point = []
for i in range(len(lst)-1):
    if lst[-1][0] == lst[i][0]:
        cities_start.append(lst[i])

for i in cities_start:

    if lst[-1][1] == i[1]:
        x_min = int(i[-1])
    else:
        point = i[1]
        for z in range(len(lst) - 1):
            for j in point:
                if j == lst[z][0]:
                    if lst[-1][1] == lst[z][1]:
                        print(lst[z], cities_continue)
                        if int(lst[z][-1]) + int(i[-1]) < x_min:
                            print(1)
                            x_min = int(lst[z][-1]) + int(i[-1])
                            res.append(i)
print(res)

