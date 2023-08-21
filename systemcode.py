import BarcodeScanner
import online
import motor
import time

looptest = True

while looptest:
    #t0 = time.perf_counter()
    BarcodeScanner.scanner()
    #t1 = time.perf_counter()
    #print("Execution time for scanner: ", t1 - t0, "seconds")
    
    file1 = open("dataFiles.txt", "r") 
    parse_data = file1.readline()
    file1.close()

    #will stop code and check bool at start of while after clearing dataFiles
    if parse_data == "exit code":
        looptest = False
        
        #clears file
        parsedData = open("dataFiles.txt",'a')  
        with open("dataFiles.txt",'r+') as file:
            file.truncate(0)
        parsedData.close()
        
        break
    
    if parse_data != "":
        binnumber = online.onlinedaq()
        
        t3 = time.perf_counter()
        motor.control(binnumber)
        t4 = time.perf_counter()
        print("Execution time for motor: ", t4 - t3, "seconds")
        
    #binnumber = online.onlinedaq()

    #code to clear file
    parsedData = open("dataFiles.txt",'a')  
    with open("dataFiles.txt",'r+') as file:
        file.truncate(0)
    parsedData.close()
        