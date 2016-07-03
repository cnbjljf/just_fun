import yaml,time
f=open('top.ljf','r')
c=yaml.load(f)

def xxx():
    for i in c:
         #print('modules',i)
         for h in c.get(i):
             #print('hostname',h)
             for cm in c.get(i)[h]:
                 yield i,h,cm

def main():
    while 1:
        c=xxx()
        xa=c.__next__()
        #print(xa)
        modu,host,cmd=xa
        print(modu,host,cmd)
        time.sleep(3)


main()


              
