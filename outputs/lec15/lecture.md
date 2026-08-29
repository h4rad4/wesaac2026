# Statistical Sins and Wrapup

How charts deceive — through axis scaling and interval choice — using the global-warming debate as the case study, and the habits of mind that let an educated consumer of data catch the deception.

## What the global temperature record measures — and why the scale matters

Before judging any temperature chart, you need to know what quantity is being plotted. **Global surface temperature (GST)** is the average temperature of Earth's surface at a given time, formed by combining sea surface temperature and near-surface air temperature over land, weighted by their respective areas. The IPCC Sixth Assessment Report's version, **global mean surface temperature (GMST)**, is the estimated global average of near-surface air temperatures over land and sea ice plus sea surface temperature over ice-free oceans, normally expressed as departures from a reference period; the closely related **GSAT** averages air temperatures only, and the two differ slightly. Surface data come mainly from weather stations and satellites, with proxies — tree rings, corals, ice cores — extending knowledge into the distant past. Reliable regional series begin in the 1850–1880 window (the instrumental temperature record), the Central England series reaches back to 1659, and quasi-global records start in 1850. Values are aggregated by year or month.

Three quantitative facts anchor everything that follows:

- The **current annual GMST is about 15 °C (59 °F)**, though monthly temperatures vary almost 2 °C (4 °F) above or below that figure — partly due to natural internal variability such as the El Niño–Southern Oscillation. The planet's temperature therefore "lives" in a narrow band of a few degrees Fahrenheit.
- The record shows warming of **1.09 °C (range 0.95–1.20 °C)** from 1850–1900 to 2011–2020 across multiple independently produced datasets, and at least **1.1 °C (1.9 °F) above 1880 levels**. Through 1940 temperatures rose, were relatively stable between 1940 and 1975 (a plateau mostly attributed to sulfate aerosol), and since 1975 have climbed roughly 0.15–0.20 °C per decade. Land has warmed faster than the sea surface (1.59 °C vs. 0.88 °C over the same baseline period).
- The major datasets — NASA GISS, HadCRUT, NOAA, Japan, Berkeley Earth — agree closely: pairwise correlations of the four longer-term series are at least 99.29%. The warming signal is not an artifact of one organization's processing.

![Source: Wikipedia, article "[Global surface temperature](https://en.wikipedia.org/wiki/Global_surface_temperature)".](https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/20200324_Global_average_temperature_-_NASA-GISS_HadCrut_NOAA_Japan_BerkeleyE.svg/500px-20200324_Global_average_temperature_-_NASA-GISS_HadCrut_NOAA_Japan_BerkeleyE.svg.png)

These facts matter for chart design: because the physically meaningful range is narrow, the choice of y-axis baseline determines whether a real trend is visible or erased.

## Sin or virtue? Truncating the y-axis

Monday's warning was: beware of charts whose y-axis doesn't start at zero. Today's examples complicate that rule.

**Case 1 — the alarming chart.** A plot of average global temperature from 1880 to 2014 (NASA data) runs its y-axis from about 55 °F to 60 °F. The line wiggles around 56–57 °F through the first half of the twentieth century, then climbs fairly steadily to nearly 59 °F by 2014. It looks clearly, alarmingly upward — and the non-zero baseline should trigger suspicion.

**Case 2 — the flat chart.** The *National Review* (December 2015) plotted the same kind of data, average annual global temperature in Fahrenheit from 1880 to 2015, but let the y-axis run from −10 to 110 °F. The result: a completely flat line — "nothing to see here." Yet this is a case where the truncated axis is the *honest* one. A change of a few degrees Fahrenheit in global average temperature is a really big deal; insisting on a zero-based axis implies that planetary temperatures could plausibly swing from −10 to 110 °F, which is physically absurd. Here the sin belongs to the flat chart, which uses a technically-non-zero-based axis to hide a real trend.

