lst = []
input = "Hello, World!"
lst.append(chr for chr in input if chr.isalpha())
print(lst)  # Generator object

print([chr for chr in input if chr.isalpha()])  # The actual list

lst = []
for chr in input:
    if chr.isalpha():
        lst.append(chr)
print(lst)  # The actual list
