import sys


num = int(sys.argv[1])
sozluk = {}

for i in range(num):
  x=[]
  print("ID, isim, soyisim, yas giriniz")
  kelime = input()
  x = kelime.split(" ")
  uzunluk=len(x)
  n=uzunluk
  id=int(x[0])
  n=n-1
  yas=int(x[uzunluk-1])
  n=n-1
  soyisim=str(x[uzunluk-2])
  n=n-1
  isim=[]
  if id not in sozluk.keys():
     for j in range(n):
       isim.append(str(x[j+1]))


     isim.append(soyisim)
     isim.append(yas)
     tuplex = tuple(isim)
     sozluk[id] = tuplex
     print("\n")

dictionary_items = sozluk.items()
sorted_items = sorted(dictionary_items)
print(sorted_items)
