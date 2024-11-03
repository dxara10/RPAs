from botcity.web import *
from botcity.core import *
import subprocess
from datetime import datetime
from botcity.plugins.excel import *

class Bot:
    def bot(self):
        # Open Application Activity
        title = "BankSystem"
        executablePath = "C:\\Users\\dougl\\OneDrive\\Área de Trabalho\\BankSystem.exe"
        deskBot = DesktopBot()
        deskBot.execute(executablePath)
        deskBot.connect_to_app(backend=Backend.WIN_32, timeout=60000, title=title, path=executablePath)
        popup_Window = deskBot.find_app_window(waiting_time=10000, title=title)

        # Read Excel Activity
        excelBot = BotExcelPlugin()
        file_or_path = "C:\\Users\\dougl\\OneDrive\\Área de Trabalho\\extract.xlsx"

        lista = excelBot.read(file_or_path=file_or_path).as_list(sheet='extrato')[1:]
        # ForEach Activity
        for linha in lista:
            # If Activity
            if linha[0]=="Debito":
                # Find And Click Activity
                field_rbDebito.click()


            # Else Activity
            else:
                # Find And Click Activity
                field_rbCredito.click()


            # Type Into Activity
            field_txtDescricao.type_keys(keys=linha[1], with_spaces=True)

            # Type Into Activity
            field_txtValor.type_keys(keys=linha[2], with_spaces=True)

            # Type Into Activity
            field_Data.type_keys(keys=linha[3], with_spaces=True)

            # Find And Click Activity
            field_btnConfirmar.click()



        return
if __name__ == '__main__':
    bot = Bot()
    bot.bot()