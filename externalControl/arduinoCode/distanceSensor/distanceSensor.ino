#define echoPin 2
#define trigPin 3
#define signalPin 13
#define resPin 5

long duration;
int distance;
int readings[10];
int readingsPointer = 0;
int average = 0;

int maxBallDist = 10;

bool ballDetected = false;


void setup() {
  // put your setup code here, to run once:
  pinMode(trigPin, OUTPUT);
  pinMode(signalPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(resPin, INPUT);
  Serial.begin(9600);
  Serial.println("Ultrasonic sensor");
}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);

  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;

  if (distance > 30) {
    distance = 30;
  }
  
  //Serial.print(distance);
  //Serial.print(" , ");
  
  //addReading();
  //getAverage();
  detectBall();

  if (ballDetected) {
    checkResPin();
  }
}

void addReading() {
  readings[readingsPointer] = distance;
  readingsPointer ++;

  if (readingsPointer > 9) {
    readingsPointer = 0;
  }
}

void printReadings() {
  for (int i = 0; i < maxBallDist; i++) {
    Serial.print("[ ");
    Serial.print(readings[i]);
    Serial.print(" ]");
  }
  Serial.println("  | All readings |");
}

void getAverage() {
  int counter = 0;
  for (int i = 0; i < 10; i++) {
    average = average + readings[i];
    counter ++;
  }
  average = average / counter;
}

void detectBall() {
  if (distance < maxBallDist) {
    Serial.println("Ball! ");
    ballDetected = true;
    digitalWrite(signalPin, HIGH);
  }
}

void detectBallAverage() {
  if (average < 8) {
    Serial.println("Ball! ");
    ballDetected = true;
    digitalWrite(signalPin, HIGH);
  }
}

void checkResPin() {
  if (digitalRead(resPin)) {
    digitalWrite(signalPin, LOW);
    ballDetected = false;
  }
}
