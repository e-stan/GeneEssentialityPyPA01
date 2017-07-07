from EssentialGeneFinder import *
from pandas import DataFrame


def creationOfEssentialReactData():
    assent = ['GSE90620','GDS4244','GDS3572','GSE30021','GSE65870']
    nsamples = [12,12,6,9,6]
    model = cobra.io.read_sbml_model("iPAE1146.xml")
    createEssentialReactionModel(model,'IPAE1146')
    for i in range(len(assent)):
        createSingleReactionDeletionData(assent[i],model,nsamples[i],'C:\Users\Ethan Stancliffe\Desktop\Summer2017\Papin Lab\Pseudomonas Aeruginosa ABR Project\GeneEssentialityPA01')



#creationOfEssentialReactData()

normal = ComparisionGene('IPAE1146','This is a test',type = 'React')

reference = {'GSE90620':[0,0,0,1,1,1,1,1,1,1,1,1],'GDS3572':[1,1,1,0,0,0],'GSE65870':[1,1,1,1,1,1],'GDS4244':[0,0,0,0,0,0,1,1,1,1,1,1],'GSE30021':[0,0,0,0,0,0,1,1,1]}

CSD = []

controlSample = DataFrame(columns = ['Name', 'Count', 'Mean', 'Std', 'Sum', 'Pvalue', 'GEM_FBM', 'CS_FBM'])
experimentalSample = DataFrame(columns = ['Name', 'Count', 'Mean', 'Std', 'Sum', 'Pvalue', 'GEM_FBM', 'CS_FBM'])
data = [controlSample,experimentalSample]
for x in reference:
    temp = CSGene(x,reference[x],type = 'React')
    temp.processSamples()
    CSD.append(temp)

results = []
i=0
sampleCount = [0,0]
typeOfSample = [0,1]
for g in typeOfSample:
    results = []
    i = 0
    j=0
    sampleCount[g] = 0
    for x in CSD:
        temp,tempCount = x.findChangedFluxGenes(normal.getData(),g)
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
        sampleCount[g]+= tempCount

    types = {1: 'ExperimentalReact', 0: 'ControlReact'}
    for x in results:
        name,count,mean,std,sum,pval = x.letsPrint()
        if( abs(mean) > .001 ):
            data[g].loc[j] = [name,count,mean,std,sum,pval,str(normal.getData()[x.name]),normal.getData()[x.name]+ mean]
            j+=1
    print data[g]
    footer = 'Total Number of %s Samples = %d' % (types[g],sampleCount[g])
    print footer
y = []
for z,m,sd in zip(data[1]["Name"].values,data[1]["Mean"].values,data[1]["Std"].values):
    try:
        con = controlSample.loc[controlSample['Name'] == z]
        y.append(t_testUnpaired_fromSum(m,sd**2,sampleCount[1],con['Mean'].values,con['Std'].values**2,sampleCount[0]))
    except:
        y.append(0.0)
    print y
data[1].insert(len(data[1].columns.values),"PVal(cont)", y)
i = 0;
for x in data:
    x.to_csv(types[i]+'.txt',sep = " ",float_format="%.5f",index=False)
    i+=1

