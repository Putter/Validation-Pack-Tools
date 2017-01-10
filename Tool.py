#-*- encoding:UTF-8 -*-
import os,re,sys,time
from Tkinter import *
import tkMessageBox
import tkFileDialog
import subprocess
import shutil
from subprocess import Popen, PIPE
import threading
import xlrd
import xlwt
from Config import Config
from Executables import AnalyzeResult,Downflash,Log,Pack_Switch, Packlist, UI

class RunTest(threading.Thread):
    def __init__(self, getvarlist):
        self.Packlist = Packlist.Pack_list()
        threading.Thread.__init__(self)
        self.alltime=0.0
        self.packtime = 0.0
        self.starttime = 0.0
        self.newselectlist=[]
        self.stopFlag = False
        self.auexcel = ''
        self.metaexcel = ''
        self.getvarlist = getvarlist
        self.phonepacklist=Log.dirlist()
    def exe_display(self,command=""):
        adb_pipe = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=1)
        if ( command != "" ):
            for line in iter(adb_pipe.stdout.readline, ''):
                print line
                UI_Screen().printf(line)
    def run(self):
        self.downbuild()
        self.Pack_Run()
        
    def downbuild(self):
        self.METApath = path['META']
        self.AUpath = path['AU']
        self.OEMpath = path['OEM']
        UI_Screen().printf( 'META: '+ self.METApath)
        UI_Screen().printf( 'AUpath: '+ self.AUpath)
        UI_Screen().printf ( 'oemname: '+ self.OEMpath)
        if self.METApath != '' and self.AUpath != '':
            self.flashMeta()
            self.flashAU()
            time.sleep(150)
        elif self.METApath == '' and self.AUpath != '':
            self.flashAU()
            time.sleep(150)
        os.chdir('C:')
        os.system('adb wait-for-device root')
        time.sleep(5)
        verity=os.popen('adb disable-verity')
        verityout = verity.read()
        verityout = verityout.replace('\n','')
        if verityout == 'Verity already disabled on /system' or verityout =='':
            pass
        else:
            os.system('adb reboot')
            time.sleep(5)
            os.system('adb wait-for-device root')
    def flashMeta(self):
        os.chdir(self.METApath)
        self.exe_display('adb reboot bootloader')
        time.sleep(10)
        self.exe_display('python fastboot_complete.py')
        self.metaexcel = self.METApath.split('\\')[-3]
    def flashAU(self):
        os.chdir(self.AUpath)
        self.exe_display('adb reboot bootloader')
        time.sleep(10)
        UI_Screen().printf('fastboot flash aboot emmc_appsboot.mbn')
        self.exe_display('fastboot flash aboot emmc_appsboot.mbn')
        UI_Screen().printf('fastboot erase boot')
        self.exe_display('fastboot erase boot')
        UI_Screen().printf('fastboot flash userdata userdata.img')
        self.exe_display('fastboot flash userdata userdata.img')
        UI_Screen().printf('fastboot flash cache cache.img')
        self.exe_display('fastboot flash cache cache.img')
        UI_Screen().printf('fastboot flash recovery recovery.img')
        self.exe_display('fastboot flash recovery recovery.img')
        UI_Screen().printf('fastboot flash recovery recovery.img')
        self.exe_display('fastboot flash boot boot.img')
        UI_Screen().printf('fastboot flash system system.img')
        UI_Screen().printf('flash system.img ...')
        UI_Screen().printf('writing system...')
        self.exe_display('fastboot flash system system.img')
        if self.OEMpath !='':
            UI_Screen().printf('fastboot flash oem %s' %self.OEMpath)
            self.exe_display('fastboot flash oem %s' %self.OEMpath)
        UI_Screen().printf('rebooting...')
        self.auexcel = self.AUpath.split('\\')[-5]+'_'+self.AUpath.split('\\')[-1]
        self.exe_display('fastboot reboot')
        
    def Pack_Run(self):
        self.newselectlist = []
        os.system('adb wait-for-device')
        for m in self.getvarlist:
            if m in self.phonepacklist['vendor'] or m in self.phonepacklist['oem']:
                self.newselectlist.append(m)
        UI_Screen().printf(self.newselectlist)
        os.system('adb root')
        time.sleep(5)
        os.system('adb remount')
        os.chdir(Result_Path)
        defaultvudel=os.popen('adb shell cat /persist/speccfg/spec |grep Default')
        while defaultvudel.read().replace('\n','') =='':
            self.Run_Pack_Swith('Default')
            defaultvudel=os.popen('adb shell cat /persist/speccfg/spec |grep Default')
        UI_Screen().logtxt('perl Excel.pl --QGP_pack "Default" --excelFile "" --QGP_pack_type vendor', '%slog'%'Default')
        i = 0
        while self.newselectlist != []:
            i += 1
            for selectpack in self.newselectlist:
                if self.stopFlag == True:
                    j = 6
                    break
                self.starttime = time.time()
                self.Run_Pack_Swith(selectpack)
                returnpack=os.popen('adb shell cat /persist/speccfg/spec |grep '+selectpack)
                if returnpack.read() !='':
                    self.Run_perl(selectpack)
                    self.newselectlist.remove(selectpack)
                    self.packtime = time.time() - self.starttime
                    UI_Screen().finishtext(selectpack+' Runtime:%s s'%int(self.packtime))
                    self.alltime = self.packtime + self.alltime
                else:
                    UI_Screen().finishtext(' Skip: %s'%selectpack)
            if i >5:
                break
        if os.path.exists('Summary.xls'):
            os.remove('Summary.xls')
        AnalyzeResult.run(Result_Path)
        if self.auexcel != '':
            if os.path.exists('Summary_'+ self.metaexcel+ '_'+ self.auexcel+ '.xls'):
                os.remove('Summary_'+ self.metaexcel+ '_'+ self.auexcel+ '.xls')
                AnalyzeResult.run(Result_Path)
            os.rename('Summary.xls', 'Summary_'+ self.metaexcel+ '_'+ self.auexcel+ '.xls')
        UI_Screen().printf('Analyze Result finished')
        filelist =['Validation_Sheet_V1.0.xlsx', 'Excel.pl']
        for c in filelist:
            if os.path.exists(c):
                os.remove(c)
        UI_Screen().printf('**************************Test Finished*************************')
        UI_Screen().finishtext('Alltime: %s s'%int(self.alltime))
        Runicon.configure(state = NORMAL)
        Downloadicon.configure(state = NORMAL)
        Stoptest.configure(state = NORMAL)
        return self.alltime
    
    def Run_Pack_Swith(self, selectpack):
        UI_Screen().printf('Pack Switch...')
        os.system('adb root')
        time.sleep(5)
        os.system('adb remount')
        os.chdir(scriptpath)
        os.system('adb push Executables\AutoRunner.jar data/local/tmp')
        self.UIpacklist = Pack_Switch.UIpacklist
        if selectpack in self.UIpacklist:
            UI_Screen().logtxt('adb shell uiautomator runtest AutoRunner.jar -c Test.Switch_pack#Switch_package -e package "%s"' %self.UIpacklist[selectpack], '%slog'%selectpack)
        UI_Screen().printf ("Reboot phone please wait.")
        time.sleep(60)
        os.system('adb wait-for-device')
        os.system('adb root')
        time.sleep(5)
        os.system('adb remount')
        os.chdir(Result_Path)
        time.sleep(60)
        
    def Run_perl(self, selectpack):
        if selectpack in self.phonepacklist['vendor']:
            UI_Screen().logtxt('perl Excel.pl --QGP_pack "'+selectpack+'" --excelFile "" --QGP_pack_type %s'%'vendor', '%slog'%selectpack)
        else:
            UI_Screen().logtxt('perl Excel.pl --QGP_pack "'+selectpack+'" --excelFile "" --QGP_pack_type %s'%'oem', '%slog'%selectpack)
     
    def stop(self):
        self.stopFlag=True
        UI_Screen().printf( '\n*******************Test Will Stop*********************\n')
        
