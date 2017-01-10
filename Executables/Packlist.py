
class Pack_list():
    def __init__(self):
        self.alllist ={'vendor':['Cambodia', 'DTGermany', 'EEEU', 'H3GItalia', 'H3GUK', 'IndonesiaOpenmarket', 'Laos', 'LatamBrazil',
                                     'LatamTelefonica', 'LatamTelefonicaArgentina', 'LatamTelefonicaBrazil', 'LatamTelefonicaChile', 'LatamTelefonicaColombia', 'LatamTelefonicaCostaRica', 
                                     'LatamTelefonicaEcuador', 'LatamTelefonicaElSalvador', 'LatamTelefonicaGuatemala', 'LatamTelefonicaMexico', 'LatamTelefonicaNicaragua', 'LatamTelefonicaPanama', 
                                     'LatamTelefonicaPeru', 'LatamTelefonicaUruguay', 'LatamTelefonicaVenezuela', 'MalaysiaOpenMarket', 'NorthAmerica', 'PhilippinesOpenMarket', 'RJIL', 'TelefonicaColombia', 
                                     'TelefonicaGermany', 'TelefonicaSpain', 'ThailandOpenMarket', 'VodafoneCzech', 'VodafoneES', 'VodafoneGermany', 'VodafoneGreece', 'VodafoneGroup', 'VodafoneHungary', 
                                     'VodafoneIT', 'VodafoneIreland', 'VodafoneNetherlands', 'VodafonePT', 'VodafoneSouthAfrica', 'VodafoneTurkey', 'VodafoneUK'],
                            'oem1': ['TMO','MPCS'] ,
                            'ome2' : ['LatamAMX', 'LanixTelcelMexico', 'LatamTelcelMexico'],
                            'ome3':['LatamClaroBrazil', 'LatamClaroChile', 'LatamClaroColombia', 'LatamClaroPeru', 'LanixClaroColombia'],
                            'ome4': ['IndiaCommon', 'TelecomItaliaMobile','OrangeBelgium', 'OrangeFrance', 'OrangeMoldavia', 'OrangePoland', 'OrangeRomania', 'OrangeSlovakia', 'OrangeSpain','Cherry',
                                     'CherryCambodia', 'CherryLaos', 'CherryMyanmar', 'CherryPhilippines', 'CherryThailand','VietnamOpenMarket']}
        self.allpacklist={}
        self.typelist={'EU':['DTGermany','H3GItalia', 'H3GUK','EEEU','TelecomItaliaMobile'],
           'OM':['IndiaCommon', 'Laos', 'LatamBrazil', 'IndonesiaOpenmarket', 'MalaysiaOpenMarket', 'PhilippinesOpenMarket', 'RJIL', 'ThailandOpenMarket','Cherry','CherryCambodia', 'CherryLaos', 'CherryMyanmar', 'CherryPhilippines', 'CherryThailand', 'Cambodia','VietnamOpenMarket'],
           'AMX':['LanixTelcelMexico', 'LatamTelcelMexico','LanixClaroColombia', 'LatamAMX', 'LatamClaroBrazil', 'LatamClaroChile', 'LatamClaroColombia', 'LatamClaroPeru'],
           'TMO':['TMO','MPCS'],
           'ORN':['OrangeBelgium', 'OrangeFrance', 'OrangeMoldavia', 'OrangePoland', 'OrangeRomania', 'OrangeSlovakia', 'OrangeSpain'],
           'VDF':['VodafoneCzech', 'VodafoneES', 'VodafoneGermany', 'VodafoneGreece', 'VodafoneGroup', 'VodafoneHungary', 'VodafoneIT', 'VodafoneIreland', 'VodafoneNetherlands', 'VodafonePT', 'VodafoneSouthAfrica', 'VodafoneTurkey', 'VodafoneUK'],
           'TEF':['TelefonicaColombia', 'TelefonicaGermany', 'TelefonicaSpain','LatamTelefonica', 'LatamTelefonicaArgentina', 'LatamTelefonicaBrazil', 'LatamTelefonicaChile', 'LatamTelefonicaColombia', 'LatamTelefonicaCostaRica', 'LatamTelefonicaEcuador', 
                  'LatamTelefonicaElSalvador', 'LatamTelefonicaGuatemala', 'LatamTelefonicaMexico', 'LatamTelefonicaNicaragua', 'LatamTelefonicaPanama', 'LatamTelefonicaPeru', 'LatamTelefonicaUruguay', 'LatamTelefonicaVenezuela']
           }