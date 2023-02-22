from objects import selector,make_root,get_ACIXSTORE
from bs4 import BeautifulSoup as bs
from os import listdir,path
Debug = 0
if Debug:
    LCES_dir="./resources/LCES/"
   
    CASD="./resources/CASD_11110.html"
  
else:
    LCES_dir=input("LCES directory : ")

    CASD=input("CASD file : ")

ACIXSTORE=get_ACIXSTORE()
LCES_lis=[]
for LCES in listdir(LCES_dir):
    filename, file_extension = path.splitext(LCES)
   
    if file_extension == ".html":
        LCES_lis.append(make_root(LCES_dir+LCES))

CASD=make_root(CASD)
s=selector(LCES_lis,CASD,ACIXSTORE)

i=input("command: ")
while i != "exit":
    s.run(i)
    i=input("command: ")
    
print("GOOD BYE ~")






    
        


