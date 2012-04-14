#coding=utf-8
from __future__ import division

import unittest

from measurement import *
from measurement.united_states_customary import *

import arithmetic

class ElectronicsTestCase(unittest.TestCase):
    "These tests take (paraphrased) examples of electronics calculations to act as 'user story' tests for measurement.  These examples "
    "were taken from the fantastic book 'Practical Electronics for Inventors', by Paul Scherz."
    
    def testElectronsFlowingThroughAWire(self):
        "The when 1 Amp of current is moving through a wire, there are about 6.24e18 electrons flowing per second through a cross-section. (PEfI, p. 7)"
        arithmetic.assert_close((1 * Ampere) / -ElementaryCharge, 
                                -6.24150964712e+18 / Second)
        
    def testElectronsFlowingThroughAWireOverTime(self):
        "How many electrons pass a given point in 3s if a conductor is carrying a 2A current?  About 3.74e19. (PEfI, p. 8)"
        arithmetic.assert_close(((2 * Ampere) * (3 * Second)) / -ElementaryCharge,
                                -3.74490578827e+19 * One)
    
    def testGeneralizedPowerLaw1(self):
        "A 1.5V flashlight circuit draws 0.1A.  How much power does the circuit consume?  0.15W. (PEfI, p. 15)"
        arithmetic.assert_close((1.5 * Volt) * (0.1 * Ampere), 0.15 * Watt)
    
    def testGeneralizedPowerLaw2(self):
        "A 12V device is rated at 100W.  How much current does it draw?  8.333A.  (PEfI, p. 15)"
        arithmetic.assert_close((100 * Watt) / (12 * Volt), 8.33333333333 * Ampere)
    
    def testResistanceAndOhmicHeatingOfMetalRods(self):
        "Determine the resistance of the following four round rods of material, each 1m long and 1mm radius: "
        "copper, brass, stainless steel, and graphite; also, how much power is lost to heating if a current of 0.2A"
        "flows through each one. (PEfI, pp. 33-34)"
        def resistance_of_rod(resistivity, length, radius):
            return resistivity * (length / (Pi * radius**2))
        def ohmic_heating(current, resistance):
            return (current**2) * resistance
        
        resistivity = {
                       "copper": 1.72e-8 * (Ohm * Meter),
                       "brass": 7e-8 * (Ohm * Meter),
                       "stainless steel": 7.2e-7 * (Ohm * Meter),
                       "graphite": 3.5e-5 * (Ohm * Meter)
                       }
        
        arithmetic.assert_close(resistance_of_rod(resistivity["copper"], 1 * Meter, 1 * (Milli * Meter)),
                                5.48e-3 * Ohm, tolerance = 0.001)
        arithmetic.assert_close(ohmic_heating(0.2 * Ampere, resistance_of_rod(resistivity["copper"], 1 * Meter, 1 * (Milli * Meter))),
                                2.2e-4 * Watt, tolerance = 0.005)
        
        arithmetic.assert_close(resistance_of_rod(resistivity["brass"], 1 * Meter, 1 * (Milli * Meter)),
                                2.23e-2 * Ohm, tolerance = 0.001)
        arithmetic.assert_close(ohmic_heating(0.2 * Ampere, resistance_of_rod(resistivity["brass"], 1 * Meter, 1 * (Milli * Meter))),
                                8.9e-4 * Watt, tolerance = 0.002)
        
        arithmetic.assert_close(resistance_of_rod(resistivity["stainless steel"], 1 * Meter, 1 * (Milli * Meter)),
                                2.31e-1 * Ohm, tolerance = 0.008)
        arithmetic.assert_close(ohmic_heating(0.2 * Ampere, resistance_of_rod(resistivity["stainless steel"], 1 * Meter, 1 * (Milli * Meter))),
                                9.2e-3 * Watt, tolerance = 0.004)
        
        arithmetic.assert_close(resistance_of_rod(resistivity["graphite"], 1 * Meter, 1 * (Milli * Meter)),
                                11.1 * Ohm, tolerance = 0.004)
        arithmetic.assert_close(ohmic_heating(0.2 * Ampere, resistance_of_rod(resistivity["graphite"], 1 * Meter, 1 * (Milli * Meter))),
                                0.44 * Watt, tolerance = 0.02)
    
    def testThermalConduction(self):
        "Given a thin-film resistor in an integrated circuit, of area 0.1\"x0.2\", with a 0.025\" thick alumina ceramic, "
        "a 0.002\" thick layer of silicon grease, and a 0.125\" thick aluminum ground plane...how hot will it get with "
        "2 W dissipated over it's surface (100 W/in²), assuming the ground plane is at 80°C. (PEfI, p.38)"
        
        thermal_resistivities = {
                                 "alumina ceramic": 2.13 * ((Celsius * Inch) / Watt),
                                 "silicon grease": 46.0 * ((Celsius * Inch) / Watt),
                                 "aluminum": 0.23  * ((Celsius * Inch) / Watt)
                                 }
        
        resistor_area = (0.1 * Inch) * (0.2 * Inch)
        resistor_layers = [
                            ("alumina ceramic", 0.025 * Inch),
                            ("silicon grease", 0.002 * Inch),
                            ("aluminum", 0.125 * Inch)
                          ]
    
        def heat_transfer_through_solid(thermal_resistivity, length, cross_sectional_area, power):
            return thermal_resistivity * (length / cross_sectional_area) * power
        
        total_temperature_transfer = 0 * Celsius
        for resistor_layer in resistor_layers:
            total_temperature_transfer += heat_transfer_through_solid(thermal_resistivities[resistor_layer[0]],
                                                                      resistor_layer[1],
                                                                      resistor_area,
                                                                      2 * Watt)
        arithmetic.assert_close(total_temperature_transfer, 17.4 * Celsius)
        arithmetic.assert_close(total_temperature_transfer + 80 * Celsius, 97.4 * Celsius)
    
    def testResistorPowerRatings1(self):
        "Using an ammeter you measure a current of 1.0 mA through a 4.7 kΩ resistor.  What voltage must exist across "
        "the resistor?  How much power does the resistor dissipate? (PEfI, p. 52)"
        current = 1.0 * (Milli*Ampere)
        resistance = 4.7 * (Kilo*Ohm)
        
        arithmetic.assert_close(current * resistance, 4.7 * Volt)
        arithmetic.assert_close(current**2 * resistance, (4.7 * (Milli*Watt)))
    
    def testResistorPowerRatings2(self):
        "Using a voltmeter you measure 24 V across an unmarked resistor.  With an ammeter, you measure "
        "a current of 50 mA.  Determine the resistance and power generated by the resistor. (PEfI, p. 52)"
        voltage = 24 * Volt
        current = 50 * (Milli*Ampere)
        
        arithmetic.assert_close(voltage / current, 480 * Ohm)
        arithmetic.assert_close(voltage * current, 1.2 * Watt)
    
    def testResistorPowerRatings3(self):
        "You apply 3 V to a 1 MΩ resistor.  Find the current through the resistor and the "
        "power dissipated in teh process. (PEfI, p. 52)"
        voltage = 3 * Volt
        resistance = 1 * (Mega*Ohm)
        
        arithmetic.assert_close(voltage / resistance, 3 * (Micro*Ampere))
        arithmetic.assert_close(voltage**2 / resistance, 9 * (Milli*Watt))
    
    def testResistorPowerRatings3(self):
        "You are given 2 Ω, 100 Ω, 3 kΩ, 68 kΩ, and 1 MΩ resistors, all with 1 W power ratings.  What's the "
        "maximum voltage that can be applied without exceeding their power ratings?"
        
        arithmetic.assert_close(((1 * Watt) * (2 * Ohm))**0.5, 1.4 * Volt, tolerance = 0.02)
        arithmetic.assert_close(((1 * Watt) * (100 * Ohm))**0.5, 10.0 * Volt)
        arithmetic.assert_close(((1 * Watt) * (3 * (Kilo*Ohm)))**0.5, 57.4 * Volt, tolerance = 0.05)
        arithmetic.assert_close(((1 * Watt) * (68 * (Kilo*Ohm)))**0.5, 260.7 * Volt, tolerance = 0.0003)
        arithmetic.assert_close(((1 * Watt) * (1 * (Mega*Ohm)))**0.5, 1000.0 * Volt)
