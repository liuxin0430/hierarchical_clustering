Python version: 3.7.3

This is a simple example for applying bottom-up hierarchical clustering algorithm to cluster SARSCoV-2 genomes. The clustering algorithm will stop when having just one cluster.


The similarity between all pairs of sequences is provided as a matrix(SCOV2_96_matrix.txt). The first line is the name of these sequences. Then all the other lines contain the pairwise similarity following the order of the first line. 


usage: 
python hierarchical_clustering.py SCOV2_96_matrix.txt

output: 
The program will print out the sequence IDs inside each cluster on the terminal and plot
corresponding heatmap figures for each k=2 to 5.


