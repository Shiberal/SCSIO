#connect to microsoft flight simulator using SimConnect library
#print the current aircraft position and attitude
#this is a test script to see if the SimConnect library works
from ast import Return, Try
from importlib.metadata import SelectableGroups
import eventlet
import socketio


from asyncio.windows_events import NULL
from distutils.command import clean
from pickle import FALSE, TRUE
from time import sleep, time
from datetime import datetime
from tkinter import VERTICAL
from turtle import clear
from SimConnect import *
from pprint import pp
test = {
    "fruit": "Apple",
    "size": "Large",
    "color": "Red"
}

def connectSM():
    print ("trying to connect to the simulator");
    sm = SimConnect();
    return sm;
                          

def getAQ(sm):
    aq = AircraftRequests(sm, _time=200);
    return aq;



def fetchdata(aq):
        heading_true = 0;
        #POSITION
        altitude = aq.get("PLANE_ALTITUDE")
        ground_altitude = aq.get("GROUND_ALTITUDE")
        plane_abv_ground = aq.get("PLANE_ALT_ABOVE_GROUND")
        latitude = aq.get("PLANE_LATITUDE")
        longitude = aq.get("PLANE_LONGITUDE")
        #DIRECTION
        heading_true = aq.get("PLANE_HEADING_DEGREES_TRUE")
        heading_magnetic = aq.get("PLANE_HEADING_DEGREES_MAGNETIC")
        heading_gyro = aq.get("PLANE_HEADING_DEGREES_GYRO")
        pitch = aq.get("PLANE_PITCH_DEGREES")
        bank = aq.get("PLANE_BANK_DEGREES")
        #SPEED
        relative_ground_speed = aq.get("SURFACE_RELATIVE_GROUND_SPEED")
        airspeed_ind = aq.get("AIRSPEED_INDICATED")
        airspeed_true = aq.get("AIRSPEED_TRUE")
        vertical_speed = aq.get("VERTICAL_SPEED")
        vertical_velocity = aq.get("VERTICAL_VELOCITY")
        #INFO
        aircraft_title = aq.get("TITLE")
        callsign = aq.get("ATC_AIRLINE")
        flight_number = aq.get("ATC_FLIGHT_NUMBER")
        CAF1 = aq.get("COM_ACTIVE_FREQUENCY:1")
        CAF2 = aq.get("COM_ACTIVE_FREQUENCY:2")
        CAF3 = aq.get("COM_ACTIVE_FREQUENCY:3")
        TFC = aq.get("FUEL_TOTAL_CAPACITY")
        TFQ = aq.get("FUEL_TOTAL_QUANTITY")
        TFCW =aq.get("FUEL_TOTAL_QUANTITY_WEIGHT")
        #OUTSIDE DATA
        wind_x = aq.get("AIRCRAFT_WIND_X")
        wind_y = aq.get("AIRCRAFT_WIND_Y")
        wind_z = aq.get("AIRCRAFT_WIND_Z")
        std_atm_temp = aq.get("STANDARD_ATM_TEMPERATURE")
        air_temp = aq.get("TOTAL_AIR_TEMPERATURE")
        #USELESS STUFF
        gforce = aq.get("G_FORCE")

        

        #make a object to store the data
        data_heading = {
            "rotation":{
                "pitch":pitch,
                "bank":bank
            },
            "raw" : {
                "heading_true" : heading_true,
                "heading_magnetic" : heading_magnetic,
                "heading_gyro" : heading_gyro
            },
            "processed" : {
                "360_heading_true" : ((heading_true * 180)/3.14),
                "360_heading_magnetic" : ((heading_magnetic * 180)/3.14),
                "360_heading_gyro" : ((heading_gyro * 180)/3.14)
            }
        }

        position = {
            "altitude" : altitude,
            "ground_altitude" : ground_altitude,
            "plane_abv_ground" : plane_abv_ground,
            "latitude" : latitude,
            "longitude" : longitude,
        }

        data_movement = {
            "vertical":{
                "vertical_speed" : vertical_speed,
                "vertical_velocity" : vertical_velocity
            },
            "airspeed":{
                "airspeed_ind" : airspeed_ind,
                "airspeed_true" : airspeed_true
            },
            "horizontal":{
                "relativeGspeed":relative_ground_speed
            },
            "g":gforce
        }


        

        data_outside = {
            "wind" : {
                "x" : wind_x,
                "y" : wind_y,
                "z" : wind_z
            },
            "temperature" : {
                "standard_atm_temperature": std_atm_temp,
                "air_temperature" : air_temp
            } 
        }

        

       
        


        composedData = {
            
            "aircraft":{
                "info": {
                    "aircraft" : str(aircraft_title),
                    "callsign" : str(callsign),
                    "flight": int(flight_number),
                    "radio":{
                        "CAF1":float(CAF1),
                        "CAF2":float(CAF2),
                        "CAF3":float(CAF3)
                    },
            "fuel":{
                "TFC":TFC,
                "TFQ":TFQ,
                "TFCW": TFCW
            }
        },
                "navdata":{
                    "position":position,
                    "heading":data_heading,
                    "spdvel":data_movement,
                },
            },
            "outside":data_outside
        }
        return(composedData);
    
        
    
        
    
   



def main():
    sm = connectSM();
    aq = getAQ(sm)


    
    sio = socketio.Client()
    app = socketio.WSGIApp(sio)
    
    @sio.event
    def connect():
        print("I'm connected!")
        sio.emit('user', { "username": "Shiberal" } )

    def userok(data):
        if(data.userok == TRUE):
            print("auth ok")
            sio.emit('nav_data', fetchdata(aq) )

    
    @sio.event
    def beat(data):
        sleep(2)
        
        print("sending data")
        
        sio.emit('nav_data', fetchdata(aq) )
   
    @sio.event
    def connect_error(data):
        print("The connection failed!")

    @sio.event
    def disconnect():
        print("I'm disconnected!")
        

    sio.connect('http://localhost:3000')


if __name__ == "__main__":
    try:
        main()
    except:
        print("GOT ERROR")
        sleep(5)
    
    
    
    

    