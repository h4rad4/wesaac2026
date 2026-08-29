

## Stratified Sampling: Partition First, Then Draw

Stratified sampling completes our tour of sampling techniques. Instead of drawing one simple random sample from the whole population, you first divide the population into subgroups — **strata** — and then sample from each stratum separately (typically by simple random sampling within each). For the division to be valid, the strata must form a true *partition* of the population: **collectively exhaustive and mutually exclusive**, meaning every element belongs to one and only one stratum.

There are two main situations where this pays off:

1. **Guaranteeing representation of small subgroups.** Under simple random sampling, a small subgroup might, purely by chance, contribute very few members — or none at all. Stratification guarantees they show up. The classic application is a political survey that deliberately includes participants from various minority groups (race, religion) in proportion to their share of the population; such a survey can legitimately claim to be *more representative* than a simple random or systematic sample of the same size.

2. **Mirroring the population's composition.** Consider estimating average votes per candidate in a country of three towns: Town A has 1 million factory workers, Town B has 2 million office workers, Town C has 3 million retirees. A single random sample of 60 drawn from the whole population risks being poorly balanced across towns — and therefore biased whenever the outcome of interest is distributed differently between them. Drawing 10, 20, and 30 from Towns A, B, and C respectively produces a *smaller estimation error for the same total sample size*.

There is also a statistical bonus: **stratification can reduce the sample size needed for a given precision**. The reason is that strata are constructed to be internally homogeneous, so the variability *within* subgroups is typically less than the variability of the entire population. Formally, stratification aims to reduce sampling error and can yield a weighted mean with less variability than the arithmetic mean of a simple random sample; in computational statistics it is used as a variance-reduction technique for Monte Carlo estimation.

The standard allocation rule is **proportional allocation**: the sample taken from stratum $h$ is sized in proportion to the stratum's share of the population,
$$n_h = n \cdot w_h, \qquad w_h = \frac{N_h}{N},$$
i.e., multiply each group's size by the desired sample size and divide by the total population size. (A company wanting a stratified sample of 40 staff would first compute each category's percentage of the total, then allocate the 40 slots accordingly.) The exact mean and variance formulas for stratified sampling carry a **finite population correction**, the factor $(N_h - n_h)/(N_h - 1) = 1 - \frac{n_h-1}{N_h-1}$ computed per stratum; dropping this correction yields the simpler large-population versions.

But stratified sampling demands care — you have to get the strata right:

- **Don't scale subgroup sample sizes to the amount of data available** from each subgroup; scale them to subgroup sizes (or to their variances, if known to differ significantly, e.g., via an $F$ test). If subgroup variances differ substantially, you cannot simultaneously make sample sizes proportional to both size and variance — "optimum allocation" handles groups differing in means, variances, and costs.
- Where population density varies greatly across a region, unequal sampling fractions restore *equal accuracy*: an Ontario-wide survey might oversample the sparsely populated north, since a province-wide fraction would otherwise yield only a handful of northern observations, making sub-region comparisons statistically underpowered.
- If the class priors (the true subpopulation ratios) are unknown, performance of downstream analyses such as classification can suffer; minimax sampling ratios make the dataset robust to that uncertainty.
- Merging sub-strata just to get adequate counts can trigger **Simpson's paradox**: trends that exist within groups can vanish or even reverse once the groups are combined.

Because getting the strata right requires real care, this course will stick to simple random samples — keeping the mathematics clean so we can focus on the concepts.

## Simple Random Sampling: The Course's Baseline

A **simple random sample (SRS)** is a subset chosen so that every individual has the same probability of selection — and, more strongly, *every subset of $k$ individuals has the same probability of being chosen as any other subset of size $k$*. The canonical picture is a fair lottery: ten students compete for six basketball tickets, each is assigned a number from 1 to 10, random numbers are generated (ignoring out-of-range values and repeats), and the first six distinct numbers identify the winners.

Key structural facts:

