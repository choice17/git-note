# metrics

## p-values

* [What is p-value ?](#What)  
* [When do we use p-value ?](#When)  
* [How to calcuate p-value ?](#How)  

## What  

P-value is a metric to state a null hypothesis (or reject a hypothesis for alternative hypothesis) by means of statistics.  
Imagine there is a normal distribution population of a observation, data scientists want to claim a statement (null hypothesis), then p-value would be a good metric to understand the statistic significant of the data to the statement.    

Btw, people call null hypothesis as h0, and alternative hypothesis as h1.  

And when the data is statistical significant to the hypothesis, data-scientists often require p-value have to below a threshold value (alpha), or say 0.05 in most of time.  

## When  

There are three different ways we want to use p-value to make statement. Suppose there is a normal distribution population of a observation. We may want to make statement for below condition.  

I. Right tail test `(h0: u >= u0, h1: u < u0)`  
II. Left tail test `(h0: u <= u0, h1: u > u0)`  
III. Two tails test `(h0: u == u0, h1: u != u0)`  

## How  

Here is an example(right tail test) for illustration.  

Imagine there is a college. And I want to make a statement that students in class C are tallest among the whole school.  
i.e.
```
h0: Students in class C are tallest among the whole school.  
h1: Students in class C are not the tallest among the whole school.  
```
Okay, let us talk about the data we have here.  

| data                | value | population |  
|---------------------|-------|------------|  
| Mean of heights of population | 1.65m | |  
| Mean of heights of students in class C(sample) | 1.70m | 40 |  
| Std of heights of population | 0.1m | |  

Firstly, we would like to find some intermediate z-score  
```
Standard Error(SE) = std_P / sqrt(N) where std_N (Population standard deviation), N (sample size)
                   = 0.1 / sqrt(40)
                   = 0.0158
z-score = (x_mean_N - x_mean_P) / SE where x_mean_N (Sample mean), x_mean_P (Population mean)
        = (1.7 - 1.65) / 0.0158
        = 3.16
```

Then we check the [z-score lookup table](http://www.z-table.com/). so

```
p-value = 0.9992
```

However, what people want to do is to find the area under the right tail in the distribution curve.  
We simply take complement of the p-value to  

```
p-value = 1 - 0.9992 = 0.0008 < 0.05
```

i.e. The data statistic is statistical significant to support the null hypothesis in right tail test.  

## reference  

* [z-test-example](https://www.sophia.org/tutorials/how-to-find-a-p-value-from-a-z-test-statistic-2)  



