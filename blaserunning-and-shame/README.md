**DRAFT**

# Effects of the "Blaserunning" decree on shame

[Society for Internet Blaseball Research](https://github.com/Society-for-Internet-Blaseball-Research)

Authors: iliana etaoin (she/her)

**Abstract**: We consider whether the "Blaserunning" decree in the ILB Season 3 election, which awards 0.1 runs for a team that successfully steals a base, impacts the number of games resulting in shame.
We apply this rule to past games and find a 21.6% decrease in games where the away team is shamed.

## Shame and Blaserunning

In [blaseball](https://blaseball.com), the *shame phase* was the first major difference between its ruleset and that of reality league baseball.
The [Blaseball Official Rulebook](https://blaseball.com/thebook)[1] defines it:

> Shame Phase: If the home team scores the winning run in the bottom of the final inning, the away team must complete the game in shame, despite being mathematically eliminated.

For example, if the Magic is playing at the Tacos and the score is tied entering the bottom of the 9th inning, the Tacos can win the game by scoring a run, thus shaming the Magic.
This is different from reality league baseball, where scoring a run results in a walk-off win; instead, the game finishes when three outs are earned.

ILB voters may vote for "Blaserunning" in the Season 3 election, described simply as "Stolen Bases are worth 0.1 Runs".
There is some margin for misunderstanding here: will the scoreboard[2] actually show decimal values for runs? Or does an extra integer run get added when a team reaches 10 steals? For this analysis, we choose to interpret this proposed rule as introducing fractional runs to the league.

In order to help determine the impact of "excitement" that this proposed rule change introduces to the league, we analyze its impact on shame.
Shame is a uniquely exciting part of blaseball's rules: #watchparty on the official Discord becomes extremely active when a team is shamed.

[1]: It is Forbidden.

[2]: This research does not discuss implications for stadium scoreboard operators.

## Methodology and results

Our sample consists of 982 game logs where the last out is present.
Logs start in the middle of Season 2, and a number of games have incomplete logs due to various issues.[3]

In the sample, we searched for stolen bases and re-scored games, then determine whether those games ended in shame.
The code for this research can be found in [shame.py](./shame.py), and source data can be found in 
`blaseball-archive-iliana.s3.us-west-2.amazonaws.com` (accessible via an S3 client; log timestamps 1596003134151 through 1596605456865).

In this sample, 97 games (9.9%) resulted in shame under their original rule sets.
Under "Enhanced Shame", 76 games (7.8%) resulted in shame; 25 games that originally resulted in shame no longer did so; and 4 games ended in shame that originally did not. Refer to Table 1 for the re-scored games.

**Table 1 data in table1.csv**

Out of the 25 affected games, 13 results in a new team winning. Of those, seven occurred in the latter half of Season 2 (where data is available).
After retabulating Season 2 results with these changes (see Table 2), we find that the Breckenridge Jazz Hands would have been awarded the third seed in the Evil League instead of the Canada Moist Talkers.
This change is likely moot, as both ultimately faced the Philly Pies in the playoffs and lost.
This retabulation however does *not* take into account games that originally ended in shame and still ended in shame, or games that originally did not end in shame and still did not end in shame, where the result was reversed by the decree.

**Table 2 data in table2.csv**

## Analysis

The shame phase is popular among ILB viewers, and the proposed Blaserunning decree reduces the number of games resulting in shame in our sample by 21.6%.
SIBR does not endorse voting for or against specific decrees, as that is up to the individual votes — but it is the opinion of the authors that its intended purpose to add excitement to games may be misguided[4].

[3]: Some data from Season 3 was lost due to siestas, blasphemy, and so, so many birds.

[4]: The commissioner is doing a great job.

## Future work

Future work could identify changes with the combination of Enhanced Shame, a [Season 2 decree](https://blaseball.fandom.com/wiki/Season_2#Decrees) that did not pass, with Blaserunning.

Researchers may also wish to perform a superior retabulation of the Season 2 standings with the Blaserunning rule applied to the latter half of the season for which we have data.