- **Sampling is done without replacement**: once an element is chosen, it does not go back into the pool, so it cannot be chosen again. (With-replacement variants exist but are uncommon.) Without replacement the draws are no longer independent — but the sample remains **exchangeable**, so most results of mathematical statistics still hold. Moreover, for a small sample from a large population, sampling without replacement is approximately the same as with replacement, since the probability of drawing the same individual twice is tiny.
- Survey methodology treats SRS without replacement as the **benchmark against which the relative efficiency of other designs is measured** — precisely why it is the right default for a course establishing baseline concepts.
- **Unbiasedness is about averages, not guarantees.** An unbiased selection procedure ensures that if many samples were drawn, the average sample would accurately represent the population; it does *not* guarantee that any particular sample perfectly mirrors the population. SRS lets us draw externally valid conclusions about the whole population from a sample.
- **It requires a complete sampling frame** — a full list of population units — which may be unavailable or infeasible for large populations. Its advantages are that it is free of classification error, requires minimal prior knowledge beyond the frame, and produces easily interpreted data. It best suits settings where little is known about the population or where sampling cost is low enough that simplicity outweighs efficiency; otherwise stratified or cluster sampling may serve better.

One subtlety worth separating: **equal probability of inclusion (epsem)** is weaker than SRS. Every SRS is epsem, but not conversely. A teacher who picks one of six columns at random from a classroom arranged in 5 rows × 6 columns gives each student the same inclusion probability, yet only column-shaped subsets of 5 students are eligible — so not all subsets are equally likely. **Systematic random sampling** behaves similarly: number students 0001–1000, pick a random start (say 0533), take every 10th name thereafter; each unit has equal marginal probability, but different *sets* of units have different probabilities, and the choice of the first unit determines the rest. Such epsem samples are **self-weighting** — the inverse of the selection probability is the same for every sampled unit. In the school example (100 of 1000 students), each student has roughly a 1-in-10 chance of selection whether or not names are returned to the bucket after drawing.

## The Data: Daily Temperatures from 21 U.S. Cities

To move from abstractions to real data, we use daily high and low temperatures from the **U.S. National Centers for Environmental Information (NCEI)** for 21 U.S. cities: Albuquerque, Baltimore, Boston, Charlotte, Chicago, Dallas, Detroit, Las Vegas, Los Angeles, Miami, New Orleans, New York, Philadelphia, Phoenix, Portland, San Diego, San Francisco, San Juan, Seattle, St. Louis, and Tampa. The records span **1961 through 2015**, giving **421,848 data points** — "examples" in our terminology. This entire collection plays the role of the *population* we will sample from.

Two new programming tools enter here:

- `numpy.std` computes the **standard deviation** of a collection of numbers — converting the spread measure we've discussed conceptually into something we can calculate directly.
- `random.sample(population, sampleSize)` returns a list of `sampleSize` **randomly chosen *distinct* elements** of the population. The word "distinct" is the crucial one: this is sampling **without replacement**. Once an element is selected it cannot be selected again — exactly the SRS convention described above, and it matters for interpreting everything that follows.

## The Population Distribution of Daily High Temperatures

Histogramming **all 421,848 daily high temperatures** across all 21 cities and all years gives the population picture:

- **Mean:** $\mu = 16.3$ °C.
- **Standard deviation:** $\sigma \approx 9.4$ °C.
- **Shape:** roughly bell-shaped, centered in the high teens to mid-twenties. Counts rise steadily from the cold end near $-30$ °C, peak around 20–25 °C at close to 60,000 days per bin, and fall off again toward 40 °C.

This is the ground truth against which samples will be judged.

## A Single Random Sample of Size 100

In practice we almost never see the whole population — that is the entire motivation for sampling. So we draw one random sample of $n = 100$ and histogram it:

