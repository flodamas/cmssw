import FWCore.ParameterSet.Config as cms

phfCoincFilterPF2Th4  = cms.EDFilter('HiHFFilterPF',
    pfCandidateSrc = cms.InputTag('packedPFCandidates'),
    threshold      = cms.double(4.),
    minnumtowers   = cms.int32(2)
)

phfCoincFilterPF1Th4 = phfCoincFilterPF2Th4.clone(minnumtowers = 1)

phfCoincFilterPF1Th3 = phfCoincFilterPF2Th4.clone(threshold = 3, minnumtowers = 1)
phfCoincFilterPF2Th3 = phfCoincFilterPF2Th4.clone(threshold = 3, minnumtowers = 2)

phfCoincFilterPF1Th5 = phfCoincFilterPF2Th4.clone(threshold = 5, minnumtowers = 1)
phfCoincFilterPF2Th5 = phfCoincFilterPF2Th4.clone(threshold = 5, minnumtowers = 2)

phfCoincFilterPF1Th13 = phfCoincFilterPF2Th4.clone(threshold = 13, minnumtowers = 1)


pphfCoincFilterPF1Th3 = cms.Path(phfCoincFilterPF1Th3)
pphfCoincFilterPF2Th3 = cms.Path(phfCoincFilterPF2Th3)
pphfCoincFilterPF1Th4 = cms.Path(phfCoincFilterPF1Th4)
pphfCoincFilterPF2Th4 = cms.Path(phfCoincFilterPF2Th4)
pphfCoincFilterPF1Th5 = cms.Path(phfCoincFilterPF1Th5)
pphfCoincFilterPF2Th5 = cms.Path(phfCoincFilterPF2Th5)
pphfCoincFilterPF1Th13 = cms.Path(phfCoincFilterPF1Th13)
