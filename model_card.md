# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**TasteMatch 1.0**

---

## 2. Intended Use  

**Goal / Task:** TasteMatch tries to suggest the top 5 songs from a small catalog that best fit one user's taste. It gives each song a score and a reason, then ranks them.

**Intended use:** classroom project to learn how a simple recommender turns data into suggestions. It assumes the user can describe their taste with one favorite genre, one mood, an energy level, and whether they like acoustic music.

**Not intended for:** real users or a real music app. It only knows 18 songs, it cant learn from what people actually listen to, and it shouldnt be used to decide what real artists get heard.

---

## 3. How the Model Works  

Every song gets points, then the songs are sorted from highest to lowest and the top 5 are shown.

- Genre matches the user's favorite: +2.0
- Mood matches: +1.0
- Energy is close to what the user wants: up to +1.0 (closer = more points)
- Acousticness fits what the user likes: up to +0.5

The best possible score is 4.5. Each song also shows its reasons, like "genre match (+2.0)", so you can see why it was picked. I changed the starter code by adding all of this, since the starter had no scoring at all.

---

## 4. Data  

- 18 songs in data/songs.csv (10 from the starter, 8 I added).
- Each song has genre, mood, energy, tempo, valence, danceability and acousticness. Only genre, mood, energy and acousticness are used for scoring.
- 15 genres and 14 moods, but 13 of the 15 genres have only one song. Lofi has 3.
- Missing: lyrics, language, artist popularity, decade, and what other people listen to. The data is made up, so it doesnt reflect real music taste.

---

## 5. Strengths  

- It works well when the user's genre and mood are in the catalog. Chill Lofi matched my gut feeling, and Deep Intense Rock got the right #1 (Storm Runner), though the #2 pick was off.
- The reasons make it easy to see why a song ranked where it did.
- Different profiles got clearly different lists, for example loud pop vs quiet lofi had no songs in common.

---

## 6. Limitations and Bias 

The biggest weakness I found is that energy gives points to every song, even when genre and mood dont match. Gym Hero (intense pop) showed up in the top 5 for 5 out of 6 test profiles, and it still did when I turned genre off completely, so the genre weight wasnt the problem. Most of my test profiles want high energy and Gym Hero's energy is 0.93, so it usually gets close to full energy points. The catalog is also small (13 of 15 genres have only one song), so after the one matching song theres not much else to pick from. This means a few high energy songs end up in front of lots of different users, which is like a mini filter bubble.

---

## 7. Evaluation  

**Profiles I tested** (top 5 for each is in the README under Profile Test Outputs):

- High-Energy Pop (pop, happy, 0.8)
- Chill Lofi (lofi, chill, 0.35, likes acoustic)
- Deep Intense Rock (rock, intense, 0.92)
- Sad but Energetic (pop, sad, 0.9) - made to trick it
- Unknown Genre / k-pop (k-pop, happy, 0.8) - made to trick it
- Conflicting Taste (classical, aggressive, 0.95, likes acoustic) - made to trick it

I also ran one experiment: energy x2 and genre x0.5 (details in the README). It mostly just changed the order, it didnt make things more accurate.

**What surprised me:**

- Gym Hero showed up in 5 out of 6 lists, even when I turned genre off.
- "sad" isnt a mood in my songs, so the system just ignored it and didnt say anything.
- The Conflicting Taste user wants energy 0.95 but the #1 song is a quiet classical piece (energy 0.18), because genre and acoustic points beat the energy points.
- Gym Hero (pop) came before Iron Requiem (metal) for the rock profile, because "intense" matched exactly and "aggressive" didnt.

**Why Gym Hero keeps showing up for Happy Pop (plain version):**
The system doesnt hear any music. It just gives points for matching labels and numbers. Gym Hero is labeled pop, so it gets the genre points, and its energy is really high so it is close to what a happy pop fan wants. The only thing it misses is the mood, because its mood is "intense" and not "happy". So it loses one point but still beats almost everything else. It's not that the system thinks Gym Hero is happy, it just doesnt have many other pop songs to pick from.

