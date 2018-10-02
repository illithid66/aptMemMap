#Task is to read the IO and declare report files
#Written on 32 bit RedHat
#Original code (pre git) v1_8 is first Git commit

#OS for opening folders and files
import os;

#Define globals for reports
global buffer;
buffer = 'The buffer has not been set yet.';


#for each program, there is a PRR directory and a UNIT directory
def openProgram(programName):
    global buffer;
    buffer = 'The APT ' + programName + ' has a number of points, which sum up to..., \n';
    print("You are in "+os.getcwd());
    fileNamesHere = os.getcwd()+"/"+programName
    listDirectory = os.listdir(fileNamesHere)
    print(listDirectory);

    checkPRR(fileNamesHere);
    checkUNITS(fileNamesHere);

    fileToWrite = open(programName+".csv","wb");
    fileToWrite.write(buffer);
    print('Buffer written to text file.');
    
#check for PRR whenever called
def checkPRR(directory): #opens PRR folders and searches them
    if(os.path.exists(directory+"/PRR")): #Open IO & DECLARE
        print("Opening PRR tables in "+directory);
        openDeclare(directory);
        openIO(directory);
        return(True);
    else:
        return(False);
        
def checkUNITS(directory): #opens UNIT folders and searches them for RPTs
    global buffer;
    isTrue = (os.path.exists(directory+"/UNITS")); #open the program again
    if isTrue:
        print("Opening UNITS in "+directory);
        unitsHere = os.listdir(directory+"/UNITS");
        print 'There are ',len(unitsHere),' here, specifically ',unitsHere;
        for i in range(len(unitsHere)):
            buffer = buffer + unitsHere[i];
            openIO(directory+'/UNITS/'+unitsHere[i]);
            openDeclare(directory+'/UNITS/'+unitsHere[i]);
    else:
         unitsHere = "";
    return(isTrue,unitsHere)

def openDeclare(directory): #safe opening of a declare report
    global buffer;
    buffer = buffer + directory + '/Declare,\n';
    target = directory+"/PRR/DECLARE.RPT";
    if os.path.isfile(target):
        fileOpen = open(target);
        text = fileOpen.read();
        fileOpen.close();
        readDeclare(text);
        print(directory+' declare found');
    else:
        text = "File not present";
        print(directory+' declare not found');
    return text;

def openIO(directory): #reads an IO report
    global buffer;
    buffer = buffer + directory + '/IO,\n';
    target = directory+"/PRR/IO.RPT";
    if os.path.isfile(target):
        fileOpen = open(target);
        text = fileOpen.read();
        fileOpen.close();
        readIO(text);
        print(directory+' IO found');
    else:
        text = "File not present";
        print(directory+' IO not found');
    return text;

def readDeclare(declareRPT): #reads values imported from a declare report
    global buffer
    for i in range(len(declareRPT)-8):
        if declareRPT[i:(i+4)] == 'Name':
            #print('Found one!')
            nameIs =getName(declareRPT[i+6:]); 
            nextInput = declareRPT[i+6+len(nameIs):];
            typeIs = getType(nextInput); 
            addressIs = getDeclareAddress(nextInput);
            addToBuffer = nameIs + ',' + typeIs + ',' + addressIs;
            buffer = buffer + nameIs + ',' + typeIs + ',' + addressIs + ',\n';
    return();

def readIO(IORPT): #reads values imported from an IO report
    global buffer
    for i in range(len(IORPT)-8):
        if IORPT[i:(i+4)] == 'Name':
            #print('Found one!');
            nameIs = getName(IORPT[i+6:]);
            nextInput = IORPT[i+6+len(nameIs):];
            typeIs = getType(nextInput);
            addressIs = getIOAddress(nextInput);
            addToBuffer = nameIs + ',' + typeIs + ',' + addressIs +',\n';
            buffer = buffer + addToBuffer;
    return();

                         
def getName(text): #reads the text until the first space
    i = 0;
    while(not(text[i].isspace())):
        i = i + 1;
    #print('First space is at ',i);
    hasTheName = text[:i];
    return(hasTheName);

def getType(text):
    i=0; #remove spaces
    while(text[i].isspace()):
        i = i + 1;
    i = i + 6; #remove Type :
    
    if (text[i:i+10] == 'B  Boolean'):
        dataType = 'B';
    elif (text[i:i+10] == 'I  Integer'):
        dataType = 'I';
    elif (text[i:i+7] == 'R  Real'):
        dataType = 'R';
    elif (text[i:i+13] == 'ST Slow Timer'):
        dataType = 'ST';
    elif (text[i:i+16] == 'BA Boolean Array'):
        dataType = 'BA';
    elif (text[i:i+16] == 'AO Analog output'):
        dataType = 'AO';
    elif (text[i:i+15] == 'AI Analog input'):
        dataType = 'AI';
    elif (text[i:i+16] == 'DI Digital input'):
        dataType = 'DI';
    elif (text[i:i+17]  == 'DO Digital output'):
        dataType = 'DO';
    elif (text[i:i+14] == 'WO Word Output'):
          dataType = 'WO';
    elif (text[i:i+13] == 'WI Word Input'):
          dataType = 'WI';
    else:
          dataType = 'error';

    #print(text[i:i+12]);
    return dataType;

def getDeclareAddress(text): #if it has a %--- address, get it before the next name
    i = 0; n = 0; foundIt = False; value = 'Automatic';
    while (not(text[i:(i+4)] == 'Name') and not foundIt and not(text[i] == '-')):
        #print(i);
        i = i+1;
        if text[i].isspace() and n>0:
            foundIt = True;
            value = text[n:i];
        elif (text[i] == '%'):
            n=i; #mark the start position
    #print(value);
    return(value);        

def getIOAddress(text): #if it has a Reserved Address, get it before the next name
    i = 0; n = 0; foundIt = False; value = 'Automatic'; nextValue = False;
    while (not foundIt and not nextValue):
        if (text[i] == '-'):
           nextValue = True;
        elif (text[i:i+9] == 'Address: '):
            foundIt = True; n = i;
        i = i + 1;
    if (n > 0) and not text[i] == '-':
        i = i+9;
        while (not(text[i].isspace())):
            i = i + 1;
        value = text[n+9:i];
    return(value);
        

#Think of this as the main section of the program
openProgram("HZPS");
openProgram("HH");
openProgram("FWPS");
