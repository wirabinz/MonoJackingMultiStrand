class CableTensioningSimulation:
    def __init__(self, Zk, nos, lk, KO, Eu, Au):
        self.Zk = Zk
        self.nos = nos
        self.lk = lk
        self.KO = KO
        self.Eu = Eu
        self.Au = Au

    def force_drop(self, strand, strand_jacking_load, current_length, total_shortening, total_force):
        current_length = self.lk - total_shortening
        strain_force_ratio = self.KO * self.Eu * self.Au / (current_length * 1000)
        strand_shortening = self.KO * strand_jacking_load / (1 + (strand - 1) * strain_force_ratio)
        total_shortening = strand_shortening + total_shortening
        total_force = strand_jacking_load / (1 + (strand - 1) * strain_force_ratio) + total_force

        return strain_force_ratio, strand_shortening, total_shortening, current_length, total_force

    def cycle_load_reading(self, final_shortening, total_shortening, strand_jacking_load):
        strand_partial_shortening = final_shortening - total_shortening
        drop_force = strand_partial_shortening * self.Eu * self.Au / (self.lk - total_shortening) / 1000
        reduced_force = strand_jacking_load - drop_force

        return strand_partial_shortening, drop_force, reduced_force

    def perform_cycle_tension(self, strand_jacking_loads,current_length,total_shortening,total_force, initial_jacking_loads):
        # Similar implementation as before

        # Initialize lists to compile results
        strain_force_ratio_list = []
        strand_shortening_list = []
        total_shortening_list = []
        current_length_list = []
        total_force_list = []

        #Calculation of accumulated shortening and total force
        for strand in range(1,len(strand_jacking_loads)+1):
            # Access the jacking load for the current strand index
            strand_jacking_load = strand_jacking_loads[strand - 1]

            # Perform force drop calculation for the current strand
            strain_force_ratio, strand_shortening, total_shortening,    current_length,    total_force = self.force_drop(
                strand, strand_jacking_load, current_length, total_shortening,      total_force
            )

            # Append results to lists
            strain_force_ratio_list.append(strain_force_ratio)
            strand_shortening_list.append(strand_shortening)
            total_shortening_list.append(total_shortening)
            current_length_list.append(current_length)
            total_force_list.append(total_force)

        # print(len(total_shortening_list))
        strand_partial_shortening_list = []
        drop_force_list = []
        reduced_force_list = []

        #Colculating Drop Force and Residual Force
        for strand in range(1,len(initial_jacking_loads)+1):
            #Access the final shortening
            final_shortening=total_shortening_list[-1]

            #Access the total shortening list and strand jacking load 
            total_shortening=total_shortening_list[strand- 1]
            strand_jacking_load=initial_jacking_loads[strand - 1]

            strand_partial_shortening, drop_force, reduced_force =  self.cycle_load_reading(final_shortening,total_shortening,    strand_jacking_load) 

            #append result to List 
            strand_partial_shortening_list.append(strand_partial_shortening)
            drop_force_list.append(drop_force)
            reduced_force_list.append(reduced_force)

        return drop_force_list, current_length_list, total_shortening_list,     total_force_list,reduced_force_list

    def tensioning_simulation(self,cycle_number,strand_jacking_loads,current_length, total_shortening,total_force,initial_jacking_loads):

        for i in range(cycle_number):
            drop_force_list, current_length_list, total_shortening_list,    total_force_list,reduced_force_list=self.perform_cycle_tension  (strand_jacking_loads,current_length,total_shortening,total_force,    initial_jacking_loads)

            #Extracting previous tension result for the next tensioning cycle
            strand_jacking_loads = drop_force_list
            current_length=current_length_list[-1]
            total_shortening=total_shortening_list[-1]
            total_force=total_force_list[-1]

        return reduced_force_list,drop_force_list,current_length_list,  total_shortening_list
    

# Initial data

Zk=1200  #kN
dv=15.98  #mm
theta=53.3 #degree
lk = 60000 #mm
Xik =60 #mm
KO = Xik/Zk #mm/kN
Eu = 194000 #MPa
Au = 150 #mm^2
nos = 12

# Calculate strand jacking load
strand_tensioning = Zk / nos

# Create a list of strand jacking loads
initial_jacking_loads = [strand_tensioning] * nos
strand_jacking_loads=initial_jacking_loads

#initial input
current_length=lk
total_shortening=0
total_force=0
cycle_number = 4


# Initialize the simulation object
simulation = CableTensioningSimulation(Zk, nos, lk, KO, Eu, Au)

reduced_force_list,drop_force_list,current_length_list, total_shortening_list=simulation.tensioning_simulation(cycle_number,strand_jacking_loads,current_length,total_shortening,total_force, initial_jacking_loads)

print(reduced_force_list)
print(drop_force_list)
print(current_length_list)
print(total_shortening_list)