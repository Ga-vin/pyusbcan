#!/bin/python env
#-*- coding: gb18030 -*-

import ctypes
import os
import sys
import time

## =============================================================================
## Device type list
## =============================================================================
VCI_PCI5121     = 0x01
VCI_PCI9810     = 0x02
VCI_USBCAN1     = 0x03
VCI_USBCAN2     = 0x04
VCI_USBCAN2A    = 0x04
VCI_PCI9820     = 0x05
VCI_CAN232      = 0x06
VCI_PCI5110     = 0x07
VCI_CANLITE     = 0x08
VCI_ISA9620     = 0x09
VCI_ISA5420     = 0x0A
VCI_PC104CAN    = 0x0B
VCI_CANETUDP    = 0x0C
VCI_CANETE      = 0x0C
VCI_DNP9810     = 0x0D
VCI_PCI9840     = 0x0E
VCI_PC104CAN2   = 0x0F
VCI_PCI9820I    = 0x10
VCI_CANETTCP    = 0x11
VCI_PEC9920     = 0x12
VCI_PCIE_9220   = 0x12
VCI_PCI5010U    = 0x13
VCI_USBCAN_E_U  = 0x14
VCI_USBCAN_2E_U = 0x15
VCI_PCI5020U    = 0x16
VCI_EG20T_CAN   = 0x17
VCI_PCIE9221    = 0x18
VCI_WIFICAN_TCP = 0x19
VCI_WIFICAN_UDP = 0x1A
VCI_PCIe9120    = 0x1B
VCI_PCIe9110    = 0x1C
VCI_PCIe9140    = 0x1D
VCI_USBCAN_4E_U = 0x1F

CAN_DEVICE_TYPE_LIST = [VCI_PCI5121, VCI_PCI9810, VCI_USBCAN1, VCI_USBCAN2,\
                        VCI_USBCAN2A, VCI_PCI9820, VCI_CAN232, VCI_PCI5110,\
                        VCI_CANLITE, VCI_ISA9620, VCI_ISA5420, VCI_PC104CAN,\
                        VCI_CANETUDP, VCI_CANETE, VCI_DNP9810, VCI_PCI9840,\
                        VCI_PC104CAN2, VCI_PCI9820I, VCI_CANETTCP, VCI_PEC9920,\
                        VCI_PCIE_9220, VCI_PCI5010U, VCI_USBCAN_E_U, VCI_USBCAN_2E_U,\
                        VCI_PCI5020U, VCI_EG20T_CAN, VCI_PCIE9221, VCI_WIFICAN_TCP,\
                        VCI_WIFICAN_UDP, VCI_PCIe9120, VCI_PCIe9110, VCI_PCIe9140,\
                        VCI_USBCAN_4E_U]

CAN_DEVICE_DLL_DICT = {
    VCI_PCI5121     : 'PCI51XXE.dll',
    VCI_PCI9810     : 'PCI9810B.dll',
    VCI_USBCAN1     : 'usbcan.dll',
    VCI_USBCAN2     : 'usbcan.dll',
    VCI_PCI9820     : 'PCI9820B.dll',
    VCI_CAN232      : 'CAN232.dll',
    VCI_PCI5110     : 'PCI51XXE.dll',
    VCI_CANLITE     : 'CANLite.dll',
    VCI_ISA9620     : 'ISA9620B.dll',
    VCI_ISA5420     : 'isa5420.dll',
    VCI_PC104CAN    : 'PC104CAN.dll',
    VCI_CANETUDP    : 'CANETE.dll',
    VCI_DNP9810     : 'DNP9810B.dll',
    VCI_PCI9840     : 'PCI9840B.dll',
    VCI_PC104CAN2   : 'PC104C2.dll',
    VCI_PCI9820I    : 'PCI9820I.dll',
    VCI_CANETTCP    : 'CANET_TCP.dll',
    VCI_PEC9920     : 'pec9920.dll',
    VCI_PCI5010U    : 'pci50xx_u.dll',
    VCI_USBCAN_E_U  : 'USBCAN_E.dll',
    VCI_USBCAN_2E_U : 'USBCAN_E.dll',
    VCI_PCI5020U    : 'pci50xx_u.dll',
    VCI_EG20T_CAN   : 'topcliff_can.dll',
    VCI_PCIE9221    : 'pcie9221.dll',
    VCI_WIFICAN_TCP : 'CANWIFI_TCP.dll',
    VCI_WIFICAN_UDP : 'CANWIFI_UDP.dll',
    VCI_PCIe9120    : 'pcie9120.dll',
    VCI_PCIe9110    : 'pcie9140.dll',
    VCI_PCIe9140    : 'pcie5010p.dll',
    VCI_USBCAN_4E_U : 'USBCAN_4E_U.dll'
}

