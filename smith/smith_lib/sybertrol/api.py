#!/usr/bin/env python

from scapy.all import *
import smith_protocol.py

#Create hash table for translating commands into packet code
#(apiStr: type, func, subset, offset, readOnly)
general_cmd_map = {'flow rate description': [0, 0, 0, 0, False],
    'volume units description': [0, 0, 1, 0, False],
    'combined id': [0, 0, 2, 0, False],
    'combinated reports start time and date': [0, 0, 3, 0, False],
    'combinated reports end time and date': [0, 0, 4, 0, False],
    'combinated reports print time and date': [0, 0, 5, 0, False],
    'alpha date': [0, 0, 6, 0, True],
    'numeric date': [0, 0, 7, 0, False],
    'time': [0, 0, 8, 0, False], 
    'automatic skid report select 1': [2, 0, 0, 0, False], 
    'reference temperature': [5, 0, 0, 0, False],
    'combinated report offset': [5, 0, 1, 0, False], 
    'mode': [6, 0, 0, 0, False],
    'communications address': [6, 0, 1, 0, False],
    'volume units': [6, 0, 2, 0, False],
    'temperature units': [6, 0, 3, 0, False],
    'density units': [6, 0, 4, 0, False],
    'pressure units': [6, 0, 5, 0, False],
    'mass units': [6, 0, 6, 0, False],
    'flow rate units': [6, 0, 7, 0, False],
    'alarm relay i/o': [6, 0, 8, 0, False],
    'combinated auto print select': [6, 0, 9, 0, False],
    'combinated totals and averages select': [6, 0, 10, 0, False],
    'fiom standalone': [6, 0, 11, 0, False],
    'sybertrol status output': [6, 0, 12, 0, False],
    'fcpb firmware revision': [6, 0, 13, 0, True],
    'fiom firmware revision': [6, 0, 14, 0, True],
    'api rounding': [6, 0, 15, 0, False], 
    'ram alarm': [6, 9, 0, 0, True],
    'rom alarm': [6, 9, 1, 0, True],
    'watchdog error': [6, 9, 2, 0, True],
    'parameters reinitialized to factory default': [6, 9, 3, 0, True],
    'flash error': [6, 9, 4, 0, True],
    'canbus down': [6, 9, 5, 0, True],
    'fiom ram fail': [6, 9, 6, 0, True],
    'fiom rom fail': [6, 9, 7, 0, True],
    'fiom flash fail': [6, 9, 8, 0, True],
    'fiom watchdog': [6, 9, 9, 0, True],
    'parameters not saved on power failure': [6, 9, 10, 0, True],
    'passcodes reset': [6, 9, 11, 0, True],
    'power fail limit': [6, 9, 12, 0, True],
    'fcpb power failure alarm': [6, 9, 13, 0, True],
    'user defined system alarm 1': [6, 9, 14, 0, True],
    'user defined system alarm 2': [6, 9, 15, 0, True],
    'user defined system alarm 3': [6, 9, 16, 0, True],
    'user defined alarm 4': [6, 9, 17, 0, True],
    'user defined alarm 5': [6, 9, 18, 0, True],
    'user defined alarm 6': [6, 9, 19, 0, True],
    'user defined alarm 7': [6, 9, 20, 0, True],
    'user defined alarm 8': [6, 9, 21, 0, True],
    'user defined alarm 9': [6, 9, 22, 0, True],
    'user defined system alarm 10': [6, 9, 23, 0, True],
    'report queue full': [6, 9, 24, 0, True], 
    'communications passcode': [2, 21, 0, 0, False], 
    'sybertrol address': [6, 21, 0, 0, False],
    'prover address': [6, 21, 1, 0, False],
    'request system default report command': [6, 21, 2, 0, False],
    'request system configurable report command': [6, 21, 3, 0, False],
    'update software command': [6, 21, 4, 0, False],
    'set system alarm': [6, 21, 5, 0, False],
    'acknowledge system alarm': [6, 21, 6, 0, False],
    'clear system alarm': [6, 21, 7], 
    'timer 1 reset': [7, 21, 0, 0, False],
    'timer 2 reset': [7, 21, 1, 0, False],
    'timer 3 reset': [7, 21, 2, 0, False],
    'timer 4 reset': [7, 21, 3, 0, False],
    'timer 5 reset': [7, 21, 4, 0, False],
    'timer 6 reset': [7, 21, 5, 0, False],
    'timer 7 reset': [7, 21, 6, 0, False],
    'timer 8 reset': [7, 21, 7, 0, False],
    'timer 9 reset': [7, 21, 8, 0, False],
    'timer 10 reset': [7, 21, 9, 0, False],
    'timer 11 reset': [7, 21, 10, 0, False],
    'timer 12 reset': [7, 21, 11, 0, False],
    'timer 13 reset': [7, 21, 12, 0, False],
    'timer 14 reset': [7, 21, 13, 0, False],
    'timer 15 reset': [7, 21, 14, 0, False],
    'timer 16 reset': [7, 21, 15, 0, False]
}
#SKID DATA (needs offset value)
#all data is RW and offset will be user defined (1 thru 3)
skid_cmd_map = {'skid id': [0, 25, 0],
    'report 1 start time and date': [0, 25, 1],
    'report 2 start time and date': [0, 25, 2],
    'report 1 end time and date': [0, 25, 3],
    'report 2 start time and date': [0, 25, 4],
    'report 1 print time and date': [0, 25, 5],
    'report 2 start time and date': [0, 25, 6],
    'max pulse output frequency': [2, 25, 0],
    'auto skid report select 1': [2, 25, 1],
    'auto skid report select 2': [2, 25, 2],
    'skid report 1 offset': [5, 25, 0],
    'skid report 2 offset': [5, 25, 1],
    'meter numbers': [6, 25, 0],
    'auto print selection 1': [6, 25, 1],
    'auto print selection 2': [6, 25, 2],
    'totals and avgs reset 1': [6, 25, 3],
    'totals and avgs reset 2': [6, 25, 4],
    'flow echo io point': [6, 25, 5],
    'flow echo type select': [6, 25, 6],
    'pulse output digital io point': [6, 25, 7]
}

