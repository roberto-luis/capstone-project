#take data set and parse information

def parseData(data, MouserPN):

    #check the beginning of the string to see the vendor
    if data.startswith(">"):
        parsedDataStr = "K5Mouser, "
    elif data.endswith("0000000000000000000000"):
        parsedDataStr = "K5Digikey, "
    elif data.startswith("["):
        parsedDataStr = "K5ti, "
    else:
        parsedDataStr = "K5UnkownVendor,"

    #if statements to find the beginning of the codes used to identify different information
    #if the code is found then the relevent information is taken from the string and saved as a new variable
    #The new variable is then added to the string parsedDataStr

    #Vendor Part Number
    if data.find('P') and data.startswith('['):
        vendorPartNum = data[data.find('P')+1:]
        vendorPartNum = vendorPartNum[:vendorPartNum.find('\x1d')]
        if len(vendorPartNum) != 0:
            parsedDataStr += ("K9" + vendorPartNum + ",")
        
    #Adding Mouser P/N to list
    if MouserPN != 0:
        parsedDataStr += ("K9" + MouserPN + ",")

    #Manufacturer Part Number
    if data.find('1P') != -1:
        partNum = data[data.find('1P')+2:]
        partNum = partNum[:partNum.find('\x1d')]
        if len(partNum) != 0:
            parsedDataStr += ("K1" + partNum + ",")

    #Part Order Number
    #if data.find('\x1dK') != -1:
    #    customPO = data[data.find('K')+1:]
    #    customPO = customPO[:customPO.find('\x1d')]
    #    parsedDataStr += ("PONumber" + customPO + ",")

    #Line Item
    #if data.find('14K') != -1:
    #    lineItem = data[data.find('14K')+3:]
    #    lineItem = lineItem[:lineItem.find('\x1d')]
    #    parsedDataStr += ("lineItem" + lineItem + ",")

    #Quantity
    #if data.find('Q') != -1:
    #    quantity = data[data.find('Q')+1:]
     #   quantity = quantity[:quantity.find('\x1d')]
     #   parsedDataStr += ("K9" + quantity + ",")

    #Invoice Number
    #if data.find('11K') != -1:
    #    invoiceNum = data[data.find('11K')+3:]
    #    invoiceNum = invoiceNum[:invoiceNum.find('\x1d')]
    #    parsedDataStr += ("InvoiceNum" + invoiceNum + ",")

    #Country of Origin
    #if data.find('4L') != -1:
    #    countryOrigin = data[data.find('4L')+2:]
    #    countryOrigin = countryOrigin[:countryOrigin.find('\x1d')]
    #    parsedDataStr += ("COO:" + countryOrigin + ",")

    #Manufacturer
    if data.find('1V') != -1:
        mfg = data[data.find('1V')+2:]
        mfg = mfg[:mfg.find('\x1d')]
        parsedDataStr += ("K2" + mfg + ",")

    #SO Number
    #if data.find('\x1d1K') != -1:
    #    soNum = data[data.find('1K')+2:]
    #    soNum = soNum[:soNum.find('\x1d')]
    #    parsedDataStr += ("SO#:" + soNum + ",")

    #Part ID
    if data.find('12Z') != -1:
        partID = data[data.find('12Z')+3:]
        partID = partID[:partID.find('\x1d')]
        parsedDataStr += ("PartID:" + partID + ",")

    #Load ID
    #if data.find('13Z') != -1:
    #    loadID = data[data.find('13Z')+3:]
    #    loadID = loadID[:loadID.find('\x1d')]
    #    parsedDataStr += ("LoadID:" + loadID + ",")

    #Opens and writes the parsedDataStr to a text file
    #Specifically uses the append function so it does not overwrite previous data to the same file
    parsedData = open("dataFiles.txt",'a')
    #code to clear file
    with open("dataFiles.txt",'r+') as file:
        file.truncate(0)
        
    parsedData.write(parsedDataStr + '\n')
    parsedData.close()