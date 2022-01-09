# Harassment Filter
This repo contains code and data supporting our effort to create a "harassment filter" for Twitter.
Below, you'll find an explanation of what's contained within the repo. 

---
### Data
In accordance with [the restrictions of Twitter's API](https://developer.twitter.com/en/developer-terms/more-on-restricted-use-cases), 
we're unable to share the raw Tweet data that we'd processed for our experiments. Still, though: we can share an unlimited amount 
of Tweet IDs and User IDs, so we've provided those instead. 

We've also provided the node2vec and word2vec embeddings we'd calculated from each account. 

As follows is an explanation of the files contained within the Data folder: 

- **Account Labels.json** - this contains two arrays of Twitter User IDs. The first array contains the User IDs of the 86 "Blocked" accounts, and the
  second contains the User IDs of the 105 "Not-Blocked" accounts.


- **Tweets** - this folder contains the Tweet IDs that we used as textual data for our experiments. Each .json file in this folder
  is named using the User ID of the account that these Tweets are associated with. Within each .json, you'll find three lists - each of these contain 
  Tweet IDs for Tweets the account posted, retweeted, or liked.


- **Network Data** - This folder contains .json's for each of the Blocked / Not-Blocked accounts. Within each .json, you'll find
  two lists - each of these contain the User IDs of accounts that the Blocked / Not-Blocked account follows / is followed by. 
  This data could be used to reconstruct the network discussed in the paper. 

  
- **Embeddings** - This folder contains the following files:

  - ***word2vec embeddings.json*** - 128-dim vectors for each of the Blocked / Not-Blocked accounts. Each of these is a 
  weighted average of the different word2vec embeddings corresponding with the words contained within the Tweets associated with this account. 
  
  - ***node2vec embeddings.json*** - 128-dim vectors for each of the Blocked / Not-Blocked accounts. Each of these is a node2vec
    embedding of the account's position in the large graph we'd created. 


---
### Code
We've also included some of the code that we used when building our model. As follows is a list of the different code that 
was used: 

