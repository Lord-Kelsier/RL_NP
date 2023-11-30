import numpy as np
import json
import os
from Params import FOLDERRANDOM as FOLDER, AuAtoms, EPSILON
import time
import ase
Molecule = "Au7Ag6"
def randomPolicy(observation):
  # para Au7Ag6
  AuAtms = 7
  AgAtoms = 6
  AuPos = 1.0 # pos in [Au,Ag,C,H,O,Cu,Al] + 1
  AgPos = 2.0
  for i, obs in enumerate(observation[0]):
    if obs[0] == ase.data.atomic_numbers["Au"]:
      AuAtms -= 1
    elif obs[0] == ase.data.atomic_numbers["Ag"]:
      AgAtoms -= 1
    if i == 0: continue
    if obs[1][0] == 0.0 and obs[1][1] == 0.0 and obs[1][2] == 0.0:
      break
  totalAtoms = AuAtms + AgAtoms
  stop = 0.0
  focus = np.random.choice([e for e in range(i )])
  element = np.random.choice([AuPos, AgPos], 1, p=[AuAtms/totalAtoms, AgAtoms/totalAtoms])[0]
  distance = np.random.normal(2.75, 0.8)
  angle = np.random.uniform(0.0, np.pi)
  dihedral = np.random.uniform(0, np.pi)
  kappa = np.random.choice([-1, 1])
  out =  np.array([stop, focus, element, distance, angle, dihedral, kappa])
  return out

def checkFiles():
  def createFile():
    with open(f"{FOLDER}/{Molecule}-epsilon={EPSILON}.json", "w") as f:
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
  if f"{Molecule}-epsilon={EPSILON}.json" not in os.listdir(FOLDER):
    createFile()
  
def saveMaxReward(reward, observation, step):
  checkFiles()
  if observation[0][-1][0] == 0:
    return
  with open(f"{FOLDER}/{Molecule}-epsilon={EPSILON}.json", "r") as f:
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
  with open(f"{FOLDER}/{Molecule}-epsilon={EPSILON}.json", "w") as f:
    json.dump(MaxReward, f)