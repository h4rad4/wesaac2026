# Wrapping Up Classification: KNN vs. Logistic Regression, and Why Feature Correlation Matters

This lecture closes the classification unit by benchmarking k-nearest-neighbors against logistic regression on the Titanic data, then opens up the fitted logistic model to ask what its weights actually mean — discovering along the way that correlated features, regularization choices, and redundant encodings all shape the answer, and setting up the next topic, "statistical sins."

## The head-to-head: evaluation protocol and results

On Monday a logistic regression model was fit to the Titanic data; the natural question is how it compares to the k-nearest-neighbors (KNN) classifier built earlier. Two evaluation protocols were run for each method:

- **Average of 10 random 80/20 splits** — repeatedly hold out 20% of the data for testing, train on the remaining 80%, and average performance over ten such random partitions.
- **Leave-one-out testing** — a more exhaustive resampling scheme in which each example takes its turn as the test case.

Performance was summarized with four standard metrics, where "positive" means *Survived*:

| Metric | Meaning | KNN, avg. of 10× 80/20 | KNN, leave-one-out | LogReg, avg. of 10× 80/20 | LogReg, leave-one-out |
|---|---|---|---|---|---|
| Accuracy | fraction of all passengers classified correctly | 0.744 | 0.769 | 0.804 | 0.786 |
| Sensitivity | fraction of actual survivors correctly identified | 0.629 | 0.663 | 0.719 | 0.705 |
| Specificity | fraction of actual deaths correctly identified | 0.829 | 0.842 | 0.859 | 0.842 |
| Positive predictive value | fraction of predicted survivors who actually survived | 0.728 | 0.743 | 0.767 | 0.754 |

The conclusion: **the performance is not much different between the two methods** — logistic regression is slightly better, but only slightly, edging out KNN on every metric under both protocols. Since raw predictive power barely distinguishes them, the choice should be made on other grounds. And there the winner is clear: **logistic regression provides insight about the variables**. KNN just hands you a label; logistic regression hands you a model you can actually look inside of.

## Why the scores are close: what each algorithm actually computes

### k-nearest neighbors: voting over nearby examples

