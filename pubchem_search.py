#Kuijun
#

from random import shuffle
import numpy as np
import pickle
import sys
import pybel
import fp_con_func
#---------Load the data-----------
input_file = "NIST20_LR_predic_dict.p"

with open(input_file, 'rb') as handle:
    DATA = pickle.load(handle)

 
#---------Take a look at input_pickle(with first 10 inchikeys)-----------
sam_p = {}
s = 0
for key,value in DATA.items():
    sam_p[key]=value
    s = s + 1
    if s > 100:
        break
 #value[0]: compound name
 #value[1]: inchikey
 #value[2]: formulas
 #value[3]: precursor mass
 #value[4]: exact mass
 #value[5]: mass spectra length 945
 #value[6]: predict fingerprint length 528

 
#--------Extract the inchikey from the original data in a dict---------
eva={}
for key,value in DATA.items():
	eva[key] = [value[0],value[1],value[2],value[-1]]
 #value[0]: compound name
 #value[1]: inchikey
 #value[2]: formulas
 #value[3]: predict fingerprint length 528
    
#--------Search Formula using Pubchempy---------
import pubchempy
i=0
#empty result dict with key=inchikey, value=formular, candidates

for key,value in eva.items():
	if len(value)>7:
		print("skip the "+str(i)+" inchikey")
		continue
	try:
		print("now handling the "+str(i)+" inchikey")
		print(key)
		candidate_dict={}
		#----use inchikey to search for formula(pubchempy)----
		formula=pubchempy.get_compounds(identifier=key,namespace="inchikey")[0].molecular_formula
		print("formula is retrieved:"+formula)
        #----use formula to search for candidate(pubchempy)----
		candidate_list = pubchempy.get_compounds(identifier=formula,namespace="formula",listkey_count=100)
		print("this compound has "+str(len(candidate_list))+" candidates#")
        #----use candidate smile to search fingerprint (OpenBabel)----
		used_list=[]
		for candidate in candidate_list:
			if candidate.inchikey.split("-")[0] not in used_list:
				used_list.append(candidate.inchikey.split("-")[0])
				smiles=candidate.canonical_smiles
				mol = pybel.readstring( "smi", smiles)
				fp_vec=fp_con_func.fp_con_func(mol.calcfp('FP3').bits,mol.calcfp('FP4').bits,mol.calcfp('MACCS').bits)
				candidate_dict[candidate.inchikey]=fp_vec 
		value.append(candidate_dict)#save the candidate inchikey and fingerprint
		i+=1

		print("currently we have {} compound for evaluation".format(len(candidate_dict.keys())))
		print("\n")

	except Exception as e:
		print(e)
		print("@@@@@@@@@@@@@@ this compound("+key+") is bad")
		i+=1
		print("currently we have {} compound for evaluation".format(len(candidate_dict.keys())))
		print("\n")

        

# -----------output file---------
pickle_out = open("NIST20_LR_pubchemcandidate.p", "wb")
pickle.dump(eva, pickle_out)
pickle_out.close()