class UI_Screen():
    def __init__(self):
        self.Packlist = Packlist.Pack_list()
        
    def UI_Button(self):
        global Runicon, Stoptest, Downloadicon
        Downloadicon = Button(root, text ="Download", height=2, width=10, command = self.Download_build_Display)
        Downloadicon.place(x=550,y=350)
        Runicon = Button(root, text="Run", height=2, width=10, command=self.startruntest)
        Runicon.place(x=650, y=350)
        Stoptest = Button(root, text ="Stop", height=2, width=10, command=self.Stop)
        Stoptest.place(x=750,y=350)
        Stoptest.configure(state = DISABLED)
        View_result_icon = Button(root, text ="View Result", height=2, width=20, command=self.Analyze_result)
        View_result_icon.place(x=850,y=350)
        
    def Analyze_result(self):
        os.system('start "" "%s"'%Result_Path)
        
    def Stop(self):
        self.Thread_test.stop()
        
    def Download_build_Display(self):
        Downflash.Flash_Build(path).UI_Screen()
        
    def OUTPUT(self):
        L1=Label(root, text = 'OUTPUT:').place(x=0, y=400)
        Label(root, text = 1000*'_').place(x=0, y=420)
        self.printf('')
        Label(root, text = 'Status:').place(x=600, y=150)
        self.finishtext(' ')
        
    def printf(self, line):
        OUTPU_TEXT.place(x=0,y=450)
        OUTPU_TEXT.insert(INSERT, "%s\n" %line)
        OUTPU_TEXT.see(END)
        OUTPU_TEXT.update()
        
    def finishtext(self, pack):
        FINISHED_TEXT.place(x=650,y=50)
        FINISHED_TEXT.insert(INSERT, pack+'\n')
        FINISHED_TEXT.update()
        
    def logtxt(self, command="", logname=''):
        adb_pipe = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=1)
        if (command != ""):
            i=0
            f = open(Result_Path+'\\%s.txt'%logname,'a')
            for line in iter(adb_pipe.stdout.readline, ''):
                print line
                self.printf(line)
                f.write(line+'\n')
                i+=1
                if i>=500:
                    OUTPU_TEXT.delete('0.0', index2=END)
                    i = 0
        f.close()
   
    def startruntest(self):
        global scriptpath
        scriptpath = os.getcwd()
        print scriptpath
        AUpath = path['AU']
        print AUpath
        os.chdir(scriptpath)
        filelist =['Validation_Sheet_V1.0.xlsx', 'Excel.pl']
        for c in filelist:
            if c == 'Validation_Sheet_V1.0.xlsx':
                shutil.copy(os.path.join(os.getcwd(),'Config\%s'%c),Result_Path)
            else:
                shutil.copy(os.path.join(os.getcwd(),'Executables\%s'%c),Result_Path)
        Runicon.configure(state = DISABLED)
        Downloadicon.configure(state = DISABLED)
        Stoptest.configure(state = NORMAL)
        getvarlist = UI.Pack_UI(self.bar).Start_one()
        self.Thread_test = RunTest(getvarlist)
        self.Thread_test.start()
        
    def root_tk(self):
        global root, OUTPU_TEXT, FINISHED_TEXT, Result_Path, path
        path = {'META':'', 'AU':'', 'OEM':''}
        root = Tk()
        self.var = IntVar()
        root.title('Data Pack Validation Tool')
        root.geometry('1024x850')
        root.resizable(0, 0)
        iconpath = os.getcwd()
        img = PhotoImage(file='%s\\Executables\\Qualcom.gif'%iconpath)
        root.tk.call('wm', 'iconphoto', root._w, img)
        OUTPU_TEXT = Text(root, width=130, wrap=WORD)
        FINISHED_TEXT = Text(root, width=40, height=15, wrap=WORD)
        Result_Path = Log.logpatch()
        
    def Tool_UI(self):
        self.root_tk()
        self.bar = Menu(root)
        UI.Pack_UI(self.bar).MAKE_PACK_MENU()
        self.UI_Button()
        self.OUTPUT()
        root.config(menu=self.bar)
        root.mainloop()
if __name__ == "__main__":
    a = UI_Screen()
    a.Tool_UI()