- **Sample mean:** 17.07 °C — close to the population's 16.3, but *not equal*.
- **Sample standard deviation:** $\approx 10.4$ — noticeably larger than the population's $\approx 9.4$.
- **Shape:** recognizably similar to the population histogram — the bulk of the mass sits in the warmer temperatures with a tail extending toward the cold end — but far **noisier**. With only 100 points, the bars jump around, showing gaps and little clusters that reflect no real structure in the population, merely the luck of the draw.

Both the near-miss of the mean and the overshoot of the standard deviation are instances of the same phenomenon: a particular sample is never a perfect representation of its population, even under unbiased selection. The similarity in shape despite the noise is encouraging — the sample carries genuine information about the population — but the deviations demand explanation.

## The Guiding Question: How Well Do Samples Approximate Populations?

Everything above converges on the question that drives the rest of this lecture: **how well do statistics computed from a sample — like the mean of 17.07 we just observed — approximate the true population values?** We saw one sample of size 100 land near the truth; a different sample of the same size would land somewhere else. Quantifying that variability — understanding the relationship between sample statistics and population parameters — is exactly what we pursue next.



## From the Central Limit Theorem to the Spread of Sample Means

Everything in this part of the lecture builds on the Central Limit Theorem (CLT), which the professor recaps as making three promises about a sufficiently large sample drawn from a population with mean $\mu$ and variance $\sigma^2$:

1. **Shape:** the sample means are approximately normally distributed;
2. **Center:** that normal distribution has a mean close to the population mean $\mu$;
3. **Spread:** the variance of the sample means is close to the population variance divided by the sample size, $\sigma^2/n$.

Features 1 and 2 were already exploited earlier in the course — checking that simulated sample means looked Gaussian and centered near $\mu$. Feature 3 is new territory, and it is the quantitative heart of the theorem. The Wikipedia treatment makes precise what "approximately normal with variance $\sigma^2/n$" means: for i.i.d. random variables $X_1, X_2, \ldots$ with mean $\mu$ and finite variance $\sigma^2$, the *normalized* fluctuation of the sample mean,

$$\sqrt{n}\left(\bar{X}_n - \mu\right)\ \overset{d}{\longrightarrow}\ \mathcal{N}(0, \sigma^2),$$

converges in distribution to a normal with mean $0$ and variance $\sigma^2$. Equivalently, for large enough $n$, the distribution of $\bar{X}_n$ itself gets arbitrarily close to a normal with mean $\mu$ and variance $\sigma^2/n$. Crucially, this holds **regardless of the shape of the distribution of the individual $X_i$** — which is why probabilistic methods built for normal distributions apply to problems involving almost any underlying distribution. The law of large numbers explains that $\bar{X}_n$ converges to $\mu$; the CLT describes the *size and shape* of the stochastic fluctuations around that limit during convergence. Historically, versions of the theorem date back to 1811 (the earliest being the de Moivre–Laplace theorem, approximating the binomial by the normal), but the modern precise statement only crystallized in the 1920s.

Feature 3 is what licenses the next step: if we know how much sample means vary, we can quantify the uncertainty in any single estimated mean.

## The Standard Error of the Mean

The **standard error (SE)** of a statistic is defined as the standard deviation of its *sampling distribution* — the distribution formed by repeatedly sampling from the same population and recording the statistic (here, the mean) per sample. For the sample mean specifically, the third CLT feature translates directly into a formula. Since the variance of the sampling distribution of the mean equals the population variance divided by the sample size, taking square roots gives the **standard error of the mean (SEM)**:

$$\sigma_{\bar{x}} = \frac{\sigma}{\sqrt{n}},$$

where $\sigma$ is the population standard deviation and $n$ the sample size. The professor implements this in two lines of Python:

```python
def sem(popSD, sampleSize):
    return popSD/sampleSize**0.5
```

**Why does this formula hold?** The Wikipedia derivation shows it is not merely an empirical observation but follows from basic variance algebra. Let $T = x_1 + x_2 + \cdots + x_n$ be the sum of $n$ independent observations from a population with standard deviation $\sigma$. By the Bienaymé formula (variances of independent variables add),

