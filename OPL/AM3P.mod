/*********************************************
 * OPL 12.6.0.0 Model
 * Author: salfati
 * Creation Date: 06/12/2018 at 11:27:43
 *********************************************/

// Number of Services
int nServices = ...;
range S = 1..nServices;

// Number of Buses
int nBuses = ...;
range B = 1..nBuses;

// Number of Drivers
int nDrivers = ...;
range D = 1..nDrivers;

// Starting time of each Service
int startingTimeService[s in S] = ...;

// Duration time of each Service
int durationTimeService[s in S] = ...;

// Distance (in km) of each Service
float distanceService[s in S] = ...;

// Number of passengers for each Service
int nPassengersService[s in S] = ...;

// Capacity of the Buses
int capacityBus[b in B] = ...;

// Cost of Bus in Euros/Minute
float costBusEurosMin[b in B] = ...;

// Cost of Bus in Euros/KM
float costBusEurosKm[b in B] = ...;

// Max number of minutes that a Driver can work
int maxMinutesDriver[d in D] = ...;

// Max number of Buses we can use
int maxBuses = ...;

// BaseMinutes
int baseMinutes = ...;

// CMB: Cost Base Minutes.
// The Company pays CMB euros for the first BM minutes of work
float CBM = ...;

// CEM: Cost Extra Minutes. (Referred to extra time).
// The Company pays CEM euros for the remaining minutes.
float CEM = ...; 

/********************************
 *		Decision Variables		*
 ********************************/
 
 // Which Bus operates each Service
 dvar boolean x_bs[b in B, s in S];
 
 // Which Driver operates in each Service
 dvar boolean x_ds[d in D, s in S];
 
 // How many minutes each driver works
 dvar int x_min_d[d in D];
 
 // Number of extra minutes that a driver worked
 dvar int x_extra[d in D];
 
 // True if bus b is used
 dvar boolean x_used[b in B];
 
 // Objective function
 dvar float+ z;
 
/****************************
 *			Model			* 
 ****************************/
 
 minimize z;
 
 subject to {
 	
 	// Constraint related to the capacity of the bus in a service
 	forall(b in B, s in S)
 	  	capacityBus[b] >= nPassengersService[s] * x_bs[b, s];
 	  	
 	// Constraints related to the amount of working time for a driver
 	forall(d in D)
 	  	x_min_d[d] + x_extra[d] <= maxMinutesDriver[d];
 	
 	forall(d in D)
 	  	x_min_d[d] + x_extra[d] == sum(s in S) x_ds[d, s] * durationTimeService[s]; 
 
 	forall(d in D)
 	  	x_min_d[d] <= baseMinutes;
 
 	// Restrain the number of buses used
 	forall(b in B)
 	  	nServices * x_used[b] >= sum(s in S) x_bs[b, s];
 	
 	forall(b in B)
 	  	x_used[b] <= maxBuses;
 	
 	// Avoid overlapping
 	forall(s in S, d in D, b in B)
 	  	forall(s2 in S: startingTimeService[s] + durationTimeService[s] < startingTimeService[s2] + durationTimeService[s2])
	 		x_bs[b, s] * (startingTimeService[s] + durationTimeService[s]) <=  x_bs[b, s2] * (startingTimeService[s2] + durationTimeService[s2]);
 	
 	// Checking that all buses are assigned correctly to all services
 	sum(b in B, s in S) x_bs[b, s] == nServices;
 	  	
 	// Checking that all drivers are assigned correctly to all services
 	sum(d in D, s in S)x_ds[d, s] == nServices;
 	  	  	
 	// Objective Function: We want to minimize the cost per time and per km for each bus in service and the cost of the driver
 	z == sum(b in B, s in S) (x_bs[b, s] * (costBusEurosMin[b] * durationTimeService[s] + costBusEurosKm[b] * distanceService[s])) + sum(d in D) (x_min_d[d] * CBM + x_extra[d] * CEM);
 
}
 
 
 
 