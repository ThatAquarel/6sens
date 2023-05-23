#define COLS 8
#define ROWS 6

const int a[3] = {D7, D8, D9};
const int r[6] = {D1, D2, D3, D4, D5, D6};
const int enable = D0;

void setup() {
  for (int i = 0; i < 3; i++) {
    pinMode(a[i], OUTPUT);
    digitalWrite(a[i], HIGH);
  }
  for (int i = 0; i < ROWS; i++) {
    pinMode(r[i], OUTPUT);
    digitalWrite(r[i], HIGH);
  }
  
  pinMode(enable, OUTPUT);
  digitalWrite(enable, HIGH);
}

void loop() {
  for (int col = 0; col < COLS; col++) {
    for (int j = 0; j < 3; j++){
      digitalWrite(a[j], (1 << j) & (~col));
    }
    
    digitalWrite(r[5], LOW);
    delay(50);
    digitalWrite(r[5], HIGH);
  
    // for (int row = 0; row < ROWS; row++) {
    //   digitalWrite(r[row], LOW);
    //   delay(50);
    //   digitalWrite(r[row], HIGH);
    // }
  }
}