**Comparing each pair of profiles:**

1. Pop vs Lofi: no songs in common. Pop gets loud electronic songs, lofi gets quiet acoustic ones. Makes sense, their energy and acoustic wishes are opposite.
2. Pop vs Rock: same three songs show up (Sunrise City, Gym Hero, Storm Runner) but in a different order. Pop's #1 is Sunrise City (genre + mood), rock's #1 is Storm Runner. Genre and mood pick the #1, energy fills the rest.
3. Pop vs Sad: same genre, but nothing matches "sad". Sunrise City loses its mood point so Gym Hero (energy closer to 0.9) takes #1. Shows how much that one mood point was holding Sunrise City up.
4. Pop vs k-pop: same mood and energy, but nobody is k-pop. Sunrise City stays #1 on mood, but Gym Hero falls from #2 to #4 since it lost the genre points.
5. Pop vs Conflicting: only Gym Hero and Storm Runner overlap. Conflicting puts classical and metal on top because its genre, mood and energy all point at different songs.
6. Lofi vs Rock: total opposites, no overlap. Quiet and acoustic vs loud and intense, as expected.
7. Lofi vs Sad: no overlap. Same reason, low energy acoustic songs vs high energy ones.
8. Lofi vs k-pop: no overlap. Lofi gets chill songs, k-pop gets happy upbeat ones.
9. Lofi vs Conflicting: no overlap even though both like acoustic. Conflicting wants energy 0.95 so it still gets loud songs after the quiet classical one.
10. Rock vs Sad: the exact same 5 songs in a different order. Both want really high energy, so the pop vs rock genre only reshuffles them.
11. Rock vs k-pop: rock #1 is Storm Runner (intense), k-pop #1 is Sunrise City (happy). Mood is what separates them, since energy is similar.
12. Rock vs Conflicting: both want very high energy so 4 songs overlap. Conflicting adds the classical song on top and Iron Requiem moves up to #2 because its mood is aggressive.
13. Sad vs k-pop: Sunrise City is in both. Sad has Gym Hero #1 (pop + higher energy), k-pop has Sunrise City #1 because "happy" matches. Makes sense.
14. Sad vs Conflicting: both want high energy, but Sad stays with loud songs while Conflicting puts a quiet classical song first. Shows that genre (+ acoustic) can beat energy.
15. k-pop vs Conflicting: k-pop never gets a genre point so it falls back to happy upbeat songs. Conflicting does get genre and mood matches, but for totally different songs, so its list is a weird mix.

---

## 8. Future Work  

- Let the user pick several genres and moods, not just one.
- Count close moods as partly matching ("intense" and "aggressive"), so the metal song isnt beaten by a pop song.
- Add a rule to mix up the top 5 (for example, not too many songs by the same artist or genre) and add more songs per genre.

---

## 9. Personal Reflection  

**Biggest learning moment:** The data limits the system a lot. My scoring rules were simple, but with only 18 songs (and 13 of 15 genres having just one song) there werent many real choices, so the same few songs kept showing up. Gym Hero was in 5 out of 6 lists even when I turned genre off. A better formula wouldnt fix that, I would need more songs.

**How AI helped, and when I double-checked it:** AI helped me build each step fast, like the scoring code, the test profiles and writing up the results. But I had to double-check it when it mixed up numbers and versions. It told me Gym Hero was in the top 2 for 4 profiles when it was really 3, and it mixed results from the experiment weights with the original weights. I asked it to redo the analysis and say which version each number came from, and the corrected numbers are the ones in my model card.

**What surprised me:** Just adding up points felt like a real recommender. Chill Lofi gave three lofi songs, then ambient and jazz, and that matched what I would expect. It is only genre, mood, energy and acousticness, but the reasons next to each song made it feel like it understood the taste.

**What I would try next:** Let a user pick more than one genre and mood, and add a rule that mixes up the top 5 so it doesnt repeat the same artist or genre too much. After that I would add more songs per genre.
