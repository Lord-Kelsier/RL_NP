import numpy as np
from policyRandom import randomPolicy
import os
import json
from Params import FOLDERGREEDY as FOLDER, AuAtoms, EPSILON

def checkFiles():
  def createFile():
    with open(f"{FOLDER}/Au{AuAtoms}-epsilon={EPSILON}.json", "w") as f:
      atoms = {i:{
        "reward": None,
        "action": None,
      } for i in range(AuAtoms)}
      json.dump(atoms, f)
  if FOLDER not in os.listdir():
    os.mkdir(FOLDER)
  if f"Au{AuAtoms}-epsilon={EPSILON}.json" not in os.listdir(FOLDER):
    createFile()


  


def udpateGreedyPolicy(reward, action, length):
  with open(f"{FOLDER}/Au{AuAtoms}-epsilon={EPSILON}.json", "r") as f:
    atoms = json.load(f)
  isUpdating = False
  if atoms[str(length)]["reward"] == None: 
    isUpdating = True
  elif reward > atoms[str(length)]["reward"]:
    isUpdating = True
  if isUpdating:
    atoms[str(length)]["reward"] = reward
    atoms[str(length)]["action"] = list(action)
  with open(f"{FOLDER}/Au{AuAtoms}-epsilon={EPSILON}.json", "w") as f:
    json.dump(atoms, f)
def getGreedyAction(obs, length):
  with open(f"{FOLDER}/Au{AuAtoms}-epsilon={EPSILON}.json", "r") as f:
    atoms = json.load(f)
  if atoms[str(length)]["reward"] == None:
    return randomPolicy(obs)
  else:
    return np.array(atoms[str(length)]["action"])
def greedyPolicy(observation):
  checkFiles()
  length = 0
  for obs in observation[0]:
    if obs[0] == 0:
      break
    length += 1
  if np.random.uniform(0, 1) < EPSILON:
    return randomPolicy(observation), length
  else:
    return getGreedyAction(observation, length), length
