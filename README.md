# innovationsproject

there are 3 classes:
clipboard - copy text from clipboard computer(as we do copy on keyboard)
keyListener - log every alphabet char that pressed on the keyboard
temperature - take the cpu temperature and log it(right now only the cpu temp)

those classes uses in dictionary structure and use in 3 storage access:
reddisDB - working as data structure - contain hash and list. we use on hash
elasticSearch - working as indexs so every index will have its own data with type(int/double/date/etc) and id of every document
mongoDB - working as collections which contains documents. every document conatin data as json, key and value

*the program is running in 3 threads which means need to be careful when we access to same object on the 3 classes.
*i made a logger which wrote the logs to file and print them to console.


for each storage access we have a structure to each class:
reddisDB:
    will contain a dict that all 3 classes have data together. the key is what different between them. will have a key which is a date of today without time. the value will be the data from 3 classes. the structure will look like that:
        "10/8/2020": {
        a:1,
        b:2,
        cpu:[60,50,30,20,50],
        clipboard:[some,text,that,copied]
        }


    -clipboard -  will have structure like that:
        {clipboard:[some,text,that,copied]}

    -keyListener - will have structure like that:
        {a:1,b:2,c:3, d:9}

    -temperature - will have structure like that:
        {cpu:[60,50,30,20,50]}

    there were a problem that because the program running on 3 threads, and i made a common dict for all 3 classes, they access to the object on same time and override the data of other. what cause to update incorrect data on redisDB. the solution is to use on data struture syncronized. i used on queue which after on every update of the object, i added to the queue and then the update to reddisDB done by the queue object and there is a real queue to update the data instead update on same time.

elasticSearch:
    will contain index for each class with value of date + class name. i made it like
    that because if i will do it only with date all the data from three classes will mix, and i want to sepreate them. the date will be without any special char because elastic doesnt support that. for example: "1882020keyListner"

    -clipboard - will have structure like that:
        index: 1882020keyListner(date + class name) 
        data: {a:1,b:2,c:3}

    -keyListener - will have structure like that:
        index: 1882020cpu(date + class name) 
        data: {cpu:[60,70,10]}  

    -temperature - will have structure like that:
        index: 1882020clipboard(date + class name) 
        data: {clipboard: [some,text,copied,here]}

mongoDB:
    will contain db in name of "innovations" which contain 3 colletions, the name of the collection will see like that: (date + class name), for example, "24082020keyListner".
    the date is without special chars for convient. so there will be 3 collections which conatin the data in json/dict. the collections names:
    %date%keyListner, for example, 24082020keyListner
    %date%temperature, for example, 24082020temperature
    %date%clipboard, for example, 24082020clipboard

    the data object will contain key with name of the class and the data of the class.

    -clipboard - will have structure like that:
        collection name: 24082020clipboard:
        data: {name: clipboard, data: [some,text,that,copied]}

    -keyListener - will have structure like that:
        collection name: 24082020keyListner:
        data: {name: keyListner, data: {a:1,b:2,c:3,g:8}}

    -temperature - will have structure like that:
        collection name: 24082020temperature:
        data:  {name: cpu, data: [10,70,50]}