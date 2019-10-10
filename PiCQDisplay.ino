#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_PCD8544.h>

const char* ssid = "SSIDhere";
const char* password = "PWDhere";

Adafruit_PCD8544 display = Adafruit_PCD8544(D0, D1, D2);

WiFiUDP Udp;
unsigned int localUdpPort = 4210;  // local port to listen on
char incomingPacket[255];  // buffer for incoming packets
//char  replyPacket[] = "Hi there! Got the message :-)";  // a reply string to send back

void setup()
{
  display.begin();
  display.setContrast(40);
  display.setReinitInterval(10);
  display.clearDisplay();   // clears the screen and buffer
  display.setTextSize( 1);
  display.setTextColor(BLACK);
  display.setCursor(0, 0);
  
  Serial.begin(115200);
  Serial.println();

  Serial.printf("Connecting to %s ", ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" connected");
  WiFi.hostname("PiCQDisplay1");
  Udp.begin(localUdpPort);
  Serial.printf("Now listening at IP %s, UDP port %d\n", WiFi.localIP().toString().c_str(), localUdpPort);
  display.println("Now listening at IP %s, UDP port %d\n");
  display.display();
}

void loop()
{
  int packetSize = Udp.parsePacket();
  if (packetSize)
  {
    // receive incoming UDP packets
    Serial.printf("Received %d bytes from %s, port %d\n", packetSize, Udp.remoteIP().toString().c_str(), Udp.remotePort());
    int len = Udp.read(incomingPacket, 255);
    if (len > 0)
    {
      incomingPacket[len] = 0;
    }
    Serial.printf("UDP packet contents: %s\n", incomingPacket);
    String namen = split(incomingPacket,';',0);
    String namens=namen.substring(0,14);
    String daten = split(incomingPacket,';',1);
    String datens=daten.substring(0,14);
    String fakten = split(incomingPacket,';',2);
    String faktens=fakten.substring(0,14);

    String lhnamen = split(incomingPacket,';',3);
    String lhnamens=lhnamen.substring(0,14);
    String lhdaten = split(incomingPacket,';',4);
    String lhdatens=lhdaten.substring(0,14);
    String lhfakten = split(incomingPacket,';',5);
    String lhfaktens=lhfakten.substring(0,14);

    Serial.println(namens);
    Serial.println(datens);
    Serial.println(faktens);

    Serial.println(lhnamens);
    Serial.println(lhdatens);
    Serial.println(lhfaktens);

    
    display.clearDisplay();
    
    display.setTextSize( 1);
    display.setCursor(0, 0);
    //display.println(incomingPacket);
    //display.print('>');
    display.print(namens);
    //display.print('>');
      display.setTextSize( 1);
    display.setCursor(0, 8);
    display.print(datens);
    //display.print('>');
    display.setCursor(0, 16);
    display.print(faktens);
    display.display(); 

    display.setTextSize( 1);
    display.setCursor(0, 24);
    //display.println(incomingPacket);
    //display.print('>');
    display.print(lhnamens);
    //display.print('>');
      display.setTextSize( 1);
    display.setCursor(0, 32);
    display.print(lhdatens);
    //display.print('>');
    display.setCursor(0, 40);
    display.print(lhfaktens);
    display.display(); 
    
    // send back a reply, to the IP address and port we got the packet from
   // Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
   // Udp.write(replyPacket);
    Udp.endPacket();
  }
}

String split(String s, char parser, int index) {
  String rs="";
  int parserIndex = index;
  int parserCnt=0;
  int rFromIndex=0, rToIndex=-1;
  while (index >= parserCnt) {
    rFromIndex = rToIndex+1;
    rToIndex = s.indexOf(parser,rFromIndex);
    if (index == parserCnt) {
      if (rToIndex == 0 || rToIndex == -1) return "";
      return s.substring(rFromIndex,rToIndex);
    } else parserCnt++;
  }
  return rs;
}
