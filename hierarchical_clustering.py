# !/usr/bin/python
# coding: utf-8
# Python version: 3.7.3

import sys
import os
import math
import numpy as np
from matplotlib import pyplot as plt
import seaborn
 

def heatmap(cluster_contents, initial_similarity, k):
    sequence_number = initial_similarity.shape[0] # get sequence number: 96
    
    # transfer the cluster contents dict into list
    groups = []
    for value in cluster_contents.values():
        for v in value:
            groups.append(v)

    # reorganize the similarity matrix
    data = initial_similarity.copy()
    for i in range(sequence_number):  
        for j in range(0, i):
            data[i][j] = initial_similarity[groups[i]][groups[j]]
            data[j][i] = data[i][j]

    # plot heatmap using the generated matrix
    plt.cla()
    seaborn.heatmap(data, cmap='jet')
    plt.title("k = {}".format(k))
    plt.savefig("heatmap_k_{}.png".format(k))
    plt.clf()
    plt.cla()
    plt.close() 
    #plt.show()


# ---get input argument---
if len(sys.argv[1:]) != 1:
    raise IOError('''
    please input one parameter, which is the full path + name of the input sequence file.
    For example: python 56049841.py /documents/hw5/SCOV2_96_matrix.txt
    ''')

sequence_filename = sys.argv[1]

if not os.path.exists(sequence_filename):
    raise IOError("input file not exist!")

# ---read sequence file and get similarity matrix---
with open(sequence_filename, 'r') as f:
    file_content = f.readlines() # input file content, a string list
    #print(len(file_content))
    sequence_names = file_content[0].split() #  the name of these sequences
    sequence_number = len(sequence_names) # total number of sequences to be clustered

    # similarity matrix of all sequences
    similarity_matrix = []
    for i in range(1, len(file_content)):
        one_line = list(map(float, file_content[i].split()[1:]))
        similarity_matrix.append(one_line)
    #print(len(similarity_matrix))
    #print(len(similarity_matrix[0]))
    similarity_matrix = np.array(similarity_matrix)
    #print(similarity_matrix[:5, :5])
    
# similarity matrix is symmetric
for i in range(1, sequence_number):
    for j in range(i):
        similarity_matrix[i][j] = similarity_matrix[j][i]

initial_similarity = similarity_matrix.copy() 



# --- bottom-up hierarchical clustering ---
row_index = -1
col_index = -1
cur_cluster_result = [] 
k = sequence_number # initial cluster number, from 96 to 1

# start with the sequences as individual clusters
for n in range(sequence_number):
    cur_cluster_result.append(n)

# at each step, merge the closest pair of clusters until only one cluster (or k clusters) left
while k >= 2:
    max_val = -1*math.inf
    row_index = -1
    col_index = -1

    # 1. find the maximum value from the right triangle of similarity matrix 
    for i in range(0, sequence_number):
        for j in range(i+1, sequence_number):
            cur_val = similarity_matrix[i][j]
            if(cur_val > max_val):
                max_val = cur_val
                row_index = i
                col_index = j
    
    outdated_m = min(row_index, col_index) # the index to be merged
    outdated_d = max(row_index, col_index) # the index to be deleted
    #print("outdated_m: {}, outdated_d: {}".format(outdated_m, outdated_d))

    dict = {}
    for key in cur_cluster_result:
        dict[key] = dict.get(key, 0) + 1
    m_count = dict[outdated_m] # the count of sequences with outdated_m as index
    d_count = dict[outdated_d] # the count of sequences with outdated_d as index

    # 2. update the similarity matrix using “average similarity” between clusters
    average = (similarity_matrix[outdated_m, :] * m_count + similarity_matrix[outdated_d, :] * d_count ) / (m_count + d_count)
    similarity_matrix[outdated_m, :] = average
    similarity_matrix[:, outdated_m] = average

    similarity_matrix[outdated_d, :] = -1*math.inf
    similarity_matrix[:, outdated_d] = -1*math.inf

    # 3. update the merged clusters' label
    label_d = cur_cluster_result[outdated_d]
    label_m = cur_cluster_result[outdated_m]
    for i in range(sequence_number):
        if cur_cluster_result[i] == label_d:
            cur_cluster_result[i] = label_m
    
    k = len(set(cur_cluster_result)) # current clusters number
    #print(" k = {}".format(k))
    
    # output when k = 2 to 5
    if k >= 2 and k <= 5:

        # get the sequence IDs inside each cluster
        cluster_contents = {}
        cluster_sequences = {}
        for i in range(sequence_number):
            cur_label = cur_cluster_result[i]
            if not cur_label in cluster_contents:
                cluster_contents[cur_label] = []
                cluster_sequences[cur_label] = []
            cluster_contents[cur_label].append(i)
            cluster_sequences[cur_label].append(sequence_names[i])


        # show the sequence IDs inside each cluster
        print("-"*96)
        print("\nWhen k = {}, the sequence IDs inside each cluster: \n".format(k))
        print(cluster_contents)
        print("\nthe sequence names inside each cluster:\n")
        print(cluster_sequences)
        print("\n")

        # plot the heatmap
        heatmap(cluster_contents, initial_similarity, k)


        
       