## =============================================================================
## CAN error code
## =============================================================================
ERR_CAN_OVERFLOW        = 0x0001  ## CAN控制器内部FIFO溢出
ERR_CAN_ERRALARM        = 0x0002  ## CAN控制器错误报警
ERR_CAN_PASSIVE         = 0x0004  ## CAN控制器消极错误
ERR_CAN_LOSE            = 0x0008  ## CAN控制器仲裁丢失
ERR_CAN_BUSERR          = 0x0010  ## CAN控制器总线错误
ERR_CAN_BUSOFF          = 0x0020  ## 总线关闭错误
ERR_CAN_BUFFER_OVERFLOW = 0x0040  ## CAN控制器内部BUFFER溢出

## =============================================================================
## Gerenally error code
## =============================================================================
ERR_DEVICE_OPENED       = 0x0100  ## 设备已经打开
ERR_DEVICE_OPEN         = 0x0200  ## 打开设备错误
ERR_DEVICE_NOT_OPEN     = 0x0400  ## 设备没有打开
ERR_BUFFER_OVERFLOW     = 0x0800  ## 缓冲区溢出
ERR_DEVICE_NOT_EXIST    = 0x1000  ## 此设备不存在
ERR_LOAD_KERNEL_DLL     = 0x2000  ## 装载动态库失败
ERR_CMD_FAILED          = 0x4000  ## 执行命令失败错误码
ERR_BUFFER_CREATE       = 0x8000  ## 内存不足

## =============================================================================
## System Call status
## =============================================================================
STATUS_OK               = 0x1
STATUS_ERR              = 0x0

CMD_DESIP               = 0x0
CMD_DESPORT             = 0x1
CMD_CHGDESIPANDDPORT    = 0x2
CMD_SRCPORT             = 0x2
CMD_TCP_TYPE            = 0x4     ## tcp 工作方式，服务器:1 或是客户端:0
CMD_CLIENT_COUNT        = 0x5     ## 连接上的客户端计数
CMD_CLIENT              = 0x6     ## 连接上的客户端
CMD_DISCONN_CLIENT      = 0x7     ## 断开一个连接
CMD_SET_RECONNECT_TIME  = 0x8     ## 使能自动重连

TCP_CLIENT              = 0x0
TCP_SERVER              = 0x1

## =============================================================================
## USBCAN-4E-U设备的波特率
## =============================================================================
USBCAN_4E_BAUD_5Kbps    = 5000
USBCAN_4E_BAUD_10Kbps   = 10000
USBCAN_4E_BAUD_20Kbps   = 20000
USBCAN_4E_BAUD_50Kbps   = 50000
USBCAN_4E_BAUD_100Kbps  = 100000
USBCAN_4E_BAUD_125Kbps  = 125000
USBCAN_4E_BAUD_250Kbps  = 250000
USBCAN_4E_BAUD_500Kbps  = 500000
USBCAN_4E_BAUD_800Kbps  = 800000
USBCAN_4E_BAUD_1000Kbps = 1000000

USBCAN_4E_BAUD_LIST     = [USBCAN_4E_BAUD_5Kbps, USBCAN_4E_BAUD_10Kbps,\
                           USBCAN_4E_BAUD_20Kbps, USBCAN_4E_BAUD_50Kbps,\
                           USBCAN_4E_BAUD_100Kbps, USBCAN_4E_BAUD_125Kbps,\
                           USBCAN_4E_BAUD_250Kbps, USBCAN_4E_BAUD_500Kbps,\
                           USBCAN_4E_BAUD_800Kbps, USBCAN_4E_BAUD_1000Kbps]

## =============================================================================
## USBCAN-4E-U设置属性类型
## =============================================================================
USBCAN_4E_ATTR_SET_BAUD           = 0x0
USBCAN_4E_ATTR_SET_LIGHT          = 0x2
USBCAN_4E_ATTR_SET_COUNTER        = 0x3
USBCAN_4E_ATTR_START_STOP_COUNTER = 0x4
USBCAN_4E_ATTR_SEND_AUTO          = 0x5
USBCAN_4E_ATTR_DATA_TRANS         = 0x6
USBCAN_4E_ATTR_FILL_FILTER        = 0x7
USBCAN_4E_ATTR_START_FILTER       = 0x8
USBCAN_4E_ATTR_STOP_FILTER        = 0x9
USBCAN_4E_ATTR_CLEAR_FILTER       = 0xA

## =============================================================================
## USBCAN-E-U设置属性类型
## =============================================================================
USBCAN_E_ATTR_SET_BAUD            = 0x0
USBCAN_E_ATTR_FILL_FILTER         = 0x1
USBCAN_E_ATTR_START_FILTER        = 0x2
USBCAN_E_ATTR_CLEAR_FILTER        = 0x3
USBCAN_E_ATTR_SET_RESEND_TIMEOUT  = 0x4
USBCAN_E_ATTR_SEND_AUTO           = 0x5
USBCAN_E_ATTR_CLEAR_AUTO          = 0x6

