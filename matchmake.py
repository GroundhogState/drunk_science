import os
import sys
import csv
import numpy as np
import re
import matplotlib.pyplot as plt

def match_words(tweepcsv,fieldname,cull_words):
	names = [name for name in tweepcsv]
	print('===')
	print('Matching %s:'%fieldname)
	print('===')
	adj_mat = np.zeros([len(names),len(names)])
	pairs = dict()
	whist = dict()
	for [ii,this_tweep] in enumerate(names):
		pairs[this_tweep] = dict()
		this_info = tweepcsv[this_tweep][fieldname].lower()
		these_words = re.findall('[\w]*[\w]',this_info)
		# print(these_words)
		for this_word in these_words:	
			if this_word in whist:
				whist[this_word] += 1
			else:
				whist[this_word] = 1	
		for [jj,that_tweep] in enumerate(names[ii+1:]):
			
			pairs[this_tweep][that_tweep] = dict()
			pairs[this_tweep][that_tweep]['words'] =[]
			pairs[this_tweep][that_tweep]['counts'] = 0 
			that_fieldname =tweepcsv[that_tweep][fieldname].lower()
			those_words = re.findall('[\w]*[\w]',that_fieldname)
			# search only through unique words
			unique_words = []
			for [idx,temp_word]  in enumerate(these_words):
				other_words = these_words[:idx]+these_words[(idx+1):]
				# print('is ',temp_word,' in ',pairs[this_tweep][that_tweep]['words'])
				duplicate = temp_word in these_words[idx+1:]
				cull = temp_word in cull_words
				if not duplicate and not cull:
					unique_words.append(temp_word)
			for this_word in unique_words:
				if this_word in those_words:
					# print(' %s and %s match: %s'%(this_tweep,that_tweep,this_word))
					adj_mat[ii][ii+jj+1] += 1
					pairs[this_tweep][that_tweep]['words'].append('%s'%this_word)
					pairs[this_tweep][that_tweep]['counts'] += 1
					# print(pairs[this_tweep][that_tweep])
	field_words = []
	field_counts = []
	for [i,key] in enumerate(whist):
		field_words.append(key)
		field_counts.append(whist[key])
	sort_order = np.argsort(field_counts)

	height = 2
	width = 2
	f = plt.figure()
	# plt.subplot(height,width,1)
	plt.imshow(adj_mat+adj_mat.transpose())
	plt.title('Shared keywords: %s'%fieldname)
	plt.savefig('%s_viz.png'%fieldname)
	plt.savefig('%s_viz.svg'%fieldname)

	return [names,adj_mat,pairs,field_words,field_counts,sort_order]

def rank_words_pairs(names,field_A,field_P,field_words,field_counts,field_order,fieldname):
	# Finding the highest-linked pairs
	ranked_field_pairs = []
	A_flat = np.ndarray.flatten(field_A)
	sargs = np.argsort(A_flat)
	num_names = len(names)
	for i in range(num_top_pairs):
		this_count = int(A_flat[sargs[-(i+1)]])
		this_position = sargs[-(i+1)]+1
		row_idx = int(np.floor((this_position-1)/num_names))
		col_idx = np.mod((this_position-1),num_names) 
		shared_words = field_P[names[row_idx]][names[col_idx]]['words']
		ranked_field_pairs.append([this_count,names[row_idx],names[col_idx],shared_words])
	# write the output
	with open(os.path.join(pwd,'%s_pairs.txt'%fieldname),'w') as filename:
		for row in ranked_field_pairs:
			filename.write('%s and %s share %u words: %s\n'%(row[1],row[2],row[0],row[3]))
		filename.close()

	# Sort the individual words and strip bad words
	field_words_ranked = [field_words[i] for i in field_order]
	field_counts_ranked = [field_counts[i] for i in field_order]
	cleaned_words= []
	for i in range(len(field_order)):
		if field_words_ranked[-(i+1)] not in cull_words:
			cleaned_words.append([field_counts_ranked[-(i+1)],field_words_ranked[-(i+1)]])	
	# Write results to file
	with open(os.path.join(pwd,'%s_words.txt'%fieldname),'w') as file:
		# print('The most common field words are:')
		for i in range(min(num_common_words,len(field_order))):
			string = '{0},{1}\n'.format(cleaned_words[i][0],cleaned_words[i][1])
			file.write(string)
		# freader = csv.reader(file,delimiter=',')
		# for [i,index] in enumerate(field_order):
		file.close()
	return [ranked_field_pairs,cleaned_words]

pwd = os.getcwd()
fname = 'drunk_science.csv'

plotting = False
real_life = True

cull_words = ['we','or','s','happy','could','things','work','you','other','would','your','talk', 'my', 'is','and','also','outreach','about','m','with','i','to','while','in','a','this','but','for','the','how','it','what','of','on','do','as','etc','have','that','can','be','used','are','they','from','all','so','at','like','awesome','just']

tweepcsv = dict()
if real_life:
	with open(os.path.join(pwd,fname),'r') as file:
		freader = csv.reader(file,delimiter=',')
		for [i,row] in enumerate(freader):
			if i>0:
				# print(i)
				tweepcsv[row[0]] = dict()
				tweepcsv[row[0]]['field'] = row[1].lower()
				tweepcsv[row[0]]['position'] = row[2].lower()
				tweepcsv[row[0]]['pronoun'] = row[3].lower()
				tweepcsv[row[0]]['topic'] = row[4].lower()
				tweepcsv[row[0]]['avail'] = row[5].lower()
				tweepcsv[row[0]]['handle'] = row[6]
else:
	tweepcsv['alice'] = dict()
	tweepcsv['alice']['topic'] = 'a b c c e ee'
	tweepcsv['alice']['field'] = 'quantum science'
	tweepcsv['bob'] = dict()
	tweepcsv['bob']['topic'] = 'a b c  d dd'
	tweepcsv['bob']['field'] = 'social science'
	tweepcsv['charlie'] = dict()
	tweepcsv['charlie']['topic'] = 'e ee d  f g'
	tweepcsv['charlie']['field'] = 'quantum computing'
	tweepcsv['delta'] = dict()
	tweepcsv['delta']['topic'] = 'q'
	tweepcsv['delta']['field'] = 'social science'




# OK next: whenever you encounter a word, add it 

# print('The topic pairs are')
# for p in topic_P:
# 	print([p,topic_P[p]])

# The most popular shared words are... And shared by X Y Z

num_top_pairs = 10
num_common_words = 25

[names,field_A,field_P,field_words,field_counts,field_order] = match_words(tweepcsv,'field',cull_words)
[ranked_field_pairs,cleaned_words] = rank_words_pairs(names,field_A,field_P,field_words,field_counts,field_order,'field_of_study')
[names,field_A,field_P,field_words,field_counts,field_order] = match_words(tweepcsv,'topic',cull_words)
[ranked_field_pairs,cleaned_words] = rank_words_pairs(names,field_A,field_P,field_words,field_counts,field_order,'topic_of_interest')







if plotting:

	height = 2
	width = 2
	f = plt.figure()
	plt.subplot(height,width,1)
	plt.imshow(field_A+field_A.transpose())
	plt.title('Shared keywords: field of study')

	plt.subplot(height,width,2)
	plt.imshow(topic_A+topic_A.transpose())
	plt.title('Shared keywords: Discussion topic')

	plt.subplot(height,width,3)
	plt.plot(topic_counts)
	plt.title('Word counts: topic')

	plt.subplot(height,width,4)
	# plt.plot([topic_counts[i] for i in topic_order[-20:]])
	plt.title('Word counts: field')

	plt.show()
