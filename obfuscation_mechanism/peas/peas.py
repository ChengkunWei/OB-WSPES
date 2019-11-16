""" PESA obfuscation machanism
"""
import networkx as nx
from networkx.algorithms.approximation import clique
import pickle
import operator
import random
import os
import sys

import _thread
from multiprocessing import Pool

import pdb


class PEAS(object):

    def __init__(self):
        self.original_user_data_path = "/hdd/OB-WSPES_git/data_warehouse/sampled_user_data_original/"
        self.save_path_prefix = "/hdd/OB-WSPES_git/obfuscation_mechanism/peas/data/result_data_list/"


    def build_coccurrence_matric(self, file_list):
        """ We use a graph to build 
        1. build graph
        2. generate max clique
        """
        G = nx.Graph()
        for filename in file_list: # all query files
            #print(filename)
            with open(os.path.join(self.original_user_data_path, filename),'r' ) as fo: 
                for line in fo:
                    l_data = line.strip().split("\t")
                    query = l_data[1].strip().lower()
                    words = query.split(" ")
                    if len(words) <= 1:
                        continue
                    else:
                        for i in range(len(words)):
                            for j in range(i+1, len(words)): # add edge
                                if G.has_edge(words[i],words[j]): # weight equals to frequency
                                    G[words[i]][words[j]]['weight'] = G[words[i]][words[j]]['weight'] + 1 
                                else:
                                    G.add_edge( words[i],words[j], weight=1)
        temp_sum = 0.0
        for edge in G.edges():
            temp_sum = temp_sum + G[edge[0]][edge[1]]['weight']    
        for edge in G.edges():
            G[edge[0]][edge[1]]['weight'] = G[edge[0]][edge[1]]['weight'] / temp_sum
        #------------------------------
        m_clique = nx.find_cliques(G)
        clique_list = []
        for clq in m_clique:
            if len(clq) >= 8:
                clique_list.extend(clq)
        max_clique_list = list( set( clique_list )  )
        #----------------------------------------------
        #pdb.set_trace()
        return G, max_clique_list
        #return G, clique.max_clique(G)


    def generate_k_query(self,query,max_clique,k,fw,graph,Pu):
        """Generate k fake queries for a real query

        Args: 
            query: real query
            graph: graph of co-ccurence
            max_clique: max cliquer of graph to generate fake queries
            k: the number of fake quries to generate 
            Pu: past user profile
            fw: frequency width

        Return:
            result_fake_query_list = ['xxx','xx']

        """
        result_fake_query_list = []
        words = query.split(" ")
        if len(words) <=1:
            result_fake_query_list = random.choices(max_clique,k=k)
        else:
            # file p_min
            temp_p_min = 1
            for i in range(len(words)):
                for j in range(i+1, len(words)):
                    if graph[words[i]][words[j]]["weight"] <= temp_p_min:
                        temp_p_min = graph[words[i]][words[j]]["weight"]

            f_min = random.uniform(temp_p_min - (fw/2), temp_p_min)
            f_max = f_min + fw
            # find len(words) fake words

            temp_words = []
            for edge in graph.edges():
                if graph[edge[0]][edge[1]]['weight'] <= f_max and  graph[edge[0]][edge[1]]['weight'] >= f_min:
                    temp_words.append(edge[0])
                    temp_words.append(edge[1])

            source_fake_query = list( set(temp_words).intersection(set(max_clique)))
            source_fake_query = list( set(source_fake_query).difference(set(Pu)))
            #pdb.set_trace()
            for i in range(k):
                if len(source_fake_query) <= len(words):
                    temp_fake_query = source_fake_query
                else:
                    temp_fake_query = random.choices(source_fake_query, k=len(words))
                #pdb.set_trace()
                if len(temp_fake_query)==0:
                    continue
                fake_query = temp_fake_query[0]
                for j in range(1, len(temp_fake_query)):
                     fake_query = fake_query + " " + temp_fake_query[j]
                #print(fake_query)
                #temp_fake_query.append(fake_query.strip())
                result_fake_query_list.append(fake_query.strip())
            #pdb.set_trace()
        return result_fake_query_list


    def generate_fake_query_file(self, filename, max_clique, k, graph, fw):
        """Proccess query of one user. 
        Generate k fake queries from max_cliques.

        1. Build past user profile
        2. generate k fake queries for every real query

        Args: 
            filename: filename of the input user's query ( xxxxx.txt )
            graph: the graph of co-ccurence
            max_clique: max clique of graph
            fw: freqency width
        
        Returns:
            [train,test]
            results of the generated fake queries for training and testing
        """
        #----------------------------
        # Build past user profile
        #----------------------------
        Pu = []
        with open( os.path.join( self.original_user_data_path, filename ), "r" ) as fo:
            for line in fo:
                l_data = line.strip().split('\t')
                if l_data[2][6] in ['3']:
                    query = l_data[1].strip().lower()
                    words = query.split(" ")
                    for word in words:
                        if not(word in Pu):
                            Pu.append(word)
        #-----------------------------
        # choose words in max_clique
        #-----------------------------
        train = []
        test = []
        with open( os.path.join(self.original_user_data_path, filename),"r") as fo:
            for line in fo:
                l_data = line.strip().split('\t')
                if l_data[2][6] in ['4']:
                    query = l_data[1].strip().lower()
                    temp_list = []
                    temp_list.append(query)
                    temp_list.append(self.generate_k_query(query,max_clique,k,fw,graph,Pu))
                    #pdb.set_trace()
                    train.append(temp_list)
                #pdb.set_trace()
                if l_data[2][6] in ["5"]:
                    query = l_data[1].strip().lower()
                    temp_list = []
                    temp_list.append(query)
                    temp_list.append(self.generate_k_query(query,max_clique,k,fw,graph,Pu))
                    test.append(temp_list)
            #pdb.set_trace()
        return [train,test]


    def proccess_peas(self,k):
        """ Proccess a group files with peas method
        The main program for peas:

        real query file in self.original_user_data_path
        save the result file in self.save_path_prefix

        1. We set 5 files as a chunk, build graph, find max_clique and generate co-ccurence matric.
        2. proccess every file to generate fake queries of each real query
        3. save the result in the correspoding file path

        Args:
            k: the number of fake queries for each real query
        """

        file_num = 0
        file_list = os.listdir(self.original_user_data_path)
        un_process_file = file_list

        while len(un_process_file) > 0:
            if len(un_process_file) >= 5:
                proccess_fill = random.choices(un_process_file, k=5)
                #pdb.set_trace()
                un_process_file = list( set(un_process_file).difference(set(proccess_fill)))
            else:
                proccess_fill = un_process_file 
                un_process_file = []
            graph, max_clique = self.build_coccurrence_matric(proccess_fill)

            #pdb.set_trace()
            for filename in proccess_fill:
                result = self.generate_fake_query_file( filename, max_clique, k, graph, fw=0.2)
                #pdb.set_trace()
                save_dir = os.path.join( self.save_path_prefix, str(k))
                os.makedirs(save_dir, exist_ok=True)
                with open(os.path.join(save_dir,str(filename[:-4])+'.pkl'),'wb') as save_f1:
                    pickle.dump(result, save_f1)
                print( "#-- %d Have saved: %d/%d  " %(k, file_num, len(file_list)))
                file_num = file_num + 1


if __name__ == "__main__":

#     # input 5 files to compute graph

#     # proccess every file to generate fake queris
    #sys.argv()
    print(len(sys.argv))
    print(sys.argv[1])
    #exit()
    PEAS().proccess_peas(int(sys.argv[1]))