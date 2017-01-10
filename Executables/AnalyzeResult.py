#-*- encoding:UTF-8 -*-

import os
import re
import xlrd
import xlwt
import xlutils.copy
import sys


typelist={'Default':'Default', 
	'DTGermany':'EU',
	'H3GItalia':'EU',
	'H3GUK':'EU',
	'EEEU':'EU',
	'TelecomItaliaMobile':'EU',
	'Laos':'OM',
	'LatamBrazil':'OM',
	'IndonesiaOpenmarket':'OM',
	'MalaysiaOpenMarket':'OM',
	'PhilippinesOpenMarket':'OM',
	'RJIL':'OM',
	'ThailandOpenMarket':'OM',
	'Cherry':'OM',
	'CherryCambodia':'OM',
	'CherryLaos':'OM',
	'CherryMyanmar':'OM',
	'CherryPhilippines':'OM',
	'CherryThailand':'OM',
	'Cambodia':'OM',
	'VietnamOpenMarket':'OM',
    'IndiaCommon':'OM',
	'LanixTelcelMexico':'AMX',
	'LatamTelcelMexico':'AMX',
	'LanixClaroColombia':'AMX',
	'LatamAMX':'AMX',
	'LatamClaroBrazil':'AMX',
	'LatamClaroChile':'AMX',
	'LatamClaroColombia':'AMX',
	'LatamClaroPeru':'AMX',
	'TMO':'TMO',
	'MPCS':'TMO',
	'OrangeBelgium':'ORN',
	'OrangeFrance':'ORN',
	'OrangeMoldavia':'ORN', 
	'OrangePoland':'ORN', 
	'OrangeRomania':'ORN', 
	'OrangeSlovakia':'ORN', 
	'OrangeSpain':'ORN',
	'VodafoneCzech':'VDF', 
	'VodafoneES':'VDF', 
	'VodafoneGermany':'VDF', 
	'VodafoneGreece':'VDF', 
	'VodafoneGroup':'VDF', 
	'VodafoneHungary':'VDF', 
	'VodafoneIT':'VDF', 
	'VodafoneIreland':'VDF', 
	'VodafoneNetherlands':'VDF', 
	'VodafonePT':'VDF', 
	'VodafoneSouthAfrica':'VDF', 
	'VodafoneTurkey':'VDF', 
	'VodafoneUK':'VDF',
	'TelefonicaColombia':'TEF', 
	'TelefonicaGermany':'TEF', 
	'TelefonicaSpain':'TEF',
	'LatamTelefonica':'TEF', 
	'LatamTelefonicaArgentina':'TEF', 
	'LatamTelefonicaBrazil':'TEF', 
	'LatamTelefonicaChile':'TEF', 
	'LatamTelefonicaColombia':'TEF', 
	'LatamTelefonicaCostaRica':'TEF', 
	'LatamTelefonicaEcuador':'TEF', 
	'LatamTelefonicaElSalvador':'TEF', 
	'LatamTelefonicaGuatemala':'TEF', 
	'LatamTelefonicaMexico':'TEF', 
	'LatamTelefonicaNicaragua':'TEF', 
	'LatamTelefonicaPanama':'TEF', 
	'LatamTelefonicaPeru':'TEF', 
	'LatamTelefonicaUruguay':'TEF', 
	'LatamTelefonicaVenezuela':'TEF',
	}
	

def copy_excel_data(file_name,new_file):
    # copy all test result to summary.xls
    file = xlrd.open_workbook(file_name)
    sheet1 = new_file.add_sheet(file_name[:-4], cell_overwrite_ok=True)
    table = file.sheets()[0]
    nrows = table.nrows
    for i in range(nrows):
        for n in range(6):
            sheet1.write(i, n, table.row_values(i)[n], type_list(1))
            sheet1.col(0).width = 256 * 5
            sheet1.col(1).width = 256 * 40
            sheet1.col(2).width = 256 * 90
            sheet1.col(3).width = 256 * 90
            sheet1.col(4).width = 256 * 10
            sheet1.col(5).width = 256 * 25
            if (table.row_values(i)[4] == 'Failed'):
                sheet1.write(i, n, table.row_values(i)[n], type_list(6))
    print 'copy excel'

