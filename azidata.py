import pandas as pd
import requests
import json
import time

debut = time.time()

DATAPATH="./data/"

dfInsee = pd.read_csv(DATAPATH+'correspondance-code-insee-code-postal.csv', sep=";")

listInsee = dfInsee['Code INSEE'].tolist()

# limitInsee à choisir (nb insee : 36742 - temps:  )
#limitInsee=100
limitInsee=len(listInsee)
listAziData = list()

'''

for i, codeInsee in enumerate(listInsee, 1):
    if i <= limitInsee:
        print(codeInsee)
        url = "https://www.georisques.gouv.fr/api/v1/gaspar/azi?code_insee=" + codeInsee + "&rayon=10000"
        dicAzi = json.loads(requests.get(url).text)
        listAziData = listAziData + dicAzi['data']
    else:
        break
'''
def enumerate_with_step(iterable, start=0, step=1):
    for i, item in enumerate(iterable):
        yield start + i * step, item
li=0
starticodeinsee=2-2
#starticodeinsee=36731-2 # idx = ligne xls -2 pour code 32383
for i in range(starticodeinsee,len(listInsee),10):
    if i <= limitInsee:
        #print(listInsee[i])
        urlinsee=""
        for j in range(1,10,1):
            k=i+j-1
            if k > len(listInsee) -1:
                break
            else:
                urlinsee=urlinsee + listInsee[k]
                if j < 9 and k < len(listInsee) -1:
                    urlinsee=urlinsee+','

        url = "https://www.georisques.gouv.fr/api/v1/gaspar/azi?code_insee=" + urlinsee + "&rayon=10000"
        li+=1
        print("url", li, ":" , urlinsee)
        dicAzi = json.loads(requests.get(url).text)
        listAziData = listAziData + dicAzi['data']
    else:
        break

#print(len(listAziData))


dfAziData = pd.DataFrame(listAziData)
print(dfAziData.head()['code_insee'])

dfAziData.to_json(DATAPATH+'azidata.json', orient='index')
fin = time.time()
