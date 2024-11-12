#include "lsolve.h"
#include "version.h"
#include "model.h"
#include <stdio.h>
#include <math.h>

void initialEquations(CBD* cbd) {
	Real delta = 0.0001;
	_Controller_Err_Negate_IN1 = _Controller_IN;
	_Controller_Err_Negate_OUT1 = (-_Controller_Err_Negate_IN1);
	_Controller_Err_setPoint_OUT1 = 10.0;
	_Controller_Err__Err_IN2 = _Controller_Err_setPoint_OUT1;
	_Controller_Err__Err_IN1 = _Controller_Err_Negate_OUT1;
	_Controller_Err__Err_OUT1 = (_Controller_Err__Err_IN1 + _Controller_Err__Err_IN2);
	_Controller_P__Kp_OUT1 = 15.0;
	_Controller_P__P_IN2 = _Controller_P__Kp_OUT1;
	_Controller_P__P_IN1 = _Controller_Err__Err_OUT1;
	_Controller_P__P_OUT1 = (_Controller_P__P_IN1 * _Controller_P__P_IN2);
	_Controller_I__I__zero_OUT1 = 0;
	_Controller_I__I__delayIn_IC = _Controller_I__I__zero_OUT1;
	_Controller_I__I__delayIn_OUT1 = _Controller_I__I__delayIn_IC;
	_Controller_I__I__delayIn_IN1 = _Controller_Err__Err_OUT1;
	_Controller_I__I__delta_t_OUT1 = delta;
	_Controller_I__I__multDelta_IN2 = _Controller_I__I__delta_t_OUT1;
	_Controller_I__I__multDelta_IN1 = _Controller_I__I__delayIn_OUT1;
	_Controller_I__I__multDelta_OUT1 = (_Controller_I__I__multDelta_IN1 * _Controller_I__I__multDelta_IN2);
	_Controller_I__I_init_OUT1 = 0;
	_Controller_I__I__delayState_IC = _Controller_I__I_init_OUT1;
	_Controller_I__I__delayState_OUT1 = _Controller_I__I__delayState_IC;
	_Controller_I__I__delayState_IN1 = _Controller_I__I__sumState_OUT1;
	_Controller_I__I__sumState_IN2 = _Controller_I__I__delayState_OUT1;
	_Controller_I__I__sumState_IN1 = _Controller_I__I__multDelta_OUT1;
	_Controller_I__I__sumState_OUT1 = (_Controller_I__I__sumState_IN1 + _Controller_I__I__sumState_IN2);
	_Controller_I__Ki_OUT1 = 1.0;
	_Controller_I__P_IN2 = _Controller_I__Ki_OUT1;
	_Controller_I__P_IN1 = _Controller_I__I__sumState_OUT1;
	_Controller_I__P_OUT1 = (_Controller_I__P_IN1 * _Controller_I__P_IN2);
	_Controller_D__D_init_OUT1 = 0;
	_Controller_D__D__delta_t_OUT1 = delta;
	_Controller_D__D__multIc_IN2 = _Controller_D__D__delta_t_OUT1;
	_Controller_D__D__multIc_IN1 = _Controller_D__D_init_OUT1;
	_Controller_D__D__multIc_OUT1 = (_Controller_D__D__multIc_IN1 * _Controller_D__D__multIc_IN2);
	_Controller_D__D__neg1_IN1 = _Controller_D__D__multIc_OUT1;
	_Controller_D__D__neg1_OUT1 = (-_Controller_D__D__neg1_IN1);
	_Controller_D__D__sum1_IN2 = _Controller_Err__Err_OUT1;
	_Controller_D__D__sum1_IN1 = _Controller_D__D__neg1_OUT1;
	_Controller_D__D__sum1_OUT1 = (_Controller_D__D__sum1_IN1 + _Controller_D__D__sum1_IN2);
	_Controller_D__D__delay_IC = _Controller_D__D__sum1_OUT1;
	_Controller_D__D__delay_OUT1 = _Controller_D__D__delay_IC;
	_Controller_D__D__delay_IN1 = _Controller_Err__Err_OUT1;
	_Controller_D__D__neg2_IN1 = _Controller_D__D__delay_OUT1;
	_Controller_D__D__neg2_OUT1 = (-_Controller_D__D__neg2_IN1);
	_Controller_D__D__sum2_IN2 = _Controller_Err__Err_OUT1;
	_Controller_D__D__sum2_IN1 = _Controller_D__D__neg2_OUT1;
	_Controller_D__D__sum2_OUT1 = (_Controller_D__D__sum2_IN1 + _Controller_D__D__sum2_IN2);
	_Controller_D__D__inv_IN1 = _Controller_D__D__delta_t_OUT1;
	_Controller_D__D__inv_OUT1 = 1.0/_Controller_D__D__inv_IN1;
	_Controller_D__D__mult_IN2 = _Controller_D__D__inv_OUT1;
	_Controller_D__D__mult_IN1 = _Controller_D__D__sum2_OUT1;
	_Controller_D__D__mult_OUT1 = (_Controller_D__D__mult_IN1 * _Controller_D__D__mult_IN2);
	_Controller_D__Kd_OUT1 = 22.0;
	_Controller_D__P_IN2 = _Controller_D__Kd_OUT1;
	_Controller_D__P_IN1 = _Controller_D__D__mult_OUT1;
	_Controller_D__P_OUT1 = (_Controller_D__P_IN1 * _Controller_D__P_IN2);
	_Controller_Sum_IN3 = _Controller_D__P_OUT1;
	_Controller_Sum_IN2 = _Controller_I__P_OUT1;
	_Controller_Sum_IN1 = _Controller_P__P_OUT1;
	_Controller_Sum_OUT1 = (_Controller_Sum_IN1 + _Controller_Sum_IN2 + _Controller_Sum_IN3);
	_Controller_OUT = _Controller_Sum_OUT1;

	cbd->time_last = cbd->time;
}

