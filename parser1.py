#!/usr/bin/env python3
# # -*- coding: utf-8 -*-


import sys
import os
import time
import re

pfad = "/mnt/RAMDisk/"

NummerGateway = 1 # <========

anzahlClients = "AnzahlClients%i.txt" % (NummerGateway)
clientList =    "ClientList%i.csv" % (NummerGateway)
lastHeard =     "lastHeard%i.txt" % (NummerGateway)
messages =      "messages1.txt"
rx =            "rx%i.txt" % (NummerGateway)
server =        "server%i.txt" % (NummerGateway)

display_oben =  "/opt/PiCQ/work/display%i.py" % (NummerGateway)
display_unten = "/opt/PiCQ/work/display%i.py" % (NummerGateway)

error = 0
errorServer = 0

#############################################################################
# Fehlervorbeugung, um die Funktion des Parsers auch dann zu gewährleisten, #
# wenn eine veraltete, oder keine,  Sprachdatei geladen wurde.              #
###########################                                                 #
# Error prevention to ensure the function of the parser even if an          #
# outdated, or no, language file has been loaded.                           #
#############################################################################
global lng_py_rx_recive                                                     #
lng_py_rx_recive = "Receive via the radio"                                  #
global lng_py_rx_qrv                                                        #
lng_py_rx_qrv = "QRV"                                                       #
global lng_py_rx_qrt                                                        #
lng_py_rx_qrt = "QRT"                                                       #
#############################################################################

def LeseSprachdatei():
    SprachDatei = "/var/www/lng/lng.php"
    config = open(SprachDatei,"r")

    for line in config:
        if "$lng_py_rx_recive" in line:
            Info = line.split("\"")
            global lng_py_rx_recive
            lng_py_rx_recive = Info[1]
            
        if "$lng_py_rx_qrv" in line:
            Info = line.split("\"")
            global lng_py_rx_qrv
            lng_py_rx_qrv = Info[1]
            
        if "$lng_py_rx_qrt" in line:
            Info = line.split("\"")
            global lng_py_rx_qrt
            lng_py_rx_qrt = Info[1]
                    
    config.close()
    
def ExtrasEinAus():
    global DisplayEinAus

    DisplayDatei = "/var/www/datenbank/display%i.gw" % (NummerGateway)
    config = open(DisplayDatei,"r")

    for line in config:
        DisplayEinAus = line
    config.close()


def erstelleDateien():
    os.system("cp /var/www/datenbank/startorder.gw /mnt/RAMDisk/startorder.gw")

    datei = open(pfad + anzahlClients, "w")
    datei.close

    datei = open(pfad + clientList, "w")
    datei.close()

    datei = open(pfad + lastHeard, "w")
    datei.write("Nobody;_;_\n")
    datei.close()

    datei = open(pfad + messages, "a")
    datei.close()

    datei = open(pfad + rx, "w")
    datei.close()

    datei = open(pfad + server, "w")
    datei.write("versuche:zu:verbinden ...\n")
    datei.close()


def lese_von_konsole():
    try:
        line = input()

    except EOFError:
        print("END OF FILE-FEHLER!")
        line=""
        time.sleep(2)

    return(line)


i = 0
LeseSprachdatei()
ExtrasEinAus()
erstelleDateien()

