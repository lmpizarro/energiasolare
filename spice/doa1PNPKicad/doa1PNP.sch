EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:special
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:doa1PNP-cache
EELAYER 27 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date "24 may 2017"
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L BC557 Q3
U 1 1 592443ED
P 3600 3000
F 0 "Q3" H 3600 2851 40  0000 R CNN
F 1 "BC557" H 3600 3150 40  0000 R CNN
F 2 "TO92" H 3500 3102 29  0000 C CNN
F 3 "" H 3600 3000 60  0000 C CNN
	1    3600 3000
	-1   0    0    1   
$EndComp
$Comp
L BC557 Q4
U 1 1 592443FA
P 4350 3000
F 0 "Q4" H 4350 2851 40  0000 R CNN
F 1 "BC557" H 4350 3150 40  0000 R CNN
F 2 "TO92" H 4250 3102 29  0000 C CNN
F 3 "" H 4350 3000 60  0000 C CNN
	1    4350 3000
	1    0    0    1   
$EndComp
$Comp
L BC557 Q2CS1
U 1 1 5924441E
P 3400 2300
F 0 "Q2CS1" H 3400 2151 40  0000 R CNN
F 1 "BC557" H 3400 2450 40  0000 R CNN
F 2 "TO92" H 3300 2402 29  0000 C CNN
F 3 "" H 3400 2300 60  0000 C CNN
	1    3400 2300
	1    0    0    1   
$EndComp
$Comp
L DIODE D2
U 1 1 59244502
P 3200 2100
F 0 "D2" H 3200 2200 40  0000 C CNN
F 1 "DIODE" H 3200 2000 40  0000 C CNN
F 2 "~" H 3200 2100 60  0000 C CNN
F 3 "~" H 3200 2100 60  0000 C CNN
	1    3200 2100
	0    1    1    0   
$EndComp
$Comp
L DIODE D1
U 1 1 5924451E
P 3200 1700
F 0 "D1" H 3200 1800 40  0000 C CNN
F 1 "DIODE" H 3200 1600 40  0000 C CNN
F 2 "~" H 3200 1700 60  0000 C CNN
F 3 "~" H 3200 1700 60  0000 C CNN
	1    3200 1700
	0    1    1    0   
$EndComp
$Comp
L R R1
U 1 1 59244524
P 3500 1850
F 0 "R1" V 3580 1850 40  0000 C CNN
F 1 "R" V 3507 1851 40  0000 C CNN
F 2 "~" V 3430 1850 30  0000 C CNN
F 3 "~" H 3500 1850 30  0000 C CNN
	1    3500 1850
	1    0    0    -1  
$EndComp
$Comp
L R R3
U 1 1 5924462B
P 3500 4150
F 0 "R3" V 3580 4150 40  0000 C CNN
F 1 "R" V 3507 4151 40  0000 C CNN
F 2 "~" V 3430 4150 30  0000 C CNN
F 3 "~" H 3500 4150 30  0000 C CNN
	1    3500 4150
	1    0    0    -1  
$EndComp
$Comp
L R R5
U 1 1 59244760
P 4450 4150
F 0 "R5" V 4530 4150 40  0000 C CNN
F 1 "R" V 4457 4151 40  0000 C CNN
F 2 "~" V 4380 4150 30  0000 C CNN
F 3 "~" H 4450 4150 30  0000 C CNN
	1    4450 4150
	1    0    0    -1  
$EndComp
Wire Wire Line
	2000 1500 6800 1500
Wire Wire Line
	3500 1500 3500 1600
Wire Wire Line
	3500 2500 3500 2800
Connection ~ 3500 2800
Wire Wire Line
	3500 3900 3500 3200
Wire Wire Line
	4450 3200 4450 3900
Connection ~ 4450 2800
Wire Wire Line
	2000 4400 6800 4400
