# Lecture 7: Confidence Intervals

This lecture builds the platform on which confidence intervals will stand: it makes explicit the two assumptions hidden inside the empirical rule, verifies them with a million-sample simulation, recaps probability density functions as "probability = area under a curve," and pins down exactly how much probability a normal distribution places within one, two, and three standard deviations of its mean.

## The two assumptions behind the empirical rule

Before trusting the empirical rule, we name what we assumed when we used it:

1. **The mean estimation error is zero.** If we could repeat the estimation process over and over, the errors would average out to zero — we are not systematically biased in one direction.
2. **The errors in the estimates are normally distributed** (Gaussian).

Assumption 2 is pictured by the classic bell curve: a normal distribution with mean $0$ and standard deviation $1$, centered at zero on the x-axis, peaking at about $0.40$ right at the mean, and falling off symmetrically toward $-4$ and $+4$. That symmetry around zero is precisely what assumption 1 captures.

The lecture insists on checking these assumptions rather than taking them on faith — a healthy instinct, since the normal distribution is frequently misused in contexts where the data are not actually normal and is therefore a poor model.

## The normal distribution: shape, parameters, and why it's plausible

A normal (Gaussian) distribution is a continuous probability distribution for a real-valued random variable, denoted $N(\mu, \sigma^2)$, with density

$$f(x)=\frac{1}{\sqrt{2\pi\sigma^2}}\exp\!\left(-\frac{(x-\mu)^2}{2\sigma^2}\right),$$

where $\mu$ is the mean (also the median and mode) and $\sigma^2$ is the variance, with $\sigma>0$ the standard deviation. The special case $\mu=0$, $\sigma^2=1$ is the **standard normal**, with density

$$\varphi(z)=\frac{e^{-z^2/2}}{\sqrt{2\pi}},$$

whose peak value $1/\sqrt{2\pi}\approx 0.399$ at $z=0$ is the "about 0.40" seen in the lecture's

## The Gaussian Probability Density Function: Definition and Implementation

The normal distribution (also called the Gaussian distribution) is a continuous probability distribution for a real-valued random variable. Its probability density function has the general form:

