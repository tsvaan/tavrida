#!/usr/bin/python3
# coding=utf-8
__author__ = 'Vasily.A.Tsilko'
# Python 3.5+
# Simple test client for tcp_server.py

import wx
import wx.xrc
from wxasync import WxAsyncApp, StartCoroutine
import asyncio
import random


###########################################################################
## Global
###########################################################################

srv = ('127.0.0.1', 8888) # server host (this part of software)
cln = ('127.0.0.1', 9999) # device host
data_in_len = 700
data_out_len = 600

###########################################################################
## Class DataIn
###########################################################################

class DataIn(object):
	def __init__(self):
		self._data = {"command":0,}
		for x in range(1, 65):
			self._data["input" + str(x)] = 0
		for x in range(1, 4):
			self._data["reserved" + str(x)] = 0.0

	def str_do_dict(self, str1):
		self._str=str1[:(str1.find(";X"))]
		# print(self._str)
		self._result = dict((key.strip(), float(value.strip()) 
			if len(value.strip())>1 else int(value.strip()))  
				for key, value in (element.split('=')  
					for element in self._str.split(';'))) 
		# print(result)
		self._data.update(self._result)

	@property
	def out(self):
		# random.seed(20)
		# self._data['input1'] = random.randint(1,200)
		return self._data
	

###########################################################################
## Class DataOut
###########################################################################

class DataOut(object):
	def __init__(self):
		self._data={"command":0,}
		for x in range(1, 17):
			self._data["output" + str(x)] = 0
		for x in range(1, 13):
			self._data["ampl" + str(x)] = 321.0
			self._data["phase" + str(x)] = -123.0
		self._data["freq"] = 0.0
		for x in range(1, 4):
			self._data["reserved" + str(x)] = 456.0
	
	def GetData(self, key):
		# print(f"{str(self._data[key])}")
		return self._data[key]
	
	def SetData(self, key, value):
		self._data[key] = value

	def dict_to_str(self):
		self._len = data_out_len
		self._result=str(self._data)
		for f in "'{} ":
			self._result=self._result.replace(f,"")
		self._result=self._result.replace(",",";")
		self._result=self._result.replace(":","=")
		self._result += ";"
		for s in range(self._len - len(self._result)):
			self._result += "X"
		return self._result
		# print(self._result)
		# print(len(self._result))
	
	@property
	def out(self):
		# random.seed(20)
		# self._data['input1'] = random.randint(1,200)
		return self._data