def get_summary_data(file_name, m, summary_sheet):
    # copy all fail test case to summary sheet
    file = xlrd.open_workbook(file_name)
    table = file.sheets()[0]
    nrows = table.nrows
    package_name = file_name[:-4]
    # Add hyperlink
    n = "HYPERLINK"
    summary_sheet.write(m, 2, xlwt.Formula(n + '("#'+package_name+'! A1";"'+package_name+'")'), type_list(3))
    summary_sheet.write(m, 1, typelist[package_name],type_list(1))
    summary_sheet.write(m, 0, m, type_list(5))
    a = 3
    for i in range(nrows):
        if (table.row_values(i)[4] == 'Failed'):
            a += 1
    summary_sheet.write(m, 3, str(nrows - a + 2) + '/' + str(nrows - 1),type_list(2))
    print 'summary data'

def summary_default():
    # create and initialize 'summary.xls'
    new_file = xlwt.Workbook(style_compression=2)
    sheet1 = new_file.add_sheet('Summary', cell_overwrite_ok=True)

    sheet1.col(0).width = 256 * 10
    sheet1.col(1).width = 256 * 10
    sheet1.col(2).width = 256 * 30
    sheet1.col(3).width = 256 * 10

    tall_style = xlwt.easyxf('font:height 1000;')
    sheet1.row(0).set_style(tall_style)

    sheet1.write(0, 0, "No.", type_list(4))
    sheet1.write(0, 1, "Region", type_list(4))
    sheet1.write(0, 2, "Package", type_list(4))
    sheet1.write(0, 3, "Pass Rate", type_list(4))
    return sheet1,new_file

def get_result_file(path):
    # get all test result, return list
    file_list = []
    for parent,dirnames,filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith(".xls"):
                file_list.append(filename)
    return file_list

def change_pattern(style,pattern_fore_colour):
    # change pattern style
    pattern = xlwt.Pattern()
    pattern.pattern =pattern.SOLID_PATTERN
    pattern.pattern_fore_colour =pattern_fore_colour
    style.pattern = pattern
    return style

def change_fone(style,colour_index,bold,name,underline):
    # change fone style
    font = xlwt.Font()
    font.colour_index = colour_index
    font.bold = bold
    font.name = name
    font.underline = underline #xlwt.Font.UNDERLINE_SINGLE
    style.font = font
    return style

def change_alignment(style,horz,vert):
    # change alignment style
    alignment = xlwt.Alignment()
    alignment.horz = horz #xlwt.Alignment.HORZ_CENTER
    alignment.vert = vert #xlwt.Alignment.VERT_CENTER
    style.alignment = alignment
    return style

def change_borders(style,bottom_colour):
    # change borders style
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    borders.bottom_colour = bottom_colour #0x3A
    style.borders = borders
    return style

def create_style():
    style = xlwt.XFStyle()
    return style

def type_list(num):
    # type1: Add black border around the cell
    if num ==1:
        return change_borders(create_style(), 0x3A)


    # type2: Add black border around the cell, white background colour,red fone,no underline
    elif num ==2:
        return change_fone(change_pattern(change_borders(create_style(), 0x3A), 0x2A), 0, True, 'Arial',
                        xlwt.Font.UNDERLINE_NONE)
    # type3: Add black border around the cell,white background colour, blue fone,single underline
    elif num ==3:
        return change_fone(change_borders(create_style(), 0x3A), 4, False, 'Arial', xlwt.Font.UNDERLINE_SINGLE)

    # type4: Add black border around the cell, bule background colour, white fone.
    elif num == 4:
        return change_alignment(change_fone(change_pattern(change_borders(create_style(), 0x3A), 0x36),1, True, 'Arial',
                        xlwt.Font.UNDERLINE_NONE),xlwt.Alignment.HORZ_LEFT,xlwt.Alignment.VERT_CENTER)

    # type5:Add black border around the cell,center in horz and vert
    elif num == 5:
        return change_alignment(change_borders(create_style(), 0x3A),
                                               xlwt.Alignment.HORZ_CENTER, xlwt.Alignment.VERT_CENTER)

    #
    elif num ==6:
        return change_pattern(change_fone(change_borders(create_style(), 0x3A),1, True, 'Arial',xlwt.Font.UNDERLINE_NONE),0x10)

    else:
        print "No type to choose."

def run(path):
    file_list =get_result_file(path)
    (summary_sheet,new_file) = summary_default()
    num = 1
    for file_name in file_list:
        print file_name
        get_summary_data(file_name,num,summary_sheet)
        num +=1
        copy_excel_data(file_name, new_file)
    new_file.save(os.path.join(path,'Summary.xls'))

#run(path) 
#run(os.getcwd())