void calculateEquations(CBD* cbd) {
	Real delta = cbd->time - cbd->time_last;

	_Controller_Err_Negate_IN1 = _Controller_IN;
	_Controller_Err_Negate_OUT1 = (-_Controller_Err_Negate_IN1);
	_Controller_Err_setPoint_OUT1 = 10.0;
	_Controller_Err__Err_IN2 = _Controller_Err_setPoint_OUT1;
	_Controller_Err__Err_IN1 = _Controller_Err_Negate_OUT1;
	_Controller_Err__Err_OUT1 = (_Controller_Err__Err_IN1 + _Controller_Err__Err_IN2);
	_Controller_P__Kp_OUT1 = 15.0;
	_Controller_P__P_IN2 = _Controller_P__Kp_OUT1;
	_Controller_P__P_IN1 = _Controller_Err__Err_OUT1;
	_Controller_P__P_OUT1 = (_Controller_P__P_IN1 * _Controller_P__P_IN2);
	_Controller_I__I__delayIn_OUT1 = _Controller_I__I__delayIn_IN1;
	_Controller_I__I__delta_t_OUT1 = delta;
	_Controller_I__I__multDelta_IN2 = _Controller_I__I__delta_t_OUT1;
	_Controller_I__I__multDelta_IN1 = _Controller_I__I__delayIn_OUT1;
	_Controller_I__I__multDelta_OUT1 = (_Controller_I__I__multDelta_IN1 * _Controller_I__I__multDelta_IN2);
	_Controller_I__I__delayState_OUT1 = _Controller_I__I__delayState_IN1;
	_Controller_I__I__sumState_IN2 = _Controller_I__I__delayState_OUT1;
	_Controller_I__I__sumState_IN1 = _Controller_I__I__multDelta_OUT1;
	_Controller_I__I__sumState_OUT1 = (_Controller_I__I__sumState_IN1 + _Controller_I__I__sumState_IN2);
	_Controller_I__Ki_OUT1 = 1.0;
	_Controller_I__P_IN2 = _Controller_I__Ki_OUT1;
	_Controller_I__P_IN1 = _Controller_I__I__sumState_OUT1;
	_Controller_I__P_OUT1 = (_Controller_I__P_IN1 * _Controller_I__P_IN2);
	_Controller_D__D__delay_OUT1 = _Controller_D__D__delay_IN1;
	_Controller_D__D__neg2_IN1 = _Controller_D__D__delay_OUT1;
	_Controller_D__D__neg2_OUT1 = (-_Controller_D__D__neg2_IN1);
	_Controller_D__D__sum2_IN2 = _Controller_Err__Err_OUT1;
	_Controller_D__D__sum2_IN1 = _Controller_D__D__neg2_OUT1;
	_Controller_D__D__sum2_OUT1 = (_Controller_D__D__sum2_IN1 + _Controller_D__D__sum2_IN2);
	_Controller_D__D__delta_t_OUT1 = delta;
	_Controller_D__D__inv_IN1 = _Controller_D__D__delta_t_OUT1;
	_Controller_D__D__inv_OUT1 = 1.0/_Controller_D__D__inv_IN1;
	_Controller_D__D__mult_IN2 = _Controller_D__D__inv_OUT1;
	_Controller_D__D__mult_IN1 = _Controller_D__D__sum2_OUT1;
	_Controller_D__D__mult_OUT1 = (_Controller_D__D__mult_IN1 * _Controller_D__D__mult_IN2);
	_Controller_D__Kd_OUT1 = 22.0;
	_Controller_D__P_IN2 = _Controller_D__Kd_OUT1;
	_Controller_D__P_IN1 = _Controller_D__D__mult_OUT1;
	_Controller_D__P_OUT1 = (_Controller_D__P_IN1 * _Controller_D__P_IN2);
	_Controller_Sum_IN3 = _Controller_D__P_OUT1;
	_Controller_Sum_IN2 = _Controller_I__P_OUT1;
	_Controller_Sum_IN1 = _Controller_P__P_OUT1;
	_Controller_Sum_OUT1 = (_Controller_Sum_IN1 + _Controller_Sum_IN2 + _Controller_Sum_IN3);
	_Controller_I__I_init_OUT1 = 0;
	_Controller_I__I__zero_OUT1 = 0;
	_Controller_D__D_init_OUT1 = 0;
	_Controller_D__D__multIc_IN2 = _Controller_D__D__delta_t_OUT1;
	_Controller_D__D__multIc_IN1 = _Controller_D__D_init_OUT1;
	_Controller_D__D__multIc_OUT1 = (_Controller_D__D__multIc_IN1 * _Controller_D__D__multIc_IN2);
	_Controller_D__D__neg1_IN1 = _Controller_D__D__multIc_OUT1;
	_Controller_D__D__neg1_OUT1 = (-_Controller_D__D__neg1_IN1);
	_Controller_D__D__sum1_IN2 = _Controller_Err__Err_OUT1;
	_Controller_D__D__sum1_IN1 = _Controller_D__D__neg1_OUT1;
	_Controller_D__D__sum1_OUT1 = (_Controller_D__D__sum1_IN1 + _Controller_D__D__sum1_IN2);
	_Controller_D__D__delay_IN1 = _Controller_Err__Err_OUT1;
	_Controller_D__D__delay_IC = _Controller_D__D__sum1_OUT1;
	_Controller_I__I__delayState_IN1 = _Controller_I__I__sumState_OUT1;
	_Controller_I__I__delayState_IC = _Controller_I__I_init_OUT1;
	_Controller_I__I__delayIn_IN1 = _Controller_Err__Err_OUT1;
	_Controller_I__I__delayIn_IC = _Controller_I__I__zero_OUT1;
	_Controller_OUT = _Controller_Sum_OUT1;

	cbd->time_last = cbd->time;
}

void getContinuousStates(CBD* cbd, double x[], size_t nx) {
}

void setContinuousStates(CBD* cbd, const double x[], size_t nx) {
//	calculateEquations(cbd);
}

void getDerivatives(CBD* cbd, double dx[], size_t nx) {
//	calculateEquations(cbd);
}

void getStateEvents(CBD* cbd, double z[], size_t nz) {
	// No state events found
}

void stateEvent(CBD* cbd) {
	// No state events found
	cbd->nominalsOfContinuousStatesChanged = False;
	cbd->terminateSimulation = False;
	cbd->nextEventTimeDefined = False;
}

Status doStep(CBD* cbd, double t, double tNext) {
	// No state events found
	Boolean timeEvent;


	double h = tNext - t;
	while(cbd->time + h < tNext + 0.01 * h) {

		timeEvent = cbd->nextEventTimeDefined && cbd->time >= cbd->nextEventTime;

		if(timeEvent) {
			stateEvent(cbd);
		}

		if(cbd->terminateSimulation) {
			// Force termination
			return Discard;
		}
		cbd->time += h;
		calculateEquations(cbd);
	}

	return OK;
}