$$\operatorname{Var}(T) = \operatorname{Var}(x_1) + \cdots + \operatorname{Var}(x_n) = n\sigma^2.$$

The sample mean is $\bar{x} = T/n$, and scaling a variable by a constant divides its variance by the constant squared:

$$\operatorname{Var}(\bar{x}) = \operatorname{Var}\!\left(\frac{T}{n}\right) = \frac{1}{n^2}\operatorname{Var}(T) = \frac{1}{n^2}\, n\sigma^2 = \frac{\sigma^2}{n}.$$

The standard error is, by definition, the standard deviation of $\bar{x}$ — the square root of this variance — yielding $\sigma_{\bar{x}} = \sigma/\sqrt{n}$.

**Why the $\sqrt{n}$ matters practically:** the $1/\sqrt{n}$ factor means precision is expensive. To cut the error in your estimate of a population mean by a factor of two, you need **four times** as many observations; to reduce it by a factor of ten, you need **one hundred times** as many. This diminishing return is the key trade-off between sample size and accuracy. Conceptually, the SEM measures the dispersion of sample means around the true population mean: larger samples make individual means cluster more tightly, because no single sample's quirks dominate an average of many observations. The standard error is also the standard ingredient in calculating confidence intervals — foreshadowing the statistical methods coming up in the course.

## Validating the SEM by Simulation

A formula copied from a theorem is only trustworthy if it predicts what actually happens, so the lecture tests it head-to-head against simulation. The experimental design:

- A tuple of sample sizes: $(25, 50, 100, 200, 300, 400, 500, 600)$, with **50 trials run at each size**.
- The population is `getHighs()` — the daily high temperature dataset used throughout the course — and its standard deviation is computed with `numpy.std(population)` over the **entire population** (a detail that becomes important below).
- For each sample size, two numbers are collected:
  - the **theoretical** value: `sem(popSD, size)`, appended to a list of SEMs;
  - the **observed** value: 50 random samples of that size are drawn with `random.sample`, each sample's mean computed, and then `numpy.std(means)` taken across those 50 means.
- Both series are plotted against sample size: the observed values as a solid line labeled "Std of 50 means," the theoretical SEM as a red dashed line, titled "SD for 50 Means and SEM."

**Result:** the two curves track each other remarkably closely. Both start near $2$ at $n = 25$, drop steeply, and flatten out to roughly $0.35$ by sample sizes of $400$–$600$, with the red dashed theory line practically on top of the blue solid empirical line — especially as $n$ grows. This confirms the formula works: the standard error genuinely predicts the spread of sample means, exactly as the third CLT feature promises. It also illustrates the $1/\sqrt{n}$ decay concretely — quadrupling the sample size roughly halves the spread of the means.

## When $\sigma$ Is Unknown: Substituting the Sample SD

There is a catch, flagged explicitly in the lecture: **in any realistic setting, we do not know the population standard deviation.** The validation experiment quietly cheated — the whole temperature population sat in memory, so computing `popSD` was trivial. With real data you have only a sample; the population itself is unavailable, so $\sigma$ cannot be computed directly.

The obvious fix is to use the **sample standard deviation as a stand-in** for $\sigma$:

$$\sigma_{\bar{x}} \approx \frac{\sigma_x}{\sqrt{n}},$$

where $\sigma_x$ (or $s$) is the standard deviation computed from the sample. Because this is only an *estimator* of the true standard error rather than the exact quantity, alternative notations such as $\widehat{\sigma}_{\bar{x}} := \sigma_x/\sqrt{n}$ or $s_{\bar{x}} := s/\sqrt{n}$ are common, signaling the estimated status.

How good is this approximation? The lecture answers with a figure plotting, for the high-temperature data, the **percent difference between the sample SD and the true population SD as a function of sample size**:

- At very small sample sizes the error is huge — starting around **14%**;
- By $n = 100$ it has fallen to roughly **4–6%**;
- Approaching $n = 500$–$600$ it settles down to about **2%**.