$$f(x) = \frac{1}{\sqrt{2\pi\sigma^2}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

Here $\mu$ is the mean (also the median and mode), while $\sigma^2$ is the variance and $\sigma$ is the standard deviation. In code, this formula decomposes naturally into two multiplicative pieces — a normalizing constant and an exponential term:

```python
def gaussian(x, mu, sigma):
    factor1 = 1/(sigma * (2*pi)**0.5)
    factor2 = e**(-(x-mu)**2 / (2*sigma**2))
    return factor1 * factor2
```

`factor1` is the prefactor $1/(\sigma\sqrt{2\pi})$, and `factor2` is the exponential $e^{-(x-\mu)^2/(2\sigma^2)}$. Their product is exactly the boxed formula.

To visualize it, we sample the function at closely spaced points from $x = -4$ to $x = +4$ (stepping by 0.05), setting $\mu = 0$ and $\sigma = 1$. This is the **standard normal distribution** — the special case where $\mu = 0$ and $\sigma^2 = 1$, whose density is conventionally written as:

$$\varphi(z) = \frac{e^{-z^2/2}}{\sqrt{2\pi}}$$

The resulting plot shows the familiar bell curve: centered at zero, symmetric, rising to a peak of roughly $0.4$ at the mean, then falling off rapidly toward $\pm 4$. That peak value is not arbitrary — the standard normal density attains its maximum value $1/\sqrt{2\pi} \approx 0.3989$ at $z = 0$, with inflection points at $z = \pm 1$.

## Densities Are Not Probabilities: Why Integration Is Required

A critical conceptual point: **the y-axis values on a PDF plot are not probabilities.** You cannot read off "the probability of getting exactly zero is 0.4." These values are *densities*. The PDF is the derivative of the cumulative distribution function (CDF), and because we are dealing with derivatives, we must use integration to interpret a PDF.

To obtain an actual probability from a PDF, we integrate it over a region — the probability of landing in some interval equals the area under the curve over that interval. This is why the total area under any PDF must equal 1, and why the density itself can exceed 1 at its peak without violating anything.

## Numerical Integration with `scipy.integrate.quad`

Since most integrals involving Gaussians have no closed-form elementary antiderivative, we turn to numerical methods. The SciPy library provides `scipy.integrate.quad`, a workhorse function that computes definite integrals numerically. It takes up to four arguments:

1. A function or method to be integrated,
2. A number representing the lower limit,
3. A number representing the upper limit,
4. An optional tuple supplying values for all remaining arguments of the function beyond the first.

That fourth argument matters here because our `gaussian` function takes three parameters $(x, \mu, \sigma)$, but `quad` integrates only over the first one — so we pass $\mu$ and $\sigma$ along in a tuple. The function returns a tuple containing an approximation to the integral and an estimate of the absolute error; we index with `[0]` to keep just the approximation.

## The Empirical Rule Verified by Integration

The **68–95–99.7 rule** (also called the empirical rule or three-sigma rule) states that for a normal distribution, approximately 68%, 95%, and 99.7% of values lie within one, two, and three standard deviations of the mean respectively:

$$\Pr(\mu - 1\sigma \leq X \leq \mu + 1\sigma) \approx 68.27\%$$
$$\Pr(\mu - 2\sigma \leq X \leq \mu + 2\sigma) \approx 95.45\%$$
$$\Pr(\mu - 3\sigma \leq X \leq \mu + 3\sigma) \approx 99.73\%$$

We can verify this empirically by choosing random values of $\mu$ (integer between $-10$ and $10$) and $\sigma$ (integer between $1$ and $10$), then integrating the Gaussian between $\mu - n\sigma$ and $\mu + n\sigma$ for $n = 1, 1.96, 3$ using `quad`. Across trials such as $(\mu=9, \sigma=6)$, $(\mu=-6, \sigma=5)$, and $(\mu=2, \sigma=6)$, the results are always identical to four decimal places: 0.6827, 0.95, and 0.9973.

This invariance is no accident. Making the change of variable to the standard score $z = (x-\mu)/\sigma$, the probability becomes:

$$\Pr(\mu - n\sigma \leq X \leq \mu + n\sigma) = \frac{1}{\sqrt{2\pi}}\int_{-n}^{n} e^{-z^2/2}\,dz$$

which is completely independent of $\mu$ and $\sigma$. Only the shape of the bell curve matters — not where it is centered or how wide it is. The precise values come from the CDF $\Phi$: for example, $\Phi(2) \approx 0.9772$, so the two-sided interval gives $\Phi(2) - \Phi(-2) \approx 0.9545$.

## Caveats and Broader Significance of the Rule

The usefulness of the empirical rule depends critically on the data genuinely being normally distributed. Among bell-shaped distributions seen in real data, the normal has notoriously **thin tails** — an unusual concentration of probability near its center. If the data instead follow a similar-looking but fat-tailed distribution, the actual fractions within each band will be lower than the rule predicts.

Several related benchmarks exist for cases where normality cannot be assumed:

- **Chebyshev's inequality**: even for non-normal variables, at least 88.8% of cases fall within three standard deviations.
- **Vysochanskij–Petunin inequality**: for unimodal distributions, at least 95% fall within three standard deviations.

In practice, the three-sigma rule serves different purposes across fields. In the empirical sciences, treating 99.7% as near certainty is a conventional heuristic. In the social sciences, a result may be considered statistically significant at roughly a two-sigma level (95% confidence). In particle physics, the bar is far higher — a five-sigma effect ($99.99994\%$ confidence) is required to qualify as a discovery. The rule also underlies practical tools: quick rough probability estimates given a standard deviation, simple outlier tests, and normality checks when population normality is uncertain.



## What a confidence interval actually certifies — and what it does not

The simulation has produced an answer with a small standard deviation, and the natural temptation is to read that as "we are close to the true value of $\pi$." That reading deserves to be pushed on. Consider two statements about the interval $[3.13743875875,\ 3.14567467875]$:

1. *95% of the time we run this simulation, our estimate of $\pi$ lands in this interval.*
2. *With probability 0.95, the actual value of $\pi$ lies in this interval.*

They sound nearly identical, and in this particular case both happen to be factually correct — $\pi$ really does sit between those two numbers, and repeated runs really would land in that range 95% of the time. But only the **first** statement can be inferred from the simulation. The second makes a claim about $\pi$ itself, and that is a leap the simulation alone does not justify.

The Wikipedia material on confidence intervals explains exactly why. In **frequentist inference**, a confidence interval (CI) is a range of values likely to contain the true value of an unknown parameter *in repeated sampling*. Crucially, a 95% confidence level does **not** imply a 95% probability that the true parameter lies within one particular calculated interval — that interpretation belongs to the *credible interval* of Bayesian inference. The confidence level instead reflects the **long-run reliability of the method**: if the same sampling procedure were repeated 100 times, approximately 95 of the resulting intervals would be expected to contain the true value. Formally, for a random sample $X$ from a distribution with parameters $(\theta, \phi)$, a CI at confidence level $\gamma$ is a pair of random variables $(u(X), v(X))$ with the property

$$P\big(u(X) < \theta < v(X)\big) = \gamma \quad \text{for all } (\theta, \phi),$$

typically with $\gamma = 0.95$, written as $1 - \alpha$ with $\alpha = 0.05$. The asymmetry is the whole point: the true parameter $\theta$ is a **fixed unknown constant**, while the sample is random — so it is the interval *endpoints* that are random variables, and the probability statement is about the procedure across repeated samples, not about any one realized interval. (Some authors only require $P(u(X) < \theta < v(X)) \geq \gamma$; such "conservative" intervals err on the safe side, and approximate intervals with coverage $\approx \gamma$ are accepted when exact ones are hard to construct.)

Two widely applicable methods exist for building such intervals: **bootstrapping** and the **central limit theorem**. The CLT route shows the repeated-sampling logic concretely. For an independent sample from a normal population with unknown mean $\mu$ and variance $\sigma^2$, define the sample mean $\bar{X} = \frac{1}{n}(X_1 + \cdots + X_n)$ and the unbiased sample variance $S^2 = \frac{1}{n-1}\sum_{i=1}^n (X_i - \bar{X})^2$. Then

$$T = \frac{\bar{X} - \mu}{S/\sqrt{n}}$$

has a Student's $t$ distribution with $n-1$ degrees of freedom. $T$ is a **pivotal quantity**: its distribution does not depend on the unobservable parameters $\mu$ and $\sigma^2$. Taking $c$ as the 97.5th percentile of $T$ (the $t$ distribution is symmetric about 0, so 2.5% of the mass falls below $-c$ and 2.5% above $+c$), we get $P(-c \leq T \leq c) = 0.95$, and rearranging yields

$$P_X\!\left(\bar{X} - \frac{cS}{\sqrt{n}} \leq \mu \leq \bar{X} + \frac{cS}{\sqrt{n}}\right) = 0.95,$$

a statement about how often the constructed interval covers $\mu$ in repeated sampling. The lesson to write down: **statistically valid is not the same as true**. A confidence interval tells us about the reliability of our *procedure*, not directly about the *world*.

## Precision is not correctness: the factor-of-two bug

To see why that distinction matters in practice, introduce a deliberate bug into `throwNeedles`. The buggy version looks almost identical: throw `numNeedles` needles, pick $x$ and $y$ at random, test whether $(x^2 + y^2)^{1/2} \leq 1.0$ (the test for landing inside the quarter circle), and count the hits in `inCircle`. But the return statement reads

```python
return 2 * inCircle / numNeedles   # should be 4
```

Recall where the factor of 4 came from: the quarter circle sits inside a one-by-one square, so the fraction of needles inside must be multiplied by 4 to recover $\pi$. Multiply by 2 instead, and the program will happily **converge — tightly, with a beautifully small standard deviation — to a value near $\pi/2$**. Every statistical check from the previous discussion reports success: the estimates cluster, the standard deviation shrinks, the confidence interval is narrow. And the answer is wrong.

This is the "Right?" with the question mark. The statistics can only measure how *consistent* the procedure is; they cannot tell us whether the model of the world — here, that factor of 4 — is correct in the first place. The Wikipedia material reinforces the point from the numerical-analysis side: unlike deterministic methods, the Monte Carlo estimate of error is **not a strict error bound** — random sampling may fail to uncover important features of the problem, resulting in an *underestimate* of the error — and among the recognized limitations of Monte Carlo methods generally are the reliability of random number generators and the **verification and validation** of results. Precision is not correctness.

## The general technique: Monte Carlo integration

The needle experiment is one instance of a very general and useful procedure. To estimate the area of a region $R$:

1. Pick an **enclosing region** $E$ such that the area of $E$ is easy to calculate and $R$ lies completely within $E$.
2. Pick a set of **random points** lying within $E$.
3. Let $F$ be the **fraction** of those points that fall within $R$.
4. Estimate $\text{area}(R) \approx \text{area}(E) \times F$.

In the needle problem, $E$ was the unit square (area 1), $R$ was the quarter circle, and $F$ was the fraction of needles landing inside. The Wikipedia article on Monte Carlo integration formalizes this as a technique for numerical integration using random numbers: where deterministic rules such as the trapezoidal rule evaluate the integrand on a regular grid, Monte Carlo **randomly chooses the points** at which it evaluates, so each realization gives a different outcome and the final result is an approximation accompanied by error bars within which the correct value is likely to lie. The problem it addresses is the multidimensional definite integral

$$I = \int_{\Omega} f(\overline{\mathbf{x}})\, d\overline{\mathbf{x}},$$

where $\Omega \subset \mathbb{R}^m$ has volume $V = \int_\Omega d\overline{\mathbf{x}}$. The naive approach samples $N$ points uniformly on $\Omega$ and forms

$$I \approx Q_N \equiv V \frac{1}{N}\sum_{i=1}^{N} f(\overline{\mathbf{x}}_i) = V\langle f \rangle,$$

which converges by the **law of large numbers**: $\lim_{N\to\infty} Q_N = I$. The error bars come from the sample variance: since $\mathrm{Var}(Q_N) = V^2\,\mathrm{Var}(f)/N$, the error estimate is

$$\delta Q_N \approx \sqrt{\mathrm{Var}(Q_N)} = V\frac{\sqrt{\mathrm{Var}(f)}}{\sqrt{N}},$$

which is the standard error of the mean scaled by $V$ and **decreases as $1/\sqrt{N}$**. The crucial payoff: this rate **does not depend on the dimension** $m$ of the integral, whereas most deterministic methods depend exponentially on dimension — the promised advantage of Monte Carlo integration in high dimensions.

![Source: Wikipedia, article "[Monte Carlo integration](https://en.wikipedia.org/wiki/Monte_Carlo_integration)".](https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/MonteCarloIntegrationCircle.svg/500px-MonteCarloIntegrationCircle.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

The figure above shows the four-step recipe in action: the domain $D$ (inner circle) sits inside the easily-measured square $E$; with 40 of 50 sampled points inside the circle, the fraction $F = 0.8$ gives $\text{area}(E) \times F = 4 \times 0.8 = 3.2 \approx \pi$. The Wikipedia article presents exactly this as the paradigmatic example: with the indicator function $H(x,y) = 1$ if $x^2 + y^2 \leq 1$ and $0$ otherwise, on $\Omega = [-1,1]\times[-1,1]$ with $V = 4$, the integral $I_\pi = \int_\Omega H(x,y)\,dx\,dy = \pi$, so $Q_N = 4\,\frac{1}{N}\sum_i H(x_i, y_i)$ estimates $\pi$ — the needle experiment written as an integral.

![Source: Wikipedia, article "[Monte Carlo integration](https://en.wikipedia.org/wiki/Monte_Carlo_integration)".](https://upload.wikimedia.org/wikipedia/en/thumb/7/72/Relative_error_of_a_Monte_Carlo_integration_to_calculate_pi.svg/960px-Relative_error_of_a_Monte_Carlo_integration_to_calculate_pi.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

The second figure confirms the theory empirically: plotting the relative error $(Q_N - \pi)/\pi$ against the number of samples $N$ shows the predicted $1/\sqrt{N}$ scaling. Note also that the naive uniform sampler is only the baseline — the Wikipedia article stresses that beating deterministic algorithms requires **problem-specific sampling distributions**, exploiting the fact that higher-dimensional integrands are typically very localized (only a small subspace contributes meaningfully to the integral). Two standard improvement strategies are **stratified sampling** (dividing the region into sub-domains) and **importance sampling** (drawing from non-uniform distributions); recursive stratified sampling generalizes one-dimensional adaptive quadrature by estimating the integral and error on each sub-volume with plain Monte Carlo and recursively splitting any sub-volume whose error exceeds the required accuracy.

## Worked example: integrating $\sin(x)$ and recovering $\pi$

The same recipe estimates integrals directly. Suppose we want the area under $\sin(x)$ from $x = 0$ to $x = \pi$ — the curve rises from zero at the origin, peaks at 1 around $x \approx 1.5$, and returns to zero just past 3. Apply the four steps:

- $R$ = the region under the curve, i.e. the area whose value is $\int_0^\pi \sin(x)\,dx$.
- $E$ = the box spanning $x \in [0, \pi]$ and $y \in [0, 1]$. The curve never leaves this box, and its area is trivial: $\pi \times 1 = \pi$.
- Throw random darts uniformly at the box and let $F$ = the fraction landing **below the curve**.
- Estimate the integral as $\text{area}(E) \times F = \pi \cdot F$.

No symbolic integration is ever performed — just darts and counting. And the example comes full circle: calculus tells us that $\int_0^\pi \sin(x)\,dx = 2$, so if we *estimate the integral* we can **back out $\pi$ itself** — the very quantity we started with when throwing needles. This is the broader principle from the Wikipedia material: Monte Carlo methods can solve any problem having a probabilistic interpretation, and by the law of large numbers, integrals expressible as the expected value of a random variable can be approximated by the empirical (sample) mean of independent draws. Same idea, new application — that is what makes the technique generally useful.

## Estimating an Integral by Throwing Darts

The closing picture of the lecture compresses the whole Monte Carlo method into one experiment. The plot shows $y = \sin x$ on $[0, \pi]$ — the interval where sine rises from zero, peaks at one, and falls back to zero — inside a box of width $\pi$ and height $1$, so the box has area $A_{\text{box}} = \pi \cdot 1 = \pi$. The program then throws "darts": each throw picks an $x$ uniformly between $0$ and $\pi$ and a $y$ uniformly between $0$ and $1$. Each point is classified by a single test: if $y < \sin x$ the point landed *under* the curve and is painted red (a hit, filling the region beneath the hump); otherwise it is painted black (a miss, piling up in the two upper corners on either side of the hump).

The punchline is that **the fraction of darts landing under the curve should roughly equal the fraction of the box's area lying under the curve**. So counting hits gives an estimate of the integral:

$$\int_0^\pi \sin x \, dx \;\approx\; \pi \cdot \frac{\#\text{red}}{\#\text{total}}.$$

Calculus supplies the exact answer to check against: the area under the hump is $2$. As more darts are thrown, the estimate tightens — the randomness averages out, and the law of large numbers does the work.

This is a concrete instance of what the literature calls **Monte Carlo integration**: a technique for numerical integration using random numbers, which numerically computes a definite integral

$$I = \int_\Omega f(\overline{\mathbf{x}})\, d\overline{\mathbf{x}},$$

where $\Omega \subset \mathbb{R}^m$ has volume $V$. Where deterministic schemes like the trapezoidal rule evaluate the integrand on a regular grid, Monte Carlo instead randomly chooses the points at which the integrand is evaluated. The naive scheme samples $N$ points uniformly on $\Omega$ and approximates

$$I \approx Q_N \equiv V \frac{1}{N}\sum_{i=1}^{N} f(\overline{\mathbf{x}}_i) = V\langle f \rangle.$$

In the dart picture, $f$ is the indicator function of the region under the sine curve — it equals $1$ for a hit and $0$ for a miss — so the sample average $\langle f \rangle$ is exactly the red-dot fraction, and multiplying by the box volume $V = \pi$ recovers the integral. Note the character of the result: unlike a deterministic method, each realization gives a different outcome, so the output is an approximation accompanied by error bars within which the correct value likely lies.

The professor explicitly connects this back to the earlier trick of estimating $\pi$ itself — and the structure is identical. The paradigmatic Monte Carlo integration example defines $H(x,y) = 1$ if $x^2 + y^2 \leq 1$ and $0$ otherwise, on the square $\Omega = [-1,1]\times[-1,1]$ with $V = 4$; then $I_\pi = \int_\Omega H(x,y)\,dx\,dy = \pi$, and picking $N$ random points and computing $Q_N = 4\,\frac{1}{N}\sum_i H(x_i, y_i)$ estimates $\pi$. Throw points into a box, count the ones that land where you want, read the answer off the ratio: integration is just area, and random sampling finds area for us.

![Source: Wikipedia, article "[Law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers)".](https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Law_of_large_numbers_%28black_%26_red_balls%29.png/960px-Law_of_large_numbers_%28black_%26_red_balls%29.png)

## Why the Estimate Tightens: The Law of Large Numbers

The engine behind "throw more darts and the answer improves" is the **law of large numbers**: in probability theory, the mathematical law stating that the average of results obtained from a large number of independent random samples converges to the true value, if it exists. Formally, for a sample of independent and identically distributed values, the sample mean converges to the true mean. Its importance is that it guarantees stable long-term results for the averages of random events — the classic illustration being a casino, which may lose money on any single spin of the roulette wheel but whose earnings tend toward a predictable percentage over many spins; any player's winning streak is eventually overcome by the parameters of the game.

The die example makes the mechanism tangible: a single roll of a six-sided die yields $1$ through $6$ with equal probability, so the expected value is $(1+2+3+4+5+6)/6 = 3.5$. Roll many dice and the average of their values approaches $3.5$, with precision increasing as more are rolled.

![Source: Wikipedia, article "[Law of large numbers](https://en.wikipedia.org/wiki/Law_of_large_numbers)".](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c9/Lawoflargenumbers.svg/960px-Lawoflargenumbers.svg.png)

The dart-counting case is the **Bernoulli** specialization, which matters most for Monte Carlo: each throw is a binary trial (hit or miss), and the law guarantees that the empirical probability of success over a series of Bernoulli trials converges to the theoretical probability. For a Bernoulli variable the expected value *is* the theoretical success probability, and the average of $n$ i.i.d. such variables is precisely the relative frequency — so the red-dot fraction converges to the true area ratio. The fair-coin version: the proportion of heads after $n$ flips almost surely converges to $1/2$. One subtlety worth internalizing: although the *proportion* of heads approaches $1/2$, the absolute difference in the numbers of heads and tails almost surely becomes *large* as flips accumulate — the expected difference grows, just at a slower rate than the number of flips, so the ratio of the difference to the number of flips goes to zero. Ratios stabilize even though raw counts do not balance out; our integral estimator relies entirely on the ratio.

The Monte Carlo method is cited directly as a prime application of the law: a broad class of computational algorithms relying on repeated random sampling to obtain numerical results, where more repetitions give better approximations. Its importance stems mainly from situations where other approaches are difficult or impossible.

Two cautions temper the promise. First, the law applies only to large numbers of observations — there is no principle that a small sample will coincide with the expected value, nor that a streak of one outcome must be immediately "balanced" by others (the gambler's fallacy). Second, convergence can fail outright: for heavy-tailed distributions the sample average need not converge at all. The Cauchy distribution has no expectation — generated, for instance, by taking the tangent of an angle uniform on $(-90°, +90°)$; its median is zero, but the average of $n$ such variables has the same distribution as a single one and does not converge in probability to anything. For Pareto distributions with $\alpha < 1$ the expectation is infinite. And if trials embed a selection bias, as in human economic behavior, more trials do not cure it — the bias remains.

Historically, Gerolamo Cardano (1501–1576) stated without proof that the accuracy of empirical statistics improves with the number of trials; Jacob Bernoulli first proved a special form for binary random variables, taking over twenty years to produce a rigorous proof published posthumously in his *Ars Conjectandi* (1713), where he called it his "golden theorem" — it became known as Bernoulli's theorem (not to be confused with Bernoulli's principle, named for his nephew Daniel). S. D. Poisson described it in 1837 as "la loi des grands nombres," and both names circulated thereafter, with "law of large numbers" becoming standard.

## How Fast It Converges — and Why Monte Carlo Wins in High Dimensions

The quantitative payoff comes from the error analysis. With $Q_N = V\langle f\rangle$ built from $N$ uniform samples, the variance of the estimate is

$$\mathrm{Var}(Q_N) = \frac{V^2}{N^2}\sum_{i=1}^{N}\mathrm{Var}(f) = V^2\frac{\mathrm{Var}(f)}{N},$$

using the unbiased variance estimate $\mathrm{Var}(f) = \frac{1}{N-1}\sum_i \mathrm{E}\left[(f(\overline{\mathbf{x}}_i) - \langle f\rangle)^2\right]$. The error therefore behaves as

$$\delta Q_N \approx \sqrt{\mathrm{Var}(Q_N)} = V\frac{\sqrt{\mathrm{Var}(f)}}{\sqrt{N}},$$

which decreases as $1/\sqrt{N}$ — the standard error of the mean scaled by the volume $V$. This is why the professor says the estimate "tightens up" as darts accumulate: quadrupling the trials halves the error. Crucially, this rate **does not depend on the number of dimensions** of the integral, which is the promised advantage of Monte Carlo over most deterministic methods, whose cost depends exponentially on dimension. It is why the method is particularly useful for higher-dimensional integrals, where evaluating an integrand on a regular grid becomes hopeless.

Two honest qualifications complete the picture. Unlike a deterministic method's error control, the Monte Carlo error bar is *not* a strict bound: random sampling may fail to uncover important features of the integrand, producing an underestimate of the true error. And the naive uniform sampler is only a baseline — real gains come from problem-specific sampling distributions, exploiting the fact that almost all higher-dimensional integrands are highly localized, with only a small subspace contributing meaningfully to the integral. The two canonical refinements are **stratified sampling**, dividing the region into sub-domains (recursive stratified sampling generalizes one-dimensional adaptive quadrature: at each recursion step the integral and error are estimated by plain Monte Carlo, and any sub-volume whose error exceeds the required accuracy is split further — though simple "dividing by two" does not transfer to multiple dimensions), and **importance sampling**, drawing from non-uniform distributions concentrated where the integrand matters. A large share of the Monte Carlo literature is devoted to such error-reduction strategies. Even the textbook $\pi$-estimation experiment confirms the theory empirically: plotting the relative error $(Q_N - \pi)/\pi$ against $N$ shows the predicted $1/\sqrt{N}$ decay.

So the method in one breath: model the randomness, run the trials, and infer the quantity you care about from the statistics of the outcomes — with the law of large numbers guaranteeing that the statistics converge, and the $1/\sqrt{N}$ error law telling you exactly how fast.
