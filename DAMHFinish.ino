#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27,16,2);

int demd = 0;
int demx = 0;
int demv = 0;
int demk = 0;

void setup() {

  pinMode(13, OUTPUT); //Led signal
  Serial.begin(9600); 
  
//LCD init
  lcd.init();
  lcd.backlight();
  
//Loi Chao  
  lcd.setCursor(2,0);
  lcd.print("Do an Mon Hoc");
  lcd.setCursor(1,1);
  lcd.print("PLSP-Theo Hinh");
  delay(5000);
  lcd.clear();
  
  lcd.setCursor(0,0);
  lcd.print("Squ:");
  lcd.setCursor(0,1);
  lcd.print("Rec:");
  lcd.setCursor(9,0);
  lcd.print("Cir:");
  lcd.setCursor(9,1);
  lcd.print("Tri:"); 
}

void loop(){
    //Signal Input
    if(Serial.available() > 0){
      String str = Serial.readString();
      
      //Signal Vuong
      if( str == String("Vuong")){
        delay(100);
        //Disp LCD
        demd = demd + 1; lcd.setCursor(5,0); lcd.print(round(demd));
        if (demd > 5){
            demd = 0; digitalWrite(13,HIGH); delay(200); digitalWrite(13,LOW);
            delay(200);
           }
      }
      
      //Signal HCN
      else if(str == String("HCN")){
        delay(100);
        //Disp LCD
        demx = demx + 1; lcd.setCursor(5,1); lcd.print(round(demx));
        if (demx > 5){
           demx = 0; digitalWrite(13,HIGH); delay(200); digitalWrite(13,LOW);
           delay(200);
          }
      }
       
      //Signal Tron 
      else if(str == String("Tron")){
        delay(100);
        //Disp LCD
        demv = demv + 1; lcd.setCursor(15,0); lcd.print(round(demv));
        if (demv > 5){
          demv = 0; digitalWrite(13,HIGH); delay(200); digitalWrite(13,LOW);
          delay(200);
         }
      }
      
      //Signal TamGiac 
      else if(str == String("TamGiac")){
      delay(100);
        //Disp LCD
        demk = demk + 1; lcd.setCursor(15,1); lcd.print(round(demk));
        if (demk > 5){
          demk = 0; digitalWrite(13,HIGH); delay(200); digitalWrite(13,LOW);
          delay(200);
         }
      }
      
      //Signal Unknown
      else
        delay(100);
      }
  
}
