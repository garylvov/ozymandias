#include <ros.h>
#include <std_msgs/Int32.h>

#define input_left_A 20  //A-phase-left encoder
#define input_left_B 21  //B-phase-left encoder

#define input_right_A 18  //A-phase-right encoder
#define input_right_B 19  //B-phase-right encoder

#define output_left_A 6
#define output_left_B 5

#define output_right_A 3
#define output_right_B 4

volatile int counter_left = 0;
volatile int counter_right = 0;

volatile int left_motor_speed = 0;
volatile int right_motor_speed = 0;
ros::NodeHandle nh;

void left_motor_callback(const std_msgs::Int32& msg) {
  left_motor_speed = msg.data;
}

void right_motor_callback(const std_msgs::Int32& msg) {
  right_motor_speed = msg.data;
}

std_msgs::Int32 ros_counter_left;
std_msgs::Int32 ros_counter_right;

ros::Publisher left_encoder("left_encoder", &ros_counter_left);
ros::Publisher right_encoder("right_encoder", &ros_counter_right);
ros::Subscriber <std_msgs::Int32> left_motor("left_motor", &left_motor_callback);
ros::Subscriber <std_msgs::Int32> right_motor("right_motor", &right_motor_callback);

void setup() {
  pinMode (input_right_A, INPUT_PULLUP);
  pinMode (input_right_B, INPUT_PULLUP);
  pinMode (input_left_A, INPUT_PULLUP);
  pinMode (input_left_B, INPUT_PULLUP);

  pinMode(output_left_A, OUTPUT);
  pinMode(output_left_B, OUTPUT);
  pinMode(output_right_A, OUTPUT);
  pinMode(output_right_B, OUTPUT);

  attachInterrupt(digitalPinToInterrupt(20), update_left, CHANGE);
  attachInterrupt(digitalPinToInterrupt(18), update_right, CHANGE);

  nh.initNode();
  nh.advertise(left_encoder);
  nh.advertise(right_encoder);
  nh.subscribe(left_motor);
  nh.subscribe(right_motor);
}

void loop() {
  ros_counter_left.data = counter_left;
  ros_counter_right.data = counter_right;
  left_encoder.publish(&ros_counter_left);
  right_encoder.publish(&ros_counter_right);

  if (left_motor_speed > 0) {
    analogWrite(output_left_A, 0);
    analogWrite(output_left_B, abs(left_motor_speed));
  }
  else {
    analogWrite(output_left_A, abs(left_motor_speed));
    analogWrite(output_left_B, 0);
  }

  if (right_motor_speed > 0) {
    analogWrite(output_right_A, abs(right_motor_speed));
    analogWrite(output_right_B, 0);
  }
  else {
    analogWrite(output_right_A, 0);
    analogWrite(output_right_B, abs(right_motor_speed));
  }
  nh.spinOnce();
}

void update_left() {
  if (digitalRead(input_left_B) != digitalRead(input_left_A))
  {
    counter_left --;
  }

  else
  {
    counter_left ++;
  }
}

void update_right() {
  if (digitalRead(input_right_B) != digitalRead(input_right_A))
  {
    counter_right ++;
  }

  else
  {
    counter_right --;
  }
}
