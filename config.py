# config.py
import os

# Безпечний варіант: токен читається з Environment Variable
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")  

PREMIUM_TAX = 0.04   # податок з преміумом
NO_PREMIUM_TAX = 0.08
SETUP_FEE = 0.025    # комісія на виставку

RRA = {  # Return Resource Amount залежно від міста
    "Bridgewatch": 0.539,
    "Martlock": 0.367,
    "Lymhurst": 0.367,
    "Fort Sterling": 0.367,
    "Thetford": 0.367,
    "Caerleon": 0.367
}