## =============================================================================
## PCI-5010-U, PCI-5020-U, USBCAN-E-U, USBCAN-2E-U设备的波特率
## =============================================================================
USBCAN_E_BAUD_5Kbps     = 0x1C01C1
USBCAN_E_BAUD_10Kbps    = 0x1C00E0
USBCAN_E_BAUD_20Kbps    = 0x1600B3
USBCAN_E_BAUD_50Kbps    = 0x1C002C
USBCAN_E_BAUD_100Kbps   = 0x160023
USBCAN_E_BAUD_125Kbps   = 0x1C0011
USBCAN_E_BAUD_250Kbps   = 0x1C0008
USBCAN_E_BAUD_500Kbps   = 0x060007
USBCAN_E_BAUD_800Kbps   = 0x060004
USBCAN_E_BAUD_1000Kbps  = 0x060003

USBCAN_E_BAUD_LIST = [USBCAN_E_BAUD_5Kbps,   USBCAN_E_BAUD_10Kbps,\
                      USBCAN_E_BAUD_20Kbps,  USBCAN_E_BAUD_50Kbps,\
                      USBCAN_E_BAUD_100Kbps, USBCAN_E_BAUD_125Kbps,\
                      USBCAN_E_BAUD_250Kbps, USBCAN_E_BAUD_500Kbps,\
                      USBCAN_E_BAUD_800Kbps, USBCAN_E_BAUD_1000Kbps]

## =============================================================================
## Work mode 
## =============================================================================
WORK_NORMAL_MODE        = 0x0
WORK_LISTEN_ONLY_MODE   = 0x1

## =============================================================================
## Send type
## =============================================================================
SEND_NORMAL             = 0x0
SEND_SINGLE             = 0x1
SEND_SELF_RECV          = 0x2
SEND_SELF_RECV_SIGNAL   = 0x3
SEND_TYPE_LIST          = [SEND_NORMAL, SEND_SINGLE,\
                           SEND_SELF_RECV, SEND_SELF_RECV_SIGNAL]

## =============================================================================
## Data type conversion
## =============================================================================
CHAR                    = ctypes.c_char
UCHAR                   = ctypes.c_ubyte
BYTE                    = ctypes.c_ubyte

USHORT                  = ctypes.c_uint16

WORD                    = ctypes.c_int16
DWORD                   = ctypes.c_int32
UINT                    = ctypes.c_uint32

PTR                     = ctypes.byref
PVOID                   = ctypes.c_void_p
HANDLE                  = ctypes.c_void_p

## =============================================================================
## Key structures
## =============================================================================
class REMOTE_CLIENT(ctypes.Structure):
    _fields_ = [
        ('iIndex',  DWORD),
        ('port',    DWORD),
        ('hClient', HANDLE),
        ('szip',    32 * CHAR)
    ]

class CHGDESTIPANDPORT(ctypes.Structure):
    _fields_ = [
        ('szpwd',       10 * CHAR),
        ('szdesip',     20 * CHAR),
        ('desport',     DWORD),
        ('blistenonly', BYTE)
    ]

## =============================================================================
## ZLGCAN系列接口卡信息的数据类型
## =============================================================================
class VCI_BOARD_INFO(ctypes.Structure):
    _fields_ = [
        ('hw_Version',     USHORT),
        ('fw_Version',     USHORT),
        ('dr_Version',     USHORT),
        ('in_Version',     USHORT),
        ('irq_Num',        USHORT),
        ('can_Num',        BYTE),
        ('str_Serial_Num', 20 * CHAR),
        ('str_hw_Type',    40 * CHAR),
        ('Reserved',       4 * USHORT)
    ]

## =============================================================================
## CAN信息帧的数据类型
## =============================================================================    
class VCI_CAN_OBJ(ctypes.Structure):
    _fields_ = [
        ('ID',         UINT),
        ('TimeStamp',  UINT),
        ('TimeFlag',   BYTE),
        ('SendType',   BYTE),
        ('RemoteFlag', BYTE),     ## 是否是远程帧
        ('ExternFlag', BYTE),     ## 是否是扩展帧
        ('DataLen',    BYTE),
        ('Data',       8 * BYTE),
        ('Reserved',   3 * BYTE)
    ]

## =============================================================================
## 定义CAN控制器状态的数据类型
## =============================================================================    
class VCI_CAN_STATUS(ctypes.Structure):
    _fields_ = [
        ('ErrInterrupt', UCHAR),
        ('regMode',      UCHAR),
        ('regStatus',    UCHAR),
        ('regALCapture', UCHAR),
        ('regECCapture', UCHAR),
        ('regEWLimit',   UCHAR),
        ('regRECounter', UCHAR),
        ('regTECounter', UCHAR),
        ('Reserved',     DWORD)
    ]

## =============================================================================
## 定义错误信息的数据类型
## =============================================================================
class VCI_ERR_INFO(ctypes.Structure):
    _fields_ = [
        ('ErrCode',         UINT),
        ('Passive_ErrData', 3 * BYTE),
        ('ArLost_ErrData',  BYTE)
    ]

## =============================================================================
## 定义初始化CAN的数据类型
## =============================================================================    
class VCI_INIT_CONFIG(ctypes.Structure):
    _fields_ = [
        ('AccCode',  DWORD),
        ('AccMask',  DWORD),
        ('Reserved', DWORD),
        ('Filter',   UCHAR),
        ('Timing0',  UCHAR),
        ('Timing1',  UCHAR),
        ('Mode',     UCHAR)
    ]