The k-nearest neighbors algorithm is a **non-parametric supervised learning method** that assigns weight only to the $k$ nearest neighbors of an entity when making a decision about it. In classification, a new example is assigned the label held by the **plurality vote** of its $k$ nearest training examples; $k$ is a small user-chosen integer ($k=1$ reduces to simply copying the single nearest neighbor's class). Developed by Evelyn Fix and Joseph Hodges in 1951 and later expanded by Thomas Cover, it has a peculiar structure: there is **no explicit training step** — "training" consists only of storing the feature vectors and labels, and all computation is deferred until the moment of classification. Because everything depends on distances, KNN is **sensitive to the local structure of the data**, and if features come in different units or vastly different scales, feature-wise normalization of the training data can greatly improve accuracy; noisy or irrelevant features, or scales inconsistent with their importance, can severely degrade it. Euclidean distance is the common metric for continuous variables, while overlap/Hamming distance serves discrete data, and correlation coefficients have been used in domains like gene expression. The best $k$ depends on the data: **larger $k$ reduces the effect of noise but makes class boundaries less distinct**. Majority voting also has a known weakness under **skewed class distributions** — the more frequent class dominates predictions because it tends to be common among any point's neighbors — which can be countered by weighting each neighbor's vote by $1/d$, the inverse of its distance to the test point.

![Source: Wikipedia, article "[K-nearest neighbors algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)".](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/KnnClassification.svg/500px-KnnClassification.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

The figure above shows the mechanism directly: the same test point becomes a red triangle under $k=3$ but a blue square under $k=5$, purely because the vote within the neighborhood flipped. This is exactly the "hands you a label" character of KNN — the output is a vote count, with no object you can inspect to learn *why*.

### Logistic regression: a linear model of the log-odds

A logistic (or logit) model **models the log-odds of an event as a linear combination of one or more independent variables**:

$$\log\frac{p}{1-p} = \beta_0 + \beta_1 x_1 + \cdots + \beta_m x_m,$$

where $p$ is the probability of the value labeled "1". The unit of the log-odds scale is the **logit** (*log*istic *unit*), and the **logistic function** converts log-odds back to a probability lying strictly between 0 and 1:

$$p = \sigma(\beta_0 + \beta_1 x_1 + \cdots + \beta_m x_m), \qquad \sigma(t) = \frac{1}{1+e^{-t}}.$$

In binary logistic regression the dependent variable is a single binary indicator coded "0"/"1", while each independent variable may itself be binary or continuous. The defining characteristic of the model is that **increasing one independent variable multiplicatively scales the odds of the outcome at a constant rate**: a one-unit increase in $x_j$ multiplies the odds $p/(1-p)$ by $e^{\beta_j}$ — a generalization of the odds ratio. Abstractly, the logistic function is the natural parameterization for the Bernoulli distribution, making it the "simplest" way to convert a real number to a probability. Parameters are estimated by **maximum likelihood (MLE)**, which — unlike linear least squares — has no closed-form expression. Notably, logistic regression itself models a probability and "is not a classifier"; it becomes one by choosing a **cutoff value** and assigning classes according to whether the predicted probability falls above or below it. It has been the most commonly used model for binary regression since about 1970, coined by Joseph Berkson (who invented the term "logit") starting in 1944, and it underpins widely used tools like the Trauma and Injury Severity Score (TRISS) for predicting mortality in injured patients, disease-risk prediction, voter-behavior modeling, and failure prediction in engineering.

![Source: Wikipedia, article "[Logistic regression](https://en.wikipedia.org/wiki/Logistic_regression)".](https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Exam_pass_logistic_curve.svg/960px-Exam_pass_logistic_curve.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

The figure above shows the fitted model doing its job: a smooth estimated probability of passing an exam rising with hours studied, through which a cutoff would turn probabilities into classifications. Unlike KNN's opaque vote, this curve comes with coefficients attached — which is precisely what makes the Titanic model worth opening up.

## Inside the model: the fitted weights

The fitted Titanic model has classes in the order **'Died' and 'Survived'**, and the following weights are for the label *Survived*:

| Feature | Weight |
|---|---|
| Cabin class C1 | $1.66761946545$ |
| Cabin class C2 | $0.460354552452$ |
| Cabin class C3 | $-0.50338282535$ |
| Age | $-0.0314481062387$ |
| Male gender | $-2.39514860929$ |

Because each one-unit increase in a feature multiplies the odds of survival by $e^{\beta}$, these numbers translate directly into odds language: being male multiplies survival odds by $e^{-2.395} \approx 0.091$ (roughly dividing them by eleven); each additional year of age multiplies them by $e^{-0.0314} \approx 0.969$, about a 3% decrease per year; first class multiplies them by $e^{1.668} \approx 5.3$ relative to the reference embedded in the encoding.

It is tempting to look at these and start telling stories — male gender has a big negative weight, so being male was really bad for survival; age has a small negative weight, so older passengers fared a little worse. **Some of that is probably meaningful.** But the warning stands: **be wary of reading too much into the weights.** Features are often correlated, and when they are, the individual weights can be misleading.

## Correlated features and the choice of regularization

Why would correlation distort weights? The answer lies in how the model is fit. Regularization is the general technique of **converting the answer to a problem into a simpler one**, used to solve ill-posed problems and to prevent overfitting. Learning from a finite sample is always underdetermined — infinitely many functions fit the data — and the quantity we actually care about, the expected error

$$I[f_n] = \int_{X\times Y} V(f_n(x), y)\,\rho(x,y)\,dx\,dy,$$

is unmeasurable because we never know the true joint distribution $\rho$. The best available surrogate is the empirical error over the training samples, and **without bounds on model complexity, a model will be learned that incurs zero loss on that surrogate** — memorizing noise instead of pattern. Regularization fixes this by adding a penalty to the objective:

$$\min_f \sum_{i=1}^{n} V(f(x_i), y_i) + \lambda R(f),$$

where $V$ is the underlying loss, $R(f)$ penalizes complexity (via smoothness restrictions or bounds on norms), and $\lambda$ controls the trade-off between fitting the data and staying simple. The theoretical justification is that regularization **imposes Occam's razor** on the solution; in Bayesian terms, the data term corresponds to a likelihood and the regularization term to a prior, whose combination yields a posterior that stabilizes estimation. One of the earliest forms is Tikhonov regularization (ridge regression); related machine-learning techniques include early stopping, dropout, and the L1/L2 penalties below.

![Source: Wikipedia, article "[Regularization (mathematics)](https://en.wikipedia.org/wiki/Regularization_%28mathematics%29)".](https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/Regularization.svg/500px-Regularization.svg.png?utm_source

## Comparing the Original and Modified Feature Sets

To compare the two feature sets fairly, logistic regression was run twice — once on the original features, once on the modified features — and in both cases the reported numbers are averages over **20 random 80/20 train/test splits**, so that no single lucky or unlucky split drives the conclusion.

| Metric | Original features | Modified features |
|---|---|---|
| Accuracy | 0.778 | 0.779 |
| Sensitivity | 0.687 | 0.674 |
| Specificity | 0.842 | 0.853 |
| Positive predictive value | 0.755 | 0.765 |

The result: **essentially no change**. Every difference is on the order of 0.01, so all the work of modifying the features bought almost nothing in raw predictive performance. The payoff of the modification is *interpretability*, not accuracy — which is what the fitted coefficients reveal next. This distinction matters because logistic regression is, at its core, a model of *how inputs relate to the outcome*, not just a black-box scorer: it models the **log-odds** of the event as a linear combination of the independent variables, and its estimated coefficients are exactly the weights of that combination.

## Interpreting the Fitted Coefficients

Since `model.classes_` is `['Died', 'Survived']`, the printed weights are for

## Why pictures get a free pass

A **misleading graph** (also called a *distorted graph*) is a graph that misrepresents its data — a misuse of statistics from which an incorrect conclusion may be derived. Crucially, deception does not require intent: graphs can mislead because they are excessively complex or poorly constructed, or accidentally, through unfamiliarity with graphing software, misinterpretation of the data, or because the data simply cannot be accurately conveyed. Misleading graphs are common enough in false advertising that they are a standard topic in statistics education; one of the first authors to treat them systematically was Darrell Huff, whose 1954 book *How to Lie with Statistics* made the point that a graph is "vastly more effective" than words at deceiving "because it contains no adjectives or adverbs to spoil the illusion of objectivity, there's nothing anyone can pin on you."

Why do visuals slip past our defenses? Data journalist John Burn-Murdoch observes that people are more skeptical of data presented in written text than of equally dubious data presented as a graphic — partly because critical-thinking education focuses on engaging with written works rather than diagrams, leaving visual literacy neglected. He also notes that data scientists are concentrated in technology companies, where the proprietary, closed nature of much of their data hampers outside evaluation of their visualizations. The field of data visualization exists precisely to catalogue ways of presenting information that avoid these traps.

## Truncated axes: manufacturing a gap out of a tenth of a point

The lecture's central demonstration is a bar chart titled "6.0001 Mean Grade By Gender": a blue bar for the male students' mean grade, a pink bar for the female students'. As first presented, the pink bar looks roughly three times the height of the blue — apparently a stunning performance gap. The trick is in the y-axis: it is labeled "Mean Grade" but runs only from $3.90$ to $4.05$. Because the axis is **truncated** — it does not start at zero — the men's bar (about $3.945$) and the women's bar (about $4.05$) are drawn from an elevated baseline, so a real difference of roughly a tenth of a point on a scale that goes up to 5 is blown up into what looks like an enormous gap. The bars lie even though every number printed on the axis is technically correct.

Replotting the identical data with the y-axis running from 0 to 5 tells the truth: two bars of almost identical height, the male mean just under 4 and the female mean just over 4, the difference barely visible. Hence the practical rule the lecture asks you to carry into every encounter with a bar chart: **the first question to ask is where the y-axis starts** — and if it does not start at zero, be suspicious.

![Source: Wikipedia, article "[Misleading graph](https://en.wikipedia.org/wiki/Misleading_graph)".](https://upload.wikimedia.org/wikipedia/commons/9/9a/Misusestatistics_0001_%28cropped%29.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail_unscaled)

## Distorted proportions and incomparable categories

The second example shows that truncation is not the only way bars deceive. A television graphic from Fox News, headlined "Welfare vs. Full Time Jobs" and sourced to the Census Bureau (2011), reports 108.6 million people on welfare versus 101.7 million people with a full-time job. Yet the welfare bar is drawn many, many times taller than the jobs bar, even though

$$\frac{108.6}{101.7} \approx 1.07,$$

i.e., the true difference is only about seven percent. The bars are wildly out of proportion to the numbers they represent.

The lecture then flags a second, subtler defect that survives even if the bars were drawn perfectly to scale: **are the two quantities comparable at all?** What does "people on welfare" count — anyone receiving any kind of government benefit? Is that the same kind of quantity as "people with a full-time job"? The comparison may not be apples and apples. So the checklist grows: check the axis scale, and also ask whether the things being compared are genuinely comparable, because a comparison itself can mislead independently of how it is drawn.

## A wider catalogue of graphical tricks

The same principles extend well beyond bar charts, and the mechanisms are worth knowing by name:

- **Unnecessary or overloaded graphs.** Using a graph where none is needed creates confusion; generally, the more explanation a graph requires, the less the graph itself is needed — and graphs do not always convey information better than tables.
- **Loaded language and phantom trends.** Biased or loaded words in a title, axis labels, or caption can inappropriately prime the reader, and drawing trend lines through uncorrelated data manufactures the appearance of a trend where none exists — sometimes deliberate, sometimes the product of *illusory correlation*.
- **Pie charts and 3D distortion.** Comparing sectors of a pie chart is genuinely hard — in side-by-side examples it is very difficult to judge where the blue sector exceeds the green one, whereas the same percentages plotted as bar charts compare easily. Perspective (3D) pie charts are worse: slices closer to the viewer appear larger due to the viewing angle, and readers demonstrably perform worse at judging relative magnitudes in 3D than in 2D. In the canonical example, Item C appears at least as large as Item A but is actually less than half its size, while Items B and D are the same size despite looking different. Edward Tufte drew the sharp conclusion in *The Visual Display of Quantitative Information*: "Tables are preferable to graphics for many small data sets. A table is nearly always better than a dumb pie chart; the only thing worse than a pie chart is several of them…" — citing their low data-density and failure to order numbers along a visual dimension. More generally, superfluous dimensions not used to display the data of interest are discouraged for all charts.

![Source: Wikipedia, article "[Misleading graph](https://en.wikipedia.org/wiki/Misleading_graph)".](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Piecharts.svg/1280px-Piecharts.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

- **Pictogram scaling.** In bar graphs built from pictures, scaling the images uniformly is perceptually misleading because the eye reads the *area* of the pictogram, not just its height or width — so a linear scaling makes the difference appear **squared**: if one icon is drawn 3 times taller to represent a 3-fold value, its area is $3^2 = 9$ times as large, which is exactly the case in the classic example where image B is actually nine times the size of image A. Adding a third dimension cubes the effect. An improperly scaled pictogram of house sales made 2001 sales look eightfold higher than the prior year when they had merely doubled (and never stated the number of sales); such scaling can even suggest the item itself has changed in size — in one example, bananas seem more plentiful simply because their icons occupy the most area and sit furthest right.

![Source: Wikipedia, article "[Misleading graph](https://en.wikipedia.org/wiki/Misleading_graph)".](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/Graph_showing_improper_3D_pictogram_scaling.svg/330px-Graph_showing_improper_3D_pictogram_scaling.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

- **Log scales.** Logarithmic scales are a *valid* representation — they express data values as a chosen base (often 10) raised to a power, so a value of 10 gets height 1 and a value of 1,000,000 ($10^6$) gets height 6 — and they are standard for the volcanic explosivity index, the Richter scale, stellar magnitudes, and pH. They mislead when used without clear labeling or shown to readers unfamiliar with them, and even in legitimate uses the compression can make the data less apparent to the eye.

## Garbage in, garbage out

Everything so far involved lying with *good* data. The lecture next asks what happens when the data itself is bad, invoking the computer science maxim **garbage in, garbage out**, and Charles Babbage — designer of the first mechanical computers in the 1800s — as its historical voice. Asked by members of Parliament, "Pray, Mr. Babbage, if you put into the machine wrong figures, will the right answers come out?", Babbage replied that he was "not able rightly to apprehend the kind of confusion of ideas that could provoke such a question." The point endures because people commit exactly this error constantly: they feed bad data into a sophisticated analysis and then trust the output *because the analysis was fancy*. The sophistication of the analysis cannot rescue bad data.

## Do errors cancel? Random versus systematic error

The historical cautionary tale is John C. Calhoun's response to charges that the census data he relied on was riddled with errors. Calhoun — the American statesman and seventh vice president (1825–1832) who became slavery's most outspoken defender, asserting it a "positive good" rather than a necessary evil — answered that "there were so many errors they balanced one another, and led to the same conclusion as if they were all correct."

Is that ever legitimate? Yes, under one specific condition: if the measurement errors are **unbiased and independent** of each other, they will be distributed almost identically on either side of the mean, and positive and negative errors really can cancel. Was that the case here? No. Later analysis showed the errors were **systematic**, not random — pointing in one direction rather than scattering symmetrically, so nothing canceled. The stakes were enormous: this census data underwrote conclusions linking Black people and insanity, conclusions deployed to defend slavery. As James Freeman Clarke put it, "it was the census that was insane and not the colored people." Wrong data, with errors aligned rather than balanced, propped up a monstrous conclusion.

The sequence yields the lecture's closing discipline: analysis of bad data can produce dangerous conclusions, so check your axes, check your comparisons, and above all ask where the data came from — because no amount of careful computation will save an analysis that started with garbage.

## Sampling: Estimating a Whole Population from a Subset

In statistics, quality assurance, and survey methodology, **sampling** is the selection of a subset of individuals from within a statistical population in order to estimate characteristics of the whole population. The subset — the *sample* — is meant to reflect the whole population, and statisticians try to collect samples that are **representative** of it. The reason sampling exists at all is practical: it has far lower costs and faster data collection than a census recording every member of the population, and in many cases measuring the entire population is simply impossible — nobody can measure the sizes of all stars in the universe. Sampling therefore provides insight precisely in cases where a full measurement is infeasible. Each observation measures one or more properties (weight, location, color, mass) of independent objects or individuals, and in survey sampling, weights can be applied to the data to adjust for the sample design, particularly in stratified sampling. Results from probability theory and statistical theory guide the practice, which is why sampling is ubiquitous in business and medical research; a specialized form, acceptance sampling, is used to decide whether a production lot meets governing specifications.

The idea is old: random sampling by lot appears several times in the Bible. In 1786, Pierre Simon Laplace estimated the population of France from a sample using a ratio estimator, and he even computed probabilistic estimates of the error — not modern confidence intervals, but the sample size needed to achieve a particular upper bound on sampling error with probability $1000/1001$. His estimates used Bayes' theorem with a uniform prior and, crucially, *assumed his sample was random*. Alexander Ivanovich Chuprov brought sample surveys to Imperial Russia in the 1870s. Modern applications persist: Singapore's elections have used public "sample counts" since 2015, which yield an indicative result with roughly a 4% margin of error at a 95% confidence interval — though officials stress these are separate from official results.

Successful statistical practice starts with a precise definition of the **population**: all people or items with the characteristics one wishes to understand. Sometimes this is obvious — a manufacturer deciding whether a production batch is good enough to release treats the batch as the population. Often it is subtler. A staffing study might sample checkout-line lengths across times of day; a penguin study samples habitat use over time. Joseph Jagger famously studied roulette wheels at a Monte Carlo casino to identify a biased wheel: his "population" was the wheel's overall behavior — the probability distribution of its results over infinitely many trials — while his "sample" was the observed spins. Similar issues arise with repeated physical measurements like the conductivity of copper. In experiments, the sampled population may differ entirely from the population of interest: one tests a quit-smoking program on 100 patients to predict its effect on a **superpopulation** — "everybody in the country, given access to this treatment" — a group that does not yet exist; one studies rats to understand human health, or birth records from 2008 to predict outcomes for those born in 2009. Time spent pinning down exactly what was sampled and what you actually want to know about is time well spent.

## Random Sampling: The Assumption Beneath Every Statistical Technique

All statistical techniques rest on one assumption: by sampling a subset of a population, we can infer things about the population as a whole. The crucial qualifier is **random**. If the sample is drawn randomly, then meaningful mathematical statements can be made about the expected relation of the sample to the entire population — this is what licenses the machinery built up over prior lectures: the distribution of sample means, the central limit theorem, the empirical rule. Randomness is what connects the arithmetic of a small subset to claims about the whole.

There is an asymmetry worth noting between simulation and the real world. In code, obtaining a random sample is trivial: call a random-choice function and every element is equally likely to be picked. In the field, it is not so easy, because some examples are simply more convenient to acquire than others — and that convenience is exactly where sampling goes wrong.

![Source: Wikipedia, article "[Sampling (statistics)](https://en.wikipedia.org/wiki/Sampling_%28statistics%29)".](https://upload.wikimedia.org/wikipedia/commons/b/bf/Simple_random_sampling.PNG?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail_unscaled)

## Convenience Sampling: Speed Bought at the Cost of Representativeness

What people typically do in practice is **convenience sampling** — also called grab, accidental, or opportunity sampling — a type of *non-probability* sampling in which the sample is drawn from whatever part of the population is close at hand. Official statistical agencies generally do not recommend it for research because of the possibility of sampling error and its lack of representativeness. Its defining trade-off is speed versus accuracy: collected samples may not accurately represent the population of interest and can be a source of bias, though larger sample sizes reduce the likelihood of sampling error occurring.

Its popularity comes from genuine advantages. It is extremely fast, easy to use, readily available, and cost-effective — requiring almost no preparation, so researchers facing time pressure can gather data and begin calculations immediately. A questionnaire distributed to a targeted group can yield data in hours, freeing the researcher to focus on analysis rather than carefully selecting participants. Because the sample group is on hand, there is no need to travel, quotas can be met quickly, and multiple studies can run expeditiously. It is especially useful for pilot data collection — getting a quick read on trends or developing hypotheses for future research — and it is often used to secure funding for a larger project, where a quick selection of the population demonstrates the need for the comprehensive study.

But the disadvantages can outweigh all of this. Results from convenience sampling **cannot be generalized to the target population**, because the technique under-represents subgroups relative to the population of interest. Worse, the resulting bias *cannot be measured*: since the probability that any individual in the population will be sampled is unknown — true of non-probability methods generally — no reliable estimate of the sampling error can be computed. Consequently, inferences based on convenience sampling should be made only about the sample itself, and the method lacks the power to identify differences between population subgroups.

## Survivor Bias: Sampling Only Those Who Made It

One classic way non-random sampling corrupts data is **survivor bias** — drawing your sample only from entities that survived some selection process. Consider course evaluations administered at the end of a course: the only people left to fill them out are those who did not drop the course, so the sample is biased toward whatever kept them there. Or consider grading a final exam on a strict curve: the only grades visible are from students who made it to the final. In both cases, the population you are inferring about is not the population you sampled from — the dropouts and the early leavers are invisible, yet they are part of the population your conclusions implicitly describe.

## Non-Response Bias: When Respondents Are Not Typical

**Participation bias**, or **non-response bias**, is the phenomenon in which the results of studies or polls become non-representative because participants disproportionately possess certain traits that affect the outcome. The sample ends up systematically different from the target population, potentially producing biased estimates. For instance, one study found that people who refused to answer a survey on AIDS tended to be older, attend church more often, be less likely to believe in the confidentiality of surveys, and have lower sexual self-disclosure. The phenomenon can arise through many factors (catalogued by Deming in 1990) and is a particular problem in longitudinal research, where attrition accumulates over the course of the study.

A thought experiment shows how the distortion works. Suppose you poll 1000 managers in a field about their workload. Managers with a high workload may not answer because they lack the time; managers with a low workload may decline for fear that supervisors or colleagues will perceive them as surplus employees — immediately if the survey is not anonymous, or later if anonymity is compromised. The measured workload could therefore come out too low, too high, or — if the two biases happen to offset — *right for the wrong reasons*. The effect can even be self-referential: consider a survey item reading "Agree or disagree: I have enough time in my day to complete a survey."

The most famous historical failure is the 1936 U.S. presidential election. *The Literary Digest* mailed out 10 million questionnaires and received 2.38 million back — an enormous sample. Based on the returns it predicted Republican Alf Landon would win with 57.08% of the popular vote and 370 of 531 electoral votes. In reality Landon received only 37.54% of the popular vote and eight electoral votes, losing in an unprecedented landslide to Franklin D. Roosevelt. Subsequent research published in 1976 and 1988 concluded that **non-response bias was the primary source of the error** — the people who bothered to return the questionnaire were not typical voters — although the sampling frame compounded the problem: respondent names came from magazine subscription lists and telephone directories, which were themselves heavily skewed toward Republicans. A very large sample, deeply flawed, still failed catastrophically.

Non-responders tend to share characteristics — they are disproportionately younger patients, poorer communities, and the less satisfied — so their absence skews whatever is measured. Fortunately, there are ways to test for the bias. A common technique compares the first and fourth quartiles of responses for differences in demographics and key constructs. In e-mail surveys, some values are already known for *all* potential participants (age, branch of the firm, etc.) and can be compared against the values prevailing among those who answered; no significant difference is an indicator that non-response bias may be absent. Alternatively, non-responders can systematically be phoned and asked a small number of survey questions — if their answers do not differ significantly from responders', there may be no bias. This is called **non-response follow-up**.

A widespread assumption holds that low response rates signal greater risk of non-response bias, and some journals act on it — JAMA requires a 60% response rate to publish survey research, a heuristic comparable to the 0.05 p-value convention. But academic research disputes the linkage: Robert M. Groves' meta-analysis of 30 methodological studies found the coefficient of determination for variance in non-response bias explained by response rate was only $R^2 = 0.11$ — a weak predictor. Another meta-analysis of 44 studies found that methods raising response rates, such as prior notification and incentives, do not necessarily reduce non-response bias and can sometimes even increase it. Chasing higher response rates can thus be counterproductive: the money spent boosting response might be better applied elsewhere, and rigid thresholds can gatekeep surveys that are valid on their merits but fail an arbitrary heuristic.

## The Moral: Know How the Data Was Collected

Here lies the subtle danger. When samples are not random and independent, you can still compute means and standard deviations — the arithmetic always works, and the computer will happily hand you a perfectly respectable-looking number. But you should **not draw conclusions** from those statistics using tools like the empirical rule and the central limit theorem, because those results were derived under the assumptions of randomness and independence. Garbage assumptions in, garbage conclusions out — with nothing in the summary statistics to warn you.

Hence the lecture's closing injunction: **understand how data was collected, and check whether the assumptions used in the analysis are satisfied — if not, be wary.** Before trusting any statistical claim, ask where the data came from. If the sampling was not random and independent, treat the conclusions with great suspicion.
