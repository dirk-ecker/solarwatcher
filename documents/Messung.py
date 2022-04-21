import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import lcddriver
#from time import *

lcd = lcddriver.lcd()
lcd.lcd_clear()


lt = time.localtime()
#csvFile = open("Values_ALL.csv","a")
#csvFile = open("Values_%s_%s_%s_%s_%s.csv" %(lt[0],lt[1],lt[2],lt[3],lt[4]),"a")
#csvFile = open("Values.csv","a")
# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan1 = AnalogIn(ads, ADS.P0)
chan2 = AnalogIn(ads, ADS.P1)
chan3 = AnalogIn(ads, ADS.P2)
chan4 = AnalogIn(ads, ADS.P3)
zaehler = 0

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

print("{:>5}\t{:>5}".format("raw", "v"))
tempMinute= lt[4]
tempStunde= lt[3]
tempTag=    lt[2]
start= False
fLeistungJetzt=0.0
FlankeNeueMinuteAbgeschlossen=False
FlankeNeueStundeAbgeschlossen=False
FlankeErsterNeuerTagAbgeschlossen=False
fLeistungDurchschnittProMinute=0.0
fLeistungDurchschnittProStunde=0.0
fLeistungDurchschnittProTag=0.0
lLeistungsdurchschnitteProMinute=[]
lLeistungsdurchschnitteProStunde=[]
fgeleseneLeistung=0.0
fGesamtLeistung=0.0
fSpannung=0.0
fStrom1=0.0
fStrom2=0.0
fStrom3=0.0
fStromGesamt=0.0
iAnzeige=0
try:
    while True:
        lt = time.localtime()
        fSpannung = (chan1.value*260.0)/31985.0
        fStrom1 = (chan2.value-20330.0)/1500.0     #19800.0 (0)
        fStrom2 = (chan3.value-20330.0)/1500.0
        fStrom3 = (chan4.value-20330.0)/1500.0
        fStromGesamt=fStrom1+fStrom2+fStrom3



        print("{:>5}\t{:>5.3f}".format(chan1.value, fSpannung) + " V")

        print("{:>5}\t{:>5.3f}".format(chan2.value, chan2.voltage) + " V")
        print(str(lt[4]))

        lcd.lcd_clear()
        if iAnzeige<10:
            lcd.lcd_display_string("%s-%s-%s  %s:%s:%s"%(lt[0],lt[1],lt[2],lt[3],lt[4],lt[5]), 1)
            lcd.lcd_display_string("Spannung: " + "{:>3.1f}".format(fSpannung) + " V", 2)
            lcd.lcd_display_string("Strom:    " + "{:>1.3f}".format(fStromGesamt) + " A", 3)
            lcd.lcd_display_string("Leistung: " + "{:>5.1f}".format(fLeistungJetzt) + " W", 4)
        else:
            lcd.lcd_display_string("%s-%s-%s  %s:%s:%s"%(lt[0],lt[1],lt[2],lt[3],lt[4],lt[5]), 1)
            lcd.lcd_display_string("Stunde: " + "{:>5.1f}".format(fLeistungDurchschnittProStunde) + " W/h", 2)
            lcd.lcd_display_string("Tag:    " + "{:>5.1f}".format(fLeistungDurchschnittProTag) + " W/h", 3)
            lcd.lcd_display_string("Ges: " + "{:>5.2f}".format(fGesamtLeistung) + " KW/h", 4)


        if tempMinute!= lt[4]:
            if FlankeNeueMinuteAbgeschlossen==True:
                iAnzahlWerte=(len(lLeistungAktMinute))
                print(str(iAnzahlWerte))
                fLeistungAddition=0.0
                for i in range(0,len(lLeistungAktMinute),1):
                    fLeistungAddition+=lLeistungAktMinute[i]
                fLeistungDurchschnittProMinute=(fLeistungAddition/iAnzahlWerte)/60.0
                if FlankeNeueStundeAbgeschlossen:
                    lLeistungsdurchschnittDazu=[fLeistungDurchschnittProMinute]
                    lLeistungsdurchschnitteProMinute+=lLeistungsdurchschnittDazu
                print("Durchschnitt" + str(fLeistungDurchschnittProMinute))


                csvFileProMinute = open("Values_ALL.csv","a")
                csvFileProMinute.write("%s-%s-%s-%s:%s:%s;\t"%(lt[0],lt[1],lt[2],lt[3],lt[4],lt[5]))
                csvFileProMinute.write("{:>5};\t{:>5.3f}".format(chan1.value, chan1.voltage))
                csvFileProMinute.write("   ")
                csvFileProMinute.write("{:>5};\t{:>5.3f}".format(chan2.value, chan2.voltage))
                csvFileProMinute.write(" Leistung vergangene Minute: " + str(fLeistungDurchschnittProMinute))
                csvFileProMinute.write('\n')
                csvFileProMinute.close()

                csvFileReadPowerAll = open("PowerAll.csv","r")

                for line in csvFileReadPowerAll:
                    sgeleseneDatei= line.split(" ")
                    fgeleseneLeistung=float(sgeleseneDatei[1])

                csvFileReadPowerAll.close()


                fGesamtLeistung=fgeleseneLeistung + (fLeistungDurchschnittProMinute/1000.0)

                csvFileWritePowerAll = open("PowerAll.csv","w")
                csvFileWritePowerAll.write("Leistung_Gesamt: " + str(fGesamtLeistung))
                csvFileWritePowerAll.close()

            print("Neue Minute")
            fLeistungJetzt=fSpannung*fStromGesamt
            lLeistungAktMinute=[fLeistungJetzt]
            start=True
            tempMinute=lt[4]
            FlankeNeueMinuteAbgeschlossen=True
        elif start==True:
            fLeistungJetzt=fSpannung*fStromGesamt
            lLeistungdazu=[fLeistungJetzt]
            lLeistungAktMinute+= lLeistungdazu


        if tempStunde!= lt[3]:
            if FlankeNeueStundeAbgeschlossen==True:
                iAnzahlWerte=(len(lLeistungsdurchschnitteProMinute))
                print("Anzahl Messungsdurchschnitte pro Stunde: " + str(lLeistungsdurchschnitteProMinute))
                fLeistungStundeAddition=0.0
                for i in range(0,len(lLeistungsdurchschnitteProMinute),1):
                    fLeistungStundeAddition+=lLeistungsdurchschnitteProMinute[i]
                fLeistungDurchschnittProStunde=(fLeistungStundeAddition/iAnzahlWerte)*60.0
                print("Leistungsdurchschnitt der vergangenen Stunde: " + str(fLeistungDurchschnittProStunde))

                lLeistungsdurchschnitteProMinute=[]


                csvFileProStunde = open("ValuesPerHour.csv","a")
                csvFileProStunde.write("%s-%s-%s-%s;\t"%(lt[0],lt[1],lt[2],lt[3]))
                csvFileProStunde.write("   ")
                csvFileProStunde.write(" Leistung vergangene Stunde: " + str(fLeistungDurchschnittProStunde))
                csvFileProStunde.write(" kW/h" + str(iAnzahlWerte))
                csvFileProStunde.write(' Werte\n')
                csvFileProStunde.close()


            print("Neue Stunde")

            tempStunde=lt[3]
            FlankeNeueStundeAbgeschlossen=True

        if tempTag!= lt[2]:
            if FlankeErsterNeuerTagAbgeschlossen==True:
                iAnzahlWerte=(len(lLeistungsdurchschnitteProStunde))
                print("Anzahl Messungsdurchschnitte pro Stunde: " + str(lLeistungsdurchschnitteProStunde))
                fLeistungTagAddition=0.0
                for i in range(0,len(lLeistungsdurchschnitteProStunde),1):
                    fLeistungTagAddition+=lLeistungsdurchschnitteProStunde[i]
                fLeistungDurchschnittProTag=(fLeistungTagAddition/len(lLeistungsdurchschnitteProStunde))*24.0
                print("Leistungsdurchschnitt der vergangenen Stunde: " + str(fLeistungDurchschnittProTag))

                lLeistungsdurchschnitteProTag=[]


                csvFileProStunde = open("ValuesPerDay.csv","a")
                csvFileProStunde.write("%s-%s-%s;\t"%(lt[0],lt[1],lt[2]))
                csvFileProStunde.write("   ")
                csvFileProStunde.write(" Leistung: " + str(fLeistungDurchschnittProTag)+" KW/h")
                csvFileProStunde.write(" " + str(iAnzahlWerte))
                csvFileProStunde.write('Werte \n')
                csvFileProStunde.close()

            print("Neuer Tag")

            tempTag=lt[2]
            FlankeErsterNeuerTagAbgeschlossen=True

        if iAnzeige>=20:
            iAnzeige=0
        else:
            iAnzeige=iAnzeige+1

        time.sleep(1)

except KeyboardInterrupt:
    print('Logging abgebrochen')
    #csvFile.close()

else:
    print('Fehler beim empfangen der Daten')
    time.sleep(0.5)
    pass