**Case 3 — fever and the flu.** Suppose you measure your oral temperature hourly from hour 3 to hour 9 during a bout of flu. Plotted with the y-axis from 97 to 102 °F, the story reads: start near 98.6 °F, climb to about 99.5 °F by hour 5, dip slightly, reach 100 °F, and continue to about 100.5 °F by hour 9 — you're getting sicker; call a doctor. The identical data with a y-axis from 0 to 200 °F reads: flat line, don't worry. But an oral temperature of 200 °F is preposterous — you'd be dead long before that, since human body temperature varies only within a narrow band around 98.6 °F. Here truncating the axis to eliminate impossible values is the right thing to do.

The synthesis: **truncation is a sin when it exaggerates meaningless noise, and a virtue when it removes irrelevant, physically impossible range.** You cannot apply a mechanical rule; you must think about what the data means. A zero-based axis can deceive just as effectively as a truncated one.

## Don't confuse fluctuations with trends

The third exhibit is a chart headlined "The Myth of Global Warming," showing RSS global mean temperature change over 224 months, February 1997 to September 2015, blaring "No global warming for 18 years 8 months." The fitted trend over that window is essentially flat: $-0.01\ ^\circ\text{C}$ (about $-0.03\ ^\circ\text{C}$ per century) with $r^2 = 0.000$. Does this refute global warming? No. Any noisy signal — and monthly temperature measurements are noisy — will contain stretches that wiggle down or stay flat even in the middle of a strong long-term trend. If you start your clock at a particularly warm month, you can manufacture an eighteen-year "pause."

This is precisely the phenomenon the climate literature calls the **global warming hiatus**: a period of relatively little change in globally averaged surface temperatures. Many such roughly 15-year episodes appear in the surface record alongside robust evidence of long-term warming, and each is shorter than the 30-year periods over which climate is classically averaged. The publicity centered on 1998–2013: the exceptionally warm El Niño year of 1998 was an outlier from the continuing trend, so subsequent years gave the appearance of a pause — by January 2006 some claimed warming had stopped, and an April 2006 opinion piece announced an eight-year halt before being rebutted. Studies in 2009 showed decades without warming were not exceptional, and a 2011 study showed the rising trend continued unabated once known variability was accounted for. The IPCC Fifth Assessment Report, despite concerns that fifteen years is too short for a meaningful trend, defined the hiatus as a much smaller linear trend over 1998–2012 than over

## Cherry picking: choosing the data points that fit your story

**Cherry picking** is the selective choice of the most beneficial or attractive items from what is available. In journalism, law, and epidemiology it amounts to a reporting bias — the act of selectively suppressing evidence. The Wikipedia article identifies it with the *fallacy of incomplete evidence*: focusing on individual data points, case reports, or anecdotes that seem to confirm a pre-established position while wilfully ignoring the significant portion of related cases or data that contradict it. Crucially, it can be committed **intentionally or unintentionally** — the name comes from fruit harvesting, where a picker takes only the ripest, healthiest cherries, so an observer who sees only the selected fruit wrongly concludes the whole tree is in equally good condition. A non-representative sample creates a false impression of the whole.

Why is this such a pervasive failure mode? Because the individual facts a cherry picker cites are often *true* — what is missing is context. As the philosopher Michel de Montaigne observed about people trusting almanac prophecies, nobody records the infinite misses; when a seer stumbles upon one truth, "that carries a mighty report, as being rare, incredible, and prodigious." The ancient story of Diagoras of Melos makes the same point: shown votive gifts from people who supposedly escaped shipwreck by praying, he pointed out that the many who died at sea despite their prayers were not likewise commemorated — a classic case of **survivorship bias**. Scholars classify cherry picking as a fallacy of *selective attention*, whose most common example is **confirmation bias**, and it surfaces under many guises: the anecdotal-evidence fallacy, "selective use of evidence," false dichotomies, **quote mining** in debates (facts are true but stripped of moderating context), and the one-sided argument (*card stacking*, *suppressed evidence*), where only reasons supporting a proposition are supplied. Even **p-hacking** — selecting analyses until a desired result appears — is a form of cherry picking. Richard Somerville testified before the U.S. House of Representatives that emphasizing supportive results while dismissing unsupportive ones is "a hallmark of poor science or pseudo-science"; Steven Novella counters that rigorous science looks at *all* the evidence, controls for variables, and uses blinded observation to minimize bias. The practice even distorts medical research: a 2002 review of 31 antidepressant efficacy trials found that exclusion criteria meant trial participants represented only a minority of patients treated in routine clinical practice, undermining generalization of the results. Cherry picking is also one of the epistemological characteristics of **denialism**, used to seemingly contradict scientific findings in climate change denial, creationism, and tobacco-health denial.

