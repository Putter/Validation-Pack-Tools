#-*- encoding:UTF-8 -*-
import os
from Tkinter import *
import Packlist

class Pack_UI():
    def __init__(self, menubar):
        self.Packlist = Packlist.Pack_list()
        self.menubar = menubar
        self.PACK_MENU_BUTTON = Menu(menubar, tearoff=0)
        self.PACK_MENU_BUTTON.add_checkbutton(label="SELECT ALL", command=self.select_all)
        self.PACK_MENU_BUTTON.VDF = Menu(self.PACK_MENU_BUTTON)
        self.PACK_MENU_BUTTON.TEF = Menu(self.PACK_MENU_BUTTON)
        self.PACK_MENU_BUTTON.EU = Menu(self.PACK_MENU_BUTTON)
        self.PACK_MENU_BUTTON.OM = Menu(self.PACK_MENU_BUTTON)
        self.PACK_MENU_BUTTON.AMX = Menu(self.PACK_MENU_BUTTON)
        self.PACK_MENU_BUTTON.ORN = Menu(self.PACK_MENU_BUTTON)
        self.PACK_MENU_BUTTON.TMO = Menu(self.PACK_MENU_BUTTON)
    def MAKE_PACK_MENU(self):
        for pac in self.Packlist.alllist['vendor']:
            if pac in self.Packlist.alllist['oem1']:
                self.Packlist.alllist['oem1'].remove(pac)
            elif pac in self.Packlist.alllist['ome2']:
                self.Packlist.alllist['ome2'].remove(pac)
            elif pac in self.Packlist.alllist['ome3']:
                self.Packlist.alllist['ome3'].remove(pac)
            elif pac in self.Packlist.alllist['ome4']:
                self.Packlist.alllist['ome4'].remove(pac)
            if pac in self.Packlist.typelist['VDF']:
                self.PACK_MENU_BUTTON.VDF.add_checkbutton(label=pac+'(vendor)',command = self.Start_one)
            elif pac in self.Packlist.typelist['TEF']:
                self.PACK_MENU_BUTTON.TEF.add_checkbutton(label=pac+'(vendor)',command = self.Start_one)
            elif pac in self.Packlist.typelist['EU']:
                self.PACK_MENU_BUTTON.EU.add_checkbutton(label=pac+'(vendor)',command = self.Start_one)
            elif pac in self.Packlist.typelist['OM']:
                self.PACK_MENU_BUTTON.OM.add_checkbutton(label=pac+'(vendor)',command = self.Start_one)
            elif pac in self.Packlist.typelist['AMX']:
                self.PACK_MENU_BUTTON.AMX.add_checkbutton(label=pac+'(vendor)',command = self.Start_one)
        for pack in self.Packlist.alllist['oem1']:
            if pack in self.Packlist.typelist['TMO']:
                self.PACK_MENU_BUTTON.TMO.add_checkbutton(label=pack+'(oem1)',command = self.Start_one)
        for pack in self.Packlist.alllist['ome2']:
            if pack in self.Packlist.typelist['AMX']:
                self.PACK_MENU_BUTTON.AMX.add_checkbutton(label=pack+'(ome2)',command = self.Start_one)
        for pack in self.Packlist.alllist['ome3']:
            if pack in self.Packlist.typelist['AMX']:
                self.PACK_MENU_BUTTON.AMX.add_checkbutton(label=pack+'(ome3)',command = self.Start_one)
        for pack in self.Packlist.alllist['ome4']:
            if pack in self.Packlist.typelist['AMX']:
                self.PACK_MENU_BUTTON.AMX.add_checkbutton(label=pack+'(ome4)',command = self.Start_one)
            elif pack in self.Packlist.typelist['EU']:
                self.PACK_MENU_BUTTON.EU.add_checkbutton(label=pack+'(ome4)',command = self.Start_one)
            elif pack in self.Packlist.typelist['OM']:
                self.PACK_MENU_BUTTON.OM.add_checkbutton(label=pack+'(ome4)',command = self.Start_one)
            elif pack in self.Packlist.typelist['ORN']:
                self.PACK_MENU_BUTTON.ORN.add_checkbutton(label=pack+'(ome4)',command = self.Start_one)
        self.PACK_MENU_BUTTON.add_cascade(label='EU',menu=self.PACK_MENU_BUTTON.EU)
        self.PACK_MENU_BUTTON.add_cascade(label='OM',menu=self.PACK_MENU_BUTTON.OM)
        self.PACK_MENU_BUTTON.add_cascade(label='AMX',menu=self.PACK_MENU_BUTTON.AMX)
        self.PACK_MENU_BUTTON.add_cascade(label='ORN',menu=self.PACK_MENU_BUTTON.ORN)
        self.PACK_MENU_BUTTON.add_cascade(label='VDF',menu=self.PACK_MENU_BUTTON.VDF)
        self.PACK_MENU_BUTTON.add_cascade(label='TEF',menu=self.PACK_MENU_BUTTON.TEF)
        self.PACK_MENU_BUTTON.add_cascade(label='TMO',menu=self.PACK_MENU_BUTTON.TMO)
        self.menubar.add_cascade(label="Pack", menu=self.PACK_MENU_BUTTON)

    def select_all(self):
        for pac in self.Packlist.alllist['vendor']:
            if pac in self.Packlist.typelist['VDF']:
                self.PACK_MENU_BUTTON.VDF.invoke(self.PACK_MENU_BUTTON.VDF.index(pac+'(vendor)'))
            elif pac in self.Packlist.typelist['TEF']:
                self.PACK_MENU_BUTTON.TEF.invoke(self.PACK_MENU_BUTTON.TEF.index(pac+'(vendor)'))
            elif pac in self.Packlist.typelist['EU']:
                self.PACK_MENU_BUTTON.EU.invoke(self.PACK_MENU_BUTTON.EU.index(pac+'(vendor)'))
            elif pac in self.Packlist.typelist['OM']:
                self.PACK_MENU_BUTTON.OM.invoke(self.PACK_MENU_BUTTON.OM.index(pac+'(vendor)'))
            elif pac in self.Packlist.typelist['AMX']:
                self.PACK_MENU_BUTTON.AMX.invoke(self.PACK_MENU_BUTTON.AMX.index(pac+'(vendor)'))
        for pack in self.Packlist.alllist['oem1']:
            self.PACK_MENU_BUTTON.TMO.invoke(self.PACK_MENU_BUTTON.TMO.index(pack + '(oem1)'))
        for pa in self.Packlist.alllist['ome2']:
            self.PACK_MENU_BUTTON.AMX.invoke(self.PACK_MENU_BUTTON.AMX.index(pa + '(ome2)'))
        for p in self.Packlist.alllist['ome3']:
            self.PACK_MENU_BUTTON.AMX.invoke(self.PACK_MENU_BUTTON.AMX.index(p + '(ome3)'))
        for pack4 in self.Packlist.alllist['ome4']:
            if pack4 in self.Packlist.typelist['EU']:
                self.PACK_MENU_BUTTON.EU.invoke(self.PACK_MENU_BUTTON.EU.index(pack4 + '(ome4)'))
            elif pack4 in self.Packlist.typelist['OM']:
                self.PACK_MENU_BUTTON.OM.invoke(self.PACK_MENU_BUTTON.OM.index(pack4 + '(ome4)'))
            elif pack4 in self.Packlist.typelist['ORN']:
                self.PACK_MENU_BUTTON.ORN.invoke(self.PACK_MENU_BUTTON.ORN.index(pack4 + '(ome4)'))
                
    def Start_one(self):
        getvarlist = []
        for pac in self.Packlist.alllist['vendor']:
            if pac in self.Packlist.typelist['VDF']:
                if self.PACK_MENU_BUTTON.VDF.getvar(pac+'(vendor)') == "1":
                    getvarlist.append(pac)
                else:
                    if pac in getvarlist:
                        getvarlist.remove(pac)
            elif pac in self.Packlist.typelist['TEF']:
                if self.PACK_MENU_BUTTON.TEF.getvar(pac+'(vendor)') == "1":
                    getvarlist.append(pac)
                else:
                    if pac in getvarlist:
                        getvarlist.remove(pac)
            elif pac in self.Packlist.typelist['EU']:
                if self.PACK_MENU_BUTTON.EU.getvar(pac+'(vendor)') == "1":
                    getvarlist.append(pac)
                else:
                    if pac in getvarlist:
                        getvarlist.remove(pac)
            elif pac in self.Packlist.typelist['OM']:
                if self.PACK_MENU_BUTTON.OM.getvar(pac+'(vendor)') == "1":
                    getvarlist.append(pac)
                else:
                    if pac in getvarlist:
                        getvarlist.remove(pac)                      
            elif pac in self.Packlist.typelist['AMX']:
                print pac
                if self.PACK_MENU_BUTTON.AMX.getvar(pac + '(vendor)') == "1":
                    getvarlist.append(pac)
                else:
                    if pac in getvarlist:
                        getvarlist.remove(pac)
        for pack in self.Packlist.alllist['oem1']:
            if pack in self.Packlist.typelist['TMO']:
                if pack in self.Packlist.alllist['oem1']:
                    if self.PACK_MENU_BUTTON.TMO.getvar(pack + '(oem1)') == "1":
                        getvarlist.append(pack)
                    else:
                        if pack in getvarlist:
                            getvarlist.remove(pack)
        for pa in self.Packlist.alllist['ome2']:
            if pa in self.Packlist.typelist['AMX']:
                if self.PACK_MENU_BUTTON.AMX.getvar(pa + '(ome2)') == "1":
                    getvarlist.append(pa)
                else:
                    if pa in getvarlist:
                        getvarlist.remove(pa)
        for p in self.Packlist.alllist['ome3']:
            if p in self.Packlist.typelist['AMX']:
                if self.PACK_MENU_BUTTON.AMX.getvar(p + '(ome3)') == "1":
                    getvarlist.append(p)
                else:
                    if p in getvarlist:
                        getvarlist.remove(p)
        for pack4 in self.Packlist.alllist['ome4']:
            if pack4 in self.Packlist.typelist['EU']:
                if self.PACK_MENU_BUTTON.EU.getvar(pack4 + '(ome4)') == "1":
                    getvarlist.append(pack4)
                else:
                    if pack4 in getvarlist:
                        getvarlist.remove(pack4)
            elif pack4 in self.Packlist.typelist['OM']:
                if self.PACK_MENU_BUTTON.OM.getvar(pack4 + '(ome4)') == "1":
                    getvarlist.append(pack4)
                else:
                    if pack4 in getvarlist:
                        getvarlist.remove(pack4)
            elif pack4 in self.Packlist.typelist['ORN']:
                if self.PACK_MENU_BUTTON.ORN.getvar(pack4 + '(ome4)') == "1":
                    getvarlist.append(pack4)
                else:
                    if pack4 in getvarlist:
                        getvarlist.remove(pack4)
        getvarlist = list(set(getvarlist))
        getvarlist.sort()
        return getvarlist
