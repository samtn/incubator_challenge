# Restaurant's Hygiene versus its Online Reviews

CDC estimates 48 million people get sick, 128,000 are hospitalized, and 3,000 die from foodborne diseases each year in the United States. Restaurants and cafes are reported to be one of the major sources of foodborne, but how can one reduce this risk by staying away from risky restaurants? Do online reviews provided by customers tell us anything about the hygiene level of a restaurant's kitchen?

To answer these questions, I have looked at the public data provided by [DOHMH](https://catalog.data.gov/dataset/dohmh-new-york-city-restaurant-inspection-results) regarding the New York City restaurant inspection results (~25,000 restaurants and cafes). The dataset has over 400k inspection results for all the restaurants and cafes in NYC (18 inspections per case on average over 3 years). There are two types of violations, Critical and Not-Critical, and many violation codes per type. For example there are 50 violation codes for Critical violations and each has their own scores. Inspection result is reported as an score defined by summing over all violations observed during that inspection. Final score of 0-13 gives restaurant grade “A”, scores 14-27 results in grade “B” and anything above that will result in grade “C”.  Also, I was able to get Yelp's reviews for 75% of the entries by searching their phone numbers in Yelp API.

Shockingly 93% of all restaurants in NYC had at least one Critical violation! You might ask what is a “Critical” violation? Well it can be anything from storing food in unappropriated temperature and unsantizied surfaces to evidence of mice and roaches. A word-cloud representation of the common words in these reports are shown in the below picture, the larger the size of a word the more frequent it is.

![most common words in critical violations] (https://github.com/samtn/incubator_challenge/blob/master/wordcloud.png)


And a more detailed descriptions of these violations and their frequencies are in the below table:

```
+----------------+-------+-------------------------------+-------------------+
| VIOLATION CODE | Count |             descs             |        Freq       |
+----------------+-------+-------------------------------+-------------------+
|      02G       | 33517 | {'Cold food item held abov... |   0.139293744104  |
|      04L       | 30246 | {"Evidence of mice or live... |   0.125699751892  |
|      06D       | 27336 | {'Food contact surface not... |   0.11360604436   |
|      06C       | 25952 | {'Food not protected from ... |   0.107854260434  |
|      02B       | 21057 | {'Hot food item not held a... |   0.087511065119  |
|      04N       | 20560 | {'Filth flies or food/refu... |  0.0854455762382  |
|      04H       | 10653 | {'Raw, cooked or prepared ... |   0.044272943758  |
|      04M       | 10428 | {"Live roaches present in ... |  0.0433378632788  |
|      06E       |  9797 | {'Sanitized equipment or u... |  0.0407154820236  |
|      06F       |  8400 | {'Wiping cloths soiled or ... |  0.0349096712257  |
|      06A       |  8169 | {'Personal cleanliness ina... |   0.033949655267  |
|      04A       |  7915 | {'Food Protection Certific... |  0.0328940533037  |
```
Now how can we avoid such restaurants? Can we trust online reviews in these cases? unfortunately my analysis does not show any correlation between how people rate a restaurant and how hygienic its kitchen is as shown in the below figure! The green region represents grade "A", yellow and red are grades "B" and "C" respectively.

![Yelp review vs inspection results] (https://github.com/samtn/incubator_challenge/blob/master/yelp_review_vs_inspection_score.png)
We all know that restaurant owners pay a lot of attention to their online reviews because they know that it directly affects their customers. Also customers use those reviews because they are easily accessible. However it's hard to get your hands on the inspection results online since there is no central repository for them. Perhaps it is time to pay more attention to what's going on behind the scene, where our food is getting prepared. 