The lecture's example shows how credible cherry picking can sound. Lawrence Solomon wrote in the *Financial Post* (April 15, 2013): *"Yesterday, April 14th, the Arctic had more sea ice than it had on April 14, 1989 – 14.511 million square kilometres vs 14.510 million square kilometres, according to the National Snow and Ice Data Center of the United States, an official source."* Everything about this is designed to persuade: the **National Snow and Ice Data Center (NSIDC)** really is an authoritative source — a University of Colorado Boulder center affiliated with NOAA, one of twelve NASA-funded Distributed Active Archive Centers, which monitors Arctic and Antarctic sea ice in near real time. And the arithmetic is literally true: $14.511 > 14.510$. What he did was reach into thirty years of daily measurements and pluck out exactly two days that support his story. In a noisy dataset, if you are allowed to choose which two points to compare, you can almost always find a pair that supports whatever claim you like.

The full NSIDC record exposes the trick. Plotted as a **sea ice anomaly** — the deviation from the average, in millions of square kilometres — the yearly values wiggle up and down wildly: enormous year-to-year variation, i.e., noise. But the trend line through that noise starts around $+0.8$ in 1980 and declines steadily, almost monotonically, to around $-1.3$ today. Yes, the ice is melting. The cherry-picked comparison of two nearly equal days is technically accurate and completely misleading. Climate denial provides canonical illustrations of the technique: by deliberately choosing inappropriate time periods — for instance 1998–2012 — an artificial "pause" in warming can be manufactured even while the underlying trend continues upward.

