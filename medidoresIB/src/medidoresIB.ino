
#include <Wire.h>

/*
By: Nathan Seidle SparkFun Electronics  
Library: http://librarymanager/All#SparkFun_SCD30  
*/
#include "SparkFun_SCD30_Arduino_Library.h" 

#include <LiquidCrystal_I2C.h>

SCD30 airSensor;
LiquidCrystal_I2C lcd(0x27, 16, 2);
//LiquidCrystal_I2C lcd(0x3F, 16, 2);

#define buzzPIN (8)
#define buzzTime (1)
#define buttonPIN (12)

//#define RECALIBRARALINICIAR

void setup()
{
  Serial.begin(9600);
  Serial.println("SCD30 prendido");
  Wire.begin();

  if (airSensor.begin() == false)
  {
    Serial.println("No detecto el sensor. Chequear cableado. Congelando...");
    while (1);
  }

  // Numero de segundos entre medidas: de 2 to 1800 (30 minutos)
  airSensor.setMeasurementInterval(2); 

  // imprime al serial el setup actual
  info_setup();

  // inicializacion del LCD 
  lcd.init();
  lcd.backlight();

  // inicialización buzzer de alarma
  pinMode(buzzPIN,OUTPUT);  

  // inicialización botón de recalibracioón
  pinMode(buttonPIN,INPUT);
  
  // cartelito de presentación
  presentacion();  

  // depreciado
  #ifdef RECALIBRARALINICIAR
  recalibracion();
  #endif   
}


// lee CO2ppm, Temperatura y Humedad
void lecturasx3(int &co2read,int &Tread, int &Hread){
  co2read = airSensor.getCO2();
  Tread = airSensor.getTemperature();
  Hread = airSensor.getHumidity();
}


// loop principal
void loop()  
{
  // variables de las lecturas
  int co2read,Tread,Hread;

  if (airSensor.dataAvailable())
  {
    lecturasx3(co2read,Tread,Hread);

    Serial.print("co2(ppm): ");
    Serial.print(co2read);

    Serial.print(" temp(C): ");
    Serial.print(Tread, 1);

    Serial.print(" humedad(%): ");
    Serial.print(Hread, 1);

    Serial.println();

    // pulsador apretado-> recalibración forzada
    int boton = digitalRead(buttonPIN);
    Serial.print(" boton: ");
    Serial.print(boton, 1);
    if(boton==1){
      recalibracion();
    }

    // mensajes de advertencia
    char msg[12];
    if(co2read<500){
      sprintf(msg,"OK");
    }     
    if(co2read<700){
      sprintf(msg,"OK");
    }     
    if(co2read>700 && co2read<800){
      sprintf(msg,"Medio");
    }     
    if(co2read>800 && co2read<1000){
      sprintf(msg,"Ventilar");
    }
    if(co2read>1000){
      sprintf(msg,"Ventilar!");
    }
    if(co2read>1500){
      sprintf(msg,"Ventilar!!");
    }
    if(co2read>2500){
      sprintf(msg,"Alerta!!!");
      alarma();
    }

    lcd.setCursor(0, 0);
    lcd.print("CO2="+String(co2read)+" "+msg+"           ");
    
    lcd.setCursor(0, 1);
    lcd.print("T="+String(Tread)+"C, H="+ Hread+"%          ");
  }
  else
    Serial.println("Sin datos");

  delay(500);
}