$Comp
L CONN_1 Vi1
U 1 1 59244A24
P 3800 3150
F 0 "Vi1" H 3880 3150 40  0000 L CNN
F 1 "CONN_1" H 3800 3205 30  0001 C CNN
F 2 "" H 3800 3150 60  0000 C CNN
F 3 "" H 3800 3150 60  0000 C CNN
	1    3800 3150
	0    1    1    0   
$EndComp
$Comp
L CONN_1 Vi2
U 1 1 59244A4A
P 4150 3150
F 0 "Vi2" H 4230 3150 40  0000 L CNN
F 1 "CONN_1" H 4150 3205 30  0001 C CNN
F 2 "" H 4150 3150 60  0000 C CNN
F 3 "" H 4150 3150 60  0000 C CNN
	1    4150 3150
	0    1    1    0   
$EndComp
$Comp
L R R6
U 1 1 59244AA0
P 2500 2550
F 0 "R6" V 2580 2550 40  0000 C CNN
F 1 "R" V 2507 2551 40  0000 C CNN
F 2 "~" V 2430 2550 30  0000 C CNN
F 3 "~" H 2500 2550 30  0000 C CNN
	1    2500 2550
	1    0    0    -1  
$EndComp
Wire Wire Line
	3200 2300 2500 2300
Wire Wire Line
	2500 2800 2500 4400
Connection ~ 3500 4400
$Comp
L CONN_1 VEE1
U 1 1 59244B6B
P 2850 4550
F 0 "VEE1" H 2930 4550 40  0000 L CNN
F 1 "CONN_1" H 2850 4605 30  0001 C CNN
F 2 "" H 2850 4550 60  0000 C CNN
F 3 "" H 2850 4550 60  0000 C CNN
	1    2850 4550
	0    1    1    0   
$EndComp
$Comp
L CONN_1 VCC1
U 1 1 59244B71
P 3200 1350
F 0 "VCC1" H 3280 1350 40  0000 L CNN
F 1 "CONN_1" H 3200 1405 30  0001 C CNN
F 2 "" H 3200 1350 60  0000 C CNN
F 3 "" H 3200 1350 60  0000 C CNN
	1    3200 1350
	0    -1   -1   0   
$EndComp
Connection ~ 2850 4400
Connection ~ 3200 1500
$Comp
L CONN_1 GND1
U 1 1 592466DC
P 1750 3050
F 0 "GND1" H 1830 3050 40  0000 L CNN
F 1 "CONN_1" H 1750 3105 30  0001 C CNN
F 2 "" H 1750 3050 60  0000 C CNN
F 3 "" H 1750 3050 60  0000 C CNN
	1    1750 3050
	-1   0    0    1   
$EndComp
Text Label 1900 3050 0    60   ~ 0
gnd
$Comp
L CP C2
U 1 1 59246751
P 2000 4200
F 0 "C2" H 2050 4300 40  0000 L CNN
F 1 "CP" H 2050 4100 40  0000 L CNN
F 2 "~" H 2100 4050 30  0000 C CNN
F 3 "~" H 2000 4200 300 0000 C CNN
	1    2000 4200
	1    0    0    -1  
$EndComp
Connection ~ 2500 4400
Wire Wire Line
	1900 3050 2000 3050
Wire Wire Line
	2000 1900 2000 4000
Connection ~ 2000 3050
$Comp
L CP C1
U 1 1 59246817
P 2000 1700
F 0 "C1" H 2050 1800 40  0000 L CNN
F 1 "CP" H 2050 1600 40  0000 L CNN
F 2 "~" H 2100 1550 30  0000 C CNN
F 3 "~" H 2000 1700 300 0000 C CNN
	1    2000 1700
	1    0    0    -1  
$EndComp
$Comp
L BC557 Q6CS2
U 1 1 59247390
P 5450 2300
F 0 "Q6CS2" H 5450 2151 40  0000 R CNN
F 1 "BC557" H 5450 2450 40  0000 R CNN
F 2 "TO92" H 5350 2402 29  0000 C CNN
F 3 "" H 5450 2300 60  0000 C CNN
	1    5450 2300
	1    0    0    1   
