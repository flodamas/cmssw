### HiForest CMSSW Configuration
# Collisions: Oxygen-Oxygen
# Input: miniAOD
# Type: data

import FWCore.ParameterSet.Config as cms
from Configuration.Eras.Era_Run3_2025_OXY_cff import Run3_2025_OXY
process = cms.Process('HiForest', Run3_2025_OXY)

###############################################################################

# HiForest info
process.load("HeavyIonsAnalysis.EventAnalysis.HiForestInfo_cfi")
process.HiForestInfo.info = cms.vstring("HiForest, miniAOD, 150X, data")

# import subprocess, os
# version = subprocess.check_output(
#     ['git', '-C', os.path.expandvars('$CMSSW_BASE/src'), 'describe', '--tags'])
# if version == '':
#     version = 'no git info'
# process.HiForestInfo.HiForestVersion = cms.string(version)

###############################################################################

# input files
process.source = cms.Source("PoolSource",
    duplicateCheckMode = cms.untracked.string("noDuplicateCheck"),
    fileNames = cms.untracked.vstring(
         '/store/hidata/OORun2025/IonPhysics0/MINIAOD/PromptReco-v1/000/394/184/00000/c5d44688-20b6-45eb-8aa6-5f1816a02e67.root'
    ),
)

# number of events to process, set to -1 to process all events
process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

###############################################################################

# load Global Tag, geometry, etc.
process.load('Configuration.Geometry.GeometryDB_cff')
process.load('Configuration.StandardSequences.Services_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '150X_dataRun3_Prompt_v3', '')
process.HiForestInfo.GlobalTagLabel = process.GlobalTag.globaltag

###############################################################################

# Define centrality binning
process.load("RecoHI.HiCentralityAlgos.CentralityBin_cfi")
process.centralityBin.Centrality = cms.InputTag("hiCentrality")
process.centralityBin.centralityVariable = cms.string("HFtowers")

###############################################################################

# root output
process.TFileService = cms.Service("TFileService",
    fileName = cms.string("HiForest151X_OOdata.root"))

# # edm output for debugging purposes
# process.output = cms.OutputModule(
#     "PoolOutputModule",
#     fileName = cms.untracked.string('HiForestEDM.root'),
#     outputCommands = cms.untracked.vstring(
#         'keep *',
#     )
# )

# process.output_path = cms.EndPath(process.output)

###############################################################################

# event analysis
process.load('HeavyIonsAnalysis.EventAnalysis.hltanalysis_cfi')

process.load('L1Trigger.L1TNtuples.l1MetFilterRecoTree_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.particleFlowAnalyser_cfi')
process.particleFlowAnalyser.ptMin = cms.double(0.01)
process.particleFlowAnalyser.absEtaMax = cms.double(6.0)
process.load('HeavyIonsAnalysis.EventAnalysis.hievtanalyzer_data_cfi')
process.hiEvtAnalyzer.doHFfilters = cms.bool(False)
process.hiEvtAnalyzer.Vertex = cms.InputTag("offlineSlimmedPrimaryVertices")
process.hiEvtAnalyzer.doCentrality = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlane = cms.bool(False)
process.hiEvtAnalyzer.doEvtPlaneFlat = cms.bool(False)
process.hiEvtAnalyzer.doVertex = cms.bool(False)

process.load('HeavyIonsAnalysis.EventAnalysis.skimanalysis_cfi')
process.load('HeavyIonsAnalysis.EventAnalysis.hltobject_cfi')
process.hltobject.triggerNames = cms.vstring()
process.load('HeavyIonsAnalysis.EventAnalysis.l1object_cfi')
process.load("TrackingTools.TransientTrack.TransientTrackBuilder_cfi")
################################
# jet reco sequence
#process.load('HeavyIonsAnalysis.JetAnalysis.ak4PFJetSequence_ppref_data_cff')
################################
# tracks
process.load("HeavyIonsAnalysis.TrackAnalysis.TrackAnalyzers_cff")
#process.ppTracks.trackSrc = cms.InputTag("generalTracks")
process.ppTracks.dedxEstimators = cms.VInputTag(["dedxEstimator:dedxAllLikelihood", "dedxEstimator:dedxPixelLikelihood", "dedxEstimator:dedxStripLikelihood"])
process.ppTracks.trackEtaMax = cms.untracked.double(2.5)
process.ppTracks.trackPtMin = cms.untracked.double(0.195)
process.ppTracks.applyTrackSelections = cms.untracked.bool(True)


###############################################################################
# main forest sequence
process.forest = cms.Path(
    #process.HiForestInfo +
    process.centralityBin +
    #process.hltanalysis +
#    process.hltobject +
    #process.l1object +
 #   process.l1MetFilterRecoTree +
    process.trackSequencePP +
    #process.particleFlowAnalyser +
    process.hiEvtAnalyzer
)


#########################
# Event Selection -> add the needed filters here
#########################

process.load('HeavyIonsAnalysis.EventAnalysis.collisionEventSelection_cff')
process.pclusterCompatibilityFilter = cms.Path(process.clusterCompatibilityFilter)
process.pprimaryVertexFilter = cms.Path(process.primaryVertexFilter)
process.load('HeavyIonsAnalysis.EventAnalysis.hffilterPF_cfi')
process.pAna = cms.EndPath(process.skimanalysis)

from HLTrigger.HLTfilters.hltHighLevel_cfi import hltHighLevel
process.hltFilter = hltHighLevel.clone(
    HLTPaths = [
        #"HLT_HIZeroBias_v4",                                                     
        "HLT_MinimumBiasHF_OR_BptxAND_v1",
    ]
)

#from HeavyIonsAnalysis.TrackAnalysis.unpackedTracksAndVertices_cfi import *
#process.unpackedTracksAndVertices = unpackedTracksAndVertices
process.load('HeavyIonsAnalysis.VertexAnalysis.pileupvertexfilter_cfi')
process.pileupvertexfilter.doOO = True
process.pileupvertexfilter.doNeNe = False


process.filterSequence = cms.Sequence(
    process.hltFilter *
    process.primaryVertexFilter *
    process.unpackedTracksAndVertices *
    process.pileupvertexfilter
    #process.clusterCompatibilityFilter
)

process.superFilterPath = cms.Path(process.filterSequence)
process.skimanalysis.superFilters = cms.vstring("superFilterPath")
#
for path in process.paths:
    getattr(process, path)._seq = process.filterSequence * getattr(process,path)._seq

process.options   = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