///////////////////////////////////////////////////////////
// imprime informacion del setup actual del sensor
void info_setup()  
{  
    uint16_t settingVal; // The settings will be returned in settingVal
    
    if (airSensor.getForcedRecalibration(&settingVal) == true) // Get the setting
    {
      Serial.print("Forced recalibration factor (ppm) is ");
      Serial.println(settingVal);
    }
    else
    {
      Serial.print("getForcedRecalibration failed! Freezing...");
      while (1)
        ; // Do nothing more
    }

    if (airSensor.getMeasurementInterval(&settingVal) == true) // Get the setting
    {
      Serial.print("Measurement interval (s) is ");
      Serial.println(settingVal);
    }
    else
    {
      Serial.print("getMeasurementInterval failed! Freezing...");
      while (1)
        ; // Do nothing more
    }

    if (airSensor.getTemperatureOffset(&settingVal) == true) // Get the setting
    {
      Serial.print("Temperature offfset (C) is ");
      Serial.println(((float)settingVal) / 100.0, 2);
    }
    else
    {
      Serial.print("getTemperatureOffset failed! Freezing...");
      while (1)
        ; // Do nothing more
    }

    if (airSensor.getAltitudeCompensation(&settingVal) == true) // Get the setting
    {
      Serial.print("Altitude offset (m) is ");
      Serial.println(settingVal);
    }
    else
    {
      Serial.print("getAltitudeCompensation failed! Freezing...");
      while (1)
        ; // Do nothing more
    }

    if (airSensor.getFirmwareVersion(&settingVal) == true) // Get the setting
    {
      Serial.print("Firmware version is 0x");
      Serial.println(settingVal, HEX);
    }
    else
    {
      Serial.print("getFirmwareVersion! Freezing...");
      while (1)
        ; // Do nothing more
    }

    Serial.print("Auto calibration set to ");
    if (airSensor.getAutoSelfCalibration() == true)
        Serial.println("true");
    else
        Serial.println("false");

    //The SCD30 has data ready every two seconds
}

// funcion de presentacion en el LCD al iniciar
// [tipo pac-man]
void presentacion(){
  lcd.setCursor(0, 0);
  lcd.print("CO2 sensor   ");
  lcd.setCursor(0, 1);
  lcd.print(" IB-Bariloche");
  delay(100);
  //alarma();
  
  for(int i=16;i>=0; i--){
    lcd.setCursor(i, 0);    
    lcd.print("=               ");
    delay(200);

    lcd.setCursor(i, 0);    
    lcd.print(">               ");
    delay(300);
   }
   lcd.setCursor(0, 0);    
   lcd.print(" ");
   lcd.setCursor(0, 1);    
   lcd.print(">");
   delay(200);
   lcd.setCursor(0, 1);    
   lcd.print("<");
   delay(200);

  for(int i=0;i<=16; i++){
    lcd.setCursor(i, 1);    
    lcd.print(" =");
    delay(200);

    lcd.setCursor(i, 1);    
    lcd.print(" <");
    delay(300);
   }
   
  lcd.clear();
}


// funcion para recalibrar forzadamente
// se dispara con el pulsador
void recalibracion(){
  alarma();

  lcd.setCursor(0, 0);
  lcd.print("CO2 sensor   ");
  lcd.setCursor(0, 1);
  lcd.print("  IB-Bariloche  ");
  //delay(100);

  for(int i=16;i>=0; i--){
    lcd.setCursor(i, 0);    
    lcd.print("=  calibrando   ");
    delay(250);

    lcd.setCursor(i, 0);    
    lcd.print(">  calibrando   ");
    delay(500);
    int co2read = airSensor.getCO2();
    int Tread = airSensor.getTemperature();
   }
   lcd.setCursor(0, 0);    
   lcd.print(" ");
   lcd.setCursor(0, 1);    
   lcd.print(">");
   delay(250);
   lcd.setCursor(0, 1);    
   lcd.print("<");
   delay(250);

  for(int i=0;i<=16; i++){
    lcd.setCursor(i, 1);    
    lcd.print(" =");
    delay(250);

    lcd.setCursor(i, 1);    
    lcd.print(" <");
    delay(500);
    int co2read = airSensor.getCO2();
    int Tread = airSensor.getTemperature();
   }

  lcd.setCursor(0, 1);
  lcd.print("en el exterior");
  //delay(100);

  for(int n=0;n<2*60*2;n++){
      int co2read = airSensor.getCO2();
      int Tread = airSensor.getTemperature();
      delay(500);
      lcd.setCursor(0, 0);
      lcd.print("faltan "+String((2*60*2-n)*2)+" seg  ");      
  }

  //airSensor.setTemperatureOffset(5);
  airSensor.setAltitudeCompensation(800); //Bariloche
  airSensor.setAmbientPressure(1011);//Bariloche

  airSensor.setForcedRecalibrationFactor(400);
  lcd.clear();
}


// alarma beep...
void alarma(){
  for(int i=0;i<100;i++){
    digitalWrite(buzzPIN,HIGH);
    delay(buzzTime);
    digitalWrite(buzzPIN,LOW);
    delay(buzzTime);    
  }  
  delay(2000);
}
