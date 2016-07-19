# Summer_Research_2016

Title: Analysis of Greedy Algorithm Framework for Choosing Network-Probing Paths
Colgate University (Summer Research 2016)

Poster Link: https://drive.google.com/a/colgate.edu/file/d/0BxUOgM_nH9qCZjkxS3UyRTVHR3c/view?usp=sharing

Future Work:

- Master score equation with different coefficients to reflect the importance of each metric 
  that we care about
- Investigate the properties of good paths randomly picked by the algorithm to improve the score
  function
- Devise a more general search function for optimal set of coefficients, which minimizes 
  the overhead on multiple metrics, and continue studying the tradeoff among various metrics

Finished:
- Score function for edge coverage 
- Greedy Algorithm that maximizes the scores
- Tie Breaker for multiple paths with max score
- Support for reading multiple graph configurations from a text file
- Catalogue our findings (mapping results to their corresponding graphs) 
- Score functions that consider loads on nodes and edges
