#ReadMe Ticket-Bayesian Filter

<h1>Introduction</h1>

<p>For a more detailed Documentation, please read the included Document "Documentation.pdf"

<p>At my company we have our own helpdesk, which helps our colleges whenever they encounter a technical problem they cannot solve themselves. In order to organize the workflow of helping our colleges we use a “Ticket-Management-System” called Cherwell. Whenever a customer (synonym for college in this context) has a problem, thy can either open up a ticket themselves and describe their problem in it and send it to the helpdesk team or thy can call the Hotline (Helpdesk) and they will open up a ticket for them. Either way all of our tickets are received by the First Level of Support, which brings us to the next topic, the helpdesk-structure. The helpdesk has 3 different kinds of levels, the First Level, which deals with “normal” issues and request such as, “I forgot my password”, Software-Installation or help and advice. The Second and Third Level deal with more difficult and time consuming issues, such as: bug fixes, change requests, hardware installation/maintenance and so on. In this case we will focus on the First Level, because this where we aim to make some improvements. 
Currently we raise an evaluation of how many tickets have been solved on which Level each Month and will try to determine if it was a “good” or a “bad” month. The especially observant reader will notice, that this percentage of how many tickets of were solved in the First Level of Support is a very misleading number, because a rise or drop of this percentage can have a lot of reasons that have nothing to do with the quality of our First Level. For Example it could have just been that there were a lot of Bug Fixes to do which the First Level is not even supposed to handle and when the amount of “normal” issues drops at the same time (for instance, because a lot of people are on vacation) the percentage of Tickets solved on First Level is going to drop dramatically and you could think it is because this Team is lazy.
Because of this we are now trying to determine two different percentages:</p>
-	How many tickets <b>were solved</b> on First Level (same on as mentioned above)
-	How many tickets <b>could have been solved</b> on the First Level (here it starts to get tricky)

<p>In order to determine this second percentage we will use a statistical approach: </p>
<p><b>The Bayesian Filter Model.</b></p>
<p>I got the Inspiration from guy on Git called Browning and basically copied his algorithm, so please check him out: </p>
<p>https://github.com/browning/comment-troll-classifier</p>
<p>He uses an Implementation of Paul Graham’s  Spam Filter which is very detailed and even more worth checking out: </p>
<p>http://www.paulgraham.com/spam.html</p>

