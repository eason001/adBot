adBot v 2.3.0

Input: a list of urls 
    Each url should follow the format xxx.domain.xxx in order to be parsed correctly by the ibot.py script. The input file name should be urls.txt.

Output: screenshots and html source code
    ibot stores each url's screenshot and source code base on its domain name in "domain.png" and "domain.txt" format respectively. They are stored under the output path specified in the argument. Images are located under <output_path>/data/img and texts are under <output_path>/data/src. If domain name is repeated, then it adds a numeric value in the end as domainX.png and domainX.txt (where X is the auto increment numeric value).

How to run:
            python ibot.py <output_path> <number of jobs (optional)>
    ibot.py grabs a list of urls and save screenshots and source codes in the local disk, under /img and /src respectively. The default timeout for loading a page is 30 sec. 
    The maximum number of jobs is equal to the total number of available CPU cores. If no argument is specified, then ibot.py runs in single processor mode by default.
