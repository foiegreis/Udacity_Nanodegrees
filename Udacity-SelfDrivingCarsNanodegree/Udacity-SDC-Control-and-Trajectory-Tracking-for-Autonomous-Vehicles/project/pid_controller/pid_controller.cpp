/**********************************************
 * Self-Driving Car Nano-degree - Udacity
 *  Created on: December 11, 2020
 *      Author: Mathilde Badoual
 **********************************************/

#include "pid_controller.h"
#include <vector>
#include <iostream>
#include <math.h>

using namespace std;

PID::PID() {}

PID::~PID() {}

void PID::Init(double Kpi, double Kii, double Kdi, double output_lim_maxi, double output_lim_mini) {
   //Initialize PID coefficients (and errors, if needed)
   
   //Parameters
   Kp = Kpi;
   Kd = Kdi;
   Ki = Kii;
   
   //Output limits
   output_lim_max = output_lim_maxi;
   output_lim_min = output_lim_mini;
   
   //Errors
    cte_previous = 0.0;
    cte_derivative = 0.0;
    cte_integral = 0.0;
   
}


void PID::UpdateError(double cte) {
   //Update PID errors based on cte.
  
    cte_previous = cte;
    cte_derivative = (cte - cte_previous) / dt;
    cte_integral += cte * dt;
}

double PID::TotalError() {
  // Calculate and return the total error
  //The code should return a value in the interval [output_lim_mini, output_lim_maxi]
  
  double control = Kp*cte_previous + Kd*cte_derivative + Ki*cte_integral;

  //Ensure limits
  control = max(min(control, output_lim_max), output_lim_min);

  std::cout<<"New control: "<<control<<" - with Kp: "<<Kp<<", Kd: "<<Kd<<", Ki: "<<Ki<<std::endl;

  return control;
}

double PID::UpdateDeltaTime(double new_delta_time) {
   // Update the delta time with new value
   if (new_delta_time ==0){
    cout<<"***Warning delta time provided as 0, using default value 1***"<<endl;
   }
   dt = new_delta_time > 0? new_delta_time : 1;
}
