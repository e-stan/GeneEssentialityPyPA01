from EssentialGeneFinder import *
from copy import deepcopy


def creationOfEssentialGeneData():
    assent = ['GSE90620','GDS4244','GDS3572','GSE30021','GSE65870']
    nsamples = [12,12,6,9,6]

    for i in range(len(assent)):

        createEssentialGeneDataAssent(assent[i],'.mat',nsamples[i],'C:\Users\Ethan Stancliffe\Desktop\Summer2017\Papin Lab\Pseudomonas Aeruginosa ABR Project\GeneEssentialityPA01')
      #  model = cobra.io.read_sbml_model("iPAE1146.xml")
       # createEssentialGeneModel(model,'IPAE1146')


#creationOfEssentialGeneData()

#model = cobra.io.read_sbml_model("iPAE1146.xml")
#createEssentialGeneModel(model,'IPAE1146')

normal = ComparisionGene('IPAE1146','This is a test')



reference = {'GSE90620':[1,1,1,0,0,0,0,0,0,0,0,0],'GDS3572':[0,0,0,1,1,1],'GSE65870':[0,0,0,0,0,0],'GDS4244':[1,1,1,1,1,1,0,0,0,0,0,0],'GSE30021':[1,1,1,1,1,1,0,0,0]}

CSD = []


for x in reference:
    temp = CSGene(x,reference[x])
    temp.processSamples()
    CSD.append(temp)

results = []
i=0
for x in CSD:
    temp = x.findChangedFluxGenes(normal.getData())
    s = len(results)
    if i==0:
        results = temp[:]
    else:
        for y in temp:
            count = 0
            for z in range(s):

                if results[z].areEqual(y):
                    results[z].combine(y)
                    count += 1
                    break
            if count == 0:
                results = results + [y]
    i+=1
for x in results:
    x.letsPrint()


"""
uniqueData = list()

for x in CSD:
    temp,c,b = x.findUniqueFrom(normal.getData())
    uniqueData.append(temp)
    pings = list()
    count = 0

pings = findNumberofHits(uniqueData)

[j.letsPrint() for j in pings]
"""
