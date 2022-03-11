1. How many unique categories did you see in your rolled up training data when you set the minimum number of queries per category to 100? To 1000?
With dataset of 100K rows:
* unique categories: 1486
    * MIN_COUNT = 100: 480
    * MIN_COUNT = 1000: 387

2. What values did you achieve for P@1, R@3, and R@5?
I used a model with params: -lr 1.0 -epoch 25 -wordNgrams 2
* 1000 mincut:
    * p@1 0.53470
    * p@3 0.27113
    * p@5 0.19443
* 100 mincut:
    * p@1 0.59129
    * p@3 0.29841
    * p@5 0.18515

3. Give 2 or 3 examples of queries where you saw a dramatic positive change in the results because of filtering.
With query: 'laptop' predicted category: pcmcat247400050000

4. Given 2 or 3 examples of queries where filtering hurt the results, either because the classifier was wrong or for some other reason. 