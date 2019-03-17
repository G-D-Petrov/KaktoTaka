#include <SPI.h>
#include <WiFi.h>
#include <DHTesp.h>

// Initialize DHT sensor.
DHTesp dht;

char ssid[] = "IMI068";
char pass[] = "1234509876";

int status = WL_IDLE_STATUS;
//char server[] = "172.26.17.178";
char server[] = "192.168.43.224";
WiFiClient client;

void setup() {
  //Initialize serial and wait for p ort to open:
  Serial.begin(115200);
  while (!Serial) {} //wait for serial

  // initialize the DHT sensor
  dht.setup(5, DHTesp::DHT11); // configure it as a DHT11 on given pin

  Serial.print("Connecting to: ");
  Serial.println(ssid);

  while (status != WL_CONNECTED) {
    status = WiFi.begin(ssid, pass);
    delay(1000);
  }
  
  Serial.println("Connected to wifi");
  printWifiStatus();

  Serial.println("\nStarting connection to server...");
  // if you get a connection, report back via serial:
  if (client.connect(server, 5000)) {
  Serial.println("connected to server");
  String PostData = "Biri4ka!";
  client.println("POST / HTTP/1.1");
  client.println("Host:  192.168.43.224");
  client.println("User-Agent: Arduino/1.0");
  client.println("Connection: close");
  client.println("Content-Type: application/x-www-form-urlencoded;");
  client.print("Content-Length: ");
  client.println(PostData.length());
  client.println();
  client.println(PostData);
  }
}

void loop() {
  // if there are incoming bytes available
  // from the server, read them and print 
  //while (client.available()) {
    //char c = client.read();
    //client.write("Djon, Djon... Krajno vreme e da otvorim po bira!!");
    //Serial.write(c);
  //}
  String DeviceId = "|02|";
  String PostDataTemperature = "Data=" + DeviceId + "00|";
  String PostDataHumidity = "Data=" + DeviceId + "03|";
  // read sensor:
  TempAndHumidity newValues = dht.getTempAndHumidity();
  // Check if reads succesful, then print
  // Check if any reads failed and exit early (to try again).
  if (dht.getStatus() == 0)
  {
    PostDataTemperature += String(newValues.temperature);
    PostDataHumidity += String(newValues.humidity);
    
    Serial.println("\nPostDataTemperature: " + PostDataTemperature);
    Serial.println("\nPostDataHumidity: " + PostDataHumidity);
  
    if (client.connect(server, 5000)) {
      delay(100);
      //Serial.println("connected to server");
      // Make a HTTP post request:
      client.println("POST / HTTP/1.1");
      client.println("Host:  192.168.43.224");
      client.println("User-Agent: Arduino/1.0");
      client.println("Connection: close");
      client.println("Content-Type: application/x-www-form-urlencoded;");
      client.print("Content-Length: ");
      client.println(PostDataTemperature.length());
      client.println();
      client.println(PostDataTemperature);
    }
    if (client.connect(server, 5000)) {
      delay(1000);
      client.println("POST / HTTP/1.1");
      client.println("Host:  192.168.43.224");
      client.println("User-Agent: Arduino/1.0");
      client.println("Connection: close");
      client.println("Content-Type: application/x-www-form-urlencoded;");
      client.print("Content-Length: ");
      client.println(PostDataHumidity.length());
      client.println();
      client.println(PostDataHumidity);
    }
  }
}


void printWifiStatus() {
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

  // print the received signal strength:
  long rssi = WiFi.RSSI();
  Serial.print("signal strength (RSSI):");
  Serial.print(rssi);
  Serial.println(" dBm");
}