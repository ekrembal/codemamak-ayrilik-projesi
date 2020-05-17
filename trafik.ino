#define kirmizi 13
#define yesil 12
#define kirmizi2 11
#define yesil2  10

void yak(int x){digitalWrite(x, HIGH);digitalWrite(x - 2, LOW);}
void sondur(int x){digitalWrite(x, LOW);digitalWrite(x - 2, HIGH);}

int yesildenSonra = 0;
bool arabaGeldiMi = false;

void setup() {
  Serial.begin(115200);

  pinMode(kirmizi, OUTPUT);
  pinMode(yesil, OUTPUT);
  pinMode(kirmizi2, OUTPUT);
  pinMode(yesil2, OUTPUT);
  
  yak(yesil);
  delay(1000);
  sondur(yesil);

  yak(kirmizi);
}

void yesilYak(){
  delay(1000);
  yak(yesil);
  sondur(kirmizi);
  delay(1000);
  bool flag = 1;
  int say = 0;
  while(flag == true and say < 3){
    say++;
    flag = false;
    for(int i = 1; i <= 10; i++){
     delay(100);
     if(Serial.available() > 0 and Serial.read() == 'H')
      flag = true;
   }
  }
  sondur(yesil);
  yak(kirmizi);
  yesildenSonra = 0;
  arabaGeldiMi = false;
}

void loop() {
  if(arabaGeldiMi == true and yesildenSonra > 50)
    yesilYak();
  if (Serial.available() > 0 and Serial.read() == 'H'){
    arabaGeldiMi = true;
    if(yesildenSonra > 50)
      yesilYak();
  }
  // delay(100);
  yesildenSonra++;
}