![Source: Wikipedia, article "[Cherry picking](https://en.wikipedia.org/wiki/Cherry_picking)".](https://upload.wikimedia.org/wikipedia/commons/f/f4/Global_warming_hiatus.gif?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail_unscaled)

The moral: **don't cherry pick** — and when someone hands you two data points, ask what the whole dataset looks like.

## Numbers without context: the comforting percentage and the terrifying count

Two mirror-image deceptions show why a bare number carries no meaning until you know its base or its baseline.

**The comforting statistic.** You may hear that 99.8% of the firearms in the U.S. will *not* be used to commit a violent crime in any given year — which sounds deeply reassuring. But a percentage is meaningless without knowing what it is a percentage *of*. There are roughly 300,000,000 privately owned firearms in the U.S., so the 0.2% that *are* used amounts to

$$300{,}000{,}000 \times 0.002 = 600{,}000$$

— six hundred thousand firearms used to commit a violent crime in a single year. Suddenly the comforting 99.8% is not comforting at all. The general lesson: **a small percentage of a very large number can be a very large number.** Never let anyone hand you a percentage without telling you what it's a percentage of.

**The not-so-comforting statistic.** The reverse error makes small numbers frightening. On April 29, 2009, CNN reported that Mexican health officials suspected the swine flu outbreak had caused "more than 159 deaths and roughly 2,500 illnesses" — alarming headlines about a new killer flu. The calibrating question is: compared to what? Seasonal influenza kills roughly **36,000 people per year in the U.S. alone**, every single year. Each of those 159 deaths is a tragedy, but whether 159 is alarming or negligible cannot be judged without a baseline. Without context, a small number can sound terrifying — exactly as a percentage can sound comforting while hiding a huge absolute count. Same lesson from both directions: **you need the context.**

## Relative change: beware the unknown denominator

Percentage *changes* carry the same trap in a subtler form. Suppose you're told that skipping lectures increases your probability of failing 6.0002 by 50%. That sounds like a serious effect — but 50% *of what*? Both of the following are "a 50% increase":

- $0.5 \to 0.75$: failing goes from a coin flip to three-in-four — a big deal, you should come to lecture.
- $0.005 \to 0.0075$: failing goes from about half a percent to three-quarters of a percent — probably not worth losing sleep over.

Identical relative change, utterly different practical significance, because the **denominators** differ by two orders of magnitude. Hence the rule: **beware of percentage change when you don't know the denominator.** Whenever anyone quotes you a percentage change, your first question should be: *relative to what baseline?*

## Cancer clusters: when randomness looks like a pattern

A **cancer cluster** is defined by the CDC as "a greater-than-expected number of cancer cases that occurs within a group of people in a geographic area over a period of time" — more generally, a disease cluster in which a high number of cancer cases occurs in a group of people in a particular area over a limited period. In the U.S., state and local health departments respond to **more than 1,000 inquiries about suspected cancer clusters each year**, and the vast majority are deemed not significant: only **between 5% and 15%** of suspected clusters turn out to be statistically significant, i.e., with a disease rate significantly greater than that of the general population.

Why do so many apparent clusters evaporate? Random cases of cancer naturally form clumps that are misinterpreted as clusters — a well-known problem in interpreting data. And the number of *opportunities* for apparent clusters is enormous: slice the country into many small geographic areas, and each one offers many chances for a random local excess to appear. Statisticians examining such data must beware of coincidental patterns, exactly as in a randomly generated scatter plot where arcs and "clusters" appear to exist purely by coincidence — the trap known as the Texas sharpshooter fallacy, where the pattern is drawn *after* seeing where the points landed.

![Source: Wikipedia, article "[Cancer cluster](https://en.wikipedia.org/wiki/Cancer_cluster)".](https://upload.wikimedia.org/wikipedia/commons/thumb/a/aa/Texas_Sharpshooter_Fallacy_illustration.png/500px-Texas_Sharpshooter_Fallacy_illustration.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

This is why health departments follow a disciplined protocol before committing resources. When a claim is filed — usually by members of the public reporting that family members, friends, neighbors, or coworkers have been diagnosed with the same or related cancers — the department conducts a **preliminary review**: data are collected and verified on the types of cancer reported, the numbers of cases, the geographic area, and the patients' clinical histories. A committee of medical professionals then determines whether a full investigation (often lengthy and expensive) is justified. Only clusters whose disease rate is statistically significantly above the general population rate proceed. Certain features make a cluster *less likely* to be coincidental and thus more worth investigating: when the cases consist of **one type of cancer**, a **rare type**, or a type **unusual for the age group** involved.

Real clusters do exist, and history shows why the machinery matters. Well-documented work-related cancer clusters include scrotal cancer among chimney sweeps in 18th-century London; osteosarcoma among female watch-dial painters in the 20th century; skin cancer in farmers; bladder cancer in dye workers exposed to aniline compounds; and leukemia and lymphoma in chemical workers exposed to benzene. The epistemological balance is delicate: most alarms are statistical noise generated by sheer multiplicity of chances, yet the rare genuine signal — a true environmental or occupational carcinogen — is worth the careful screening that separates it from coincidence.

## A Hypothetical Cancer Cluster: The Case of Region 111

To see why stochastic thinking matters outside the classroom, consider a scenario of the kind that appears in newspapers and courtrooms. Massachusetts covers about 10,000 square miles and sees roughly 36,000 new cancer cases per year. Suppose an attorney partitions the state into 1000 regions of 10 square miles each and examines the distribution of cases. If cases spread evenly, each region should see $36000/1000 = 36$ cases per year, hence $3 \times 36 = 108$ over a three-year period. The attorney then announces that **region 111 had 143 new cancer cases over three years** — an excess of

$$\frac{143 - 108}{108} \approx 0.32,$$

i.e., more than 32% above expectation. The pressing question: how worried should the residents of region 111 be? Should they march on the statehouse? Is there something in the water?

This question is legitimate, because real cancer clusters do exist. A **cancer cluster** is a disease cluster in which a high number of cancer cases occurs in a group of people in a particular geographic area over a limited period of time. The medical literature documents well-established work-related examples: scrotal cancer among 18th-century London chimney sweeps; osteosarcoma among female watch-dial painters in the 20th century; skin cancer in farmers; bladder cancer in dye workers exposed to aniline compounds; and leukemia and lymphoma in chemical workers exposed to benzene. So "is this a real cluster?" is a question worth asking seriously — but answering it correctly requires distinguishing a genuine signal from a statistical artifact, which is exactly what the next two simulations do.

## Simulation I: The Pre-Specified Region Question

First ask the narrow question: **if cancer cases were distributed completely at random across the state, how likely would it be for some *pre-specified* region to get at least 143 cases in three years?** The simulation models each case as landing in a uniformly random region, independently of everything else:

- Set constants: `numCasesPerYear` = 36,000, `numYears` = 3, `stateSize` = 10,000 sq mi, `communitySize` = 10, and `numCommunities` = `stateSize//communitySize` = 1000 regions.
- Run 100 trials. In each trial, start with a list `locs` of zeros, one entry per community. For each of the `numYears*numCasesPerYear` = 108,000 cases, pick a community with `random.choice(range(numCommunities))` and increment its count.
- After scattering all cases, check whether region 111 got 143 or more; if so, increment `numGreater`.
- Report `prob` = `numGreater`/`numTrials`, rounded to 4 decimal places.

The estimated probability comes out **essentially zero**. This makes sense: under the random model, a region's count over three years is centered near 108 with standard deviation on the order of $\sqrt{108} \approx 10.4$, so 143 sits more than three standard deviations above the mean — a very rare draw for *one named* region. If you decided *in advance* to look at region 111, seeing 143 cases there is astronomically unlikely to be pure chance. Case closed — there must be something wrong in region 111?

Not so fast.

## Simulation II: The Any-Region Question — Multiple Hypothesis Testing

Now change the question: **what is the probability that *some* region — any region at all — has at least 143 cases?** The code is almost identical: again distribute all 108,000 cases at random across the 1000 communities each trial, but replace the fixed-region test with `if max(locs) >= 143` — i.e., examine the *most extreme* region in that trial, whatever it happens to be. Accumulate `anyRegion`, compute `aProb` = `anyRegion`/`numTrials`, and print the estimated probability.

This probability is **not small at all**. When examining 1000 regions, it is quite likely that at least one of them looks like a cluster purely by chance. Nobody chose region 111 in advance — the attorney looked at all 1000 regions and then said, "aha, look at region 111!" That is a variant of cherry picking called **multiple hypothesis testing**: implicitly, the attorney tested a thousand hypotheses and reported only the one that came out alarming.

This is a general and well-studied statistical phenomenon. The **multiple comparisons** (multiplicity, multiple testing) problem arises when many statistical tests are performed on the same dataset: each individual test carries its own chance of a **Type I error** (false positive), so the overall probability of making at least one false positive grows with the number of tests. A stated confidence level generally applies only to each test individually, not to the family of simultaneous tests. Concretely, if one test is run at the 5% level with a true null hypothesis, there is a 5% risk of incorrectly rejecting it; but if 100 independent tests are each run at the 5% level and all nulls are true, the *expected* number of false rejections is 5, and the probability of at least one incorrect rejection is approximately **99.4%**. The same inflation affects confidence intervals: 100 simultaneous 95% intervals will miss the true parameter about 5 times in expectation, with a ~99.4% chance that at least one misses.

For $m$ independent comparisons each run at level $\alpha$, the **family-wise error rate** (FWER) — the probability of at least one false positive — is

$$\bar{\alpha} = 1 - (1 - \alpha)^m,$$

and even without independence, Boole's inequality guarantees $\bar{\alpha} \le m\alpha$ (e.g., $0.2649 = 1-(1-.05)^6 \le .05 \times 6 = 0.3$). Applied to the attorney's scan: if each region has even a tiny probability $p$ of reaching 143 by pure chance, the probability that *at least one* of the 1000 regions does is $1-(1-p)^{1000} \approx 1000p$ for small $p$ — a thousandfold amplification of a seemingly negligible risk. This is why the any-region simulation returns a substantial probability while the pre-specified simulation returns essentially zero.

Because failure to compensate has real-world consequences, several correction techniques exist, typically designed to control the family-wise error rate or the false discovery rate:

- **Bonferroni correction** — the most conservative, free of dependence and distributional assumptions: require $\alpha_{\text{per comparison}} = \alpha/m$.
- **Šidák correction** — marginally less conservative for independent comparisons: solve $1-(1-\alpha_{\text{per comparison}})^m = \alpha$, giving $\alpha_{\text{per comparison}} = 1-(1-\alpha)^{1/m}$.
- **Holm–Bonferroni method** — uniformly more powerful than simple Bonferroni: test the lowest p-value against the strictest criterion and higher p-values against progressively less strict thresholds of the form $\alpha/(m-i+1)$.

The problem gained attention in the 1950s through statisticians such as Tukey and Scheffé, the first international conference on multiple comparison procedures met in Tel Aviv in 1996, and the area remains active (e.g., Emmanuel Candès, Vladimir Vovk). The practical lesson: confidence that a result will generalize to independent data should be weaker when it emerges from an analysis involving many comparisons. The binomial-testing figure below shows the mechanism in miniature — 30 samples simulated entirely under the null hypothesis, yet one produces a p-value small enough to falsely reject at the 0.05 level.

![Source: Wikipedia, article "[Multiple comparisons problem](https://en.wikipedia.org/wiki/Multiple_comparisons_problem)".](https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Multiple_binomial_testing.svg/960px-Multiple_binomial_testing.svg.png?utm_source=en.wikipedia.org&utm_campaign=parser&utm_content=thumbnail)

So how worried should the residents of region 111 be? **A lot less worried than the headline suggests.**

## What Real Cancer-Cluster Investigations Show

The region-111 story is not hypothetical in structure — it mirrors how suspected clusters actually arise and get evaluated. Cancer cluster suspicions usually begin when members of the public report that family members, friends, neighbors, or coworkers have been diagnosed with the same or related cancers. State or local health departments investigate when a claim is filed, starting with a **preliminary review**: data are collected and verified on the types of cancer reported, the numbers of cases, the geographic area, and the patients' clinical histories. A committee of medical professionals then determines whether a full investigation — often lengthy and expensive — is justified.

The statistics explain why most inquiries stop there. In the U.S., state and local health departments respond to **more than 1,000 inquiries about suspected cancer clusters each year**, and it is likely that many of these are due to chance alone: a well-known problem in interpreting data is that random cases of cancer can appear to form clumps that are misinterpreted as clusters. Accordingly, only clusters whose disease rate is *statistically significantly greater* than the general population's rate are investigated — and **between 5% and 15% of suspected cancer clusters turn out to be statistically significant**. The pre-specified-versus-any-region distinction from the simulations is precisely why: scanning a state's geography is an uncorrected multiple-comparisons exercise, so apparent clumps are the expected output of randomness.

Two features make a suspected cluster *less* likely to be coincidental, and both are absent from the attorney's presentation: a cluster is more credible if it consists of **one type of cancer**, a **rare type**, or a type **not usually found in a certain age group**. The hypothetical aggregates *all* new cancer cases in region 111 — exactly the kind of broad aggregation in which chance clumping is most plausible — which further tempers the alarm.

## Skepticism Versus Denial

The bottom line of the whole discussion: **when drawing inferences from data, skepticism is merited.** Always ask three questions — how was the data gathered? what was decided *before* the data was collected? and what was chosen *after* the fact? In the region-111 case, the answer to the last question ("which region to highlight") is what converts an unremarkable random fluctuation into a headline.

But skepticism and denial are different things. **Skepticism means asking questions and following the evidence; denial means refusing to accept the answer no matter what the evidence says.** Ambrose Bierce captured the distinction: *"Doubt, indulged and cherished, is in danger of becoming denial; but if honest, and bent on thorough investigation, it may soon lead to full establishment of the truth."* Doubt held honestly drives you toward the truth; doubt cherished for its own sake curdles into denial.

## 6.0002 Major Topics

Stepping back, the course has covered four interlocking themes:

- **Optimization problems** — formalizing goals and searching decision spaces.
- **Stochastic thinking** — reasoning under randomness, as today


