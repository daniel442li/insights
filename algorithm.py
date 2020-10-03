import pytesseract
from PIL import Image

text = pytesseract.image_to_string(Image.open('Receipt2.JPG'))
#text = spell(text)
sorted_text = text.lower().split()

total = 0

cat_totals = [0, 0, 0, 0, 0, 0, 0]

again = 1

titles = ['groceries/necessities', 'dining', 'entertainment', 'clothing', 'transportation', 'utilities', 'miscellaneous']

categories = {"costco": 0, "cvs": 0, "kroger": 0, "piggly wiggly":0, "mcdonald":1, "chick-fil-a":1, "chick fil a":1,"hattie b":1, "amc": 2, "topgolf": 2, "gap":3, "nordstrom":3,"lululemon":3, "macy":3, "macys": 3, "uber": 4, "lyft":4, "bp":4, "shell":4, "marathon": 4, "exxon": 4}

f = open("total.json", "w")

#remove while loop when integrating into flask
while again == 1:
    for x in sorted_text:
        if x == 'total' or x == 'total:':
            total = float(sorted_text[sorted_text.index(x) + 1])
            break
        elif x == 'charge' or x == 'charge:':
            total = float(sorted_text[sorted_text.index(x) + 1])
            break
        elif x == 'subtotal' or x == 'subtotal:':
            for y in sorted_text:
                if y == 'tax' or y == 'tax':
                    total = float(sorted_text[sorted_text.index(x) + 1]) + float(sorted_text[sorted_text.index(y) + 1])
                    break
        else:
            total = 0
    for x in sorted_text:
        for key in categories:
            if x == key:
                cat_totals[categories[key]] += total
                break
            else:
                cat_totals[len(cat_totals) - 1] += total
                break
        break

    print(total)

    #scan another receipt function
    inp = input('Would you like to scan another receipt? ')
    if inp == 'n':
        again = 0
        print(again)

print(cat_totals)

#export to json file
f.write("{total: " + str(total) + "}\n")
for value in range(len(cat_totals)):
    f.write(",{" + titles[value] + ": " + str(cat_totals[value]) + "}\n")