###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

	def __init__( self, parent=None):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString,
		pos = wx.DefaultPosition, size = wx.Size( 671,501 ),
		style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		self.Bar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		self.Console = wx.TextCtrl( self, style=wx.TE_MULTILINE|wx.TE_READONLY)
		# self.Console = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_READONLY )
		self.Console.SetMinSize( wx.Size( -1,300 ) )

		bSizer1.Add( self.Console, 0, wx.ALL|wx.EXPAND, 5 )

		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )

		self.SendBtn = wx.Button( self, wx.ID_ANY, u"Send", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.SendBtn, 0, wx.ALL, 5 )


		bSizer3.Add( ( 50, 0), 1, wx.EXPAND, 5 )

		self.OkBtn = wx.Button( self, wx.ID_ANY, u"Clear", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.OkBtn, 0, wx.ALL, 5 )

		self.BlaBtn = wx.Button( self, wx.ID_ANY, u"Bla Bla", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer3.Add( self.BlaBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


		bSizer1.Add( bSizer3, 1, wx.ALIGN_RIGHT, 5 )

		bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

		self.Input1 = wx.CheckBox( self, wx.ID_ANY, u"Input 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.Input1, 0, wx.ALL, 5 )

		self.Input2 = wx.CheckBox( self, wx.ID_ANY, u"Input 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.Input2, 0, wx.ALL, 5 )

		self.Input3 = wx.CheckBox( self, wx.ID_ANY, u"Input 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer4.Add( self.Input3, 0, wx.ALL, 5 )


		bSizer4.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.spinCtrl = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
		wx.DefaultSize, wx.SP_ARROW_KEYS, -50, 50, 3 )
		self.spinCtrl.SetMaxSize( wx.Size( 150,-1 ) )

		bSizer4.Add( self.spinCtrl, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer4, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.SendBtn.Bind( wx.EVT_BUTTON, self.ClickSend )
		self.OkBtn.Bind( wx.EVT_BUTTON, self.ClickOK )
		self.BlaBtn.Bind( wx.EVT_BUTTON, self.ClickBla )
		self.Input1.Bind( wx.EVT_CHECKBOX, self.InpCheck1 )
		self.Input2.Bind( wx.EVT_CHECKBOX, self.InpCeck2 )
		self.Input3.Bind( wx.EVT_CHECKBOX, self.InpCheck3 )
		self.spinCtrl.Bind( wx.EVT_SPINCTRL, self.onSpin )
		
		# self.Input1.SetValue(True)
		# Starting Server
		StartCoroutine(self.run_server, self)
		# StartCoroutine(self.client, self)
	
	def change_state(self, event):
		print("I'v here")
		self.Input1.SetValue(True)


	def log(self, text):
		self.Console.AppendText(text + "\r\n")

	def status(self, text):
		self.Bar.SetStatusText(text, 0)

	def __del__( self ):
		pass
	
	async def client(self):
		client = await asyncio.open_connection(*cln)
		try:
			reader, writer = await asyncio.open_connection(*cln)
			print(f'Send: {self._str1!r}')
			writer.write(self._str1.encode())
			await writer.drain()
			writer.close()
			await writer.wait_closed()
		except Exception:
			print("ConnectionError")

		async with client:
			await client.serve_forever()

	# Virtual event handlers, override them in your derived class
	def ClickSend( self, event ):
		self._str1 = d_out.dict_to_str()
		self.log (f"Out String = {self._str1}")
		self.log (f"{len(self._str1)} bytes long")
		StartCoroutine(self.client, self)

		# event.Skip()

	def ClickOK( self, event ):
		self.Console.Clear()
		#event.Skip()

	def ClickBla( self, event ):
		self.log(f'Бла-Бла_бла')
		# event.Skip()

	def InpCheck1( self, event ):
		self.log(f"{self.Input1.GetValue()}")
		# d_out._data[output1] = self.Input1.GetValue()
		# self.log(f"output1 = {d_out._data[output1]}")
		d_out.SetData('output1', int(self.Input1.GetValue()))
		self.log(f"output1 now is {d_out.GetData('output1')}")
		# event.Skip()

	def InpCeck2( self, event ):
		event.Skip()

	def InpCheck3( self, event ):
		event.Skip()

	def onSpin( self, event ):
		event.Skip()

	async def handle_connection(self, reader, writer):
		while True:
			try:
				data = await reader.read(data_in_len)
				if not data:
					break
				self.log(f'Received  {len(data)}  butes')
				message = data.decode()
				addr = writer.get_extra_info('peername')
				self.log(f"from {addr!r}")
				d_in.str_do_dict(message)
				feed="Ok\r\n"
				self.log(f"Send: Ok")
				self.log(f'DataIn = {d_in.out}')
				# self.change_state()
				writer.write(feed.encode())
				await writer.drain()
			except ConnectionError:
				break
		self.log("Close the connection")
		writer.close()

	async def run_server(self):
		server = await asyncio.start_server(self.handle_connection, *srv)
	
		addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
		
		self.log(f'Serving on {addrs}')
	
		async with server:
			await server.serve_forever()

async def main():            
	app = WxAsyncApp()
	frame = MainFrame()
	frame.Show()
	app.SetTopWindow(frame)
	frame.log(f'Хайло, ля!')
	# d_in = DataIn()
	# frame.log(f'DataIn = {d_in.out}')
	# frame.log(f'DataOut = {d_out.out}')
	frame.status('Завёлся, типа !')
	await app.MainLoop()

if __name__ == "__main__":
	d_out = DataOut()
	d_in = DataIn()
	asyncio.run(main())