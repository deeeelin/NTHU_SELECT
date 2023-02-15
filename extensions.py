
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





    

