Extract the gzipped tar archive, run 'make' to compile and, for example, './infomap 345234 flow.net 10' to run the code.
tar xzvf infomap_dir.tgz
cd infomap_dir
make
./infomap 345234 flow.net 10
Here ./infomap is the name of executable, 345234 is a random seed (can be any positive integer value), flow.net is the network to partition (in Pajek format), and 10 is the number of attempts to partition the network (can be any integer value equal or larger than 1). 

The output file has the extension .tree and corresponds to the best partition (shortest description length) of the attempts. The output format has the pattern
# Code length 3.32773 in 4 modules.
1:1 0.0820133 "Node 5"
1:2 0.0790863 "Node 6"
1:3 0.0459137 "Node 8"
1:4 0.0429867 "Node 7"
2:1 0.0820133 "Node 9"
2:2 0.0790863 "Node 10"
2:3 0.0459137 "Node 12"
2:4 0.0429867 "Node 11"
3:1 0.0820133 "Node 1"
3:2 0.0790863 "Node 2"
3:3 0.0459137 "Node 4"
3:4 0.0429867 "Node 3"
4:1 0.0820133 "Node 13"
4:2 0.0790863 "Node 14"
4:3 0.0459137 "Node 16"
4:4 0.0429867 "Node 15"

For each row, except the first one, which summarizes the result, the first number is the module assignment, the second number is the rank within the module, the decimal number is the steady state population of random walkers, and finally, within quotation marks, is the node name. 

Results are also written to three files in Pajek format. The partition file with extension .clu should be used together with the original network (import both files and use the command Draw->Draw-Partition in Pajek). The file with extension _map.net is a network with all nodes and links aggregated according to the modular map. Finally, the vector file with extension _map.vec gives the size of the modules and should be used together with the file _map.net (import both files and use the command Draw->Draw-Vector in Pajek). 

By uncommenting an obvious line in infomap.cc, the directed code can also handle self-links.

The code can also handle non-uniform teleportation. Just add the weight after the node name in the network file, for example:

*Vertices 16
1 "Node 1" 2
2 "Node 2" 3
3 "Node 3" 4.3
4 "Node 4" 2.1
5 "Node 5" 1.0
6 "Node 6" 2.13
... 
