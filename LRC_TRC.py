def Vertical_block(input): # calculate vertical block for each character
  vertical_block=[]
  for i in range(len(input)):
    vertical_block.append(format(ord(input[i]), '08b'))
  return vertical_block
def Horizontal_block(input):# calculate horizontal block for each word with length 8 char
  horizontal_block=[]
  a=""
  b=""
  c=""
  d=""
  e=""
  f=""
  g=""
  h=""
  
  for i in range(len(input)):
    binary=format(ord(input[i]), '08b')
    a+=binary[0]
    b+=binary[1]
    c+=binary[2]
    d+=binary[3]
    e+=binary[4]
    f+=binary[5]
    g+=binary[6]
    h+=binary[7]
  
  horizontal_block.append(a)
  horizontal_block.append(b)
  horizontal_block.append(c)
  horizontal_block.append(d)
  horizontal_block.append(e)
  horizontal_block.append(f)
  horizontal_block.append(g)
  horizontal_block.append(h)
    #horizontal_block.append(format(ord(input[i]), '08b'))
  return horizontal_block

def Parity(input):# calculate parity for each block of binary 
  x=""
  x+=str(int(input[0])^int(input[1]))
  for i in range(2,len(input)):
    x=str(int(x)^int(input[i]))
  return x

def LRC(input_arr): # calculate LRC 
  LRC=[]
  for i in input_arr:
   LRC.append(Parity(i))
  return LRC

def TRC(input_arr):#calculate TRC
  TRC=[]
  for i in input_arr:
   TRC.append(Parity(i))
  return TRC

#-----------------------find_position_faulty in LRC & TCR
def find_position_faulty(trc,trc_faulty,lrc,lrc_faulty):  
  #calculate tcr faulty position
  for i in range(len(trc)):
    if(trc[i]!=trc_faulty[i]):
      position_trc=i
      break
    else:
      position_trc=i=-1
  for i in range(len(lrc)):
    if(lrc[i]!=lrc_faulty[i]):
      position_lrc=i
      break
    else:
      position_lrc=-1
  return position_trc,position_lrc

def NOT(p): # calculate not of bit if it is faulty (bit_flip)
  if(p=='0'):
    return '1'
  else:
    return '0'

def binary_to_char(binary): # calculate character of binary text to correct faulty character
  binary_values = binary.split()
  ascii_string = ""
  for binary_value in binary_values:
    an_integer = int(binary_value, 2)
    ascii_character = chr(an_integer)
    ascii_string += ascii_character
  return ascii_string

def replace_str_index(text,index=0,replacement=''): # replace faulty char with correct char
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def detect_correct(block_word,trc_list,trc_list_F,lrc_list,lrc_list_F): # correct and detect single bit error in each word of block
  for i in range(len(block_word)):
    w1=block_word[i]
    pos_trc,pos_lrc=find_position_faulty(trc_list[i],trc_list_F[i],lrc_list[i],lrc_list_F[i])
  #print(pos_trc)
  #print(pos_lrc)
    if((pos_trc!=-1)&(pos_lrc!=-1)):
      binary=format(ord(w1[pos_trc]), '08b')
      binary=replace_str_index(binary,pos_lrc,NOT(binary[pos_lrc]))
      correct_char=binary_to_char(binary)
      correct_word=replace_str_index(w1,pos_trc,correct_char)
      block_word[i]=correct_word
    
  return block_word

if __name__ == '__main__':
  trc_list=[]
  lrc_list=[]
  # read correct text file and calculate its lrc and trc
  with open('correct_text.txt') as f:
    input = f.read()
  if((len(input)%8)!=0):
    for i in range(8-(len(input)%8)): # insert space to be multiplication 8
      input+=" "
  block_word=[]

  for i in range(0,len(input),8): # create block of word with lenght 8
    block_word.append(input[i:i+8])
  
  for i in block_word:  #create trc and lrc list for all block that create for file text
    vertical_block=Vertical_block(i)
    horizontal_block=Horizontal_block(i)
    trc_list.append(TRC(vertical_block))
    lrc_list.append(LRC(horizontal_block))

  trc_list_F=[]
  lrc_list_F=[]
  # read correct text file and calculate its lrc and trc
  with open('faulty_text.txt') as f:
      input = f.read()
  if((len(input)%8)!=0):
    for i in range(8-(len(input)%8)): # insert space to be multiplication 8
      input+=" "
  block_word=[]
  for i in range(0,len(input),8): # create block of word with lenght 8
    block_word.append(input[i:i+8])
  
  for i in block_word: #create trc and lrc list for all block that create for file text
    vertical_block=Vertical_block(i)
    horizontal_block=Horizontal_block(i)
    trc_list_F.append(TRC(vertical_block))
    lrc_list_F.append(LRC(horizontal_block))

  block_word=detect_correct(block_word,trc_list,trc_list_F,lrc_list,lrc_list_F)
  print("correct text")
  correct_text=""
  for i in range(len(block_word)):
    correct_text+=block_word[i]
  print(correct_text)
