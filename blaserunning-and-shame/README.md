**DRAFT**

# Effects of the "Blaserunning" decree on shame

[Society for Internet Blaseball Research](https://github.com/Society-for-Internet-Blaseball-Research)

Authors: iliana etaoin (she/her)

**Abstract**: We consider whether the "Blaserunning" decree in the ILB Season 3 election, which awards 0.1 runs for a team that successfully steals a base, impacts the number of games resulting in shame.
We apply this rule to past games and find a 21.6% decrease in games where the away team is shamed.

## Shame and Blaserunning

In [blaseball](https://blaseball.com), the *shame phase* was the first major difference between its ruleset and baseball's.
The [Blaseball Official Rulebook](https://blaseball.com/thebook) (It is Forbidden) defines it:

> Shame Phase: If the home team scores the winning run in the bottom of the final inning, the away team must complete the game in shame, despite being mathematically eliminated.

For example, if the Magic is playing at the Tacos, and the score is tied entering the bottom of the 9th inning, the Tacos can win the game by scoring a run, thus shaming the Magic.
This is different from baseball, where scoring a run results in a walk-off win; instead, the game finishes when three outs are earned.

ILB voters may vote for "Blaserunning" in the Season 3 election, described simply as "Stolen Bases are worth 0.1 Runs".
There is some margin for misunderstanding here: will the scoreboard¹ actually show decimal values for runs? Or does an extra integer run get added when a team reaches 10 steals?
However, we choose to interpret this proposed rule as introducing fractional runs to the league.

In order to help determine the impact of "excitement" this proposed rule change introduces to the league, we analyze its impact on shame.
Shame is a uniquely exciting part of blaseball's rules: #watchparty on the official Discord becomes extremely active when a team is shamed.

¹: This research does not discuss implications for stadium scoreboard operators.

## Methodology and results

Our sample consists of 982 game logs where the last out is present.
Logs start in the middle of Season 2, and a number of games have incomplete logs due to various issues.

On that sample, we looked for stolen bases, re-scored games, and determined whether those games ended in shame.
The code for this research can be found in [shame.py](./shame.py), and source data can be found in `blaseball-archive-iliana.s3.us-west-2.amazonaws.com` (accessible via an S3 client; log timestamps 1596003134151 through 1596605456865).

In this sample, 97 games (9.9%) resulted in shame under their original rule sets.
Under new rules, 76 games (7.8%) resulted in shame; 25 games that originally resulted in shame no longer did, and 4 games now ended in shame that originally did not.
The re-scored games are in Table 1.

**Table 1 data in table1.csv**

Out of the 25 affected games, 13 resulted in a new team winning, with 7 of those in the latter half of Season 2 where data is available.
Retabulating Season 2 results with these changes (see Table 2), the Breckenridge Jazz Hands would have been awarded the third seed in the Evil League instead of the Canada Moist Talkers.
This change is likely moot, as both already faced the Philly Pies in the playoffs and lost.

**Table 2 data in table2.csv**

## Analysis

The shame phase is popular among ILB viewers, and the proposed Blaserunning decree reduces the number of games resulting in shame in our sample by 21.6%.
SIBR does not endorse voting for or against specific decrees, as that is up to the individual votes -- but we find its proposed value to add excitement to games misguided².

²: The commissioner is doing a great job.
