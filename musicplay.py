import tkinter, os, time, threading
from tkinter.filedialog import askopenfile, askdirectory
from pygame import mixer, error
from random import randint, choice
from mutagen.mp3 import MP3

class Window:

        def __init__(self):
                self.root = tkinter.Tk()
                self.root.title("musicplay")
                self.root.config(bg="#C7C7C7")
                self.root.geometry("400x300+350+150")
                self.root.resizable(0, 0)

                self.frame_foot = tkinter.Frame(self.root, bg="#C2C0C0", width=390, height=90, relief=tkinter.RAISED)
                self.play_ico = tkinter.StringVar()
                self.zhuangtai_ico = tkinter.StringVar()
                self.button_bofang = tkinter.Button(self.frame_foot,textvariable=self.play_ico, command=self.play, width=3)
                self.button_kuaijin = tkinter.Button(self.frame_foot, text="»", width=2, command=self.kuaijin)
                self.button_houtui = tkinter.Button(self.frame_foot, text="«", width=2, command=self.back)
                self.button_bofang_zhuangtai = tkinter.Button(self.frame_foot, textvariable=self.zhuangtai_ico, command=self.change_zhuangtai, \
                                width=1, height=1, relief=tkinter.FLAT)
                self.button_next = tkinter.Button(self.frame_foot, text="⇥", width=2, command=self.next_chage)
                self.button_qianyishou = tkinter.Button(self.frame_foot, text="⇤", width=2, command=self.last_change)
                self.button_yinliang = tkinter.Button(self.frame_foot, text="♪", width=1, relief=tkinter.FLAT, command=self.open_yinliang)
                self.yinliang = tkinter.Scale(self.root)

                self.menu = tkinter.Menu(self.root)
                self.fmenu = tkinter.Menu(self.menu, tearoff=False)
                self.fmenu.add_command(label="打开文件", command=self.open_file)
                self.fmenu.add_command(label="打开文件夹", command=self.open_dir)
                self.menu.add_cascade(label="文件", menu=self.fmenu)

                self.frame_body = tkinter.Frame(self.root, bg="#989898", width=390, height=190, relief=tkinter.RAISED)
                self.path = tkinter.StringVar()
                self.time_string = tkinter.StringVar()
                self.time_label = tkinter.Label(self.frame_body, textvariable=self.time_string, fg="white", bg="#989898", font=("time", 50))
                self.show_label = tkinter.Label(self.frame_body, textvariable=self.path, bg="#989898", fg="white")
                self.music_list = tkinter.Listbox(self.frame_body, bg="#989898", fg="white", width=11, height=11, relief=tkinter.GROOVE, highlightthickness=0, \
                        )
                self.scr = tkinter.Scrollbar(self.music_list, command=self.music_list.yview, width=15)
                self.music_list.config(yscrollcommand=self.scr.set)
                self.music_list.bind("<Double-Button-1>", self.printlist)
                self.path.set("欢迎使用")
                
                self.music = ''
                self.time = 0
                self.flag = 0
                self.play_ico.set("▶")
                self.maxtime = 1
                self.dir_path = ''
                self.zhuangtai_ico.set("⇵")
                self.zhuangtai_flag = 0
                self.index = 0
                self.music_ls = list()
                self.yinliang_flag = 0
                self.yinliang_value = 0.5
                self.play_number = 1
                self.s_time_flag = 999
                self.music_dict = {}
                self.change_flag = 1
                self.kuaijin_click = 0
                self.old_music = ''

        
        def print_selection(self, v):
                self.yinliang_value = int(v) / 100
                mixer.music.set_volume(self.yinliang_value)

        def open_yinliang(self):
                if self.yinliang_flag == 0:
                        self.yinliang = tkinter.Scale(self.root, orient=tkinter.HORIZONTAL, command=self.print_selection, \
                                        from_=0, to=100,)
                        self.yinliang.set(self.yinliang_value * 100)
                        self.yinliang.place(relx=0.734, rely=0.7)
                        self.yinliang_flag = 1
                elif self.yinliang_flag == 1:
                        self.yinliang.destroy()
                        self.yinliang_flag = 0

        def play_que(self, flag):
                m = os.path.split(self.music)[1]
                if m != '':
                        n = 0
                        l = 0
                        music_ls_len = len(self.music_ls)
                        if self.music_dict != {}:
                                x = list(self.music_dict.keys())
                                if m in self.music_ls:
                                        n = self.music_ls.index(m)
                                else:
                                        n = x.index(m) + len(self.music_ls)
                                l = len(self.music_ls) + len(x)
                                if flag == "last":
                                        if n-1 > -1:
                                                n -= 1
                                        else:
                                                n = l-1
                                        self.music_list.activate(n)
                                        if n < music_ls_len :
                                                self.music = self.dir_path + '/' + self.music_ls[n]
                                        else:
                                                n = n - music_ls_len
                                                self.music = self.music_dict[x[n]] + '/' + x[n]
                                                      
                                elif flag == "next":
                                        if n+1 < l:
                                                n += 1
                                        else:
                                                n = 0
                                        self.music_list.activate(n) 
                                        if n < music_ls_len :
                                                self.music = self.dir_path + '/' + self.music_ls[n]
                                        else:
                                                n = n - music_ls_len
                                                self.music = self.music_dict[x[n]] + '/' + x[n]
                        else:
                                l = len(self.music_ls)
                                n = self.music_ls.index(m)
                                if flag == "last":
                                        if n-1 > -1:
                                                n -= 1
                                        else:
                                                n = l-1
                                elif flag == "next":
                                        if n+1 < l:
                                                n += 1
                                        else:
                                                n = 0
                                self.music_list.activate(n) 
                                self.music = self.dir_path + '/' + self.music_ls[n]     
                        self.path.set(self.music)
                        self.play_init()
                        self.qiangzhi_play()
                        self.s_time_flag = 5

        def printlist(self, event):
                self.s_time_flag = 0
                m = self.music_list.get(self.music_list.curselection())
                if m not in self.music_dict:
                        self.music = self.dir_path + '/' + m
                else:
                        self.music = self.music_dict[m] + '/' + m
                self.path.set(self.music)
                self.play_init()
                self.qiangzhi_play()                   
        
        def last_change(self):
                self.change_flag = 2
                self.zhuangtai_play()
                self.change_flag = 1

        def next_chage(self):
                self.change_flag = 1
                self.zhuangtai_play()

        def zhuangtai_play(self):
                if self.zhuangtai_ico.get() == "⇵":
                        if self.change_flag == 1:
                                self.play_que(flag="next")
                        elif self.change_flag == 2:
                                self.play_que(flag="last")
                elif self.zhuangtai_ico.get() == "↔":
                        self.play_init()
                        self.qiangzhi_play()
                        self.s_time_flag = 5
                elif self.zhuangtai_ico.get() == "≒":
                        l = len(self.music_ls) + len(self.music_dict)
                        path, m = os.path.split(self.music)
                        x = list(self.music_dict.keys())
                        music_ls_len = len(self.music_ls)
                        try:
                                m_i = self.music_ls.index(m)
                        except ValueError:
                                m_i = music_ls_len + x.index(m)
                        n = m_i
                        if m_i != 0 and m_i != l-1:
                                n1 = randint(0, m_i-1)
                                n2 = randint(m_i+1, l-1)
                                n = choice([n1, n2])
                        elif m_i == 0 and music_ls_len != 1 and len(self.music_dict) != 1:
                                n = randint(1, l-1)
                        elif m_i == l-1 and music_ls_len != 1:
                                n = randint(0, l-2)
                        elif l == 1:
                                pass
                        self.music_list.activate(n)
                        if n < music_ls_len :
                                self.music = self.dir_path + '/' + self.music_ls[n]
                        else:
                                n = n - music_ls_len
                                self.music = self.music_dict[x[n]] + '/' + x[n]
                        self.path.set(self.music)
                        self.play_init()
                        self.qiangzhi_play()
                        self.s_time_flag = 5

        def qiangzhi_play(self):
                self.play_ico.set("| |")
                self.flag = 1
                self.s_time_flag = 0
                mixer.music.play(self.play_number, self.time)
        
        def kuaijin(self):
                if self.time < self.maxtime and self.music != '':
                        self.s_time_flag = 1
                        t = mixer.music.get_pos()
                        t = str(t)
                        t = t[:-3] + '.' + t[-3:]
                        try:
                                t = eval(t)
                        except SyntaxError:
                                t = 0.0
                        t += 5
                        self.time += t
                        mixer.music.load(self.music)
                        self.qiangzhi_play()
                        self.change_flag = 1
                else:
                        pass 
        
        def back(self):
                if self.time > 5 :
                        self.s_time_flag = 2
                        t = mixer.music.get_pos()
                        t = str(t)
                        t = t[:-3] + '.' + t[-3:]
                        t = eval(t)
                        self.time += t
                        self.time -= 5
                else:
                        self.s_time_flag = 3
                        self.time = 0
                if self.music != '':
                        mixer.music.load(self.music)
                        self.qiangzhi_play()

        def play(self):
                if self.music != '':
                        if self.flag == 0:
                                mixer.music.play(self.play_number, self.time)
                                self.flag = 1
                                self.play_ico.set("| |")
                                self.s_time_flag = 0
                        elif self.flag == 1:
                                mixer.music.pause()
                                self.play_ico.set("▶")
                                self.flag = 2
                                self.s_time_flag = 4
                        elif self.flag == 2:
                                mixer.music.unpause()
                                self.play_ico.set('| |')
                                self.flag = 1
                                self.s_time_flag = 0

        def play_init(self):
                self.time = 0.0
                try:
                        mixer.music.load(self.music)
                except error:
                        self.path.set("暂不支持此格式")
                mixer.music.set_volume(self.yinliang_value)
                sound_time = MP3(self.music).info.length
                self.maxtime = float(sound_time)
                self.flag = 0
                self.play_ico.set("▶")

        def open_dir(self):
                d = askdirectory()
                if d != "":
                        self.s_time_flag = 6
                        self.dir_path = d
                        self.music_list.delete(0, tkinter.END)
                        self.music_ls.clear()
                        self.index = 0
                        try:
                                music_ls = os.listdir(d)
                        except FileNotFoundError:
                                music_ls = []
                        for m in music_ls:
                                ty = m[-4:]
                                if ('.mp3' == ty) and m not in self.music_ls:
                                        self.music_list.insert(tkinter.END, m)
                        self.music_ls = list(self.music_list.get(0, tkinter.END))
                        mixer.music.stop()
                        self.music = ''
                        self.s_time_flag = 5
                        self.play_ico.set("▶")
                        self.path.set("请选择音乐文件")
                        self.music_dict = {}

        def open_file(self):
                path = askopenfile()
                name = path.name
                if name[-4:] == ".mp3":
                        self.music = name
                        self.path.set(name)
                        self.play_init()
                        m = os.path.split(self.music)
                        music, path = m[1], m[0]
                        flag = 0
                        x = list(self.music_dict.keys())
                        if self.dir_path == '':  
                                self.dir_path = path
                                flag = 1
                        if music not in self.music_ls and music not in x:
                                if flag == 0:
                                        self.music_dict[music] = path
                                else:
                                        self.music_ls.append(music)
                                self.music_list.insert(tkinter.END, music)
                                self.play_init()
                                self.qiangzhi_play()
                                self.s_time_flag = 0
                                self.music_list.activate(tkinter.END)
                        else:
                                self.play_init()
                                self.qiangzhi_play()
                                self.s_time_flag = 0

                else:
                        self.path.set("暂不支持此格式")      
        

        def change_zhuangtai(self):
                if self.zhuangtai_flag == 0:
                        self.zhuangtai_ico.set("↔")
                        self.zhuangtai_flag = 1
                elif self.zhuangtai_flag == 1:
                        self.zhuangtai_ico.set("≒")
                        self.zhuangtai_flag = 2
                elif self.zhuangtai_flag == 2:
                        self.zhuangtai_ico.set("⇵")
                        self.zhuangtai_flag = 0

        def run(self):                
                self.root['menu'] = self.menu
                self.show_label.place(relx=0, rely=0.9)
                self.scr.pack(side='right', fill='y')
                self.music_list.place(x=271.5, y=0.5, relwidth=0.3, relheight=1.0)
                self.button_bofang.place(relx=0.45, rely=0.4)
                self.button_houtui.place(relx=0.37, rely=0.4)
                self.button_kuaijin.place(relx=0.55, rely=0.4)
                self.button_bofang_zhuangtai.place(relx=0.8, rely=0.4)
                self.button_next.place(relx=0.63, rely=0.4)
                self.button_qianyishou.place(relx=0.29, rely=0.4)
                self.button_yinliang.place(relx=0.74, rely=0.4)
                self.time_label.place(relx=0.13, rely=0.3)
                self.frame_foot.place(x = 5, y = 205)
                self.frame_body.place(x=5, y=5)
                self.root.mainloop()

