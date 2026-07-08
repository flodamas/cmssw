from CRABClient.UserUtilities import config
from CRABClient.UserUtilities import getUsername
username = getUsername()

###############################################################################
# INPUT/OUTPUT SETTINGS

jobTag = 'IonPhysics2'
input = '/IonPhysics2/OORun2025-PromptReco-v1/MINIAOD'
inputDatabase = 'global'
#inputDatabase = 'phys03'
output = '/store/group/phys_heavyions/' + username + '/LightIon2025/OO/ForestTest/'
outputServer = 'T2_CH_CERN'

###############################################################################

config = config()

config.General.requestName = jobTag
config.General.workArea = 'CrabWorkArea'
config.General.transferOutputs = True

config.JobType.psetName = 'forest_OO_Data.py'
config.JobType.pluginName = 'Analysis'
config.JobType.maxMemoryMB = 2000
config.JobType.pyCfgParams = [ 'noprint' ]
config.JobType.allowUndistributedCMSSW = True
config.JobType.maxJobRuntimeMin = 200

config.Data.inputDataset = input
config.Data.inputDBS = inputDatabase
config.Data.outLFNDirBase = output
config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 1000000
config.Data.totalUnits = -1
config.Data.publication = False
config.Data.allowNonValidInputDataset = True

config.Data.runRange = '394153-394217'
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions25OO/Cert_Collisions2025OO_394153_394217_golden.json'

config.Site.storageSite = outputServer