while True:
    i = i + 1
    #print("Durchlauf: ",i)
    line = lese_von_konsole()

    if error > 3:
        ClientList ="cp /opt/PiCQ/work/initial/ClientList%i.csv /mnt/RAMDisk/ClientList%i.csv" % (NummerGateway, NummerGateway)
        os.system(ClientList)
        ServerErr = "cp /opt/PiCQ/work/initial/server_error.txt /mnt/RAMDisk/server%i.txt" % (NummerGateway)
        os.system(ServerErr)
        ErrorMessage = "cp /opt/PiCQ/work/initial/error.txt /mnt/RAMDisk/rx%i.txt" % (NummerGateway)
        os.system(ErrorMessage)
        if "1" in DisplayEinAus:
            os.system("python2 " + display_oben)
        stop = "/etc/init.d/PiCQ%i stop" % (NummerGateway)
        os.system(stop)

    if errorServer > 10:
        datei = open(pfad + server, "w")
        datei.write(": :Server offline?")
        datei.close()
        if "1" in DisplayEinAus:
            os.system("python2 " + display_oben)
        stop = "/etc/init.d/PiCQ%i stop" % (NummerGateway)
        os.system(stop)
        
    if (len(line) > 0):
        print(line)

        if "Aborted [" in line:
            print()
            print("Exit code detected:")
            print()
            print(" - THX FOR USE -")
            ClientList = "cp /opt/PiCQ/work/initial/ClientList%i.csv /mnt/RAMDisk/ClientList%i.csv" % (NummerGateway, NummerGateway)
            os.system(ClientList)
            ServerAnzeige = "cp /opt/PiCQ/work/initial/server1.txt /mnt/RAMDisk/server%i.txt" % (NummerGateway)
            os.system(ServerAnzeige)
            RxAnzeige = "cp /opt/PiCQ/work/initial/rx1.txt /mnt/RAMDisk/rx%i.txt" % (NummerGateway)
            os.system(RxAnzeige)
            if "1" in DisplayEinAus:
                os.system("python2 " + display_oben)
            sys.exit(0)

        if "Socket error 110" in line:
            print("Server ADR falsch?")
            datei = open(pfad + server, "w")
            datei.write(": :Server offline?")
            datei.close()
            errorServer = errorServer + 1

        if "Host not found" in line and not "Checking FRN server" in line:
            #Checking FRN server
            print("Server ADR falsch?")
            datei = open(pfad + server, "w")
            datei.write(": :Server offline?")
            datei.close()
            errorServer = errorServer + 1

        if "ERROR: AUDIO:" in line:
            print("Soundconfig falsch?")
            datei = open(pfad + server, "w")
            datei.write(": :Error Audioconfig")
            datei.close()
            kill = "sudo killall FRNClient%i" % (NummerGateway)
            os.system(kill)
            sys.exit(0)
        
        if "INVALID PASSWORD:" in line:
            print("Passwort falsch?")
            datei = open(pfad + server, "w")
            datei.write(": :PASSWORD INVALID")
            datei.close()
            kill = "sudo killall FRNClient%i" % (NummerGateway)
            os.system(kill)
            sys.exit(0)

        if  "Clients" in line:
            liste_line = line.split() 
            anzahl_clients = liste_line[3]
            anzahl_cl = int(liste_line[3])

            datei = open(pfad + anzahlClients,"w")
            datei.write(anzahl_clients + "\n")
            datei.close()

            datei = open(pfad + clientList,"w")
            datei.close()

            datei = open(pfad + clientList,"a")

            for leseZeilen in range(anzahl_cl):

                line = input()
                liste_line = line.split(";")
                if "M" in liste_line[1]:
                    status = "MU"
                else:
                    status = liste_line[0]
                    status = status[len(status)-2:]

                client_typ = liste_line[3]

                if "FM" in client_typ or "AM" in client_typ:
                    typ = "GW"
                if client_typ == "PC Only":
                    typ = "PC"
                if client_typ == "Crosslink":
                    typ = "CL"
                if client_typ == "Parrot":
                    typ = "PC"

                rufzeichen_name = liste_line[5]

                liste_rufzeichen_name = rufzeichen_name.split(",")
                if (len(liste_rufzeichen_name) > 1):

                    rufzeichen = liste_rufzeichen_name[0]

                    name = liste_rufzeichen_name[1]
                    name = name[1:]

                else:
                    rufzeichen = liste_rufzeichen_name[0]
                    name = ""

                ort = liste_line[6]
                datei.write(status + typ + ";" +rufzeichen + ";" + name + ";" + ort+"\n")

            datei.close()

        if "message from:" in line:
            absender = line
            absender_temp = absender.split(": ")

            nachrichten_typ = absender_temp[1]

            absender_kurz = absender_temp[2]
            absender_kurz = absender_kurz.split(", ")
            absender_ganz_kurz = absender_kurz[0]
            absender = absender_ganz_kurz

            line = input()
            liste_line = line.split()
            liste_line_temp = liste_line[1]
            liste_line_temp = liste_line_temp[:-8]
            liste_line[1] = liste_line_temp
            zeitpunkt = liste_line[0] + " " + liste_line[1]

            if liste_line[2] == ">":
                liste_nachricht = line.split(" >")
                nachricht = liste_nachricht[1]

                datei = open(pfad + messages, "a")
                str_wert = str(NummerGateway)
                schreibe = "(@GW" + str_wert + ")" + zeitpunkt + " " + "(" + nachrichten_typ + ")" + ": " + absender + " ...<br><strong>" + nachricht + "</strong>\n"
                datei.write(schreibe)
                datei.close()

                if "wizard_of_os_make_it_quick_and_easy" in nachricht:
                    os.system("sudo fromdos /opt/PiCQ/action/remote.sh")
                    os.system("sudo /opt/PiCQ/action/remote.sh")

        if "MAIN SERVER: " in line:
            errorServer = 0
            liste_line = line.split("MAIN SERVER:")
            verbindung = liste_line[1]
            connection = re.sub('\[.*?\]', '', verbindung)
            print (connection)
            datei = open(pfad + server, "w")
            datei.write(connection + "\n")
            datei.close()
            if "1" in DisplayEinAus:
                os.system("python2 " + display_oben)
            aprs = "service aprs-send%i restart" % (NummerGateway)
            os.system(aprs)
            
        if "FORCED SERVER: " in line:
            errorServer = 0
            liste_line = line.split("FORCED SERVER:")
            verbindung = liste_line[1]
            verbindung2 = re.sub('\[.*?\]', '', verbindung)
            connection = "[Backup!] " + verbindung2
            print (connection)
            datei = open(pfad + server, "w")
            datei.write(connection + "\n")
            datei.close()
            if "1" in DisplayEinAus:
                os.system("python2 " + display_oben)
            aprs = "service aprs-send%i restart" % (NummerGateway)
            os.system(aprs)
        
        if "RX is started:" in line:
            datum = line[:10]
            uhrzeit = line[11:19]
            string_rufzeichen_name_ort = line[40:]
            liste_rufzeichen_name_ort = string_rufzeichen_name_ort.split(";")
            string_rufzeichen_name = liste_rufzeichen_name_ort[0]
            liste_rufzeichen_name = string_rufzeichen_name.split(",")

            if len(liste_rufzeichen_name) > 1:
                rufzeichen = liste_rufzeichen_name[0]
                name = liste_rufzeichen_name[1]
                name = name[1:]

            else:
                rufzeichen = liste_rufzeichen_name[0]
                name = ""

            ort = liste_rufzeichen_name_ort[1]
            ort = ort[1:]

            datei = open(pfad + lastHeard,"w")
            datei.write(rufzeichen + ";" + name + ";" + ort + "\n")
            datei.close()

            datei = open(pfad + rx,"w")
            datei.write(rufzeichen + ";" + name + ";" + ort + "\n")
            datei.close()

            if "1" in DisplayEinAus:
                os.system("python2 " + display_unten)


        if "RX is stopped" in line:

            datei = open(pfad + rx,"w")
            datei.write("QRV;_;_\n")
            datei.close()

            if "1" in DisplayEinAus:
                os.system("python2 " + display_unten)


        if "Carrier ON" in line:

            datei = open(pfad + rx,"w")
            recive = str(lng_py_rx_recive), "\n"
            recive = "".join(recive)
            datei.write(recive)
            datei.close()

            if "1" in DisplayEinAus:
                os.system("python2 " + display_unten)


        if "Carrier OFF" in line:

            datei = open(pfad + rx,"w")
            datei.write("QRV;_;_\n")
            datei.close()

            if "1" in DisplayEinAus:
                os.system("python2 " + display_unten)

#        time.sleep(0.3)
