#include <Ticker.h>
#include <SharpIR.h>
#include <ArduinoJson.hpp>
#include <ArduinoJson.h>
#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#define Rele 7
SoftwareSerial BT(9, 10, 11);

bool RUN = false;

float dist(int n) {
  return pow(3027.4 / n, 1.2134);
  //return 17569.7 * pow(n, -1.2164);
}

void datas() {
  int asharp = analogRead(3);
  String json;
  StaticJsonDocument<300> doc;
  doc["cent"] = String(dist(asharp));
  doc["inch"] = String(dist(asharp));
  doc["lbr"] = String(dist(asharp));
  doc["grs"] = String(dist(asharp));
  serializeJson(doc, json);
  Serial.println(json);

  if (RUN)
    digitalWrite(Rele, HIGH);
  else
    digitalWrite(Rele, LOW);
}

Ticker mostrarDatos(datas, 500);
void setup() {
  pinMode(Rele, OUTPUT);
  BT.begin(9600);
  Serial.begin(9600);
  mostrarDatos.start();
}

void loop() {
  if (BT.available()>0) {
    Serial.write(BT.read());
  }
  if (Serial.available()) {
    BT.write(Serial.read());
  }
  mostrarDatos.update();
}
