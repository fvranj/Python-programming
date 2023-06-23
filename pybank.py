bankovni_racuni={}
detalji_racuna={}
stanje_na_racunu={}
import datetime
import os
import random

def kreiraj_bankovni_racun():

    global naziv
    global adresa
    global postanski_broj
    global grad
    global oib 
    global ime_i_prezime
    global valuta
    global polog
    global broj_racuna

    naziv = input("Unesite naziv tvrtke:")
    if naziv in detalji_racuna.keys():
        print("Račun je već u evidenciji.")
        return
    else:
        def generiraj_broj_racuna():
            pet_broj = str(random.randint(0,99999)).zfill(5)
            broj_racuna = f'BA-{datetime.datetime.now().year}-{str(datetime.datetime.now().month).zfill(2)}-{pet_broj}'
            return broj_racuna
        
        broj_racuna = generiraj_broj_racuna()
        adresa = input("Unesite adresu:")
        postanski_broj = input("Unesite postanski_broj:")
        grad = input("Unesite grad:")
        oib = input("Unesite OIB:")
        while len(oib) != 11:
            oib = input("OIB mora imati 11 znamenki. Molimo unesite ispravan OIB.")
        ime_i_prezime = input("Unesite ime i prezime odgovorne osobe:")
        valuta = input("Odaberite valutu(HRK/EUR):")
        while valuta != "HRK" and valuta != "EUR" and valuta != "hrk" and valuta != "eur":
            valuta = input("Odaberite valutu(HRK/EUR):")
        polog = round(float(input("Upišite iznos koji želite položiti na račun:")),2)
        while polog <= 0:
            polog = round(float(input("Upišite iznos koji želite položiti na račun:")),2)
        spremi = input("želite li spremiti detalje računa?(Y/N)")
        while spremi !="Y" and spremi != "y" and spremi != "N" and spremi != "n":
            spremi = input("želite li spremiti detalje računa?(Y/N)")
        if spremi == "N" or spremi == "n":
            return
        elif spremi == "Y" or spremi == "y":
            bankovni_racuni[broj_racuna] = polog
            detalji_racuna[broj_racuna] = [naziv, adresa, postanski_broj, oib, valuta, ime_i_prezime]
            stanje_na_racunu[broj_racuna]={}
            stanje_na_racunu[broj_racuna][str(datetime.datetime.now())] = polog
            print (f"\nČestitamo, uspješno ste kreirali račun {broj_racuna} u PyBanci.")
        input("\nZa povratak na glavni izbornik stisnite enter.")
            
def dodaj_na_racun():
    global suma
    global racuni
    racuni = [i for i in list(bankovni_racuni.keys())]
    broj_racuna = input(f"Molimo upišite svoj broj računa. Trenutno postojeći računi su:{racuni}")
    try:
        suma = round(float(input("\nKoliko novca želite položiti na račun?")),2)
        while suma <= 0:
            suma = round(float(input("\nPolog mora biti pozitivan iznos.")),2)
        bankovni_racuni[broj_racuna] += suma
        stanje_na_racunu[broj_racuna][str(datetime.datetime.now())] = bankovni_racuni[broj_racuna]
        print(f"\nUspješno ste položili {suma} {detalji_racuna[broj_racuna][4]} na račun!")
    except:
        print("\nPrvo kreirajte bankovni račun!")
    input("\nZa povratak na glavni izbornik stisnite enter.")

def uzmi_s_racuna():
    racuni = [i for i in list(bankovni_racuni.keys())]
    broj_racuna = input(f"Molimo upišite svoj broj računa. Trenutno postojeći računi su:{racuni}")
    try:
        suma = round(float(input("\nKoliko novca želite podići s računa?")),2)
        while suma <= 0:
            suma = round(float(input("\nKoličina novca mora biti pozitivan iznos.")),2)
        bankovni_racuni[broj_racuna] -= suma
        stanje_na_racunu[broj_racuna][str(datetime.datetime.now())] = bankovni_racuni[broj_racuna]
        print(f"\nUspješno ste podigli {suma} {detalji_racuna[broj_racuna][4]} s računa!")
    except:
        print("\nPrvo kreirajte bankovni račun!")
    input("\nZa povratak na glavni izbornik stisnite enter.")
    
def prometi_na_racunu():
    racuni = [i for i in list(bankovni_racuni.keys())]
    broj_racuna = input(f"Molimo upišite svoj broj računa. Trenutno postojeći računi su:{racuni}")
    try:
        for vrijeme, stanje in stanje_na_racunu[broj_racuna].items(): 
            print(f'{vrijeme} stanje na Vašem računu je bilo {stanje} {detalji_racuna[broj_racuna][4]}.\n')
    except:
        print("\nPrvo kreirajte bankovni račun!")
    input("\nZa povratak na glavni izbornik stisnite enter.")
    
def stanje_racuna():
    racuni = [i for i in list(bankovni_racuni.keys())]
    broj_racuna = input(f"Molimo upišite svoj broj računa. Trenutno postojeći računi su:{racuni}")
    try:
        print(f"\nNa računu broj {broj_racuna} trenutno imate {bankovni_racuni[broj_racuna]} {detalji_racuna[broj_racuna][4]}.\nDatum i vrijeme: {datetime.datetime.now()}")
    except:
        print("\nPrvo kreirajte bankovni račun!")
    input("\nZa povratak na glavni izbornik stisnite enter.")

def ocisti_ekran():
    os.system('cls' if os.name=='nt' else 'clear')

izbor = ""
while izbor != "6":
    ocisti_ekran()
    print("Dobrodošli u PyBanku! Izaberite vrstu usluge!\n\n1)Kreiranje računa\n\n2)Prikaz stanja računa\n\n3)Prikaz prometa na računu\n\n4)Polog novca na račun\n\n5)Podizanje novca s računa\n\n6)Izlaz\n")
    izbor = input("Odaberite uslugu koju želite!:")
    if izbor !="1" and izbor !="2" and izbor !="3" and izbor !="4" and izbor !="5" and izbor !="6":
        print("Odaberite broj između 1 i 6!")
        continue
    elif izbor == "1":
        ocisti_ekran()
        kreiraj_bankovni_racun()
    elif izbor == "2":
        ocisti_ekran()
        stanje_racuna()
    elif izbor == "3":
        ocisti_ekran()
        prometi_na_racunu()
    elif izbor == "4":
        ocisti_ekran()
        dodaj_na_racun()
    elif izbor == "5":
        ocisti_ekran()
        uzmi_s_racuna()
