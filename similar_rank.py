# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 02:28:49 2020

@author: kuijun
"""

import pickle
import operator
from scipy.stats import rankdata

#---------Load the data-----------
input_file = "NIST20_LR_pubchemcandidate.p"

with open(input_file, 'rb') as handle:
    eva = pickle.load(handle)

#---------function for computing similarity score-----------
def tanimoto(candi,predi):
	# print (candi)
	predi = list(map(lambda x: int(x), predi))
	# print (predi)

	bothAB = 0
	onlyA = 0
	onlyB = 0
	for i in range(0,len(candi)):
		if candi[i] == 1 and predi[i] == 1:
			bothAB += 1
		elif candi[i] == 1 and predi[i] == 0:
			onlyB += 1
		elif predi[i] == 1 and candi[i] == 0:
			onlyA += 1
	score = bothAB/(onlyA+onlyB+bothAB)
	return score

def scoring1(candi,predicted):
	count=0
	for i in range(len(candi)):
		if candi[i]==predicted[i]:
			count+=1
	return count/528

#eva:value[1]:inchikey str
#    value[3]:predict_fingerprint is list
#    value[4]:candidate_dict is dict

topk=1
correct=0
key_list=[]
have_entire=0
        

#for key,value in eva.items():
#	if value[1] in value[4]:#use id for evaluation
#		print(key)
#	else:
#		print(str(key)+" no true candiate")        

print("\n")
print("now start to computing the similarity score")
for key,value in eva.items():
	if len(value)<5:#check whether have candidate
		continue    
	if value[1] in value[4]:#use id for evaluation
		have_entire+=1
        #value[-1]:candidate, value[-2]:predict fingerprint
		print("now begin with "+str(key))
        #---similarity score---
		key_list.append([key])
		candi_dit=value[-1]
		for can,fp in candi_dit.items():
			score=tanimoto(fp,value[-2])
			#score=scoring1(fp,value[-2])
			candi_dit[can]=score
        #---rank---
		sorted_candidateList = sorted(candi_dit.items(), key=operator.itemgetter(1))
		sorted_candidateList = [list(i) for i in sorted_candidateList]
		accuracy_list= [-i[1] for i in sorted_candidateList]
		rank_list = [int(i) for i in list(rankdata(accuracy_list))]
        ###
		if 1 not in rank_list:
			min_value=min(rank_list)
			for i in range(len(rank_list)):
				if rank_list[i]==min_value:
					rank_list[i]=1
        ###
		for i in range(len(sorted_candidateList)):
			sorted_candidateList[i][1]=rank_list[i]
		identification_set=[]
		for i in sorted_candidateList:
			if i[1]<=topk:
				identification_set.append(i[0].split("-"))
		#the last step is to tell if the topk contains correct answer
		if key.split("-") in identification_set:
			correct+=1
			print(str(key)+" is correct in top "+str(topk)+" ranking")            
print("\n")
print("the accuracy for top{} is {}%".format(topk,format(correct/have_entire*100, '.2f')))



        