So the sample SD is a poor estimate of $\sigma$ for small samples but quite good for reasonably large ones. The Wikipedia account adds an important subtlety about *why* small samples misbehave: substituting the sample SD systematically **underestimates** the population SD (and hence the SEM) when $n$ is small — the underestimate is about **25% at $n = 2$**, shrinking to about **5% by $n = 6$**. Corrections exist for this bias: Gurland and Tripathi (1971) provide a correction equation, and Sokal and Rohlf (1981) give a correction factor applicable for $n < 20$.

The practical takeaway, and the bridge to what follows in the course: plugging the sample standard deviation into the SEM formula yields a reliable estimate of how much sample means will vary — which is precisely the quantity needed for the confidence intervals and hypothesis-testing machinery ahead.

## Where the temperature experiment landed: big samples recover the population SD

Slide 26 distills the lesson of the previous experiment ("The Point"): **once the sample reaches a reasonable size, the sample standard deviation is a pretty good approximation to the population standard deviation.** In the plot "Sample SD vs Population SD, Temperatures," the percent difference between the sample SD and the true population SD of the high temperatures starts very high — around 14% — when the sample is tiny, drops very quickly, and is down to roughly 2% by a sample size of 600. In other words, a few hundred observations already estimate the spread quite well.

Before accepting this as a general law, the skeptical questions are: *is this an artifact of this particular example?* Two things could be special about temperatures: (1) the **shape** of the population's distribution, and (2) the **size** of the population itself. The rest of this segment tests each factor in turn by rebuilding the experiment with controlled synthetic populations.

## Three synthetic populations with deliberately different shapes

To break the tie between "temperatures happen to be nice" and "this always works," the function `plotDistributions` constructs three populations of 100,000 values each with very different shapes:

```python
uniform, normal, exp = [], [], []
for i in range(100000):
    uniform.append(random.random())       # even spread between 0 and 1
    normal.append(random.gauss(0, 1))     # Gaussian, mean 0, SD 1
    exp.append(random.expovariate(0.5))   # exponential, rate 0.5
makeHist(uniform, 'Uniform', 'Value', 'Frequency')
pylab.figure()
makeHist(normal, 'Gaussian', 'Value', 'Frequency')
pylab.figure()
makeHist(exp, 'Exponential', 'Value', 'Frequency')
```

Calling `pylab.figure()` between the `makeHist` calls produces three separate plots (slide 28):

- **Uniform** (`random.random()`): exactly what you'd expect — a flat histogram. Every value between 0 and 1 is equally likely, and each bin holds roughly 5,000 of the 100,000 samples. Symmetric, with no tails at all.
- **Gaussian** (`random.gauss(0, 1)`): the classic bell curve, centered at 0, peaking around 17,000 samples per bin, with most of the mass between about $-3$ and $3$. Symmetric, but with tapering tails on both sides.
- **Exponential** (`random.expovariate(0.5)`): completely different — an enormous spike near 0 (almost 45,000 samples in the first bin) followed by a long tail decaying out toward 25. Strongly **asymmetric**.

These three give a controlled comparison: flat-symmetric, peaked-symmetric, and heavily tailed-asymmetric.

## Distribution shape matters — and the culprit is skew

Repeating the original experiment — draw samples of increasing size from a population, compare sample SD to population SD — separately for each of the three populations (slide 29) gives a clear answer: **yes, distribution matters.** All three curves fall as sample size grows, but they are clearly separated:

- the **uniform** population converges fastest (lowest curve),
- the **normal** sits in the middle,
- the **exponential** is the worst — starting near a 25% difference and still around 5% even at a sample size of 600.

The explanation written on the slide is **skew**: the measure of the asymmetry of a probability distribution. Per the Wikipedia material, skewness, like kurtosis, is a *shape* characteristic of a distribution of a real-valued random variable, measured about its mean; its value can be positive, zero, negative, or undefined. For a unimodal distribution, **negative skew commonly indicates the tail is on the left side, positive skew the tail on the right** — the tapering sides of the histogram are the visual cue:

