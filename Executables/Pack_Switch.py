__author__ = 'sunzhen'
import os
import sys
import re
import subprocess
import time
import shutil
import Log

newpath=Log.logpatch()
UIpacklist = {'Default' : 'Default',
'DTGermany' : 'DT-Ge',
'EEEU' : 'EE-EU',
'H3GItalia' :'H3G-It',
'H3GUK' : 'H3G-UK',
'LatamBrazil' : 'LATAM-Br',   
'LatamTelefonica' :'LatamTelefonica',
'Cambodia' : 'OpenMarket-Ca',
'IndonesiaOpenmarket' : 'OpenMarket-In',
'Laos' : 'OpenMarket-La',
'MalaysiaOpenMarket' : 'OpenMarket-Ma',
'PhilippinesOpenMarket' : 'OpenMarket-Ph',
'ThailandOpenMarket' : 'OpenMarket-Th',
'RJIL' : 'RJIL',
'LatamTelefonicaArgentina' :'Telefonica-Ar',
'LatamTelefonicaBrazil' :'Telefonica-Br',
'LatamTelefonicaChile' : 'Telefonica-Ch',
'LatamTelefonicaColombia' : 'Telefonica-Col',
'LatamTelefonicaCostaRica' : 'Telefonica-Cos',
'LatamTelefonicaEcuador' : 'Telefonica-Ecu',
'LatamTelefonicaElSalvador' : 'Telefonica-El',
'LatamTelefonicaGuatemala' : 'Telefonica-Gu',
'LatamTelefonicaMexico' : 'Telefonica-Mex',
'LatamTelefonicaNicaragua' : 'Telefonica-Nic',
'LatamTelefonicaPanama' : 'Telefonica-Pan',
'LatamTelefonicaPeru' : 'Telefonica-Per',
'LatamTelefonicaUruguay' : 'Telefonica-Uru',
'LatamTelefonicaVenezuela' : 'Telefonica-Ven',
'VodafoneCzech' : 'Vodafone-Cze',
'VodafoneES' : 'Vodafone-ES',
'VodafoneGermany' : 'Vodafone-Ger',
'VodafoneGreece' : 'Vodafone-Gre',
'VodafoneHungary' : 'Vodafone-Hun',
'VodafoneIT' : 'Vodafone-IT',
'VodafoneIreland' : 'Vodafone-Ire',
'VodafoneNetherlands' : 'Vodafone-Nethe',
'VodafonePT' : 'Vodafone-PT',
'VodafoneSouthAfrica' : 'Vodafone-SouthA',
'VodafoneTurkey' : 'Vodafone-Tur',
'VodafoneUK' : 'Vodafone-UK',
'VodafoneGroup': 'VodafoneGroup',
'Cherry' : 'Cherry',
'CherryCambodia' : 'Cherry-Cam',
'CherryLaos' : 'Cherry-Lao',
'CherryMyanmar' : 'Cherry-Mya',
'CherryPhilippines' : 'Cherry-Phi',
'CherryThailand' : 'Cherry-Tha',
'OrangeBelgium' : 'Orange-Bel',
'OrangeFrance' : 'Orange-F',
'OrangeMoldavia' : 'Orange-Mol',
'OrangePoland' : 'Orange-Po',
'OrangeRomania' : 'Orange-Rom',
'OrangeSlovakia' : 'Orange-Slo',
'OrangeSpain' : 'Orange-Spa',
'TelecomItaliaMobile' : 'Telecom-Ita',
'VietnamOpenMarket' : 'OpenMarket-Vie',
'TelefonicaGermany' : 'Telefonica-Ger',
'TelefonicaSpain' : 'Telefonica-Spa',
'TelefonicaColombia' : 'Telefonica-Col',
'IndiaCommon':'IndiaCommon-Ind',
'LanixClaroColombia':'LanixClaroColombia',
'LatamClaroBrazil':'Claro-Bra',
'LatamClaroChile':'Claro-Chi',
'LatamClaroColombia':'Claro-Col',
'LatamClaroPeru':'Claro-Pe',
'LatamAMX':'LatamAMX',
'LatamTelcelMexico' : 'Telcel-Mex',
'LanixTelcelMexico':'LanixTelcelMexico'}
 
def run(args):
    os.system('adb root')
    print "Root phone"
    time.sleep(5)
    os.system('adb remount')
    print "Remount phone"
    if args in UIpacklist:
        print UIpacklist[args]
        os.system('adb shell uiautomator runtest AutoRunner.jar -c Test.Switch_pack#Switch_package -e package "%s"'%UIpacklist[args])
    print "Reboot phone please wait."

def check_oem(args):
    List=[]
    lines = os.popen('adb shell ls /system/vendor').readlines()
    for line in lines:
        print line.strip()
        name = line.split(' ').pop().strip('\r\n')
        List.append(name)
    #print List
    if ('%s'%args) in List:
        print "----------No need to load /oem to /system/vendor------------"
    else:
        print "--------------pack is not in /system/vendor currently, need to load /oem-------------------"
        os.system('adb shell cp -r /oem/* /system/vendor')
        time.sleep(10)
        

def exe_command(adb_pipe, command=""):
    ret_val = ""
    if ( command != "" ):
        adb_pipe.stdin.write(command)
        adb_pipe.stdin.flush()
        adb_pipe.stdout.readline()
    ch = adb_pipe.stdout.readline(1)
    one_line = ''
    f = open(newpath+'\log.txt','a')
    while ( re.match(r'^[$#]', ch, re.M|re.I) == None ):
        if ( ch != '\r'): one_line = one_line + ch #\n is for newline
        if ( ch == '\n' ):
            ret_val = ret_val + one_line
#            printf(one_line)
            f.write(one_line+'\n')
            print one_line
            one_line = ""
        ch = adb_pipe.stdout.readline(1)
    f.close()
    return one_line

def exe_display(command=""):
    adb_pipe = Popen(command, stdin=PIPE, stdout=PIPE, bufsize=1)
    if ( command != "" ):
        for line in iter(adb_pipe.stdout.readline, ''):
            print line
            
#run(sys.argv[1])
