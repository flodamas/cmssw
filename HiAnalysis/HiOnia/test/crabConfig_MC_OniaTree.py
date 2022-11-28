from WMCore.Configuration import Configuration

config = Configuration()

config.section_("General")
config.General.requestName = "Run3embeddedJpsi_12_3_0"
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_("JobType")
config.JobType.pluginName = "Analysis"
config.JobType.psetName = "hioniaanalyzer_PbPbPrompt_muonMVA_12_3_X_MC_cfg.py"
#config.JobType.maxMemoryMB = 2500         # request high memory machines.
#config.JobType.numCores = 4
config.JobType.allowUndistributedCMSSW = True #Problems with slc7
#config.JobType.maxJobRuntimeMin = 1000 #2750    # request longer runtime, ~48 hours.

config.section_("Data")
config.Data.inputDataset = '/HIN-HINPbPbAutumn18GSHIMix-00008_pTHatMin2_EMB_CMSSW_12_3_0/soohwan-RECO_MC_JPsiEMB_pTHatMin2_CMSSW_12_3_0_220530_v1-1053bdd6c72aaff65c2568bf089c019a/USER'
config.Data.inputDBS = 'phys03'
config.Data.unitsPerJob = 1000
#config.Data.totalUnits = -1
config.Data.splitting = "FileBased" #"Automatic"
config.Data.allowNonValidInputDataset = True

config.Data.outLFNDirBase = '/store/user/fdamas/2022DileptonRunPrep/JPsi_pThat-2_TuneCP5_HydjetDrumMB_5p02TeV_Pythia8/%s' % (config.General.requestName)
config.Data.publication = False
#config.Data.runRange = '327237-327237'#'327123-327564'#'326381-327122' or 326382 or 327564
#config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/HI/PromptReco/Cert_326381-327564_HI_PromptReco_Collisions18_JSON_HF_and_MuonPhys.txt'

config.section_("Site")
config.Site.storageSite = "T2_FR_GRIF_LLR"
#config.Site.whitelist = ["T2_CH_CERN"]
