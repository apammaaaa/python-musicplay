import os, sys
from tkinter.filedialog import askopenfile, askdirectory
from tkinter import Tk
from threading import Thread

root = Tk()
root.attributes("-alpha", 0.0)
root.geometry("0x0")
type_tu = ('.wav', '.m4a', '.ogg', 'wma', 'aac', 'mpeg')

def change_file():
    while 1:
        os.system('cls')
        print("1.单曲转换")
        print("2.批量转换")
        n = input("请选择:")
        if n == "1":
            filename = askopenfile()
            if filename != None:
                filename = filename.name
            else:
                continue
            filename = filename.strip()
            path, name = os.path.split(filename)
            ty = name[-4:].lower()
            if ty != ".mp3" and ty in type_tu:
                name = name.replace(ty, '.mp3')
                newfilename = path + '/' + name
                print(newfilename)
                os.system('ffmpeg\\bin\\ffmpeg.exe -i {} {}'.format(filename, newfilename))
                print("完成")
        elif n == "2":
            dirname = askdirectory()
            print(dirname)
            if dirname != '':
                filels = os.listdir(dirname)
                for i in filels:
                    print(i)
                    ty = i[-4:].lower()
                    if ty != '.mp3' and ty in type_tu :
                        i = i.strip()
                        name = i.split('.')[0]
                        filename = dirname+'/'+i
                        newfilename = dirname+'/'+name+'.mp3'
                        os.system('ffmpeg\\bin\\ffmpeg.exe -i {} {}'.format(filename, newfilename))
                print("完成")
        
t = Thread(target=change_file, args=())
t.setDaemon(True)
t.start()
root.mainloop()


    