#METER DATA (needs offset value)
#offset user defined (1 thru 9)
meter_cmd_map = {
    'meter id': [0, 1, 0, False],
    'report 1 start time and date': [0, 1, 1, False],
    'report 1 end time and date': [0, 1, 2, False],
    'report 1 print time and date': [0, 1, 3, False],
    'report 2 start time and date': [0, 1, 4, False],
    'report 2 end time and date': [0, 1, 5, False],
    'report 2 print time and date': [0, 1, 6, False],
    'auto report select 1': [2, 1, 0, False],
    'auto report select 2': [2, 1, 1, False],
    'max pulse output frequency': [2, 1, 2, False],
    'k factor': [5, 1, 0, False],
    'default temperature': [5, 1, 1, False],
    'high temperature alarm': [5, 1, 2, False],
    'low temperature alarm': [5, 1, 3, False],
    'batch min volume': [5, 1, 4, False],
    'batch max volume': [5, 1, 5, False],
    'low flow volume': [5, 1, 6, False],
    'first trip volume': [5, 1, 7, False],
    'final trip volume': [5, 1, 8, False],
    'high flow rate': [5, 1, 9, False],
    'low flow rate': [5, 1, 10, False],
    'minimum flow rate': [5, 1, 11, False],
    'flow control timer': [5, 1, 12, False],
    'high flow alarm rate': [5, 1, 13, False],
    'low flow alarm rate': [5, 1, 14, False],
    'proportional gain': [5, 1, 15, False],
    'integral gain': [5, 1, 16, False],
    'derivative gain': [5, 1, 17, False],
    'back pressure delta pressure': [5, 1, 18, False],
    'back pressure flow rate timer': [5, 1, 19, False],
    'back pressure flow rate reduction': [5, 1, 20, False],
    'back pressure min flow rate': [5, 1, 21, False],
    'back pressure control pressure': [5, 1, 22, False],
    'dual pulse error count': [5, 1, 23, False],
    'dual pulse error reset hours': [5, 1, 24, False],
    'dual pulse error reset minutes': [5, 1, 25, False],
    'dual pulse flow cutoff': [5, 1, 26, False],
    'default density': [5, 1, 27, False],
    'high density alarm': [5, 1, 28, False],
    'low density alarm': [5, 1, 29, False],
    'default pressure': [5, 1, 30, False],
    'high pressure alarm': [5, 1, 31, False],
    'low pressure alarm': [5, 1, 32, False],
    'delta pressure strainer delay': [5, 1, 33, False],
    'sediment and water limit percent': [5, 1, 34, False],
    'sampling volume interval': [5, 1, 35, False],
    'sampling time interval': [5, 1, 36, False],
    'sampling can size': [5, 1, 37, False],
    'sampling can grab': [5, 1, 38, False],
    'sampling alarm count': [5, 1, 39, False],
    'report offset 1': [5, 1, 40, False],
    'report offset 2': [5, 1, 41, False],
    'alarm shutdown': [6, 1, 0, False],
    'pulse multiplier': [6, 1, 1, False],
    'temperature io point': [6, 1, 2, False],
    'batch start': [6, 1, 3, False],
    'batch rotate': [6, 1, 4, False],
    'batch type': [6, 1, 5, False],
    'batch start io point': [6, 1, 6, False],
    'batch stop io point': [6, 1, 7, False],
    'product detect 1 io point': [6, 1, 8, False],
    'product detect 2 io point': [6, 1, 9, False],
    'product detect 3 io point': [6, 1, 10, False],
    'product detect 4 io point': [6, 1, 11, False],
    'end batch io point': [6, 1, 12, False],
    'pump io point': [6, 1, 13, False],
    'flow tolerance': [6, 1, 14, False],
    'back pressure tolerance': [6, 1, 15, False],
    'flow rate type select': [6, 1, 16, False],
    'valve type select': [6, 1, 17, False],
    'flow echo io point': [6, 1, 18, False],
    'flow echo type select': [6, 1, 19, False],
    'analog valve output io point': [6, 1, 20, False],
    'analog valve status io point': [6, 1, 21, False],
    'digital valve upstream io point': [6, 1, 22, False],
    'digital valve downstream io point': [6, 1, 23, False],
    'digital valve status io point': [6, 1, 24, False],
    'two stage valve upstream io point': [6, 1, 25, False],
    'two stage valve downstream io point': [6, 1, 26, False],
    'two stage valve status io point': [6, 1, 27, False],
    'motorized valve open signal io point': [6, 1, 28, False],
    'motorized valve closed signal io point': [6, 1, 29, False],
    'motorized valve status open io point': [6, 1, 30, False],
    'motorized valve status closed io point': [6, 1, 31, False],
    'back pressure control select': [6, 1, 32, False],
    'error reset select': [6, 1, 33, False],
    'ab level security': [6, 1, 34, False],
    'density analog io point': [6, 1, 35, False],
    'density pulse io point': [6, 1, 36, False],
    'share meter temperature': [6, 1, 37, False],
    'density temperature analog io point': [6, 1, 38, False],
    'share meter pressure': [6, 1, 39, False],
    'density pressure analog io point': [6, 1, 40, False],
    'density input type': [6, 1, 41, False],
    'pressure analog io point': [6, 1, 42, False],
    'strainer digital io point': [6, 1, 43, False],
    'sediment and water analog io point': [6, 1, 44, False],
    'sediment and water diverter valve digital io point': [6, 1, 45, False],
    'sediment and water diverter feedback digital io point': [6, 1, 46, False],
    'sampler digital io point': [6, 1, 47, False],
    'sampler interval type': [6, 1, 48, False],
    'sampler full alarm': [6, 1, 49, False],
    'sampler alarm type': [6, 1, 50, False],
    'auto print select 1': [6, 1, 63, False],
    'totals and avgs reset 1': [6, 1, 64, False],
    'detect switch io': [6, 1, 65, False],
    'master meter pulse io': [6, 1, 66, False],
    'auto print select 2': [6, 1, 67, False],
    'totals and avgs reset 2': [6, 1, 68, False],
    'pulse output digital io point': [6, 1, 69, False],
    'detect switch io 2': [6, 1, 70, False],
    'ip paper 2': [6, 1, 71, False],
    'high flow alarm': [6, 10, 0, True],
    'low flow alarm': [6, 10, 1, True],
    'no flow alarm': [6, 10, 2, True],
    'high temperature alarm': [6, 10, 3, True],
    'low temperature alarm': [6, 10, 4, True],
    'high pressure alarm': [6, 10, 5, True],
    'low pressure alarm': [6, 10, 6, True],
    'high density alarm': [6, 10, 7, True],
    'low density alarm': [6, 10, 8, True],
    'high density temperature alarm': [6, 10, 9, True],
    'low density temperature alarm': [6, 10, 10, True],
    'high density pressure alarm': [6, 10, 11, True],
    'low density pressure alarm': [6, 10, 12, True],
    'pulse error alarm': [6, 10, 13, True],
    'sampler full alarm': [6, 10, 14, True],
    'error count alarm': [6, 10, 15, True],
    'bs&w limit alarm': [6, 10, 16, True],
    'delta pressure alarm': [6, 10, 17, True],
    'back pressure alarm': [6, 10, 18, True],
    'diverter valve alarm': [6, 10, 19, True],
    'valve fault alarm': [6, 10, 20, True],
    'pulse transmission alarm': [6, 10, 21, True],
    'meter out of range': [6, 10, 22, True],
    'meter not defined': [6, 10, 23, True],
    'prover not defined': [6, 10, 24, True],
    'no batch': [6, 10, 25, True],
    'resources not available': [6, 10, 26, True],
    'pump failure': [6, 10, 27, True],

    'current flow rate command': [5, 22, 00, False],
    'set meter alarm': [6, 22, 6, False],
    'acknowledge meter alarm': [6, 22, 7, False],
    'clear meter alarm': [6, 22, 8, False],
    'product name': [0, 2, 0, False],
    'api table': [6, 2, 1, False],
    'digital i/o id': [0, 3, 0, False],
    'digital function': [6, 3, 0, False],
    'modify digital output state': [6, 23, 0, False],
    'analog i/o id': [0, 4, 0, False],
    'analog function': [6, 4, 0, False],
    'comm id': [0, 6, 0, False],
    'protocol type': [6, 6, 0, False],
    'comm handshake': [6, 6, 3, False],
    'svp comm port': [6, 7, 21, False],
    'meter temperature': [5, 17, 0, False],
    'meter pressure': [5, 17, 1, False],
    'security level id': [0, 8, 0, False],
    'passcode': [2, 8, 0, False],
    'security i/o point': [6, 8, 0, False],
    'previous level required': [6, 8, 1, False]
}

#Create hash table mapping mode to commands
cmdMode = {'acknowledge': 0,
    'read': 1,
    'write': 2,
    'read several': 3,
    'read security level': 5,
    'write security level': 6,
    'error': 9
}

#Create the packetCode class
class packetCode:
    #initialize packet values
    dType = None
    function = None
    subset = None
    offset = None
    readOnly = False
    command = None
    
    def generatePacket(apiCmd, mode):
        #call translate apiCmd table
        dType, function, subset, offset, readOnly = commandInstr[apiCmd.lower()]

        #call mode table
        command = cmdMode[mode.lower()]
        if (command != 1 or command != 3 or command != 5) and readOnly = True:
            return "This configuration is not possible because this function is read only"

        #generate packet
        #TODO: figure out how to do offset and address
        genPac = Smith(dataType = dType, func = function, sub = subset, off = offset, cmd = command)
        return genPac

    #vim note -> use :%s/, '/,\r'/gc to get nice format
