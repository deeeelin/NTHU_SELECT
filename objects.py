from bs4 import BeautifulSoup as bs
from typing import List,TypeVar,Tuple
from copy import deepcopy
from tabulate import tabulate
import numpy as np
import sys
import os
import extensions

def make_root(path,encode='cp950'):
    """create the root bs4 object of a html """
    data=open(path,mode='r',encoding=encode)
    root=bs(data.read(),"html.parser")
    root.prettify()
    return root

def get_ACIXSTORE():
    print("""
          Go to :

          https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629001.php

          get the url of a course's syllabus for better user experience , or enter "N" to ignore.
          """)
    
    SYLLABUS=input("url: ")
    if SYLLABUS != "N" :
        ACIXSTORE=SYLLABUS[(SYLLABUS.find("ACIXSTORE=")+len("ACIXSTORE=")):(SYLLABUS.find("&c_key="))]
    else : 
        ACIXSTORE=None

    return  ACIXSTORE

class selector:
    
    
    def __init__(self,LCES_lis:List[bs],CASD:bs,ACIXSTORE) -> None:
        
        
        
        self.ACIXSTORE=ACIXSTORE
        self.courses=[]
        infos=dict()

        body_CASD=CASD.find("tbody")
        courses_CASD=body_CASD.find_all(lambda tag: tag.name == 'tr' and not tag.attrs)

        for cours in courses_CASD:

            content=[cours.contents[i] for i in range(1,len(cours.contents),2)] 
            num,name,teacher,people,gpa,deviation,none1,none2=[c.text.strip() for c in content]
            
            gpa,deviation=float(gpa),float(deviation)

            infos[name+":"+teacher]=(gpa,deviation)

        for LCES in LCES_lis:
            body_LCES=LCES
            courses_LCES=body_LCES.find_all("tr",attrs={'class':"word"})
            
            for cours in courses_LCES:
                
                content=[cours.contents[i] for i in range(1,len(cours.contents),2)]
                
                if len([c.text for c in content]) == 9:
                    num,name,teacher,dimension,time,none1,none2,x1,x2=[c.text for c in content]
                else:
                    num,name,teacher,time,none1,none2,x1,x2=[c.text for c in content]

                if x1=="無限制":
                    possibility=1
                else:
                    possibility=float(x1)/(float(x2)+1)

                if not infos.get(name+":"+teacher):
                    continue
                else:
                    gpa,deviation=infos[name+":"+teacher]

                if time == ' ' :
                    time = 'X'

                self.courses.append(course(num,name,teacher,time,possibility,gpa,deviation))
                
                


        self.tables={"BASE":deepcopy(self.courses)}
        self.cur_table="BASE"
        self.show_list={
            "num":True,
            "name":True,
            "teacher":True,
            "time":True,
            "possibility":True,
            "gpa":True,
            "deviation":True
            
        }
        self.show_mode="html"
        
        
        

        
    

    def run(self,cmds):
        cmds=cmds.split()
        
        try:
            match cmds[0]:
                case "list":
                    current=[]
                    print("start listing....")
        
                    for course  in self.courses :
                        for member in self.show_list:
                            exec(member+"= course." + member)
                            
                        
                        exec("current.append(course) if ("+" ".join(cmds[1:])+") else course\n")
                    
                    self.tables[self.cur_table]=current

                    print("listed")
                    
                
                    
                case "filter":
                    current=[]
                    

                    for course  in self.tables[self.cur_table] :
                        for member in self.show_list:
                            exec(member+"= course." + member)

                        exec("current.append(course) if ("+" ".join(cmds[1:])+") else course\n")

                    self.tables[self.cur_table]=current

                    print("filtered!")

                    
                
                case "change":
                    
                    if not cmds[1] in self.tables:
                        print("no such table")
                    else :
                        self.cur_table=cmds[1]
                        print("table changed !")


                case "sort":
                    #thing
                    def func(course,string):

                        for  member in self.show_list:
                            exec(member+"= course." + member)
                        
                        loc = {}
                        exec("answer="+string, locals(), loc)
                        return loc["answer"]
    
                    if cmds[1]=="a":
                        reverse="False"
                    elif cmds[1] == "d":
                        reverse="True"

                    

                    exec("self.tables[self.cur_table].sort(key=lambda course : func(course,'"+" ".join(cmds[2:])+"'),reverse="+reverse+")",locals())

                    print("sorted !")
                
                case "function":
                    
                    exec("self.tables[self.cur_table]=self."+ " ".join(cmds[1:]))
                    print("function executed !! ")

                case "remove":
                    for i in cmds[1:]:
                        number = int(i)
                        del self.tables[self.cur_table][number]
                    
                    print("Removed !")

                case "add_table":
                    name=cmds[1]
                    if name in self.tables:
                        print("table existed !! ")
                    else:
                        if(len(cmds)>2):
                            self.add_table(name,deepcopy(self.tables[cmds[2]]))
                        else: 
                            self.add_table(name)
                        
                        print("table added  !")

                case "delete_table":
                    name=cmds[1]
                    if len(self.tables.keys())==1:

                        print("need at least one table !!")
                        
                    else:

                        self.delete_table(name)

                        if name==self.cur_table:
                            self.cur_table=list(self.tables.keys())[0]

                        print("table deleted !")

                case "reset":
                    self.tables[self.cur_table]=deepcopy(self.courses)

                    print("reset completed !")

                case "show":
                    for i in cmds[1:]:
                        self.show_list[i]=True

                case "unshow":
                    for i in cmds[1:]:
                        self.show_list[i]=False

                case "show_mode":
                        
                        if cmds[1]=="html":
                            self.show_mode="html"

                        elif cmds[1]=="text":
                            self.show_mode="fancy_grid"

                case "renew_url":
                        self.ACIXSTORE=get_ACIXSTORE()

                case _:
                    print("invalid command !! ")
            
        
        except:
            print("error !! ")
        
        
        self.show(self.show_mode)

        return 
                    
            
        
    def add_table(self,name,courses=[]):
        self.tables[name]=courses
        self.cur_table=name
        return 

    def delete_table(self,name):
        if name in  self.tables:
            del  self.tables[name]
   
    def show(self,mode):
        table=[]
        if mode=="html":
            sys.stdout=open(os.path.dirname(__file__)+"/result.html","w")
        else:
            sys.stdout=open(os.path.dirname(__file__)+"/result.txt","w")

        to_show=[]
        for j in self.show_list.keys():
            if self.show_list[j]:
                to_show.append(j)
        
        show_format={
            "num":"COURSE NUMBER",
            "name":"COURSE NAME",
            "teacher":"TEACHER",
            "time":"TIME",
            "possibility":"ENROLL POSSIBILITY",
            "gpa":"AVERAGE GPA",
            "deviation":"DEVIATION"}
        
        headers=[show_format[i] for i in to_show]
        
        table.append(headers)

        for i in range(len(self.tables[self.cur_table])):
            

            table.append(self.tables[self.cur_table][i].show(to_show))
            
        
        tmp = tabulate(table,headers='firstrow',showindex="always",tablefmt=mode,numalign="center")

        

        if mode == "html" :
            tmp = "<body bgcolor='#EBDEF0'>" + tmp + "</body>"

            output=bs(tmp,"html.parser")
            
            if self.ACIXSTORE:
                # add link of courses 
                if not "name" in to_show:
                    pass
                else:
                    ind = to_show.index("name")
                    courses=output.find("tbody").find_all("tr")
                    for i in range(len(courses)):
                        
                        tmp=(str(courses[i].contents[1].string).split(" "))
                        year=tmp[0]
                        num = tmp[-1]

                        news=output.new_tag("a", href="https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/common/Syllabus/1.php?ACIXSTORE="+self.ACIXSTORE+"&c_key="+year+"%20%20"+num)
                        news.string=courses[i].contents[ind+1].string
                        courses[i].contents[ind+1].clear()
                        courses[i].contents[ind+1].append(news)
                

            news=output.new_tag("h1",align='center' ,style="background-color:powderblue;border-radius: 12px;")
            news.string="CURRENT TABLE : "+ self.cur_table
            output.table.insert(0,news)


            output.table.attrs["bgcolor"]="#ECF0F1"
            output.table.attrs["style"]="border-radius: 12px;"
            output.table.attrs["align"]="center"

            """
            titles = output.find("tr").contents

           
            for title in titles:
                tmp = title.string
                title.clear()
                news = output.new_tag("b")
                news.string = tmp
                title.append(news)

            """
            print(output.prettify())
        elif mode == "fancy_grid" :
            print(tmp)

        sys.stdout=sys.__stdout__

    
    with open("extensions.py","r") as f:
            extension_file = f.read()
            f.close()
    
    exec(extension_file)


class course:
    def __init__(self,num,name,teacher,time,possibility,gpa,deviation) -> None:
        self.num=num
        self.name=name
        self.teacher=teacher
        self.time=time
        self.possibility=possibility
        self.gpa=gpa
        self.deviation=deviation
    def show(self,to_show):

        tmp = []
        members=["num","name","teacher","time","possibility","gpa","deviation"]
        for m in to_show:
                exec("tmp.append(self."+m+")")
    
        return tmp
        
        #print(self.num," ",self.name," ",self.teacher," ",self.time," ",self.possibility," ",self.gpa," ",self.deviation)
    