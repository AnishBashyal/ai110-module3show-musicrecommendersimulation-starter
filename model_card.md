# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

The biggest weakness I found is that energy gives points to every song, even when genre and mood dont match. Gym Hero (intense pop) showed up in the top 5 for 5 out of 6 test profiles, and it still did when I turned genre off completely, so the genre weight wasnt the problem. Most of my test profiles want high energy and Gym Hero's energy is 0.93, so it always gets close to full energy points. The catalog is also small (12 of 15 genres have only one song), so after the one matching song theres not much else to pick from. This means a few high energy songs end up in front of lots of different users, which is like a mini filter bubble.

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
