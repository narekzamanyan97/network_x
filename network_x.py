import collections
import networkx as nx
import matplotlib.pyplot as mat
import pylab as plt
import numpy as np
from statistics import *



def plot_degree_dist_2(degrees_array, title):
	#mat.figure(figsize=(20, 3))  # width:20, height:3
	binwidth = 0.5
	# mat.bar(degrees_array, range(len(degrees_array)), align='edge', width=0.3)
	# # num_bins = bins=np.arange(min(degree_ratios), max(degree_ratios)
	# #            + binwidth, binwidth)
	# if title == 'Copeland Score Histogram':
		
	# 	 #mat.xlim(-500, max(degrees_array))
	# elif title == 'Degree Ratio Histogram':
	# 	mat.xlim(min(degrees_array), max(degrees_array))
	# else:
	# 	mat.xlim()
	print('here1')
	# mat.hist(degrees_array, bins=np.arange(min(degrees_array), max(degrees_array) + binwidth, binwidth))
	
	print('here2')

	mat.title(title)
	
	mat.ylabel('Number of Nodes')

	alpha=0.5

	if title == 'Copeland Score Histogram':
		mat.xlabel('Copeland Score')
		binwidth = 2
		bins=np.arange(-100, 100, binwidth)
	elif title == 'Degree Ratio Histogram':
		mat.xlabel('Degree Ratio')
		binwidth = 0.15
		bins=np.arange(0, 14, binwidth)
	elif title == 'Betweenness Centrality Histogram':
		mat.xlabel('Betweenness Centrality')
		binwidth = 0.000003
		bins=np.arange(0, 0.0001, binwidth)
		alpha=0.5
	elif title == 'Closeness Centrality Histogram':
		mat.xlabel('Closeness Centrality')
		binwidth = 0.015
		bins=np.arange(0, 0.5, binwidth)
		alpha=0.5

	print('here3')
	mat.hist(degrees_array, bins, alpha, histtype='bar', ec='black')

	mat.legend(loc='upper right', fontsize=30)
	mat.xticks(fontsize = 20)
	mat.yticks(fontsize = 20)
	print('here4')
	mat.show()

def plot_degree_dist(degrees_array, title):
	plt.hist(degrees_array)

	plt.show()



