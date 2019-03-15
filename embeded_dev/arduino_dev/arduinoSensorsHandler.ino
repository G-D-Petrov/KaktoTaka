#define         MQ_PIN                       (0)     //define which analog input channel you are going to use
#define         RL_VALUE                     (5)     //define the load resistance on the board, in kilo ohms
#define         RO_CLEAN_AIR_FACTOR          (9.83)  //RO_CLEAR_AIR_FACTOR=(Sensor resistance in clean air)/RO,
                                                     //which is derived from the chart in datasheet
 
/**********************Software Related Macros***********************************/
#define         CALIBARAION_SAMPLE_TIMES     (50)    //define how many samples you are going to take in the calibration phase
#define         CALIBRATION_SAMPLE_INTERVAL  (500)   //define the time interal(in milisecond) between each samples in the
                                                     //cablibration phase
#define         READ_SAMPLE_INTERVAL         (50)    //define how many samples you are going to take in normal operation
#define         READ_SAMPLE_TIMES            (5)     //define the time interal(in milisecond) between each samples in 

const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;                                                   //normal operation
 
/*********************Application Related Macros*********************************/
#define         GAS_LPG                      (0)
#define         GAS_CO                       (1)
#define         GAS_SMOKE                    (2)
 
/****************************Globals**********************************************/
float           LPGCurve[3]  =  {2.3,0.21,-0.47};   //two points are taken from the curve. 
                                                    //with these two points, a line is formed which is "approximately equivalent"
                                                    //to the original curve. 
                                                    //data format:{ x, y, slope}; point1: (lg200, 0.21), point2: (lg10000, -0.59) 
float           COCurve[3]  =  {2.3,0.72,-0.34};    //two points are taken from the curve. 
                                                    //with these two points, a line is formed which is "approximately equivalent" 
                                                    //to the original curve.
                                                    //data format:{ x, y, slope}; point1: (lg200, 0.72), point2: (lg10000,  0.15) 
float           SmokeCurve[3] ={2.3,0.53,-0.44};    //two points are taken from the curve. 
                                                    //with these two points, a line is formed which is "approximately equivalent" 
                                                    //to the original curve.
                                                    //data format:{ x, y, slope}; point1: (lg200, 0.53), point2: (lg10000,  -0.22)                                                     
float           Ro           =  10;                 //Ro is initialized to 10 kilo ohms

// defines pins numbers
const int trigPin = 9;
const int echoPin = 10;
// defines variables
long duration;
int distance;

#include <dht.h>
dht DHT;
#define DHT11_PIN 7

#define DELAY_BETWEEN_MEASURMENTS  (1000)

#define TEMPERATURE_AND_HUMIDITY_SENSOR
#define LIGHT_SENSOR
#define DISTANCE_SENSOR
#define GAS_SENSOR

void setup()
{
  Serial.begin(9600); //UART setup, baudrate = 9600bps
  
  #ifdef GAS_SENSOR
  configureGasSensor();
  #endif 
   
  #ifdef DISTANCE_SENSOR
  configureParktronic();
  #endif
}
 
void loop()
{
  #ifdef TEMPERATURE_AND_HUMIDITY_SENSOR
  printTemperatureAndHumidityValues();
  #endif

  #ifdef LIGHT_SENSOR
  printLightValues();
  #endif

  #ifdef DISTANCE_SENSOR
  printDistanceValues();
  #endif

  #ifdef GAS_SENSOR
  printGasValues();
  #endif

  delay(DELAY_BETWEEN_MEASURMENTS);
}

void printDevice()
{
  Serial.print("#01%");
}

void printLightValues()
{
  printDevice();
  int analogLightValue = analogRead(A1);
  Serial.print("01&"); //Light
  Serial.println(analogLightValue);
}

void printDistanceValues()
{ 
  // Clears the trigPin
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance= duration*0.034/2;
  //Prints the distance on the Serial Monitor
  printDevice();
  Serial.print("02&"); //Distance
  Serial.println(distance);
}

void printGasValues()
{
   printDevice();
   Serial.print("04&"); //LPG
   Serial.print(MQGetGasPercentage(MQRead(MQ_PIN)/Ro,GAS_LPG) );
   Serial.print("\n");   
   printDevice();
   Serial.print("05&"); // CO 
   Serial.print(MQGetGasPercentage(MQRead(MQ_PIN)/Ro,GAS_CO) );
   Serial.print("\n");   
   printDevice();
   Serial.print("06&"); //Smoke 
   Serial.print(MQGetGasPercentage(MQRead(MQ_PIN)/Ro,GAS_SMOKE) );
   Serial.print("\n");
}

void printTemperatureAndHumidityValues()
{
  printDevice();
  int chk = DHT.read11(DHT11_PIN);
  Serial.print("00&"); //Temperature
  Serial.println(DHT.temperature);
  printDevice();
  Serial.print("03&"); //Humidity
  Serial.println(DHT.humidity);
}

void configureGasSensor()
{
  Serial.print("Calibrating...\n");                
  Ro = MQCalibration(MQ_PIN);                       //Calibrating the sensor. Please make sure the sensor is in clean air                  
  Serial.print("Calibration is done...\n"); 
  Serial.print("Ro=");
  Serial.print(Ro);
  Serial.print("kohm");
  Serial.print("\n");  
}

void configureParktronic(){
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
}
 
float MQResistanceCalculation(int raw_adc)
{
  return ( ((float)RL_VALUE*(1023-raw_adc)/raw_adc));
}
 
float MQCalibration(int mq_pin)
{
  int i;
  float val=0;
 
  for (i=0;i<CALIBARAION_SAMPLE_TIMES;i++) {            //take multiple samples
    val += MQResistanceCalculation(analogRead(mq_pin));
    delay(CALIBRATION_SAMPLE_INTERVAL);
  }
  val = val/CALIBARAION_SAMPLE_TIMES;                   //calculate the average value
 
  val = val/RO_CLEAN_AIR_FACTOR;                        //divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                        //according to the chart in the datasheet 
 
  return val; 
}
 
float MQRead(int mq_pin)
{
  int i;
  float rs=0;
 
  for (i=0;i<READ_SAMPLE_TIMES;i++) {
    rs += MQResistanceCalculation(analogRead(mq_pin));
    delay(READ_SAMPLE_INTERVAL);
  }
 
  rs = rs/READ_SAMPLE_TIMES;
 
  return rs;  
}
 
int MQGetGasPercentage(float rs_ro_ratio, int gas_id)
{
  if ( gas_id == GAS_LPG ) {
     return MQGetPercentage(rs_ro_ratio,LPGCurve);
  } else if ( gas_id == GAS_CO ) {
     return MQGetPercentage(rs_ro_ratio,COCurve);
  } else if ( gas_id == GAS_SMOKE ) {
     return MQGetPercentage(rs_ro_ratio,SmokeCurve);
  }    
  return 0;
}
 
int  MQGetPercentage(float rs_ro_ratio, float *pcurve)
{
  return (pow(10,( ((log(rs_ro_ratio)-pcurve[1])/pcurve[2]) + pcurve[0])));
}