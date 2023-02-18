###settings(functions can be modify,but don't remove it !!#########################################
def GPA(self,s):
    if s>=90:
        return 4.3
    elif s<90 and s>=85:
        return 4+(s-85)/5*0.3
    elif s<85 and s>=80:
        return 3.7+(s-80)/5*0.3
    elif s<80 and s>=77:
        return 3.3+(s-77)/3*0.4
    elif s<77 and s>=73:
        return 3.0+(s-73)/3*0.3
    elif s<73 and s>=70:
        return 2.7+(s-70)/3*0.3
    elif s<70 and s>=67:
        return 2.3+(s-67)/3*0.4
    elif s<67 and s>=63:
        return 2.0+(s-63)/3*0.3
    elif s<63 and s>=60:
        return 1.7+(s-60)/3*0.3
    else:
       # print(s)
        return 0.0
def SCORE(self,gpa):
    for i in range(100):
        if self.SCORE_TO_GPA(i,0)[0] >= gpa :
            for j in range(100):
                if self.SCORE_TO_GPA((i-1)+(j/100),0)[0] >= gpa:
                    return  (i-1)+(j/100)
def SCORE_TO_GPA(self,score,score_deviation):
    
    return (self.GPA(score-4)+self.GPA(score))/2,(score_deviation/4)*0.3

def GPA_TO_SCORE(self,gpa,deviation):
    
    return self.SCORE(gpa),(deviation/0.3*4)

#######################################functions#########################################
# sample extension function : 
def courses_in_available_time(self,available):
    current = []
    available_time=set([available[i:i+2] for i in range(0, len(available), 2)])
    for c in self.courses:
        course_time = set([c.time[i:i+2] for i in range(0, len(c.time), 2)])
        if course_time.issubset(available_time):
            current.append(c)
    current.sort(key=lambda c:c.time)
    return current


def amp(self):
    return self.courses[:200]





    

