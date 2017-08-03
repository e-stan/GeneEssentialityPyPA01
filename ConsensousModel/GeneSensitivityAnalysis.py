import CSModelDataScripts.ABResistanceAnalysis
import cobra.io
import ModelComparison
from multiprocessing import Process
from pandas import DataFrame,concat

"""Script for creating, analyzing, and comparing consensus models for a resistant and control model. Also a sensitivity analysis can be performed by sequentially activating sets of genes
The script relies on the ModelComparision and ABResistanceAnalysis files."""
model = cobra.io.read_sbml_model('iPAE1146.xml') #read base model

#Load in gene lists
geneListF = open('sharedGenes.txt', 'r')
geneListShared = [x[:-1] for x in geneListF.readlines()]
geneListF.close()
geneListF = open('RUniqGenes.txt', 'r')
geneListR = [x[:-1] for x in geneListF.readlines()]
geneListF.close()
geneListF = open('CUniqGenes.txt', 'r')
geneListC = [x[:-1] for x in geneListF.readlines()]
geneListF.close()
geneListCT = set(geneListShared + geneListC)
geneListRT = set(geneListShared + geneListR)
model.solver = 'gurobi'#change solver (may be different depeneding on system. I found gurobi to be the best with loopless FVA

results = dict()
#orderOfDel = [[[x],[]] for x in geneListC] + [[[],[x]] for x in geneListR]#delete impactful genes sequentially
orderOfDel = [[[],[]]] #manualy specify genes to be activated
mapDel2Res = {x:y for x,y in zip(range(len(orderOfDel)),orderOfDel)} #creating indexing scheme for order of activation
i = 0
x1_old = 5
x0_old = 5

for x in orderOfDel:
    rc = 0
    cc = 0
    #perform appropriate deletions, conditions make sure the same results aren't tabulated consecutively
    if not len(x[1]) == 0:
        CSModelDataScripts.ABResistanceAnalysis.consensusModelCreator(model.copy(), 'Resistant', list(geneListRT - set(x[1])))
        rc += 1
    if len(x[1]) == 0 and not x1_old == 0:
        CSModelDataScripts.ABResistanceAnalysis.consensusModelCreator(model.copy(), 'Resistant', list(geneListRT))
        rc += 1
    if not len(x[0]) == 0:
        CSModelDataScripts.ABResistanceAnalysis.consensusModelCreator(model.copy(), 'Control', list(geneListCT - set(x[0])))
        cc += 1
    if len(x[0]) == 0 and not x0_old == 0 :
        CSModelDataScripts.ABResistanceAnalysis.consensusModelCreator(model.copy(), 'Control', list(geneListCT))
        cc += 1
    #run comparision
    results[i] = ModelComparison.run()

    #print cuurent results
    print results[i]

    i += 1
    x0_old = len(x[0])
    x1_old =len(x[1])

data = DataFrame.from_dict(results,orient='index')
data = concat([data,DataFrame.from_dict(mapDel2Res,orient = 'index')],axis = 1)
data.to_csv('sensitivityResults.csv')#output sensitivity results. First column is the number of unique reaction removals. Second is the number of FVA differences
print data