def main():
	
	############################################################
	#			Reading the twitter data, converting it into a digraph
	di_graph = nx.read_edgelist("twitter_combined.txt", create_using=nx.DiGraph(), nodetype=int)

	# Getting the number of nodes in di_graph
	num_of_nodes = di_graph.number_of_nodes()
	############################################################



	############################################################
	# 			Defining Arrays later to be used for plotting
	copeland_scores = []
	degree_ratios = []
	c_centralities = []
	c_centralities_dict = {}
	b_centralities = []
	b_centralities_dict = {}
	############################################################


	############################################################
	#			Calculating Copeland Score and Degree Ratio	
	for g in di_graph:
		# print(g + '_in = ' + str(di_graph.in_degree(g)))
		# print(g + '_out = ' + str(di_graph.out_degree(g)))

		in_degree = di_graph.in_degree(g)
		out_degree = di_graph.out_degree(g)

		copeland = out_degree - in_degree
		degree = round((out_degree + 1)/(in_degree + 1), 3)
		
		copeland_scores.append(copeland)
		degree_ratios.append(degree)		
	############################################################


	############################################################
	#			Plotting Copeland Score and Degree Ration Historgrams

	plot_degree_dist_2(copeland_scores, 'Copeland Score Histogram')
	plot_degree_dist_2(degree_ratios, 'Degree Ratio Histogram')
	############################################################


	############################################################
	#			Plotting Betweenness Centrality Histogram

	# Calculating b centralities using a networkx function
	b_centrality_dict = nx.betweenness_centrality(di_graph, k=int(num_of_nodes/16))	

	# Writing Betweenness Centrality Values to a file
	f = open('b_centrality_values.txt', 'w')
	for key, val in b_centrality_dict.items():
		f.write(str(key) + ' ' + str(val))
		f.write('\n')

	# Reading B Centrality values from a file
	with open('b_centrality_values.txt', 'r') as b_file:
		line = b_file.readlines()
		for l in line:
			el = l.split()
			b_centralities.append(float(el[1]))

			b_centralities_dict[el[0]] = el[1]


	for i in range(0, len(b_centralities)):
		print(b_centralities[i])



	plot_degree_dist_2(b_centralities, 'Betweenness Centrality Histogram')
	############################################################
	


	############################################################
	# 			Plotting Closeness Centrality Histogram

	# Calculating c centralities using a networkx function
	c_centrality_dict = nx.closeness_centrality(di_graph)
	
	# Writing Closeness Centrality Values to a file
	f = open('c_centrality_values.txt', 'w')
	for key, val in c_centrality_dict.items():
		f.write(str(key) + ' ' + str(val))
		f.write('\n')
		


	# Reading Closeness Centrality Values from a file
	
	with open('c_centrality_values.txt', 'r') as c_file:
		line = c_file.readlines()
		for l in line:
			el = l.split()
			c_centralities.append(float(el[1]))

			c_centralities_dict[el[0]] = el[1]

	plot_degree_dist_2(c_centralities, 'Closeness Centrality Histogram')
	############################################################


	############################################################
	#			Mean, Median, and SD for Degree Ratio, Copeland Score, 
	#			and C Centrality for highest B Centrality 
	# 1.4
	b_centralities_high = []

	copeland_scores_high_bc = []
	degree_ratios_high_bc = []
	c_centralities_high_bc = []



	for key, val in b_centralities_dict.items():
		if float(val) > 0.00002:
			# print('appending to b_centralities_is_high')
			b_centralities_high.append(key)


	for g in di_graph:
		try:
			if b_centralities_high.index(str(g)):
				# print(g + '_in = ' + str(di_graph.in_degree(g)))
				# print(g + '_out = ' + str(di_graph.out_degree(g)))
				# rint('inside if')
				in_degree = di_graph.in_degree(g)
				out_degree = di_graph.out_degree(g)

				copeland = out_degree - in_degree
				degree = round((out_degree + 1)/(in_degree + 1), 3)
				
				copeland_scores_high_bc.append(copeland)
				degree_ratios_high_bc.append(degree)
				c_centralities_high_bc.append(float(c_centralities_dict[str(g)]))

		except ValueError:
			print('', end='')


	# Mean, Median, and SD of Copeland Score
	mean_copeland = mean(copeland_scores_high_bc)
	median_copeland = median(copeland_scores_high_bc)
	std_dev_copeland = stdev(copeland_scores_high_bc)
	print(mean_copeland)
	print(median_copeland)
	print(std_dev_copeland)
	print(copeland_scores_high_bc)

	print()
	print()
	print()

	# Mean, Median, and SD of Degree Ratio
	mean_degree = mean(degree_ratios_high_bc)
	median_degree = median(degree_ratios_high_bc)
	std_dev_degree = stdev(degree_ratios_high_bc)

	print(mean_degree)
	print(median_degree)
	print(std_dev_degree)
	print(degree_ratios_high_bc)

	print()
	print()
	print()

	# Mean, Median, and SD of Closeness Centrality
	mean_closeness = mean(c_centralities_high_bc)
	median_closeness = median(c_centralities_high_bc)
	std_dev_closeness = stdev(c_centralities_high_bc)

	print(mean_closeness)
	print(median_closeness)
	print(std_dev_closeness)
	print(c_centralities_high_bc)

	# for c in range(0, len(c_centralities_high_bc)):
		# print(c_centralities_high_bc[c])
	############################################################



	############################################################
	# 			Triadic Census
	print(nx.triadic_census(di_graph))

	############################################################



if __name__ == "__main__":
	print('Program is running')
	main()



