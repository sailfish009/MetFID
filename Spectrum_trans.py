import fpAssist_REVISED as fp
import pandas as pd
import pickle
import pybel
import pubchempy

# ------------------------------------------------------------- File Handling ------------------------------------------------------------- 

df = "All_LR.p"
output_file = "All_LR1.p"

# -------------------------Step 1---------------------------
# ----------------------------------------------------------
# -------------------------------------------------------- Merging and Filtering -------------------------------------------------------- 

inch_ref_list= []
combined_List = []

df_read = pd.read_pickle(df)
combined_List.extend(df_read.values.tolist())
    
combined_List = fp.mzRange(combined_List)
scans, merge = fp.inchikey_Dup_merge(combined_List)

# -------------------------Step 2---------------------------
# ----------------------------------------------------------
database = scans
# ---------------------------------------------------- Vector Transformation Function ----------------------------------------------------- 

def vec_transformation(mz,intensity,first_digi=39):


	input_vec=[0]*1553 #39-1591
	mz=[int(round(i,0))-first_digi for i in mz]

	intensity_digi=0
	for i in mz:
		input_vec[i]+=intensity[intensity_digi]
		intensity_digi+=1

	return input_vec

# ----------------------------------------------------------- SMILES Calculation ---------------------------------------------------------- 

# This step queries a database to identify the SMILES, a type of chemical notation that portrays structural information about the molecule


database_with_smiles = {}
i = 0

for key,value in database.items():
	i += 1
	print(i)
	try:
		print(key)
		smiles = pubchempy.get_compounds(identifier=key,namespace="inchikey")[0].canonical_smiles
		value[2] = smiles
		database_with_smiles[key]=value
	except:
		print("skipped")
		continue


# --------------------------------------------------------------- Filtering -------------------------------------------------------------- 

# Filters out compounds that do not fit into our molecular weight range

DATA = {}
for key,value in database_with_smiles.items():
	if value[9] <= 1010:
		DATA[key] = value
		
print(len(DATA.keys()))

# ---------------------------------------------------------- Vector Transformation --------------------------------------------------------- 

for key, value in DATA.items():
	value.append(vec_transformation(value[-2],value[-1]))

# ------------------------------------------------------ Eliminating Unneccessary Bins ----------------------------------------------------- 

# Removes bins from the vectors  that have little significance 

spec_set = []
for key, value in DATA.items():
	spec_set.append(value[-1])
	value.append([])


for m in range(len(spec_set[0])):
	all_zero=True
	for key,value in DATA.items():
		if value[-2][m]!=0:
			all_zero=False
			break
	if all_zero==False:
		for key,value in DATA.items():
			value[-1].append(value[-2][m])

# -------------------------Step 3---------------------------
# ----------------------------------------------------------
database = DATA
# ---------------------------------------------------- Fingerprint Conversion Function ----------------------------------------------------- 

def fp_conversion(fp3,fp4,macc,fp3_digi=23,fp4_digi=79,macc_digi=83):
	
	fp3_temp=[3, 5, 27, 28, 29, 30, 31, 34, 37, 38, 45, 48, 49, 51, 50, 35, 39, 40, 19, 4, 54, 41, 25]
	fp4_temp=[1, 2, 3, 12, 13, 14, 15, 41, 49, 56, 63, 74, 85, 88, 135, 169, 274, 275, 279, 281, 282, 283, 287, 300, 302, 303, 305, 5, 84, 137, 301, 16, 276, 289, 290, 18, 170, 136, 177, 182, 184, 4, 19, 86, 280, 278, 65, 66, 48, 23, 24, 25, 26, 33, 171, 179, 28, 121, 180, 181, 113, 143, 176, 112, 125, 98, 101, 40, 138, 102, 214, 57, 284, 183, 172, 127, 9, 72, 100]
	macc_temp=[50, 53, 54, 57, 66, 72, 76, 82, 89, 90, 91, 96, 98, 99, 101, 105, 109, 112, 113, 115, 118, 120, 123, 126, 127, 131, 132, 136, 137, 138, 139, 140, 143, 145, 146, 147, 150, 152, 153, 154, 155, 160, 162, 163, 26, 108, 116, 128, 129, 149, 62, 104, 144, 93, 141, 74, 83, 114, 80, 86, 100, 111, 142, 151, 158, 161, 75, 85, 121, 122, 135, 148, 156, 65, 79, 97, 92, 110, 117, 133, 95, 78, 119]

	fp3_box=[0]*fp3_digi
	fp4_box=[0]*fp4_digi
	macc_box=[0]*macc_digi

	fp3_temp=list(range(1,56))
	fp4_temp=list(range(1,308))
	macc_temp=list(range(1,167))
	fp3_box=[0]*len(fp3_temp)
	fp4_box=[0]*len(fp4_temp)
	macc_box=[0]*len(macc_temp)


	for i in range(len(fp3_temp)):
		if fp3_temp[i] in fp3:
			fp3_box[i]=1


	for i in range(len(fp4_temp)):
		if fp4_temp[i] in fp4:
			fp4_box[i]=1


	for i in range(len(macc_temp)):
		if macc_temp[i] in macc:
			macc_box[i]=1

	return fp3_box+fp4_box+macc_box


# ----------------------------------------------------------- Fingerprint Conversion ----------------------------------------------------------- 

for key, value in database.items():
	print(key)
	smiles=value[2]
	mol = pybel.readstring( "smi", smiles)
	fp_vec=fp_conversion(mol.calcfp('FP3').bits,mol.calcfp('FP4').bits,mol.calcfp('MACCS').bits)
	value.append(fp_vec)

# ---------------------------------------------------------------- Output ---------------------------------------------------------------- 

pickle_out = open(output_file, "wb")
pickle.dump(database, pickle_out)
pickle_out.close()
