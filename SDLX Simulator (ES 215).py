#Simulator
# ES 215 Group Project
# Group: Hirva, Shrimay, Amey


pc = 0 
next_pc = 0
prev_write_reg = -1
RAW_hazard = 0
stall_count = 0 
total_instr_count = 0
class SDLXProcessor:

    #initiation of memory and registers
    def __init__(self):
        self.registers = [0b0]*32
        self.memory = [0b0]*400
        self.pc = 0
    
    #loading program into memory from a file 
    def load_program(self, program):
        for i in range(len(program)):
            if int(program[i],2) & 0b10000000 == 0:
                self.memory[i] = int(program[i],2) 
            else:
                self.memory[i] = int(program[i],2) - 256

    #helper function for switches (memory mapped IO)
    def invert(self,x):
        if self.memory[x] == 0:
          self.memory[x] = 1
        else: 
          self.memory[x] = 0
    
    # execute function for instructions 
    def execute(self, ini, spec_count,switch_change_state):
        # mem addr 200 = switch 1, 201 = switch 2, 202 = switch 3,....
        # mem addr 208 = led 1,...... 

        global pc 
        global next_pc
        global prev_opcode
        global prev_func_code
        global prev_write_reg
        global RAW_hazard
        global stall_count 
        global total_instr_count
        self.pc = pc 
        count = 0

        if switch_change_state != 0:
          obj.invert(199+switch_change_state)
        
        for i in range(208,216):
          self.memory[i] = self.memory[i-8]

        while self.pc < len(program) and count<spec_count: #spec_count is specified count, to tell the program how many instruction we want to execute
            opcode = int(program[self.pc][0:6],2)

            if opcode == 0: #R type triadic
              rs1 = int(program[self.pc][6:8]+program[self.pc+1][0:3],2)
              rs2 = int(program[self.pc+1][3:8],2)
              rd = int(program[self.pc+2][0:5],2)
              func_code = int(program[self.pc+3][3:8],2)

              if func_code == 9 or func_code == 10:
                if prev_write_reg == rs1:
                  RAW_hazard += 1
                  stall_count += 1
              if prev_write_reg == rs1 or prev_write_reg == rs2:
                  print ("yo")
                  RAW_hazard += 1
                  stall_count += 1
              count = count +1 
              total_instr_count +=1

              #ALU for R triadic
              if func_code == 1: #ADD true
                  self.registers[rd] = self.registers[rs1] + self.registers[rs2]     

              elif func_code == 2: #SUB true
                  self.registers[rd] = self.registers[rs1] -  self.registers[rs2]
                
              elif func_code == 3: #AND true
                  self.registers[rd] = self.registers[rs1] & self.registers[rs2]  

              elif func_code == 4: #OR true
                  self.registers[rd] = self.registers[rs1] | self.registers[rs2]                

              elif func_code == 5: #XOR true
                  self.registers[rd] = self.registers[rs1] ^ self.registers[rs2]
                 
              elif func_code == 6: #SLL true 
                  shift_count = 0b11111 & self.registers[rs2] 
                  x = self.registers[rs1] << shift_count
                  b = 0b11111111111111111111111111111111
                  y = x&b
                  if (0b10000000000000000000000000000000 & y)==0:
                    y = y
                  else: 
                    y = y-2**32
                  self.registers[rd] = y
                  
              elif func_code == 7: #SRL true
                  shift_count = 0b11111 & self.registers[rs2]
                  x = self.registers[rs1]
                  i = 0
                  for i in range(0,shift_count):
                    x = x//2
                    i = i+1
                  self.registers[rd] = x

              elif func_code == 8: #SRA true
                  shift_count = 0b11111 & self.registers[rs2]
                  if self.registers[rs1] <  0:
                    x = self.registers[rs1] + 2**32
                  else: 
                    x = self.registers[rs1]
                  i = 0
                  for i in range(0,shift_count):
                    x = x//2
                    i = i+1
                  self.registers[rd] = x
                 
              elif func_code ==9 : #ROL true
                  if (self.registers[rs1]&0b1) == 0:
                    if self.registers[rs1]<0:
                      self.registers[rd] = (self.registers[rs1] + 2**32 ) //2
                    else: 
                      self.registers[rd] = (self.registers[rs1])//2
                  else: 
                    if self.registers[rs1]<0:
                      self.registers[rd] = (self.registers[rs1])//2
                    else: 
                      self.registers[rd] = (self.registers[rs1] - 2**32 ) //2
           
              elif func_code ==10 : #ROR true
                  if (self.registers[rs1]&0b01000000000000000000000000000000) == 0:
                      if self.registers[rs1]<0:
                        self.registers[rd] = (((self.registers[rs1] + 2**32 )<< 1) & 0b11111111111111111111111111111111)  + 1
                      else: 
                        self.registers[rd] = ((self.registers[rs1]<<1) & 0b11111111111111111111111111111111) 
                  else: 
                      if self.registers[rs1]<0:
                        self.registers[rd] = (self.registers[rs1]<<1)  + 1
                      else: 
                        self.registers[rd] = ((self.registers[rs1] << 1)& 0b11111111111111111111111111111111)- 2**32
             
              elif func_code == 11: #SLT true
                  if self.registers[rs1] < self.registers[rs2]:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000
 
              elif func_code == 12: #SGT true
                  if self.registers[rs1] > self.registers[rs2]:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000
                  
              elif func_code == 13: #SLE true
                  if self.registers[rs1] <= self.registers[rs2]:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000
                
              elif func_code == 14: #SGE true
                  if self.registers[rs1] >= self.registers[rs2]:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000
               
              elif func_code == 15: #UGT true
                  if self.registers[rs1] <= 0:
                      oprnd_1 = self.registers[rs1] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs1]
                  if self.registers[rs2] <= 0:
                      oprnd_1 = self.registers[rs2] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs2]
                  if oprnd_1 > oprnd_2:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000
                
              elif func_code == 16: #ULT true
                  if self.registers[rs1] <= 0:
                      oprnd_1 = self.registers[rs1] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs1]
                  if self.registers[rs2] <= 0:
                      oprnd_1 = self.registers[rs2] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs2]
                  if oprnd_1 < oprnd_2:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000
             
              elif func_code == 17: #UGE true
                  if self.registers[rs1] <= 0:
                      oprnd_1 = self.registers[rs1] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs1]
                  if self.registers[rs2] <= 0:
                      oprnd_1 = self.registers[rs2] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs2]
                  if oprnd_1 >= oprnd_2:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000
                 
              elif func_code == 18: #ULE true
                  if self.registers[rs1] <= 0:
                      oprnd_1 = self.registers[rs1] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs1]
                  if self.registers[rs2] <= 0:
                      oprnd_1 = self.registers[rs2] + 2**32
                  else: 
                      oprnd_1 = self.registers[rs2]
                  if oprnd_1 <= oprnd_2:
                    self.registers[rd]=0xffffffff
                  else:
                    self.registers[rd]=0x0000

              if ini == 0:
                self.pc +=4
              else:
                self.pc = next_pc
              
              prev_write_reg = rd

            #ALU for R-I triadic, R dyadic and Jump
            else:
                if opcode <= 30: #R-I triadic & R dyadic
                    rs1 = int((program[self.pc][6:8]+program[self.pc+1][0:3]),2)
                    rs2 = int(program[self.pc+1][3:8],2)
                    rd = int(program[self.pc+1][3:8],2) 
                    imm_const = program[self.pc+2][0:8]+program[self.pc+3][0:8] #string of 16 variables
                    if (imm_const[0]=="1"):              
                        signed_int = int(imm_const,2) - 2**16
                    else:
                        signed_int =int(imm_const,2) #integer, sign is considered

                    if opcode <= 27:
                        if prev_write_reg == rs1:
                          RAW_hazard += 1
                          stall_count += 1
                    else: 
                        if prev_write_reg == (rs1 or rd):
                          RAW_hazard +=1 
                          stall_count += 1

                    count = count+1
                    total_instr_count +=1
                    
                    # ALU for R-I triadic instructions
                    if opcode == 1: #ADDI  true
                        self.registers[rd] = self.registers[rs1] + signed_int
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 2: #SUBI  true
                        self.registers[rd] = self.registers[rs1] - signed_int
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 3: #ANDI   true
                        self.registers[rd] = self.registers[rs1] & signed_int
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 4: #ORI   
                        self.registers[rd] = self.registers[rs1] | signed_int
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 5: #XORI   
                        self.registers[rd] =self.registers[rs1] ^ signed_int
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 6: #SLLI true
                        shift_count = 0b11111 & int(imm_const,2)
                        x = self.registers[rs1] << shift_count
                        b = 0b11111111111111111111111111111111
                        y = x&b
                        if (0b10000000000000000000000000000000 & y)==0:
                           y = y
                        else: 
                           y = y-2**32
                        self.registers[rd] = y
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc
                        
                    elif opcode == 7: #SRLI  true
                        shift_count = 0b11111 & int(imm_const,2)
                        x = self.registers[rs1]
                        i = 0
                        for i in range(0,shift_count):
                          x = x//2
                          i = i+1
                        self.registers[rd] = x
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 8: #SRAI  true
                        shift_count = 0b11111 & int(imm_const,2)
                        x = self.registers[rs1] + 2**32
                        i = 0
                        for i in range(0,shift_count):
                          x = x//2
                          i = i+1
                        self.registers[rd] = x
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 9: #SLTI true
                        if self.registers[rs1] < signed_int:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 10: #SGTI true
                        if self.registers[rs1] > signed_int:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 11: #SLEI true
                        if self.registers[rs1] <= signed_int:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 12: #SGEI true
                        if self.registers[rs1] >= signed_int:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000  
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 13: #UGTI true
                        if self.registers[rs1] <= 0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        if signed_int <= 0:
                          oprnd_2 = signed_int + 2**32
                        else: 
                          oprnd_2 = signed_int
                        if oprnd_1 > oprnd_2:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 14: #ULTI true
                        if self.registers[rs1] <= 0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        if signed_int <= 0:
                          oprnd_2 = signed_int + 2**32
                        else: 
                          oprnd_2 = signed_int
                        if oprnd_1 < oprnd_2:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 15: #UGEI true
                        if self.registers[rs1] <= 0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        if signed_int <= 0:
                          oprnd_2 = signed_int + 2**32
                        else: 
                          oprnd_2 = signed_int
                        if oprnd_1 >= oprnd_2:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 16: #ULEI true
                        if self.registers[rs1] <= 0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        if signed_int <= 0:
                          oprnd_2 = signed_int + 2**32
                        else: 
                          oprnd_2 = signed_int
                        if oprnd_1 <= oprnd_2:
                          self.registers[rd]=0xffffffff
                        else:
                          self.registers[rd]=0x0000
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 17: #LHI true
                        if self.registers[rs1] <= 0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = int(imm_const,2)
                        answer = (oprnd_2 << 16) + int(bin(oprnd_1)[-16:],2)
                        if imm_const[0] =="1":
                          answer = answer - 2**32
                        else: 
                          answer = answer 
                        self.registers[rd] = answer 
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 18: #BEQZ true
                        if self.registers[rs1] == 0:
                            if ini ==0:
                                self.pc += 4
                                pc = self.pc
                                oprnd_1 = self.pc
                                oprnd_2 = signed_int << 2
                                next_pc =  (oprnd_1 + oprnd_2)
                                prev_write_reg = -1
                                obj.execute(1,1,0)
                            if ini == 1:
                                self.pc = next_pc

                    elif opcode == 19: #BNEZ true
                        if self.registers[rs1] != 0:
                            if ini ==0:
                                self.pc += 4
                                pc = self.pc
                                oprnd_1 = self.pc
                                oprnd_2 = signed_int << 2
                                next_pc =  (oprnd_1 + oprnd_2)
                                prev_write_reg = -1
                                obj.execute(1,1,0)
                            else:
                                self.pc = next_pc

                    elif opcode == 20: #JR true
                        if ini == 0:
                          self.pc += 4
                          pc = self.pc
                          oprnd_1 = self.registers[rs1]//2
                          oprnd_1 = oprnd_1 // 2
                          oprnd_1 = oprnd_1 << 2
                          oprnd_2 = signed_int << 2
                          next_pc = oprnd_1 + oprnd_2
                          prev_write_reg = -1
                          obj.execute(1,1,0)
                        else:
                          self.pc = next_pc

                    elif opcode ==21 : #JALR true
                        if ini==0:
                          self.pc += 4
                          pc = self.pc
                          self.registers[31] = self.pc + 4
                          oprnd_1 = self.registers[rs1]//2
                          oprnd_1 = oprnd_1 // 2
                          oprnd_1 = oprnd_1 << 2
                          oprnd_2 = signed_int << 2
                          next_pc = oprnd_1 + oprnd_2
                          prev_write_reg = 31
                          obj.execute(1,1,0)
                        else: 
                          self.pc = next_pc

                    elif opcode == 22: #LB true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        self.registers[rd] = self.memory[addr]
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 23: #LBU true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        if self.memory[addr] < 0:
                          self.registers[rd]= self.memory[addr]+256
                        else: 
                          self.registers[rd]= self.memory[addr]
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 24: #LH
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        if self.memory[addr+1]<0:
                          y = self.memory[addr+1] + 256
                        else: 
                          y = self.memory[addr+1]
                        self.registers[rd] = (self.memory[addr] << 8) + y
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 25: #LHU true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        if self.memory[addr+1]<0:
                          y = self.memory[addr+1] + 256
                        else: 
                          y = self.memory[addr+1]
                        if self.memory[addr]<0:
                          x = self.memory[addr] + 256
                        else: 
                          x = self.memory[addr]
                        self.registers[rd] = (x<<8) + y
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 26: #LW true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        if self.memory[addr+1]<0:
                          x = (self.memory[addr+1] + 256)<<16 
                        else: 
                          x = self.memory[addr+1] <<16
                        if self.memory[addr+2]<0:
                          y = (self.memory[addr+2] + 256) <<8 
                        else: 
                          y = self.memory[addr+2] << 8 
                        if self.memory[addr+3]<0:
                          z = (self.memory[addr+3] + 256) 
                        else: 
                          z = self.memory[addr+3]
                        self.registers[rd] = (self.memory[addr] << 24) + x + y + z
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 27: #LWU true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        if self.memory[addr] < 0:
                          w = (self.memory[addr] + 256) << 24
                        else: 
                          w = self.memory[addr] << 24
                        if self.memory[addr+1]<0:
                          x = (self.memory[addr+1] + 256)<<16 
                        else: 
                          x = self.memory[addr+1] <<16
                        if self.memory[addr+2]<0:
                          y = (self.memory[addr+2] + 256) <<8 
                        else: 
                          y = self.memory[addr+2] << 8 
                        if self.memory[addr+3]<0:
                          z = (self.memory[addr+3] + 256) 
                        else: 
                          z = self.memory[addr+3]
                        self.registers[rd] = w + x + y + z
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    elif opcode == 28: #SB true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        a = self.registers[rd] & 0b11111111
                        if self.registers[rd]<0:
                          self.memory[addr]=a-256
                        else: 
                          self.memory[addr]=a
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc
                    
                    elif opcode == 29: #SH true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        a = self.registers[rd] & 0b1111111100000000
                        if self.registers[rd]<0:
                          self.memory[addr]=(a-2**16)>>8
                        else: 
                          self.memory[addr]= a>>8
                        b = self.registers[rd] & 0b11111111
                        self.memory[addr+1]=b
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc
                    
                    elif opcode == 30: #SW true
                        if self.registers[rs1]<0:
                          oprnd_1 = self.registers[rs1] + 2**32
                        else: 
                          oprnd_1 = self.registers[rs1]
                        oprnd_2 = signed_int
                        addr = oprnd_1 + oprnd_2
                        a = self.registers[rd] & 0b11111111000000000000000000000000
                        if self.registers[rd]<0:
                          self.memory[addr]=(a-2**32)>>24
                        else: 
                          self.memory[addr]= a>>24
                        b = self.registers[rd] & 0b111111110000000000000000
                        self.memory[addr+1]=b>>16
                        c = self.registers[rd] & 0b1111111100000000
                        self.memory[addr+2]=c>>8
                        d = self.registers[rd] & 0b11111111
                        self.memory[addr+3]=d
                        if ini==0:
                          self.pc += 4
                        else: 
                          self.pc = next_pc

                    else:
                        y = 1
                    
                    if opcode <= 17:
                      prev_write_reg = rd
                    elif opcode >= 22 and opcode <= 27:
                      prev_write_reg = rd
                    elif opcode >= 18 and opcode <= 21:
                      prev_write_reg = prev_write_reg
                    else:
                      prev_write_reg = -1


                #ALU for J type
                else:  # J type
                    sign_offset = program[self.pc][6:8]+program[self.pc+1][0:8]+program[self.pc+2][0:8]+program[self.pc+3][0:8]
                    if (sign_offset[0] == "1") :              
                        signed_int = int(sign_offset,2) - 2**26 
                    else:
                        signed_int = int(sign_offset,2) #integer, sign is considered

                    
                    count = count + 1

                    if opcode == 31: #J true
                        if ini == 0: 
                          self.pc +=4
                          pc = self.pc
                          next_pc = self.pc + 4*signed_int
                          prev_write_reg = -1
                          obj.execute(1,1,0)
                        else: 
                          self.pc = next_pc
                       
                    elif opcode == 32: #JAL true
                        if ini ==0:
                          self.pc += 4
                          pc = self.pc
                          next_pc = self.pc + 4*signed_int
                          prev_write_reg = 31
                          obj.execute(1,1,0)
                          self.registers[31] = self.pc
                        else: 
                          self.pc = next_pc
                        
                    else:
                        print("Invalid opcode:",opcode)
                        break


                    

        if ini == 0: 
          print("self pc  = ",self.pc)
          print ("")
          print ("Memory")
          for i in range(25):
            for j in range(15):
              print (self.memory[16*i + j],end=" , ")
            print (self.memory[16*i + 15])
          print ("")
          print ("Registers")
          print(self.registers)
          print ("")
          print ("Switch states")
          for i in range(8):
            print ("Switch ",i+1," = ",self.memory[200+i],end=", ")
          print (" ")
          print("LED states")
          for i in range(8):
            print ("LED ",i+1," = ",self.memory[208+i],end=", ")
          print(" ")
          print("next pc = ",next_pc)
          print("prev write reg = ", prev_write_reg)
          print ("rs2 = ", rs2)
        pc = self.pc

 
#program read vscode
program = []
with open('input.txt') as instructions:
    program = instructions.read()
    program = program.split(" ")

# program_input = """00000100 00000001 00000000 00001110 00001000 00100001 00000000 00000111 00000100 00100001 00000000 00011000 00000100 00100011 00000000 00000111"""
# 01010100 00000000 00000000 00000100


obj = SDLXProcessor()
obj.load_program(program)

def input_user():
  print ("How many instructions would you like to execute?")
  num = int(input())
  if num == 0: 
    print("Program Stopped")
    print ("RAW Hazard = ",RAW_hazard)
    print ("stall_count =",stall_count)
    print("CPI = ",((total_instr_count-RAW_hazard)*2 + (RAW_hazard*3))/(2*total_instr_count))
  else:
    print("Any switch you wish to turn on or off? (Enter a number from 1 to 8, 0 otherwise)")
    switch_change_state = int(input())
    obj.execute(0,num,switch_change_state)
    input_user()

input_user()


