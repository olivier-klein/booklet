day=0
cut = (days==day+2)
index=begin[cut].argsort()
for i in index:
    talk_beg  = begin[cut][i]; start=talk_beg[:2]+':'+talk_beg[-2:]
    talk_end  = end[cut][i]  ; finsh=talk_end[:2]+':'+talk_end[-2:]
    talkcode  = code[cut][i]
    talktype  = talk[cut][i]
    flag = 0
    if talktype == 'tut':
        talktype = 'Tutorial'; flag=1
    elif talktype == 'invited':
        talktype = 'Invited Talk'; flag=1
    elif talktype == 'break':
        talktype = 'Nutrition Break'
    else:
        talktype = label[cut][i]
    if flag :
        pointer   =  where(name==speaker[cut][i])[0][0]
        thetitle  = title[pointer]
        fullname  = firstname[pointer]+' '+lastname[pointer]
        fulladdr  = instit[pointer]+', '+address[pointer]+\
                    ', '+country[pointer]
    else:
        pointer=talktype; fullname='meal'
    print i, pointer, fullname