## =============================================================================
## 
## =============================================================================
class VCI_FILTER_RECORD(ctypes.Structure):
    _fields_ = [
        ('ExtFrame', DWORD),      ## 是否为扩展帧
        ('Start',    DWORD),
        ('End',      DWORD)
    ]

## =============================================================================
## 定时自动发送帧结构
## =============================================================================
class VCI_AUTO_SEND_OBJ(ctypes.Structure):
    _fields_ = [
        ('Enable',   BYTE),       ## 使能本条报文.  0：禁能   1：使能
        ('Index',    BYTE),       ## 报文编号.   最大支持32条报文
        ('Interval', DWORD),      ## 定时发送时间。1ms为单位
        ('obj',      VCI_CAN_OBJ) ## 报文
    ]

## =============================================================================
## 设置指示灯状态结构
## =============================================================================
class VCI_INDICATE_LIGHT(ctypes.Structure):
    _fields_ = [
        ('Indicate',          BYTE),    ## 指示灯编号
        ('AttribRedMode',     BYTE, 2), ## Red LED灭/亮/闪烁/自控
        ('AttribGreenMode',   BYTE, 2), ## Green LED灭/亮/闪烁/自控
        ('AttribReserved',    BYTE, 4), ## 保留暂时不用
        ('FrequenceRed',      BYTE, 2), ## Red LED闪烁频率
        ('FrequenceGreen',    BYTE, 2), ## Green LED闪烁频率
        ('FrequenceReserved', BYTE, 4)  ## 保留暂时不用
    ]

## =============================================================================
## 设置转发结构
## =============================================================================
class VCI_CAN_OBJ_REDIRECT(ctypes.Structure):
    _fields_ = [
        ('Action',       BYTE),   ## 标识开启或停止转发
        ('DestCanIndex', BYTE)    ## CAN目标通道
    ]

## =============================================================================
## 异常类定义
## =============================================================================    
class DllFileNotExistException(Exception):
    '''
    '''
    def __init__(self, file_name):
        self.err_string = 'Dynamic library file [%s] does not exist' % file_name

    def to_string(self):
        return self.err_string

class DllLoadException(Exception):
    '''
    '''
    def __init__(self, file_name):
        self.err_string =  '[%s] loads fail' % file_name

    def to_string(self):
        return self.err_string

class DllNameInvalidException(Exception):
    '''
    '''
    def __init__(self):
        self.err_string = '[x] Dll name isf None'

    def to_string(self):
        return self.err_string

class CanDeviceTypeInvalidException(Exception):
    '''
    '''
    def __init__(self, device_type):
        self.err_string = 'Device type [%d] is invalid' % device_type

    def to_string(self):
        return self.err_string

class CanDeviceOpenException(Exception):
    '''
    '''
    def __init__(self, device_type, device_index):
        self.err_string = '[x] %-60s [FAIL]' % ('%d-%d device open' % (device_type, device_index))

    def to_string(self):
        return self.err_string

class CanDeviceCloseException(Exception):
    '''
    '''
    def __init__(self, device_type, device_index):
        self.err_string = '[x] %-60s [FAIL]' % ('Close device %d-%d' % (device_type, device_index))

    def to_string(self):
        return self.err_string

class CanDeviceIndexInvalidException(Exception):
    '''
    '''
    def __init__(self, can_index):
        self.err_string = '[x] %-60s' % ('Can device index %d is invalid' % can_index)

    def to_string(self):
        return self.err_string

class CanDeviceBaudInvalidException(Exception):
    '''
    '''
    def __init__(self, baud):
        self.err_string = '[x] %-60s' % ('Baudrate %d is invalid, not in list' % baud)

    def to_string(self):
        return self.err_string
        
