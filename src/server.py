""" Example server using asyncio streams
"""
from wxasync import WxAsyncApp, StartCoroutine
import asyncio
import wx
import random

srv = ('127.0.0.1', 9999)

class DataIn(object):
    def __init__(self):
        self._data = {"command":0,}
        for x in range(1, 65):
            self._data["input" + str(x)] = 0
        for x in range(1, 4):
            self._data["reserved" + str(x)] = 0.0
        # return self._data
    @property
    def input1(self):
        # random.seed(20)
        self._data['input1'] = random.randint(1,200)
        return self._data['input1']


class MainFrame(wx.Frame):
    def __init__(self, parent=None):
        super(MainFrame, self).__init__(parent, title="Server Example")
        vbox = wx.BoxSizer(wx.VERTICAL)
        self.logctrl =  wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
        vbox.Add(self.logctrl, 1, wx.EXPAND|wx.ALL)
        

        # # Add a button.
        # vbox = wx.BoxSizer(wx.VERTICAL)
        # self.button =  wx.Button(self, label="Press to Run")
        # vbox.Add(self.button, 1, wx.CENTRE)

        self.SetSizer(vbox)
        self.Layout()

        StartCoroutine(self.run_server, self)

    def log(self, text):
        self.logctrl.AppendText(text + "\r\n")
        
    async def handle_connection(self, reader, writer):
        while True:
            try:
                data = await reader.read(600)
                if not data:
                    break
                self.log(f'Received {len(data)} butes')
                message = data.decode()
                addr = writer.get_extra_info('peername')
                self.log(f"Received {message!r} from {addr!r}")
                self.log(f"Send: {message!r}")
                writer.write(data)
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
    frame.log(f'hello, бля!')
    d_in = DataIn()
    frame.log(f'{d_in.input1}')
    await app.MainLoop()

if __name__ == "__main__":
    asyncio.run(main())