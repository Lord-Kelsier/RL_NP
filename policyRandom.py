import numpy as np
import json
import os
from Params import FOLDERRANDOM as FOLDER, AuAtoms, EPSILON
import time
def randomPolicy(observation):
  for i, obs in enumerate(observation[0]):
    if i == 0: continue
    if obs[1][0] == 0.0 and obs[1][1] == 0.0 and obs[1][2] == 0.0:
      break
  stop = 0.0
  focus = np.random.choice([e for e in range(i )])
  element = 1.0
  distance = np.random.normal(2.75, 0.8)
  angle = np.random.uniform(0.0, np.pi)
  dihedral = np.random.uniform(0, np.pi)
  kappa = np.random.choice([-1, 1])
  out =  np.array([stop, focus, element, distance, angle, dihedral, kappa])
  return out

def checkFiles():
  def createFile():
    with open(f"{FOLDER}/Au7Ag6-epsilon={EPSILON}.json", "w") as f:
      MaxReward = {
        "reward": None,
        "positions": None,
        "time": time.time(),
        "step": None,
        "olderCandidates": []
      }
      json.dump(MaxReward, f)
  if FOLDER not in os.listdir():
    os.mkdir(FOLDER)
  if f"Au7Ag6-epsilon={EPSILON}.json" not in os.listdir(FOLDER):
    createFile()
  
def saveMaxReward(reward, observation, step):
  checkFiles()
  if observation[0][-1][0] == 0:
    return
  with open(f"{FOLDER}/Au7Ag6-epsilon={EPSILON}.json", "r") as f:
    MaxReward = json.load(f)
  isUpdating = False
  if MaxReward["reward"] == None: 
    isUpdating = True
  elif reward > MaxReward["reward"]:
    isUpdating = True
  if isUpdating:
    MaxReward["olderCandidates"].append({
      "positions": MaxReward["positions"],
      "reward": MaxReward["reward"],
      "time": MaxReward["time"],
      "step": MaxReward["step"]
      })
    MaxReward["reward"] = reward
    MaxReward["positions"] = observation[0]
    MaxReward["time"] = time.time()
    MaxReward["step"] = step
  with open(f"{FOLDER}/Au7Ag6-epsilon={EPSILON}.json", "w") as f:
    json.dump(MaxReward, f)