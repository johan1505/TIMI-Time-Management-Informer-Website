# CalendarCalculator

Command to activate the virtual environment
C:\Users\joan1\Documents\GitHub\CalendarApp\CalendarEnvironment\scripts\activate

To Do List:
    - START USING Django rest framwork and chart.js
    - Load the new Summary created on the a new page. Let the user decide whether or not he wants to save it. If yes, then save it in the database
    - Let the user decide from which week to generate the summary
    - Make a mascot for the website
    - When deleting an summary, make a window pop up, do not load a new page

    What do we consider recent summaries? The past 2 or 3 Summaries? what is considered the most most time, find the greatest first!

    Get the summaries from the past 3 weeks.
    what is considered the most most time, find the greatest first?

    For n activities return n/3 activities 
    2 5 8 2 5 10 2 5 24 10 5 -> 24, 10, 10    

    1 solution:  Sort the activites based on timeSpent -> pick the n/3 last activites (Runtime: O(nlogn))
    Problem if we have a very large number of Acitivities, the sorting could become expensive
    2 5 8 2 5 10 2 5 24 10 5 -> 2 2 2 5 5 5 5 8 10 10 24 -> 10 10 24

    2 Solution: Travese the list of activities only once, keeping track of the 3 activities with the largest timeSpent on, using a min heap of size 3.
    (Runtime: O(n))

    INPUT: 2 5 8 2 6 10 2 7 24 15 5
               
    2 5 8 -> 6 5 8  -> 6 10 8 -> 7 10 8 -> 24 10 8 -> 24 10 15 -> 24 10 15

    OUTPUT: 24 10 15


    For n activies, return the n/3 most Frequent events
    What is frequent event?
        An array of summaries can have repeated events of different times each. Use a hashtable
        Traverse all the events
            hash each event's activity ot its time
            if an event is already in the hash table then increase its time
        From the hash table, return the events with the largest times
    Change Summary Model so that it stores an array of events where an event = (activity, time)-- a pair 
