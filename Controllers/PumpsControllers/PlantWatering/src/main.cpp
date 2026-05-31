#include <Arduino.h>

#define PUMP_PIN 7
#define ENABLE_PIN 6
#define SENSOR_PIN A0

const int dry = 505;
const int wet = 220;
bool needs_watering = false;
bool debug = true;

void setup()
{

  Serial.begin(9600);
  Serial.print("Initialazing...");
  pinMode(PUMP_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  digitalWrite(PUMP_PIN, LOW);
  Serial.print("  Done.");
  Serial.println();
}

void loop()
{

  int sensorVal = analogRead(SENSOR_PIN);
  int percentageHumididy = map(sensorVal, wet, dry, 100, 0);
  if (debug == true)
  {
    String dict = String(sensorVal) + "," + String(percentageHumididy);
    Serial.print(dict);
    Serial.println();
    Serial.print(String(needs_watering));
  }
  if (debug == true)

    if (percentageHumididy < 32)
    {
      needs_watering = true;
      if (debug == true)
      {
        Serial.print("Watering...");
      }
      digitalWrite(PUMP_PIN, HIGH);
      analogWrite(ENABLE_PIN, 170);
      delay(5000);
      analogWrite(ENABLE_PIN, 0);
      delay(15000);
      analogWrite(ENABLE_PIN, 170);
      delay(5000);
      analogWrite(ENABLE_PIN, 0);
      delay(15000);
      analogWrite(ENABLE_PIN, 170);
      delay(5000);
      analogWrite(ENABLE_PIN, 0);
      delay(15000);
      analogWrite(ENABLE_PIN, 170);
      delay(5000);
      analogWrite(ENABLE_PIN, 0);
      delay(15000);
      analogWrite(ENABLE_PIN, 170);
      delay(5000);
      analogWrite(ENABLE_PIN, 0);
      if (debug == true)
      {
        Serial.print("   Watered");
      }
      int percentageHumididyAW = map(analogRead(SENSOR_PIN), wet, dry, 100, 0);
      if (percentageHumididyAW > percentageHumididy)
      {
        needs_watering = false;
        digitalWrite(PUMP_PIN, LOW);
      }
    }
  if (needs_watering == false)
  {
    delay(60UL * 60UL * 250UL);
  }
  else
  {
    delay(5000);
  }
}
