from CRABAPI.RawCommand import crabCommand
from CRABClient.ClientExceptions import ClientException
from http.client import HTTPException

# We want to put all the CRAB project directories from the tasks we submit here into one common directory.
# That's why we need to set this parameter (here or above in the configuration file, it does not matter, we will not overwrite it).
from CRABClient.UserUtilities import config
config = config()

output = '/store/group/phys_heavyions/' + username + '/PbPb2024/' + collisionSystem + '/Forest/'
outputServer = 'T2_CH_CERN'

config.section_("General")
#config.General.requestName = "HIPhysicsRawPrime5_PromptReco_v2"
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "forest_PbPb2024_Data.py"
config.JobType.maxMemoryMB = 2400         # request high memory machines.
#config.JobType.numCores = 4
config.JobType.allowUndistributedCMSSW = True #Problems with slc7
#config.JobType.maxJobRuntimeMin = 2000 # max = 2750

config.section_("Data")
config.Data.inputDBS = 'global'
#config.Data.totalUnits = -1
config.Data.splitting = "EventAwareLumiBased"
config.Data.unitsPerJob = 1000000

config.Data.allowNonValidInputDataset = True
config.Data.publication = False
config.Data.runRange = '387853-388784'
config.Data.lumiMask = 'https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions24HI/Cert_Collisions2024_HI_387853_388784_Golden.json'


config.section_("Site")
config.Site.storageSite = outputServer
#config.Site.whitelist = ["T2_US_*","T2_CH_CERN","T1_US_*"]

# Multi crab part

def submit(config):
    try:
        crabCommand('submit', config = config, dryrun=False)
    except HTTPException as hte:
        print("Failed submitting task: %s" % (hte.headers))
    except ClientException as cle:
        print("Failed submitting task: %s" % (cle))



### HIRun2024B was completely reconstructed promptly, but there are two independent versions

for i in range(60):

    config.General.requestName = f'PbPb24_RawPrime{i}'
    config.Data.inputDataset = f"/HIPhysicsRawPrime{i}/HIRun2024B-PromptReco-v2/MINIAOD"
    config.Data.outputDatasetTag = config.General.requestName

    print("Submitting CRAB job for: "+ config.Data.inputDataset)
    submit(config)