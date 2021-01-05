from collections import Counter
import pandas as pd
import pickle
import pybel

# ------------------------------------------------------------- File Handling ------------------------------------------------------------- 

#input_file = "NIST_LR_vec.p"
#output_file = "NIST_LR_fp.p"


#with open(input_file, 'rb') as handle:
#    database = pickle.load(handle)

# ---------------------------------------------------- Fingerprint Conversion Function ----------------------------------------------------- 

def fp_con_func(fp3,fp4,macc,fp3_digi=23,fp4_digi=79,macc_digi=83):
	
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

#for key, value in database.items():
#	print(key)
#	smiles=value[2]
#	mol = pybel.readstring( "smi", smiles)
#	fp_vec=fp_conversion(mol.calcfp('FP3').bits,mol.calcfp('FP4').bits,mol.calcfp('MACCS').bits)
#	value.append(fp_vec)

# ---------------------------------------------------------------- Output ---------------------------------------------------------------- 

#pickle_out = open(output_file, "wb")
#pickle.dump(database, pickle_out)
#pickle_out.close()

