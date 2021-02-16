import os, sys

class App():
    def __init__(self, f=True):
        if f:
            self.run()

    def run(self):
        print("******************\nrepository fetcher\n\noptions:")
        print("1  download source")
        print("2  edit source")
        print("q  for exit")
        print("d  for delete the\nsource")
        print("******************")

        while 1:


            # creating source if it isnt exist
            try:
                f = open("source", "r")
                f.close()
            except:
                f = open("source","w")
                f.write("")
                f.close()

            sw = input("choose : ")

            if sw == "d":
                os.remove("source")
                print("source deleted.\nnew source created.")
                continue

            elif sw == "q":
                sys.exit()

            elif sw == "1":
                self.download_source()
            
            elif sw == "2":
                self.edit_source()
            else:
                print("-\nunvalid input\n-")
                continue

    def download_source(self):
        current_path = os.getcwd()

        sw2 = input("path to download (empty for working dir):")
        if sw2 == "":
            print("current dir = {}\ncreating sources dir if not exists...".format(os.getcwd()))

            try:
                os.chdir("sources")
            except:
                os.mkdir("sources")
                os.chdir("sources")

            print("current dir = {}".format(os.getcwd()))

        elif len(sw2) > 1:
            try:
                os.chdir(sw2)

                print("current path = {}\ncreating sources dir if not exists...".format(os.getcwd()))
                try:
                    os.chdir("sources")
                except:
                    os.mkdir("sources")
                    os.chdir("sources")

                print("current path = {}".format(os.getcwd()))

            except:
                print("-\nunvalid input of path\n-")
                return


        else:
            print("-\nunvalid input of path\n-")
            return


        with open("{}/source".format(current_path),"r") as f:
            lines = f.readlines()
            
            for line in lines:
                if "repositories start" in line:
                    name = line.replace("repositories start ","").replace("\n","")
                    for repo in lines:
                        if "repositories start " in repo:
                            continue

                        if "repositories end" in repo:
                            print("\n----------\nall repos downloaded from source\n\n")
                            os.chdir(current_path)
                            
                            sys.exit()

                        host, rname = repo.replace("\n","").split("/")
                        arg = f"git clone http://{host}/{name}/{rname} {rname}"
                        print(arg)
                        os.system(arg)

        print("\nsource is empty.")
        os.chdir(current_path)

    def edit_source(self):
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

        s = input("\nr -> remove repo by id\nar -> add repo\nau -> add user\ndu -> delete user\n? ( r/ar/au/du ):")

        if s == "r":
            is_removed_flag = 0
            target_repo = ""
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

                            target_repo = line
                            is_removed_flag = 1
                    
                        i = i+1
                f.close()

                linesm = lines

            f = open("source", "w")
            for i in linesm:
                f.write(i)

            f.close()
        
            if is_removed_flag:
                print("repo deleted : "+ target_repo )
            else:
                print("there isnt a repo with id : ",target)

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
            for line in lines:
                if (selected_name in line) and ("start" in line):
                    newlines.append(line)
                    newlines.append(newline) 
                    continue

                newlines.append(line)

            f = open("source", "w")

            for line in newlines:
                if line != "\n":
                    f.write(line)

            f.close()

        elif s == "au":
            newname = input("\n\nnew name:")
                
            arg = f"repositories start {newname}\nrepositories end {newname}\n\n"
            f = open("source", "a")
            f.write(arg)
            f.close()

        elif s == "du":
            name = input("user name will deleted :")

            f = open("source", "r")
            content = f.read()
            f.close()

            if not(name in content):
                print("there is not a user with name : "+name)
                return

            lines = content.split("\n")
            rflag = 0
            lastname =""

            for line in lines:
                if ("repositories end {}".format(name) in line) and (rflag == 1):
                    content = content.replace("{}\n".format(line), "")
                    print("user {} and all repositories related are deleted.".format(name))
                    break

                if (rflag == 1) and (lastname == name):
                    content = content.replace("{}\n".format(line), "")
                    continue

                if "repositories start " in line:
                    rname = line.replace("repositories start ", "")

                    if rname == name:
                        content = content.replace("{}\n".format(line), "")
                        rflag = 1

                    lastname = rname

            f = open("source", "w")
            f.write(content)
            f.close()
                        
        else:
            print("-\nunvalid input\n-")
            return


my_app = App()

