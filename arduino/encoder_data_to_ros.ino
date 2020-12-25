//12/24/2020
#define input_left_A 20  //A-phase-left encoder
#define input_left_B 21  //B-phase-left encoder

#define input_right_A 18  //A-phase-right encoder
#define input_right_B 19  //B-phase-right encoder

#include <ros.h>
#include <std_msgs/Int32.h>

ros::NodeHandle nh;
std_msgs::Int32 ros_counter_left;
std_msgs::Int32 ros_counter_right;

ros::Publisher left_encoder("left_encoder", &ros_counter_left);
ros::Publisher right_encoder("right_encoder", &ros_counter_right);

volatile int counter_left = 0;
volatile int counter_right = 0;

void setup() {
  pinMode (input_right_A, INPUT_PULLUP);
  pinMode (input_right_B, INPUT_PULLUP);
  pinMode (input_left_A, INPUT_PULLUP);
  pinMode (input_left_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(20), update_left, CHANGE);
  attachInterrupt(digitalPinToInterrupt(18), update_right, CHANGE);

  nh.initNode();
  nh.advertise(left_encoder);
  nh.advertise(right_encoder);
}

void loop() {
  ros_counter_left.data = counter_left;
  ros_counter_right.data = counter_right;
  left_encoder.publish(&ros_counter_left);
  right_encoder.publish(&ros_counter_right);
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
