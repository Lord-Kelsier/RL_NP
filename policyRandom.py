import numpy as np
def randomPolicy(observation):
  for i, obs in enumerate(observation[0]):
    if i == 0: continue
    if obs[1][0] == 0.0 and obs[1][1] == 0.0 and obs[1][2] == 0.0:
      break
  stop = 0.0
  focus = np.random.choice([e for e in range(i )])
  element = 1.0
  distance = np.random.normal(2.75, 0.5)
  angle = np.random.uniform(0.0, np.pi)
  dihedral = np.random.uniform(0, np.pi)
  kappa = np.random.choice([-1, 1])
  out =  np.array([stop, focus, element, distance, angle, dihedral, kappa])
  return out