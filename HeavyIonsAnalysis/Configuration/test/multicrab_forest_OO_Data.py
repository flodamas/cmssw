from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

# We want to put all the CRAB project directories from the tasks we submit here into one common directory.
# That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
from CRABClient.UserUtilities import config
config = config()

from CRABClient.UserUtilities import getUsername
username = getUsername()

###############################################################################
# INPUT/OUTPUT SETTINGS

collisionSystem = 'OO' # pO, OO, or NeNe

output = '/store/group/phys_heavyions/' + username + '/LightIon2025/' + collisionSystem + '/Forest/'
outputServer = 'T2_CH_CERN'

###############################################################################

config.General.workArea = 'CrabWorkArea'
config.General.transferOutputs = True

config.JobType.psetName = 'forest_OO_Data.py'
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 2000
config.JobType.pyCfgParams = [ 'noprint' ]
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 200

config.Data.outLFNDirBase = output
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 200000
config.Data.totalUnits = -1
config.Data.publication = False
config.Data.allowNonValidInputDataset = True

config.Site.storageSite = outputServer


# settings based on collision system name
if collisionSystem == 'pO':
    config.Data.runRange = '393952-394007'
    config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions25pO/pO_golden.json' # final muon json

elif collisionSystem == 'OO':
    config.Data.runRange = '394153-394217'
    config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions25OO/Cert_Collisions2025OO_394153_394217_golden.json'

elif collisionSystem == 'NeNe':
    config.Data.runRange = '394269-394272'
    config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions25NeNe/Cert_Collisions2025Nene_394269_394272_golden.json'

else:
    print("This config script does not support CRAB job submission for collision name: %s. Check the settings!" % (collisionSystem))

# Multi crab part

def submit(config):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))

# Submit the jobs: 60 IonPhysics PDs

for i in range(6):

    config.General.requestName = f'{collisionSystem}_IonPhysics{i}'
    config.Data.inputDataset = f"/IonPhysics{i}/{collisionSystem}Run2025-PromptReco-v1/MINIAOD"
    config.Data.outputDatasetTag = config.General.requestName

    print("Submitting CRAB job for: "+ config.Data.inputDataset)
    submit(config)
