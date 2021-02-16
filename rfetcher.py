import os, sys

print("\n**********\nrepository fetcher\n\n")
print("1- download source")
print("2- edit source\n\n")


try:
    os.chdir("sources")
    os.chdir("..")
except:
    os.mkdir("sources")

try:
    f = open("source", "r")
    f.close()
except:
    f = open("source","w")
    f.write("")
    f.close()


while 1:
    sw = input("choose : ")

    if sw == "1":
        with open("source","r") as f:
            lines = f.readlines()
            
            os.chdir("sources")
            
            for line in lines:
                if "repositories start" in line:
                    name = line.replace("repositories start ","").replace("\n","")
                    for repo in lines:
                        if "repositories start " in repo:
                            continue

                        if "repositories end" in repo:
                            print("\n----------\nall repos downloaded from source\n\n")
                            sys.exit()

                        host, rname = repo.replace("\n","").split("/")
                        arg = f"git clone http://{host}/{name}/{rname} {rname}"
                        print(arg)
                        os.system(arg)
        
        os.chdir("..")

    elif sw == "2":
        f = open("source", "r")
        c = f.readlines()
        f.close()

        ns = list()
        for l in c:
            if "repositories start " in l:
                arg = l.replace("\n", "").replace("repositories start ", "")
                ns.append(arg)

        i = 1
        print("\n-----\ncurrent repositories in source:")
        with open("source", "r")as f:
            name = ""
            for line in f.readlines():
                for n in ns:
                    if n in line:
                        name = n

                if "repositories" not in line and "/" in line:
                    line = line.replace("\n", "")
                    d = f"{i}- {line} --{name}"
                    print(d)
                
                    i = i+1
            f.close()

        i = 1

        s = input("\n\ndo you want to remove or edit? ( r/ar/au ):")

        if s == "r":
            target = int(input("\nselect a repo with number:"))
            linesm = list()

            with open("source", "r")as f:
                content = f.read()
                f.seek(0, 0)

                lines = f.readlines()
                for line in lines:
                    if "repositories" not in line and "/" in line:
                        if i == target:
                            lines.remove(line)
                    
                        i = i+1
                f.close()

                linesm = lines

            f = open("source", "w")
            for i in linesm:
                f.write(i)

            f.close()
        
        elif s == "ar":
            f = open("source", "r")
            lines = f.readlines()
            f.close()

            names = list()
            for line in lines:
                if "repositories start " in line:
                    arg = line.replace("\n", "").replace("repositories start ","")
                    names.append(arg)


            print("---\nselect a name:")
            for n in names:
                print("\n-"+n)
            
            while 1:
                flag = 0
                selected_name = input("")
                for i in names:
                    if selected_name == i:
                        flag = 1

                if flag:
                    break
                print("-\nthere is not a user with this name!\n-")
                sys.exit()

            host = input("host : ")
            rname = input("repo name : ")

            newline = f"{host}/{rname}\n"

            newlines = list()
            for l in lines:
                if selected_name in l:
                    newlines.append(l)
                    newlines.append(newline) 
                    continue

                newlines.append(l)

            f = open("source", "w")

            for linen in newlines:
                if linen != "\n":
                    f.write(linen)

            f.close()

        elif s == "au":
                newname = input("\n\nnew name:")
                
                arg = f"repositories start {newname}\nrepositories end\n\n"
                f = open("source", "a")
                f.write(arg)
                f.close()
                        
        else:
            print("-\nunvalid input\n-")
            continue

    elif sw == "q":
        sys.exit()
    else:
        print("-\nunvalid input\n-")
