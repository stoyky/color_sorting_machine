from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
import time

SLAVE = 254

c = ModbusTcpClient('127.0.0.1')   # Create client object
c.connect()                           # connect to device, reconnect automatically

# Reset 
c.write_coil(0, 1, SLAVE); # emitter start
c.write_coil(1, 0, SLAVE); # load pusher reset

c.write_coil(2, 0, SLAVE); # pusher 1 reset
c.write_coil(3, 0, SLAVE); # pusher 2 reset
c.write_coil(4, 0, SLAVE); # pusher 3 reset

c.write_register(7, 0, SLAVE); #reset belt speed
c.write_register(14, 0, SLAVE); # conveyor belt off

while c.connected:

        part_ready = c.read_discrete_inputs(0, 1, SLAVE).bits[0];
        part_pres_1 = c.read_discrete_inputs(1, 1, SLAVE).bits[0];
        part_pres_2 = c.read_discrete_inputs(2, 1, SLAVE).bits[0];
        part_pres_3 = c.read_discrete_inputs(3, 1, SLAVE).bits[0];
        
        load_pusher_adv = c.read_discrete_inputs(4, 1, SLAVE).bits[0];
        load_pusher_ret = c.read_discrete_inputs(5, 1, SLAVE).bits[0];

        metal_bin = c.read_discrete_inputs(5, 1, SLAVE).bits[0];
        blue_bin = c.read_discrete_inputs(6, 1, SLAVE).bits[0];
        green_bin = c.read_discrete_inputs(7, 1, SLAVE).bits[0]
        reject_bin = c.read_discrete_inputs(8, 1, SLAVE).bits[0];

        metal_detect = c.read_input_registers(2, 1, SLAVE).registers[0];
        blue_detect = c.read_input_registers(1, 1, SLAVE).registers[0];
        green_detect = c.read_input_registers(0, 1, SLAVE).registers[0];
        
        metal_retract = c.read_input_registers(5, 1, SLAVE).registers[0];
        blue_retract = c.read_input_registers(4, 1, SLAVE).registers[0];
        green_retract = c.read_input_registers(3, 1, SLAVE).registers[0];

        belt_speed = c.read_input_registers(7, 1, SLAVE).registers[0];
        conv_off = c.read_discrete_inputs(14, 1, SLAVE).bits[0];
        
        if conv_off:
                c.write_register(7, 0, SLAVE); # Reset belt speed
        else:
                c.write_register(7, belt_speed, SLAVE); # Set belt speed based on knob
                
        if part_pres_1:
                c.write_coil(0, 0, SLAVE); # Emitter disable
        else:
                c.write_coil(0, 1, SLAVE); # Emitter enable

        if not part_ready and load_pusher_ret:
                c.write_coil(1, 1, SLAVE); # Load pusher adv
       
        if load_pusher_adv:
                c.write_coil(1, 0, SLAVE); # Load pusher retract
    
        if metal_detect == 9 and part_pres_3:
                c.write_register(2, 0x7FFF, SLAVE); # Pusher metal adv
        else:
                c.write_register(2, 0x8000, SLAVE); # Pusher metal retract
        
        if blue_detect == 2 and part_pres_2:
                c.write_register(1, 0x7FFF, SLAVE); # Pusher blue adv
        else:
                c.write_register(1, 0x8000, SLAVE); # Pusher blue retract
        
        if green_detect == 5 and part_pres_1:
                c.write_register(0, 0x7FFF, SLAVE); # Pusher green adv
        else:
                c.write_register(0, 0x8000, SLAVE); # Pusher green retract
        
        time.sleep(0.1);