![Source: Wikipedia, article "[Skewness](https://en.wikipedia.org/wiki/Skewness)".](https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Negative_and_positive_skew_diagrams_%28English%29.svg/960px-Negative_and_positive_skew_diagrams_%28English%29.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

Formally, the skewness $\gamma_1$ is the third standardized moment (Pearson's moment coefficient of skewness):

$$\gamma_1 = \frac{\mu_3}{\sigma^3} = \operatorname{E}\!\left[\left(\frac{X-\mu}{\sigma}\right)^3\right] = \frac{\kappa_3}{\kappa_2^{3/2}},$$

where $\mu_3$ is the third central moment and $\kappa_t$ the $t$-th cumulants. Cubing the standardized deviations preserves their sign and weights large departures heavily, so a long tail on one side of the mean dominates the statistic — precisely why a tailed, lopsided population is flagged.

Two cautions from the Wikipedia material refine the intuition. First, the *older* notion of nonparametric skew, $(\mu - \nu)/\sigma$ with $\mu$ the mean and $\nu$ the median, does not always agree in sign with the moment-based definition, and conflating them is misleading — the textbook rule of thumb "mean right of median under right skew" fails with surprising frequency (multimodal distributions, distributions where one tail is long but the other thick, and discrete distributions; e.g., US household-resident counts are right-skewed yet the mean sits in the heavier left tail because the majority of cases is at or below the mode, which equals the median). Second, a symmetric unimodal or multimodal distribution always has zero skewness, but zero skewness does **not** imply symmetry — one long thin tail can balance a short thick one.

Why does skew degrade small-sample SD estimates? In a highly skewed population, the extreme values that set the spread live in a long, sparsely populated tail. A small sample will frequently contain none of those tail values — understating the spread — or occasionally catch several — overstating it — so the sample SD stays unstable until the sample is large enough to represent the tail reliably. Hence the ordering observed on the slide: the tail-less uniform converges fastest, and the long-tailed exponential is slowest.

## The exponential distribution: why it is the hard case

The exponential (or negative exponential) distribution is the probability distribution of **distances between events in a Poisson point process** — a process in which events occur continuously and independently at a constant average rate. The "distance" can be any meaningful one-dimensional measure: time between production errors, or length along a roll of fabric in weaving. It is a special case of the gamma distribution and the continuous analogue of the geometric distribution, and it is defined by one key property: **memorylessness**. (Note it is a single member of the much larger "exponential family" of distributions, which also contains the normal, binomial, gamma, and Poisson families.)

Its probability density function, with rate parameter $\lambda > 0$ and support $[0,\infty)$, is

$$f(x;\lambda) = \lambda e^{-\lambda x}, \qquad x \geq 0,$$

sometimes reparametr

## The five-step recipe for estimating a population mean

The lecture pulls the whole thread together into a practical procedure — what you would actually do, step by step, to estimate a population mean from a single sample:

1. **Choose the sample size based on an estimate of the skew in the population.** The reason skew drives this choice is the central limit theorem: for i.i.d. observations $X_i$ with mean $\mu$ and finite variance $\sigma^2$, the normalized mean obeys the Lindeberg–Lévy CLT,
$$\sqrt{n}\left(\bar{X}_n - \mu\right)\ \xrightarrow{d}\ \mathcal{N}\left(0,\ \sigma^{2}\right),$$
so the distribution of $\bar{X}_n$ approaches a normal with mean $\mu$ and variance $\sigma^2/n$ *regardless of the shape of the individual $X_i$* — but only once $n$ is large enough. How large "large enough" is depends on that shape: the more skewed the population, the longer the sample means take to look normal, so the larger the sample you need before the CLT bails you out.
2. **Choose a random sample from the population** (more on why "random" and "independent" are non-negotiable below).
3. **Compute the mean and the standard deviation of that sample.**
4. **Use the sample standard deviation to estimate the standard error**, as $s/\sqrt{n}$. This substitution is necessary because the population $\sigma$ is seldom known; the estimated quantity is commonly written $\widehat{\sigma}_{\bar{x}} := \sigma_x/\sqrt{n}$ or $s_{\bar{x}} := s/\sqrt{n}$.
5. **Use that estimated SE to generate confidence intervals around the sample mean.** This is precisely the standard error's main job: it is "often used in calculations of confidence intervals."

Each downstream step inherits its validity from the mathematics of the standard error and the coverage property of confidence intervals, developed next.

## The standard error: what $\sigma/\sqrt{n}$ measures and where it comes from

The **standard error (SE)** of a statistic — usually an estimator of a parameter like the mean — is the standard deviation of its *sampling distribution*. That distribution is generated by repeatedly sampling from the same population and recording the sample mean each time; the resulting collection of sample means has its own mean and variance, and its variance equals the population variance divided by the sample size. Intuitively: as $n$ grows, sample means cluster ever more tightly around the population mean.

The formula follows from the variance algebra of sums. For independent observations $x_1,\dots,x_n$ from a population with standard deviation $\sigma$, define the total $T = (x_1 + \cdots + x_n)$. By the **Bienaymé formula**,
$$\operatorname{Var}(T) = \operatorname{Var}(x_1) + \cdots + \operatorname{Var}(x_n) = n\sigma^2.$$
Since the sample mean is $\bar{x} = T/n$, propagating the variance gives
$$\operatorname{Var}(\bar{x}) = \operatorname{Var}\!\left(\frac{T}{n}\right) = \frac{1}{n^2}\operatorname{Var}(T) = \frac{\sigma^2}{n}, \qquad\text{so}\qquad \sigma_{\bar{x}} = \sqrt{\frac{\sigma^2}{n}} = \frac{\sigma}{\sqrt{n}}.$$

Two practical consequences matter:

- **Precision is expensive.** Because of the $1/\sqrt{n}$ factor, cutting the error on your estimate in half requires *four times* as many observations; reducing it by a factor of ten requires a *hundred times* as many. Diminishing returns set in fast.
- **Estimating the SE introduces small-sample bias.** Replacing the unknown $\sigma$ with the sample standard deviation systematically *underestimates* the population standard deviation when $n$ is small — by about 25% at $n=2$, though only about 5% by $n=6$. Gurland and Tripathi (1971) provide a correction for this effect, and Sokal and Rohlf (1981) give a correction factor for small samples with $n < 20$. The lecture's recipe implicitly assumes $n$ is large enough that this bias is negligible.

## Reading a confidence interval correctly

A **confidence interval (CI)**, in the frequentist view, is a range of values likely to contain the true value of an unknown parameter *in repeated sampling*. Instead of a bare point estimate ("average screen time is 3 hours per day"), you report a range ("2 to 4 hours") together with a confidence level, typically 95%.

The most common misreading deserves emphasis: a 95% confidence level does **not** mean there is a 95% probability that the true parameter lies inside your particular computed interval — that probabilistic reading belongs to the Bayesian *credible interval*. The frequentist treats the population mean as a fixed unknown constant; what is random is the sample, and therefore the interval endpoints. The 95% instead describes the long-run reliability of the *method*: repeat the same sampling procedure 100 times and roughly 95 of the resulting intervals will contain the true mean.

Formally, for a random sample $X$ from a distribution with parameters $(\theta, \varphi)$ — where $\theta$ is the quantity to be estimated — a confidence interval $(u(X), v(X))$ with confidence coefficient $\gamma$ satisfies
$$P\big(u(X) < \theta < v(X)\big) = \gamma \quad \text{for all } (\theta, \varphi),$$
with $\gamma$ typically $0.95$, written as $1-\alpha$ where $\alpha = 0.05$. Some authors require only $P \geq \gamma$; such intervals are called *conservative*, erring on the safe side. When exact intervals are hard to construct, approximate ones are accepted if the coverage probability is approximately $\gamma$.

Two widely applicable construction methods exist: **bootstrapping** and the **central limit theorem**. The CLT route requires a large sample: compute $\bar{X}$ and $S$ and use the fact that $\dfrac{\bar{X}-\mu}{S/\sqrt{n}}$ is asymptotically standard normal. For the exact treatment of a normally distributed population, the statistic
$$T = \frac{\bar{X} - \mu}{S/\sqrt{n}}$$
follows a **Student's $t$ distribution** with $n-1$ degrees of freedom — useful because its distribution does not depend on the unobservable $\mu$ and $\sigma^2$, making $T$ a *pivotal quantity*. Choosing $c$ as the 97.5th percentile of $T$ puts 2.5% probability below $-c$ and 2.5% above $+c$ (the $t$ distribution being symmetric about 0), so $P(-c \leq T \leq c) = 0.95$, and rearranging yields the interval
$$\bar{X} - \frac{cS}{\sqrt{n}} \;\leq\; \mu \;\leq\; \bar{X} + \frac{cS}{\sqrt{n}}.$$
In the large-sample regime of the lecture's experiment, the constant playing the role of $c$ is $1.96$ — the cutoff that leaves 2.5% in each tail under the normal approximation.

## Does the recipe actually work? An empirical check

Rather than take the theory on faith, the lecture tests it directly: **are 200 samples enough?** The experiment sets `numBad` to zero, then over a number of trials draws a sample of `sampleSize` from `temps` using `random.sample`, computes the sample mean as `sum(sample)/sampleSize`, and estimates the standard error as `numpy.std(sample)/sampleSize**0.5` — implementing step four of the recipe verbatim. Because in this case the true population mean `popMean` happens to be known, each trial can be graded: if
$$|\,\texttt{popMean} - \texttt{sampleMean}\,| > 1.96 \times \text{SE},$$
then the true mean lies outside that sample's 95% confidence interval, and `numBad` is incremented. The program prints the fraction of trials falling outside the interval.

If the theory is right, that fraction should be about five percent. The observed result was **0.0511** — a hair over five percent, almost exactly what the mathematics predicted. The mechanism behind the match: by the CLT, sample means behave approximately as normals centered on $\mu$ with variance $\sigma^2/n$, so a window of $\pm 1.96$ standard errors around a sample mean should fail to cover the truth only about 5% of the time. (This refines the law of large numbers, which guarantees only that $\bar{X}_n$ converges to $\mu$; the CLT specifies the *size and distributional shape* of the fluctuations along the way.) Verdict: 200 samples suffice, and the recipe does what it claims. Varying the sample size and watching how the fraction responds is a worthwhile experiment to run yourself.

## The fine print: why samples must be random and independent

The recipe carries a red-flagged caveat: it works great for **independent random samples**, and that is not always easy to achieve — as political pollsters keep learning, much to their embarrassment. If the sample is not truly random and independent, none of the beautiful machinery developed above saves you.

The theoretical fine print explains why. The classical CLT assumes the random variables are **independent and identically distributed (i.i.d.)**; although this requirement can be weakened — convergence of the mean to normality also occurs for non-identical distributions or non-independent observations, provided they satisfy certain conditions — arbitrary dependence breaks the guarantee. For genuinely correlated random variables, even computing the sample variance correctly requires the **Markov chain central limit theorem** rather than the ordinary formulas. A further subtlety arises when the sample size itself is random — cases where you sample without knowing in advance how many observations will meet some acceptance criterion. Then $N$ is a random variable whose own variation feeds into the total:
$$\operatorname{Var}(T) = \operatorname{E}(N)\operatorname{Var}(X) + \operatorname{Var}(N)\big(\operatorname{E}(X)\big)^2,$$
so the naive $\sigma/\sqrt{n}$ understates the true uncertainty. Every departure from clean, independent randomness injects variation that the standard recipe does not account for — which is exactly why step two of the recipe is a step and not an afterthought.
