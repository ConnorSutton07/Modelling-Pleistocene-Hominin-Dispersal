# Simulating-H.-Erectus-Dispersal-with-Cellular-Automata
Understanding Pleistocene Hominin Dispersal Through Cellular
Automata & Bayesian Ensemble Modeling

Connor Sutton, 12/11/2020

Introduction

Homo Erectus, our immediate predecessor on the hominin evolutionary track, is one of
the most interesting, significant, and mysterious members of our genus. No species of human
existed longer than H. Erectus, who roamed the Afro-Eurasian continent for a majority of the
Pleistocene epoch. They exist in the fossil record from ~2 ma until 100 ka, well after the
emergence of anatomically modern H. sapiens.1
It is possible that H. Erectus was the first
hominin to leave Africa, arriving in Dmanisi, Georgia by 1.8 ma; Java, Indonesia by 1.6 ma; and
China by at least 0.7 ma.2 Persistence hunters armed with tools of their own design, they thrived
across a range of contrasting environments and traveled in communities in a manner reminiscent
of early H. sapiens.

In spite of their spatiotemporal vastness, or perhaps because of it, H. erectus remains one
of the most poorly understood hominin species. The Australopithecines—antecedents of the
Homo genus—can be described with much more confidence. In general, they were short, bipedal
apes that spent as much time roaming grasslands as climbing trees. Their brain sizes and diets
were similar to Chimpanzees, with a gradual shift towards larger brains and more frequent meateating, 
and they were moderately sexually dimorphic, indicating polygynous societies with
strong male-male competition (though not nearly as strong as those seen amongst gorillas).

Analyzing and categorizing species of Australopithecines is a much simpler task than for human
species as variations amongst Australopithecines are relatively localized, both in time and space.
Attempts to organize members of our own genus have to make sense of a chaotic, seemingly
self-contradicting fossil record.
When humans emerge, there is a sharp, rapid increase in brain size. Spatial variation
becomes sporadic, with populations appearing ~2 ma in China, Spain, and South/East Africa
with little-to-no evidence of a gradual shift or migration. A clean, successive family tree is
impossible to construct with our current amount of information, and yet this information is
crucial to understanding the origin of our species. Evolutionary biologists and geneticists are
confident that modern H. sapiens outside of Africa can be traced back, for the most part, to a
specific population that left Africa ~60 ka.3 What, then, happened to the hominins who lived in
Europe and Asia before this? Are these the ancestors of Neanderthals and Denisovans? What
population is the stem from which modern humans and Neanderthals split? Does this split
actually exist, or are these the same species with clinal variation? There are important questions
regarding the differences between H. Sapiens and H. Erectus as well. How sophisticated were 
their tools? What kinds of clothing did they wear? Were they capable of language, of art? If so,
did they tell stories, and did they worship gods?
Much work needs to be done before these questions may be answered, and this project
aims to create a probability-based foundation for understanding how H. Erectus—or more
generally, hominins of the Pleistocene—dispersed throughout the Afro-Eurasian continent, and
which factors were the most significant to this dispersal process.


Setting up the Simulation


The model which I have created for this purpose simulates cellular automata on a map of
the Afro-Eurasian continent. Each cell represents an area of ~3,500 km2
, is either occupied or
unoccupied by a community, and has a vegetation class, altitude level, population density
(referring to the number of occupied neighboring cells), and a probability of extinction, P_ext.

P_ext = P(ext | V) + P(ext | A) + P(ext | D)

P(ext | V), P(ext | A), and P(ext | D) refer to the probabilities of extinction at each time step given a
certain vegetation class, altitude, and population density, respectively. There is also a global
probability of colonization Pcol, representing the probability that an occupied cell colonizes a
neighboring unoccupied cell. The rate of dispersal can be given as P_col (1 – P_ext), meaning that
scaling Pcol based on vegetation, altitude, etc. would have a redundant effect on the rate of
dispersal.

The vegetation classes are derived from a simplified version of the BIOME4 Pleistocene
vegetation map, with the 28 original biomes being reduced to eight.

