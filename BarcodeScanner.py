import cv2
from pylibdmtx.pylibdmtx import decode as dmdecode
import time
from parseData import parseData
from imgcropping import detect_dataMatrix
from pyzbar import pyzbar

def scanner():
    #Opens a video file
    vc = cv2.VideoCapture(0)
    data_set = [] #list of data to save as backup

    #Check to see if camera is working properly
    if vc.isOpened():
        camOp, frame = vc.read()
        print("Camera operating")
    else:
        camOp = False

    #Continuous camera operation
    while camOp:
        camOp, frame = vc.read()
        key = cv2.waitKey(1) #defines key wait for a key to be pressed
        dataScanned = False
        MouserPN = 0
        
        #if ESC pressed program will exit
        if key == 27:
            
            parsedData = open("dataFiles.txt",'a')  
            with open("dataFiles.txt",'r+') as file:
                file.truncate(0)
                parsedData.write("exit code")
            parsedData.close()
    
            break
        
        #Searches frames for barcodes
        if pyzbar.decode(frame):
            t0 = time.perf_counter()
            
            #take image of video feed           
            barcodePic = cv2.imwrite("barcodetest.jpg", frame)
            
            #make img a variable to decoe
            img = cv2.imread("barcodetest.jpg")
            
            #decode the image and grab all the barcodes found in the image
            barcodePicScan = pyzbar.decode(img)

            #search the list decoded barcodes
            for barcodePicScan in barcodePicScan:

                #if "-" is found in third position it is the Mouser P/N
                if barcodePicScan.data.decode().find("-") == 3:
                    #print("test1")
                    MouserPN = barcodePicScan.data.decode()
                    
                    dataMouser = "K5Mouser," + "K9" + MouserPN
                    
                    parsedData = open("dataFiles.txt",'a')
                    #code to clear file
                    with open("dataFiles.txt",'r+') as file:
                        file.truncate(0)
                    
                    parsedData.write(dataMouser + '\n')
                    parsedData.close()
                    break

                    
            
        #stop video capture and exit BarcodeScanner program
        if MouserPN != 0:
            t1 = time.perf_counter()
            print("Execution time for scanner: ", t1 - t0, "seconds")

            break
        
        #check to see if dataMatrix is in frame
        if detect_dataMatrix(frame):

            t2 = time.perf_counter()

            #read dataMatrix from file and decode
            dataMatrix = cv2.imread("datamatrix.jpg")
            dmData = dmdecode(dataMatrix, max_count=1,timeout=100)
            
            #if data is decoded then parse and send to online DAQ
            if len(dmData) != 0:
                data = dmData[0][0].decode('utf-8')
                parseData(data,MouserPN)
                dataScanned = True
                

            
            
        #stop video capture and exit BarcodeScanner program
        if dataScanned:
            t3 = time.perf_counter()
            print("Execution time for 2d matrix scanner: ", t3 - t2, "seconds")
            break

        cv2.imshow('Scanner', frame)

        #creates a millisecond of delay between frames
        cv2.waitKey(1)

    #releases the video feed for a clean exit
    vc.release()
