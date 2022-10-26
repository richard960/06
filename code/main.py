
comp = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    'M': '1110000',
    '!D': '0001101',
    '!A': '0110001',
    '!M': '1110001',
    '-D': '0001111',
    '-A': '0110011',
    '-M': '1110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'M+1': '1110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'M-1': '1110010',
    'D+A': '0000010',
    'D+M': '1000010',
    'D-A': '0010011',
    'D-M': '1010011',
    'A-D': '0000111',
    'M-D': '1000111',
    'D&A': '0000000',
    'D&M': '1000000',
    'D|A': '0010101',
    'D|M': '1010101'
  }

dest = {
  'null': '000',
  'M': '001',
  'D': '010',
  'A': '100',
  'MD': '011',
  'AM': '101',
  'AD': '110',
  'AMD': '111'
}

jump = {
 'null': '000',
 'JGT': '001',
 'JEQ': '010',
 'JGE': '011',
 'JLT': '100',
 'JNE': '101',
 'JLE': '110',
 'JMP': '111'
}

symbolTable = {
  'SP': 0,
  'LCL': 1,
  'ARG': 2,
  'THIS': 3,
  'THAT': 4,
  'R0': 0,
  'R1': 1,
  'R2': 2,
  'R3': 3,
  'R4': 4,
  'R5': 5,
  'R6': 6,
  'R7': 7,
  'R8': 8,
  'R9': 9,
  'R10': 10,
  'R11': 11,
  'R12': 12,
  'R13': 13,
  'R14': 14,
  'R15': 15,
  'SCREEN': 16384,
  'KBD': 24576
}

def command(com) :
  if(com == '@'):
    return 'A'
  if(com == '('):
    return 'L'
  return 'C'

def binary(sym):
  return "{0:b}".format(int(sym))

def main(filePath, writeTo):
  file = open('filePath', 'r')
  lines = file.readlines()
  write = open(writeTo, 'w')
  editLines = []
  for line in lines:
    if(line == '\n' or line[:2] == '//'):
      continue
    if(line.__contains__('//')):
      line = line[:line.find('//')]
    line = line.replace(' ', '')
    newLine = []
    for char in line:
      if(char not in ['', '\n']):
        newLine.append(char)
    editLines.append(''.join(newLine))
  commandType = None
  add = -1
  commands = len(editLines)
  count = 0
  ram = 16

  while add < commands - 1:
    add += 1
    commandType = editLines[add]
    commandType = command(commandType[0])
    if(commandType == 'A' or commandType == 'C'):
      count += 1
    else:
      symbol = commandType[1:-1]
      symbolTable[symbol] = count

  add = -1

  while add < commands - 1:
    add += 1
    commandType = editLines[add]
    commandType = command(commandType[0])
    if(commandType == 'A'):
      symbol = commandType[1:]
      symbolTable[symbol] = ram
      ram += 1


  add = -1
  while add < commands - 1:
    add += 1
    commandType = editLines[add]
    commandType = command(commandType[0])
    if(commandType == 'A'):
      symbol = editLines[:1]
      if(symbol.isdigit()):
        binary = binary(symbol)
      else:
        address = symbolTable[symbol]
        binarySymbol = binary(address)
      aCom = '0' * (16 - len(binarySymbol)) + binarySymbol
      write.write(aCom + '\n')
    if(commandType == 'C'):
      ind = commandType.find('=')
      ind_ = commandType.find(';')
      desT = dest[commandType[:ind]]
      comP = comp[commandType[ind+1:ind_]]
      jumP = jump[commandType[ind+1:]]
      write.write('111' + comP + desT + jumP + '\n')
  write.close()




files = {
  '../add/Add.asm': '../add/Add.hack',
  '../max/Max.asm': '../max/Max.hack',
  '../max/MaxL.asm': '../max/MaxL.hack',
  '../pong/Pong.asm': '../pong/Pong.hack',
  '../pong/PongL.asm': '../pong/PongL.hack',
  '../rect/Rect.asm': '../rect/Rect.hack',
  '../rect/RectL.asm': '../rect/RectL.hack'
}

for keys in files:
  main(keys, files[keys])