![vegetation_map_with_key](https://user-images.githubusercontent.com/55513603/102290757-47642b00-3f07-11eb-87fe-e15ce4fc7c7f.png)

While this may seem like an oversimplification, biomes separate in the BIOME4 map such as
‘tropical evergreen broadleaf forest,’ ‘tropical semi-evergreen broadleaf forest,’ and ‘tropical
deciduous broadleaf forest’ have been condensed to more general categories like ‘tropical
forest,’ and biomes unique to the Americas or Australia have been ignored. The biomes being
considered in this model, each representing a vegetation class, include temperate forest,
grassland, desert, tropical forest, tundra, warm-temperate forest, and boreal forest, and can be
seen in Figure 1. The elevation data comes from Nasa’s Socioeconomic Data & Applications
Center (SEDAC). This data is not specific to the Pleistocene, but for the purposes of this model,
the difference is negligible; the most essential difference between the modern and Pleistocene
continents concern vegetation and sea level.


Initialization, Bayesian Model Averaging, & Tuning the Parameters


The first step in the initialization process is to create 30 ensembles, each of which
conduct their own run of the simulation. The reason for this is that each single run of the
simulation is equally arbitrary, and in order to gain any real-world insight from arbitrary
simulations, several must be conducted with minor fluctuations so that the average may be taken
and the separate runs compared. Every simulation yielding the same result is a problem
equivalent to overfitting in model prediction methods, so these fluctuations are essential.

Upon the initialization of each ensemble, a small amount of Gaussian noise is added to
each parameter affecting Pext to create variations amongst the ensembles. They are also given a
weight value—at the beginning, each ensemble has the same weight of 1
30
, and the sum of the
weights is always equal to one. As the simulation progresses, the weights are updated based on
the posterior probability of each model given the data; i.e., the more an ensemble’s simulation
resembles reality, the higher its weight will be.5 The simulation then uses Bayesian model
averaging by taking the average values of each simulation and makes a prediction for the most
likely outcome based on the ensemble weights. This prediction is used to produce an image
illustrating the H. erectus populations on a map of the Afro-Eurasian continent.

In each ensemble, the same five cells in Eastern Africaؙ—modern day Kenya—are
populated, representing the supposed origin of H. erectus. Each time step of the simulation
corresponds to 250 years, and the simulation is run from 2 ma to 1 ma. The values of P(ext | V) and
P(ext | A) were at first chosen based on intuition, with savannas, grasslands, and tropical forests,
and low-to-mid altitudes having very low probabilities of extinction, and tundras, boreal forests,
and mid-to-high altitudes being between difficult and virtually impossible to survive within. It is,
of course, impossible to know what values would yield results closest to the truth, but we do
know that H. erectus reached Georgia by 1.8 ma and Indonesia by 1.6 ma, and that the fossil 
records shows a trend towards Asia rather than Europe; based on this information, the parameters
and ensembles weights may be tuned so that the mean-ensemble image reflects this.

Perhaps the most important parameter is the value of P(ext | V) where V corresponds to the
desert biome. Unlike the other biomes, which have either very high rates of extinction or very
low rates of extinction, the desert has a more intermediate rate (warm-temperate forests being a
similar exception). Figure 1 illustrates the significance of the desert biome’s rate of extinction;
for H. erectus to make it to Asia, they must make a long trek across the Sahara Desert.

After a series of experiments with different values, I settled on the following base values
for each parameter, with Pcol = 0.20:

![table](https://user-images.githubusercontent.com/55513603/102291018-c8232700-3f07-11eb-9d0f-859ef6aa899a.png)
Table 1. Values of P(ext | V)


There is also the calculation of P(ext | D); like the hunter-gatherers from our own species,
H. erectus traveled and hunted in small communities across a range of land with which they were
deeply familiar.
3 The introduction of new communities within that land reduces the resources for
each community, and reduces the likelihood of continued inhabitation of that land. With k
representing the number of occupied cells within a 5x5 grid of cells, the extinction rate due to
population density of the center cell is given as simply as
P(ext | D) =
𝒌
𝟗𝟔
+ ƞ
(i)
, where ƞ
(i) is the Gaussian noise centered at 0 of an ensemble i.

In the case that all 24 neighboring cells are occupied, there would then be a ~25% chance
that cell goes extinct due to population density; combine this with P(ext | V), P(ext | A) and the fact
that each surrounding cell is also faced with a high population density, and the chances of having
dense desert communities are slim (Pext >> Pcol). With the parameters in place, the following
results are obtained when the model is run from 2 ma to 1.8 ma.

![dmanisi](https://user-images.githubusercontent.com/55513603/102291107-fc96e300-3f07-11eb-9ee1-28b0eec61bdd.png)
Fig. 2. Ensemble mean of simulation run from 2 ma to 1.8 ma, with Dmanisi labeled


Darker values correspond to more inhabitation across each ensemble (with black indicating full
occupation). The result indicates ~40% of the simulations made it Dmanisi by 1.8 ma. If the
parameters were again tuned to increase this number, it would likely be a case of overfitting.
Continuing this simulation to 1.6 ma yields the following distribution:

Fig. 3. Distribution of the Dmanisi colonization times
Each bar in this graph represents the number of ensembles which colonized Dmanisi
within a specific 20,000-year time frame, and on the whole, it clearly resembles a Gaussian
distribution. Based on these results, it may be presumed that with a much larger number of
ensembles, the simulation would yield a smooth Gaussian distribution of Dmanisi colonization
dates centered around 1.8 ma. Another noteworthy point from this distribution is that summing
the frequencies yields 29 instead of 30. This is because in one ensemble, the population went
completely extinct and never reached Dmanisi. Again, this is a result of keeping the simulation
generalized and avoiding overfitting and creating an arbitrary, ultimately meaningless set of data.
At this point, the simulation is set-up and tuned, and we can begin simulating over long
periods of time and generating data to analyze.
Results
Running the simulations from 2 ma to 1.5 ma yields the following four mean ensemble
images at times 1.875 ma, 1.75 ma, 1.625 ma, and 1.5 ma, respectively.
By 1.5 ma, the simulated H. erectus communities have populated all the cells of which
they are capable of long-term habitation, and simulation beyond this point yields results nearly
identical to those seen in Fig. 4d with slight fluctuations in population density. In the next
section, I make interpretations of the spatiotemporal indications of the simulation, but I am not a
trained paleontologist and these topics are highly debated amongst the trained paleontologists, so
my analysis should be understood with some reservations.
Fig. 4a. 1.875 ma Fig. 4b. 1.75 ma
Fig. 4c. 1.625 ma Fig. 4d. 1.5 ma
Analysis
We can see the progression of the H. erectus dispersion throughout the Afro-Eurasian
continent sequentially in Fig. 4, and for the most part, it lines up fairly well with the fossil
record. Starting in Kenya, the population spreads first throughout Africa, with a few brave
communities daring to cross the Sahara Desert on the path to the Near East. There are to methods
of entry: the top of the Arabian Peninsula (modern Israel) or the bottom (modern Yemen).4
Fig. 5. Illustration of hypothesized Pleistocene hominin dispersal routes. Note that the given dates do not necessarily correspond
to H. erectus, but Pleistocene hominins in general.4
In this model, the first population to reach the Arabian Peninsula does so via the Yemen
route, but are halted by the Sarawat Mountains. It is the second group who arrive by the Israel
route that continue their migration into Eurasia, reaching Georgia. The communities continuing
to move east must do through a narrow passage along the southern coast of Iran to avoid more
mountains, and in this way reach India, passing the Indus river along the way. It is my personal
belief that since it is likely that Pleistocene hominins took this route to get to India/Indonesia and
because rivers are so conducive to fossilization, sedimentary rocks along the Indus river are
likely possessors of hominin fossils.
There is also the population that moves north from Georgia, spreading across Europe and
Russia, reaching the Iberian Peninsula by ~1.6 ma. This is the most major contradiction between
the model and the fossil record as the latter implies that H. erectus arrived in Spain closer to 0.7
ma. Four potential reasons for this discrepancy come to mind.
1. A factor not considered in this model prevented dispersal throughout Europe. For
example, one fairly popular hypothesis from paleontologists Arribas & Palmqvist is
that competition with Sabre-tooth tigers prevented hominins from thriving in Europe
until humans developed advanced enough weapons to overcome them. Indeed, the
spread of hominins throughout Europe coincides with the introduction of the
Acheulean stone tool technocomplex.6
2. The value of P(ext | V) where V corresponds to warm-temperate forests is too low,
allowing populations to spread unrealistically. This seems less satisfactory as
subsequent hominin populations seem to have little issue surviving in such biomes.
3. The members of H. erectus residing in Georgia either went extinct or traveled east
towards Indonesia, and not until much later did another population arrive in Georgia
and continue to migrate into Europe. In order for this explanation to work, however,
we must assume that there are much fewer populations actively spreading than in the
model, which requires each individual population to move incredible distances to
reach Georgia by 1.8 ma and Indonesia by 1.6 ma. Using what we know about archaic
H. sapiens, migration usually occurs by slow, gradual shifts over long spans of time
since Hunter-gatherers tend to become familiar with a range of land and remain there.
making this explanation also fairly unsatisfactory.
4. Pleistocene hominins did spread into Europe, and it is just the incomplete nature of
the fossil record that causes paleontologists to believe the opposite. Only through
increased archaeological investigations in Eastern Europe can prove whether this is
true or false.
One of the most interesting results of the model is that the populations which moved
north towards Europe/Russia and those which moved east towards India end up meeting back in
China around the same time. It is easy to dismiss the Russian population as being purely a result
of the model since it also generated the European population that does not coincide with the
fossil record, but with a newfound interest in Russian hominins after the discovery of the
Denisovans in Siberia,
7
future examinations could provide more evidence for one way or the
other.
Conclusion
The combination of cellular automata simulations with Bayesian model averaging created
a remarkably insightful illustration of Pleistocene hominin dispersal, and I am very happy to
have found a way to integrate machine learning mathematics with anthropology.
There are several aspects of this project that could be improved. Perhaps the most drastic
way to improve the accuracy of this model is to incorporate wildlife data to further influence the
rate of extinction in a certain area. The rate of extinction would decrease in areas with plentiful
prey animals and little competition, and it would increase in the opposite case. This would allow 
us to test the Sabre-tooth cat hypothesis against the model to see how it holds up, and, more
generally, create a more accurate map of H. erectus communities.
Additionally, I’m not sure if my understanding and implementation of Bayesian model
averaging is accurate or some convoluted form based on a faulty interpretation. I believe,
however, that a deeper understanding of Bayesian inference techniques could lead to more robust
projects within the field of paleontology as those who practice it must work constantly on
probabilistic assumptions in trying to use scattered pieces of the past to create a cohesive story.
References
[1] Herries, Andy I. R.; Martin, Jesse M.; Leece, A. B.; Adams, Justin W.; Boschian, Giovanni; JoannesBoyau, Renaud; Edwards, Tara R.; Mallett, Tom; Massey, Jason; Murszewski, Ashleigh; Neubauer,
Simon (3 April 2020). "Contemporaneity of Australopithecus, Paranthropus, and early Homo erectus in
South Africa"
[2] Hughes, John K; Haywood, Alan; Mithen, Steven J; Sellwood, Bruce W; Valdes, Paul J (12 December
2006). “Investigating early hominin dispersal patterns: developing a framework for climate data
integration”
[3] Larsen, Clark Spencer. Our Origins: Discovering Biological Anthropology. Vol. 5, W.W. Norton &
Company, 2020.
[4] Kurt Lambeck, “Late pleistocene, holocene and present sea-levels: constraints on future
change”,Volume 89, Issue 3, 1990, Pages 205-217.
[5] Hoeting, J., Madigan, D., Raftery, A., & Volinsky, C. (1999). Bayesian Model Averaging: A
Tutorial. Statistical Science, 14(4), 382-401. Retrieved December 12, 2020, from
http://www.jstor.org/stable/2676803
[6] A. Arribas, P. Palmqvist. “On the ecological connection between sabre-tooths and hominids: faunal
dispersal events in the Lower Pleistocene and a review of the evidence for the first human arrival in
Europe.” J. Archaeol. Sci., 26 (1999), pp. 571-585
[7] Krause, J.; Fu, Q.; Good, J. M.; Viola, B.; Shunkov, M. V.; Derevianko, A. P. & Pääbo,
S. (2010). "The complete mitochondrial DNA genome of an unknown hominin from southern
Siberia". Nature. 464(7290): 894–897