class PyUsbCan(object):
    '''
    '''

    def __init__(self, device_type, dll_name = 'ControlCAN.dll'):
        '''
        Initialization for PyUsbCan class
        '''
        if device_type not in CAN_DEVICE_TYPE_LIST:
            raise CanDeviceTypeInvalidException(device_type)

        if dll_name is None:
            raise DllNameInvalidException()
            
        self.__device_type       = DWORD(device_type)
        self.__dll_name          = dll_name
        self.__usb_can           = None
        
        self.__start_flag        = False
        self.__stop_flag         = False

        self.__init_flag         = False
        
        self.__open_flag         = False
        self.__close_flag        = False
        
        self.__set_attr_flag     = False

        self.__filter_record_cnt = 0x0

        self.__current_can_index = 0x0

        self.__connected         = False

        self.load_dll()

    def load_dll(self):
        '''
        '''
        if not os.path.exists(self.__dll_name):
            raise DllFileNotExistException(self.__dll_name)

        self.__usb_can = ctypes.windll.LoadLibrary(self.__dll_name)
        if not self.__usb_can:
            raise DllLoadException(self.__dll_name)
        else:
            print '[*] %-60s [SUCCESS]' % ('Load %s dynamic library' % self.__dll_name)
        
    def open_device(self, device_index = 0):
        '''
        '''
        if self.__usb_can is None:
            raise DllLoadException(self.__dll_name)

        _reserved = DWORD(0)
        _index    = DWORD(device_index)
        ret = self.__usb_can.VCI_OpenDevice(self.__device_type, _index, _reserved)
        if ( STATUS_OK != ret):
            self.__connected = False
            raise CanDeviceOpenException(self.__device_type.value, _index.value)
        else:
            self.__connected = True
            self.__open_flag = True
            return True

    def close_device(self, device_index):
        '''
        '''
        if self.__open_flag:
            _index = DWORD(device_index)
            ret = self.__usb_can.VCI_CloseDevice(self.__device_type, _index)
            if STATUS_OK != ret:
                raise CanDeviceCloseException(self.__device_type.value, _index.value)
            else:
                self.__close_flag = True
                print '[*] %-60s [SUCCESS]' % ('Close device %d-%d' % (self.__device_type.value, _index.value))

    def is_device_init(self):
        '''
        '''
        pass

    def init_device(self, device_index, can_index, data):
        '''
        '''
        if self.__device_type == VCI_USBCAN_4E_U:
            if not self.__set_attr_flag:
                print 'should be set attribute first'
                return False

        if not isinstance(data, VCI_INIT_CONFIG):
            raise TypeError('VCI_INIT_CONFIG')

        _data    = PTR(data)
        _d_index = DWORD(device_index)
        _c_index = DWORD(can_index)
        ret      = self.__usb_can.VCI_InitCAN(self.__device_type, _d_index, _c_index, _data)
        if STATUS_OK != ret:
            self.__init_flag          = False
            self.__current_can_index += 1
            return False
        else:
            self.__init_flag          = True
            return True

    def read_board_info(self, device_index):
        '''
        '''
        _d_index         = DWORD(device_index)
        _data            = VCI_BOARD_INFO()
        _data.hw_Version = USHORT(0x0)
        _data.fw_Version = USHORT(0x0)
        _data.dr_Version = USHORT(0x0)
        _data.in_Version = USHORT(0x0)
        _data.irq_Num    = USHORT(0x0)
        _data.can_Num    = BYTE(0x0)
        _pdata           = PTR(_data)
        ret              = self.__usb_can.VCI_ReadBoardInfo(self.__device_type, _d_index, _pdata)
        if STATUS_OK != ret:
            return (False, None)
        else:
            return (True, _data)

    def read_error_info(self, device_index, can_index):
        '''
        '''
        _d_index              = DWORD(device_index)
        _c_index              = DWORD(can_index)

        _data                 = VCI_ERR_INFO()
        _data.ErrCode         = UINT(0x0)
        byte_array            = BYTE * 3
        _data.Passive_ErrData = byte_array(0x0, 0x0, 0x0)
        _data.ArLost_ErrData  = BYTE(0x0)
        _pdata                = PTR(_data)

        ret                   = self.__usb_can.VCI_ReadErrInfo(self.__device_type, _d_index, _c_index, _pdata)
        if STATUS_OK != ret:
            return (False, None)
        else:
            return (True, _data)

    def read_status(self, device_index, can_index):
        '''
        '''
        _d_index           = DWORD(device_index)
        _c_index           = DWORD(can_index)
        
        _data              = VCI_CAN_STATUS()
        _data.ErrInterrupt = UCHAR(0x0)
        _data.regMode      = UCHAR(0x0)
        _data.regStatus    = UCHAR(0x0)
        _data.regALCapture = UCHAR(0x0)
        _data.regECCapture = UCHAR(0x0)
        _data.regEWLimit   = UCHAR(0x0)
        _data.regRECounter = UCHAR(0x0)
        _data.regTECounter = UCHAR(0x0)
        _pdata             = PTR(_data)
        
        ret                = self.__usb_can.VCI_ReadCANStatus(self.__device_type, _d_index, _c_index, _pdata)
        if STATUS_OK != ret:
            return (False, None)
        else:
            return (True, _data)

    def get_reference(self):
        '''
        Mainly, it is used as accessing parameters of CANET
        '''
        pass

    def get_device_type(self):
        '''
        '''
        return self.__device_type
        
    def set_usbcan_4e_u_reference(self, device_index, can_index, ref_type, data):
        '''
        '''
        if USBCAN_4E_ATTR_SET_BAUD == ref_type:
            ## Set baudrate
            if data not in USBCAN_4E_BAUD_LIST:
                raise CanDeviceBaudInvalidException(data)

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)                
            _pbaud   = PTR(DWORD(data))
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_SET_BAUD), _pbaud)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_SET_LIGHT == ref_type:
            ## Set indicate light, should be set after VCI_InitCAN() called
            if not self.__init_flag:
                print '[*] %-60s' % ('This function should be called after VCI_InitCAN()')
                return False

            if not isinstance(data, VCI_INDICATE_LIGHT):
                raise TypeError('VCI_INDICATE_LIGHT')

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _plight  = PTR(data)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_SET_LIGHT), _plight)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_SET_COUNTER == ref_type:
            ## Set timer/clock, should be set after VCI_InitCAN() called
            if not self.__init_flag:
                    print '[*] %-60s' % ('This function should be called after VCI_InitCAN()')
                    return False

            _d_index  = DWORD(device_index)
            _c_index  = DWORD(can_index)
            _pcounter = PTR(DWORD(data))
            ret       = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                        c_index,DWORD(USBCAN_4E_ATTR_SET_COUNTER), _pcounter)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_START_STOP_COUNTER == ref_type:
            ## Start/stop timer, should be set after VCI_InitCan() called            
            if not self.__init_flag:
                    print '[*] %-60s' % ('This function should be called after VCI_InitCan()')
                    return False

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pbyte   = PTR(BYTE(data))
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_START_STOP_COUNTER), _pbyte)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_SEND_AUTO == ref_type:
            ## Set sending automatically
            if not isinstance(data, VCI_AUTO_SEND_OBJ):
                raise TypeError('VCI_AUTO_SEND_OBJ')

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(data)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_SEND_AUTO), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_DATA_TRANS == ref_type:
            ## Set datagram transmit, should be set after VCI_InitCAN() called
            if not self.__init_flag:
                    print '[*] %-60s' % ('This function should be called after VCI_InitCan()')
                    return False

            if not isinstance(data, VCI_CAN_OBJ_REDIRECT):
                raise TypeError('VCI_CAN_OBJ_REDIRECT')

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pobj    = PTR(data)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_DATA_TRANS), _pobj)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_FILL_FILTER == ref_type:
            ## Set filter for receiving data frame, add one record once when called
            if not self.__init_flag:
                    print '[*] %-60s' % ('This function should be called after VCI_InitCAN()')
                    return False

            if not isinstance(data, VCI_FILTER_RECORD):
                raise TypeError('VCI_FILTER_RECORD')
                
            self.__filter_record_cnt += 1
            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _precord = PTR(data)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_FILL_FILTER), _precord)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_START_FILTER == ref_type:
            ## Start filter
            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(None)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_START_FILTER), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_STOP_FILTER == ref_type:
            ## Stop filter
            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(None)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_STOP_FILTER), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_4E_ATTR_CLEAR_FILTER == ref_type:
            ## Clear filter
            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(None)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_4E_ATTR_CLEAR_FILTER), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                self.__filter_record_cnt = 0
                return True

    def set_usbcan_e_u_reference(self, device_index, can_index, ref_type, data):
        '''
        '''
        if USBCAN_E_ATTR_SET_BAUD == ref_type:
            ## Set baudrate
            if data not in USBCAN_E_BAUD_LIST:
                raise CanDeviceBaudInvalidException(data)

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(DWORD(data))
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_E_ATTR_SET_BAUD), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_E_ATTR_FILL_FILTER == ref_type:
            ## Fill filter table
            if not isinstance(VCI_FILTER_RECORD, data):
                raise TypeError('VCI_FILTER_RECORD')

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(data)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_E_ATTR_FILL_FILTER), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                self.__filter_record_cnt += 1
                return True
        elif USBCAN_E_ATTR_START_FILTER == ref_type:
            ## Start filter
            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(None)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_E_ATTR_START_FILTER), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_E_ATTR_CLEAR_FILTER ==  ref_type:
            ## Clear filter
            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(None)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_E_ATTR_CLEAR_AUTO), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                self.__filter_record_cnt = 0
                return True
        elif USBCAN_E_ATTR_SET_RESEND_TIMEOUT == ref_type:
            ## Set timeout for re-sending
            if data < 1500:
                return Flase

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(DWORD(data))
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_E_ATTR_SET_RESEND_TIMEOUT), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_E_ATTR_SEND_AUTO == ref_type:
            ## Send data in table automatically
            if not isinstance(data, VCI_AUTO_SEND_OBJ):
                raise TypeError('VCI_AUTO_SEND_OBJ')

            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(data)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_E_ATTR_SEND_AUTO), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True
        elif USBCAN_E_ATTR_CLEAR_AUTO == ref_type:
            ## Clear table for automatically
            _d_index = DWORD(device_index)
            _c_index = DWORD(can_index)
            _pdata   = PTR(None)
            ret      = self.__usb_can.VCI_SetReference(self.__device_type, _d_index,\
                                                       _c_index, DWORD(USBCAN_E_ATTR_CLEAR_AUTO), _pdata)
            if STATUS_OK != ret:
                return False
            else:
                return True

    def set_cannet_reference(self, device_index, can_index, ref_type, data):
        '''
        '''
        pass
            
    def set_reference(self, device_index, can_index, ref_type, data):
        '''
        '''
        if self.__device_type in [VCI_PCI5010U, VCI_PCI5020U,\
                                  VCI_USBCAN_E_U, VCI_USBCAN_2E_U]:
            if can_index > 1:
                print '[X] something error happens'
                raise CanDeviceIndexInvalidException(can_index)
                
            ret = self.set_usbcan_e_u_reference(device_index, can_index, ref_type, data)
            return ret
        elif self.__device_type.value == VCI_USBCAN_4E_U:
            if can_index > 3:
                raise CanDeviceIndexInvalidException(can_index)
                
            ret = self.set_usbcan_4e_u_reference(device_index, can_index, ref_type, data)
            return ret
        elif self.__device_type in [VCI_CANETUDP, VCI_CANETE, VCI_CANETTCP]:
            ret = self.set_cannet_reference(device_index, can_index, ref_type, data)
            return ret
        else:
            print '[*] %-60s' % ('Device-%d does not need to set reference' % self.__device_type.value)
            return True

    def get_receive_num(self, device_index, can_index):
        '''
        '''
        _d_index  = DWORD(device_index)
        _c_index  = DWORD(can_index)
        frame_cnt = self.__usb_can.VCI_GetReceiveNum(self.__device_type, _d_index, _c_index)
        return frame_cnt

    def clear_buffer(self, device_index, can_index):
        '''
        '''
        _d_index = DWORD(device_index)
        _c_index = DWORD(can_index)
        ret      = self.__usb_can.VCI_ClearBuffer(self.__device_type, _d_index, _c_index)
        if STATUS_OK != ret:
            return False
        else:
            return True

    def start_device(self, device_index, can_index):
        '''
        '''
        if not self.__connected:
            return False

        _d_index = DWORD(device_index)
        _c_index = DWORD(can_index)

        ret      = self.__usb_can.VCI_StartCAN(self.__device_type, _d_index, _c_index)
        if STATUS_OK != ret:
            return False
        else:
            return True

    def reset_device(self, device_index, can_index):
        '''
        '''
        if not self.__connected:
            return False

        _d_index = DWORD(device_index)
        _c_index = DWORD(can_index)
        ret      = self.__usb_can.VCI_ResetCAN(self.__device_type, _d_index, _c_index)
        if STATUS_OK != ret:
            return False
        else:
            return True

    def transmit(self, device_index, can_index, tx_type, _id, remote_flag, extend_flag, _len, data):
        '''
        '''
        if not self.__connected:
            return 0
            
        _d_index             = DWORD(device_index)
        _c_index             = DWORD(can_index)

        if not _len:
            print '[x] Send length should not be zero'
            return 0

        if tx_type not in SEND_TYPE_LIST:
            print '[x] Send type is invalid'
            return 0

        _data                = VCI_CAN_OBJ()
        _data.ID             = _id
        _data.TimeStramp     = UINT(0x0)
        _data.TimeFlag       = BYTE(0x0)
        _data.SendType       = BYTE(tx_type)
        if remote_flag:
            _data.RemoteFlag = BYTE(0x1)
        else:
            _data.RemoteFlag = BYTE(0x0)
        if extend_flag:
            _data.ExternFlag = BYTE(0x1)
        else:
            _data.ExternFlag = BYTE(0x0)
        _data.DataLen        = BYTE(len(data))
        for i in range(len(data)):
            _data.Data[i]    = data[i]

        _pdata               = PTR(_data)
        ret                  = self.__usb_can.VCI_Transmit(self.__device_type, _d_index, _c_index, _pdata, 1)
        if ret > 0:
            return ret
        else:
            return 0

    def receive(self, device_index, can_index, _len, timeout = -1):
        '''
        '''
        if not self.__connected:
            return (False, 0, None)
            
        _d_index          = device_index
        _c_index          = can_index
        
        _data             = VCI_CAN_OBJ()
        _data.ID          = UINT(0x0)
        _data.TimeStamp   = UINT(0x0)
        _data.TimeFlag    = BYTE(0x0)
        _data.SendType    = BYTE(0x0)
        _data.RemoteFlag  = BYTE(0x0)
        _data.ExternFlag  = BYTE(0x0)
        _data.DataLen     = BYTE(0x0)
        for i in range(8):
            _data.Data[i] = BYTE(0x0)
        _pdata            = PTR(_data)
        ret               = self.__usb_can.VCI_Receive(self.__device_type, _d_index, _c_index, _pdata, _len, timeout)
        if 0xFFFFFFFF == ret:
            return (False, 0, None)
        else:
            return (True, ret, _data)

    def error_string(self, error_data):
        '''
        '''
        if not isinstance(error_data, VCI_ERR_INFO):
            raise TypeError('VCI_ERR_INFO')

        err_str = ''

        if error_data.ErrCode & 0x0100:
            err_str += 'Device has been opened '

        if error_data.ErrCode & 0x0200:
            err_str += 'Open device error '

        if error_data.ErrCode & 0x0400:
            err_str += 'Device is not opened '

        if error_data.ErrCode & 0x0800:
            err_str += 'Buffer is overflow '

        if error_data.ErrCode & 0x1000:
            err_str += 'Device does not exist '

        if error_data.ErrCode & 0x2000:
            err_str += 'Load dynamic library fail '

        if error_data.ErrCode & 0x4000:
            err_str += 'Execute command fail '

        if error_data.ErrCode & 0x8000:
            err_str += 'Memory is not enough '

        if error_data.ErrCode & 0x0001:
            err_str += 'FIFO inner CAN device overflow '

        if error_data.ErrCode & 0x0002:
            err_str += 'Error alarm of CAN controler '

        if error_data.ErrCode & 0x0004:
            if ((error_data.Passive[0]>>6) & 0xFC) == 0x0:
                err_str += 'Passive error of CAN controler: bit error '
            elif ((error_data.Passive[0]>>6) & 0xFC) == 0x1:
                err_str += 'Passive error of CAN controler: format error '
            elif ((error_data.Passive[0]>>6) & 0xFC) == 0x2:
                err_str += 'Passive error of CAN controler: fill error '
            elif ((error_data.Passive[0]>>6) & 0xFC) == 0x3:
                err_str += 'Passive error of CAN controler: other error '

            if ((error_data.Passive[0]>>5) & 0x1) == 0x0:
                err_str += 'TX error '
            else:
                err_str += 'RX error '

            if error_data.Passive[1] > 0:
                err_str += 'RX error cnt: %d ' % (error_data.Passive[1])

            if error_data.Passive[2] > 0:
                err_str += 'TX error cnt: %d ' % (error_data.Passive[1])

        if error_data.ErrCode & 0x0008:
            err_str += 'Arbit lost of CAN controler '

        if error_data.ErrCode & 0x0010:
            err_str += 'Bus error of CAN controler '

        return err_str    
        
