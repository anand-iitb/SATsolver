# SAT Solver
**Z3** solver is an python based library to solve **SAT** problems. SAT meaning Satisfiability is solving the boolean variables such that it satisfies all the given condition.
We can use this property in solving logical puzzles and games. For this we have to decode all the rules and regulations in terms of boolean variables.
Now give these rules to **Z3** solver then it will set the variables **True** or **False** accordingly.
Here I have used this property to solve some puzzles and games.

# Sudoku Solver
You can use it by simply running the given code. If you want to try on customized input then modify the code to view the effect.

# K-colourable Graph
I guess you have heard k-colourable term more than infi times (you are not alone :) ).  

For those who have never heard let me explain in simple words.  
You have a connected and undirected graph with some edges.
You have to colour all the vertex using **k** colours such that **there should not exist any pair of vertex/nodes having edge between them and having same colour**.  
**Simply all the adjacent vertex/nodes must have different colours.**  

If You can colour using K-colours then it is K-colourable.
I have decoded this problem in terms of boolean and solved using **Z3 SAT solver**.
So I have tried to visualize the reultant colourfull graph using Networkx library. For trying, you can run the given code and follow the intructions given by output shell.

This is a random graph having 20 Nodes and 50 edges.
![Screenshot from 2022-06-22 18-40-29](https://user-images.githubusercontent.com/73160197/175037692-6d82f286-4a9b-4a60-ae8a-020cc2e2e24c.png)
