names = ["Ayala", "Ali", "Enlik"]
scores = [90,85,95]

#enumerate
for index, name in enumerate(names):
    print(index, name)

#zip
for name, score in zip(names, scores):
    print(name, score)