def switch_end(win):
        while 1:
                if win.s_time_flag == 0:
                        s = "00:{:0>2}"
                        s2 = "{:0>2}:{:0>2}"
                        s_time = 0
                        while 1:
                                t = mixer.music.get_pos()
                                t = str(t)
                                t = t[:-3]
                                try:
                                        t = eval(t)
                                except SyntaxError:
                                        t = 0
                                t = int(win.time + t)
                                s_time = t
                                if win.s_time_flag == 1:
                                        win.s_time_flag = 0
                                elif win.s_time_flag == 2:
                                        win.s_time_flag = 0
                                elif win.s_time_flag == 3:
                                        win.s_time_flag = 0
                                elif win.s_time_flag == 4:
                                        """4:暂停状态码"""
                                        while win.s_time_flag == 4:
                                                if win.s_time_flag != 4:
                                                        break
                                elif win.s_time_flag == 5:
                                        """5:重置状态码"""
                                        s_time = 0
                                        win.s_time_flag = 0
                                elif win.s_time_flag == 6:
                                        s_time = 0
                                        win.time_string.set(s.format(s_time))
                                        while win.s_time_flag == 6:
                                                if win.s_time_flag != 6:
                                                        break
                                if s_time - 60 < 0:
                                        win.time_string.set(s.format(s_time))
                                else:
                                        win.time_string.set(s2.format(s_time//60, s_time - 60*(s_time//60)))
                                s_time += 1
                                if s_time >= win.maxtime - 3:
                                        print('切换')
                                        win.zhuangtai_play()
                                        s_time = 0
                                time.sleep(0.1)
                else:
                        time.sleep(0.1)
                        

if __name__ == "__main__":
        mixer.init()
        win = Window()
        t = threading.Thread(target=switch_end, args=(win,))
        t.setDaemon(True) # 设置在主进程结束后结束
        t.start()
        win.run()