## =============================================================================
## Main entry for unit test
## =============================================================================        
def main():
    try:
        ## Load dynamic library & create class object
        dll_path = './' + 'kerneldlls/' + CAN_DEVICE_DLL_DICT[VCI_USBCAN_4E_U]
        usb_can = PyUsbCan(device_type = VCI_USBCAN_4E_U,\
                           dll_name = dll_path)

        ## Open can device
        device_index = 0
        can_index    = 0
        ret = usb_can.open_device(device_index)
        if ret:
            print '[*] %-60s [SUCCESS]' % ('Can device %d-%d open' % (self.__device_type.value, _index.value))

        ## Set can device baudrate, using standard baudrate with ZLG calculated
        baud_rate = USBCAN_4E_BAUD_500Kbps
        ret       = usb_can.set_reference(device_index, can_index, USBCAN_4E_ATTR_SET_BAUD, baud_rate)
        if not ret:
            print '[X] %-60s [FAIL]' % 'Set reference for baudrate'
        else:
            print '[*] %-60s [SUCCESS]' % 'Set reference for baudrate'

        ## Initialize can device    
        init_config      = VCI_INIT_CONFIG()
        init_config.Mode = WORK_NORMAL_MODE
        ret              = usb_can.init_device(device_index, can_index, init_config)
        if not ret:
            print '[X] %-60s [FAIL]' % 'Initialize device'
        else:
            print '[*] %-60s [SUCCESS]' % 'Inititalize device'

        ## Set filter for different ID
        pass

        ## Start can device
        ret = usb_can.start_device(device_index, can_index)
        if not ret:
            print '[X] %-60s [FAIL]' % 'Start can device'
        else:
            time.sleep(1)
            print '[*] %-60s [SUCCESS]' % 'Start can device'

        flag, result = usb_can.read_error_info(device_index, can_index)
        if not flag:
            print '[X] %-60s [FAIL]' % 'Get error information'
        else:
            err_str = usb_can.error_string(result)
            if not len(err_str):
                print '[*] %-60s' % 'No error'
            else:
                print 'error string: ',
                print usb_can.error_string(result)
                usb_can.reset_device(device_index, can_index)
                flag, result = usb_can.read_error_info(device_index, can_index)
                if not flag:
                    print '[X] %-60s [FAIL]' % 'Get error information'
                else:
                    err_str = usb_can.error_string(result)
                    if not len(err_str):
                        print '[*] %-60s' % 'No error'
                    else:
                        print 'error string: ',
                        print usb_can.error_string(result)

        flag, result = usb_can.read_board_info(device_index)
        if not flag:
            print '[X] %-60s [FAIL]' % 'Read board information'
        else:
            print '[*] %-60s [SUCCESS]' % 'Read board information'
            print 'HW version  : %d' % result.hw_Version
            print 'FW version  : %d' % result.fw_Version
            print 'DR version  : %d' % result.dr_Version
            print 'IN version  : %d' % result.in_Version
            print 'IRQ num     : %d' % result.irq_Num
            print 'CAN num     : %d' % result.can_Num
            print 'Serial num  : %s' % result.str_Serial_Num
            print 'HW type     : %s' % result.str_hw_Type
    except CanDeviceTypeInvalidException, e:
        print e
        sys.exit(-1)
    except DllNameInvalidException, e:
        print e
        sys.exit(-1)
    except DllFileNotExistException, e:
        print e
        sys.exit(-1)
    except DllLoadException, e:
        print e
        sys.exit(-1)
    else:
        usb_can.close_device(device_index)

if __name__ == "__main__":
    main()
