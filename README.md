# Smart Traffic Light Optimizer

A 4-way intersection where cars arrive randomly. It runs two traffic lights side
by side so you can compare them:

- **fixed timer** – switches every X seconds no matter what (the dumb way)
- **AI adaptive** – watches how many cars are waiting in each direction and
  gives green to whichever side has the longest queue

Watch the "cars through" counters: the adaptive light clears traffic noticeably
faster because it reacts to the actual demand.

## run

```bash
pip install pygame
python sim.py
```

tags: ai, optimization, smart-city, traffic, simulation, pygame

simple idea - give green to whoever's busiest - but it really does beat a fixed timer.
