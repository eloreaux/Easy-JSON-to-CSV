"""Utility Functions"""

# This is the limit of columns allowed for lists of multiple values
# if the repLimit argument is invoked. Feel free to change.
REPLIMIT = 3

BLANKVALUE = ""

def addStringValue(dictObj, key, value, row):
    """Adds a string value to a dictionary of lists under a new or existing key.
    
    Args:
        dictObj: (dict) dictionary object to add value to
        key: (str) current key of interest
        value: (str) current value of interest
        row: (int) current number of rows in dictionary object

    ------------------------------------------------------
    Returns:
        NULL
    """

    if key in dictObj:
            dictObj[key].append(value)
    else:
        dictObj[key] = ([BLANKVALUE] * row) + [value]


def addListValue(dictObj, key, listValue, row, repLimit = False):
    """Adds a list value to a dictionary of lists under a new or existing key,
        by using a different key for each item in the list.

    Args:
        dictObj: (dict) dictionary object to add value to
        key: (str) current key of interest (will serve as root for other keys)
        listValue: (list) current value of interest
        row: (int) this gives you the ability to limit the amount of new columns created.
            e.g. if customer_phone_number key has a list value of 10 numbers, will only create
            a certain number of columns before discarding the rest.
        repLimit: (bool) this gives you the ability to limit the amount of new columns created.
            e.g. if customer_id key has a list value of 10 keys, will only create
            'REPLIMIT' columns and discard the rest.

    ------------------------------------------------------
    Returns:
        NULL

    """

    # the stringList argument is assumed to be False, since this function
    # shouldn't be called if it is True.

    for index, value in enumerate(listValue):
        if repLimit:
            if index == REPLIMIT:
                break
        if index == 0:
            addValue(dictObj, key, value, row, stringList = False)
        else:
            addValue(dictObj, key+"."+str(index+1), value, row, stringList = False)


def addValue(dictObj, key, value, row, stringList = False, repLimit = False):
    """Adds an arbitrary value to a dictionary of lists under a new or existing key.
    
    Args:
        dictObj: (dict) dictionary bucket to add value to
        key: (string) current key of interest
        value: (str | dict | list) current value of interest
        row: (int) current row of bucket, for filling in empty values
            when a never before seen column is created
        stringList: (bool) whether entries in list form should be kept as a large string object,
            or whether they should be enumerated as different columns (e.g. if a "customer_id"
            key in a dict has a list of two ids, [123,321], stringList = False will lead to two columns,
            customer_id with value 123, & customer_id.2 with value 321. stringList = True will lead to
            one column, customer_id with value '[123, 321]')
        repLimit: (int) used if stringList = False - likely unnecessary;
            this gives you the ability to limit the amount of new columns created.
            e.g. if customer_id key has a list value of 10 keys, will only create
            'REPLIMIT' columns and discard the rest.

    ------------------------------------------------------
    Returns:
        NULL
    """
    
    if type(value) == str:
        
        # simplest case - if value is just a string, add it
        addStringValue(dictObj, key, value, row)
    
    elif type(value) == dict:
        
        # create new series of keys with original 'key' as root, go deeper
        for key2 in value:
            addValue(dictObj, key+"."+key2, value[key2], row, stringList = stringList, repLimit = repLimit)
    
    elif type(value) == list:

        if len(value) == 1:
            addValue(dictObj, key, value[0], row, stringList = stringList, repLimit = repLimit)
        else:
            if stringList:
                addStringValue(dictObj, key, str(value), row)
            else:
                addListValue(dictObj, key, value, row, repLimit = repLimit)

def dictDump(emptyDict, fillDict, emptyDictQuantity, fillDictQuantity):
    """Empty one set of dictionary values into another dictionary

    Args:
        emptyDict: (dict) dictionary to be emptied
        fillDict: (dict) dictionary to be filled
        emptyDictQuantity: (int) quantity of rows in dictionary to be emptied
        fillDictQuantity: (int) quantity of rows in dictionary to be filled

    ------------------------------------------------------
    Returns:
        {}: empty dict to replace the dict to be emptied
    """

    for key in emptyDict:
        if key in fillDict:
            fillDict[key] += emptyDict[key]
        else:
            fillDict[key] = ([BLANKVALUE] * fillDictQuantity) + emptyDict[key]
    for key in fillDict:
        if key not in emptyDict:
            fillDict[key] += ([BLANKVALUE] * emptyDictQuantity)

    return {}


def valuesPush(dictList, quantitiesList, transferQuantity, index = 0):
    """Recursively pushes all values in full dict up to next highest dict in a list of dicts;

    Args:
        dictList: (list) list of dictionarys with rows
        quantitiesList: (list) list of row quantities in dictionaries
        transferQuantity: (int) This is the max quantity of values in the first bucket
            before it is dumped to a larger bucket with 100X capacity.
        index: (int) at what location in the list is the valuesPush being initiated

    ------------------------------------------------------
    Returns:
        NULL
    """
        
    # check if a larger bucket exists
    # if not, make a new one
    if len(dictList) == index + 1:
        dictList.insert(index, {})
        quantitiesList.insert(index, 0)
    else:
        
        dictList[index] = dictDump(emptyDict = dictList[index],
                                    fillDict = dictList[index + 1],
                                    emptyDictQuantity = quantitiesList[index],
                                    fillDictQuantity = quantitiesList[index + 1])

        # set the new quantities
        quantitiesList[index+1], quantitiesList[index] = quantitiesList[index] + quantitiesList[index+1], 0
        
        # check if we have now exceeded the max capacity of next highest dict
        if quantitiesList[index + 1] > transferQuantity * 100:
            index += 1
            transferQuantity *= 100
            valuesPush(dictList, quantitiesList, transferQuantity, index)