$EndComp
$Comp
L R R8
U 1 1 592473A2
P 5550 1850
F 0 "R8" V 5630 1850 40  0000 C CNN
F 1 "R" V 5557 1851 40  0000 C CNN
F 2 "~" V 5480 1850 30  0000 C CNN
F 3 "~" H 5550 1850 30  0000 C CNN
	1    5550 1850
	1    0    0    -1  
$EndComp
Wire Wire Line
	5550 1500 5550 1600
Wire Wire Line
	5250 2300 5250 2300
Connection ~ 5250 1500
Wire Wire Line
	5250 2300 5250 2600
Connection ~ 4450 4400
$Comp
L BC547 Q7
U 1 1 59247545
P 5700 3700
F 0 "Q7" H 5700 3551 40  0000 R CNN
F 1 "BC547" H 5700 3850 40  0000 R CNN
F 2 "TO92" H 5600 3802 29  0000 C CNN
F 3 "" H 5700 3700 60  0000 C CNN
	1    5700 3700
	1    0    0    -1  
$EndComp
$Comp
L R R9
U 1 1 592475B3
P 5800 4150
F 0 "R9" V 5880 4150 40  0000 C CNN
F 1 "R" V 5807 4151 40  0000 C CNN
F 2 "~" V 5730 4150 30  0000 C CNN
F 3 "~" H 5800 4150 30  0000 C CNN
	1    5800 4150
	1    0    0    -1  
$EndComp
Connection ~ 5250 4400
Wire Wire Line
	5500 3700 4450 3700
Wire Wire Line
	5800 3500 5800 2500
Wire Wire Line
	5800 2500 5550 2500
Connection ~ 3500 1600
Connection ~ 3500 1500
Connection ~ 5500 3700
Connection ~ 4450 3700
Wire Wire Line
	3500 2800 4450 2800
Wire Wire Line
	2950 2300 2950 2600
Wire Wire Line
	2950 2600 6500 2600
Connection ~ 2950 2300
$Comp
L BC557 Q5
U 1 1 592586E3
P 6700 4000
F 0 "Q5" H 6700 3851 40  0000 R CNN
F 1 "BC557" H 6700 4150 40  0000 R CNN
F 2 "TO92" H 6600 4102 29  0000 C CNN
F 3 "" H 6700 4000 60  0000 C CNN
	1    6700 4000
	1    0    0    1   
$EndComp
$Comp
L BC557 Q1CS3
U 1 1 592586EC
P 6700 2350
F 0 "Q1CS3" H 6700 2201 40  0000 R CNN
F 1 "BC557" H 6700 2500 40  0000 R CNN
F 2 "TO92" H 6600 2452 29  0000 C CNN
F 3 "" H 6700 2350 60  0000 C CNN
	1    6700 2350
	1    0    0    1   
$EndComp
Wire Wire Line
	6800 4400 6800 4200
Connection ~ 5800 4400
Wire Wire Line
	5800 3350 6500 3350
Wire Wire Line
	6500 3350 6500 4000
Connection ~ 5800 3350
Wire Wire Line
	6500 2600 6500 2350
Connection ~ 5250 2600
Wire Wire Line
	6800 2550 6800 3800
$Comp
L R R2
U 1 1 5925881A
P 6800 1900
F 0 "R2" V 6880 1900 40  0000 C CNN
F 1 "R" V 6807 1901 40  0000 C CNN
F 2 "~" V 6730 1900 30  0000 C CNN
F 3 "~" H 6800 1900 30  0000 C CNN
	1    6800 1900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6800 1500 6800 1650
Connection ~ 5550 1500
$Comp
L CONN_1 Out1
U 1 1 5925B523
P 6950 3050
F 0 "Out1" H 7030 3050 40  0000 L CNN
F 1 "CONN_1" H 6950 3105 30  0001 C CNN
F 2 "" H 6950 3050 60  0000 C CNN
F 3 "" H 6950 3050 60  0000 C CNN
	1    6950 3050
	1    0    0    -1  
$EndComp
Connection ~ 6800 3050
$EndSCHEMATC
