import numpy as np
import json
import os
import time
from Params import FOLDERRANDOM as FOLDER, AuAtoms, EPSILON
def randomPolicy(observation, randomParams):
  for i, obs in enumerate(observation[0]):
    if obs[0] == 0: break
  
  stop = 0.0
  element = 1.0
  if randomParams == None:
    if i == 0: 
      focus = 0
    else:
      focus = np.random.choice([e for e in range(i )])
    distance = np.random.normal(2.75, 0.5)# 0.15 normal scale
    angle = np.random.uniform(0.0, np.pi) # 0.25 normal scale
    dihedral = np.random.uniform(0, np.pi) # 0.25 normal scale
  else:
    focus = randomParams['focus'][i]
    distance = np.random.normal(randomParams['distanceMean'][i], 0.15)
    angle = np.random.normal(randomParams['angleMean'][i], 0.25)
    dihedral = np.random.normal(randomParams['dihedralMean'][i], 0.25)
  kappa = np.random.choice([-1, 1])
  out =  np.array([stop, focus, element, distance, angle, dihedral, kappa])
  return out

def checkFiles():
  def createFile():
    with open(f"{FOLDER}/Au7Ag6-epsilon={EPSILON}-GreedyRandom.json", "w") as f:
      MaxReward = {
        "reward": None,
        "positions": None,
        "params": None,
        "time": time.time(),
        "oldersCandidates": {
          "reward": [],
          "positions": [],
          "time": []
        },
      }
      json.dump(MaxReward, f)
  if FOLDER not in os.listdir():
    os.mkdir(FOLDER)
  if f"Au7Ag6-epsilon={EPSILON}-GreedyRandom.json" not in os.listdir(FOLDER):
    createFile()
  
def saveMaxReward(reward, observation, actionsDone):
  checkFiles()
  if observation[0][-1][0] == 0:
    return
  with open(f"{FOLDER}/Au7Ag6-epsilon={EPSILON}-GreedyRandom.json", "r") as f:
    MaxReward = json.load(f)
  isUpdating = False
  newParams = None
  if MaxReward["reward"] == None: 
    isUpdating = True
  elif reward > MaxReward["reward"]:
    isUpdating = True
  if isUpdating:
    # MaxReward["olderCandidates"].append({
    #   "positions": MaxReward["positions"],
    #   "reward": MaxReward["reward"]
    #   })
    MaxReward["oldersCandidates"]["positions"].append(MaxReward["positions"])
    MaxReward["oldersCandidates"]["reward"].append(MaxReward["reward"])
    MaxReward["oldersCandidates"]["time"].append(MaxReward["time"])
    MaxReward["reward"] = reward
    MaxReward["positions"] = observation[0]
    MaxReward["time"] = time.time()
    stops, focuses, elements, distances, angles, dihedrals, kappas = zip(*actionsDone)
    newParams = {
      "focus": focuses,
      "distanceMean": distances,
      "angleMean": angles,
      "dihedralMean": dihedrals
    }
    MaxReward["params"] = newParams

  with open(f"{FOLDER}/Au7Ag6-epsilon={EPSILON}-GreedyRandom.json", "w") as f:
    json.dump(MaxReward, f)
  return newParams
