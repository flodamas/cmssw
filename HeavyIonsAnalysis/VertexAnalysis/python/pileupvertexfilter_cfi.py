import FWCore.ParameterSet.Config as cms

#from HeavyIonsAnalysis.TrackAnalysis.unpackedTracksAndVertices_cfi import *
#process.unpackedTracksAndVertices = unpackedTracksAndVertices

pileupvertexfilter  = cms.EDFilter('PileUpVertexFilter',
    vertexSrc = cms.InputTag("unpackedTracksAndVertices"),
    doOO = cms.bool(True),
    doNeNe = cms.bool(False),
    surfaceCutParameters1OO = cms.vdouble(
       0.850271, 0.754963, 0.695127, 0.645343, 0.613325, 0.590003, 0.505241, 0.37611, 0.42144, 0.0500003
    ),
    surfaceCutParameters2OO = cms.vdouble(
       9.26551, 3.9179, 2.94908, 2.67405, 2.60579, 1.74096, 1.99159, 2.4446, 2.04628, 2.09011
    ),
    surfaceCutParameters1NeNe = cms.vdouble(
       0.864887, 0.759109, 0.69555, 0.646559, 0.615701, 0.576282, 0.508488, 0.49317, 0.375646, 0.05
    ),
    surfaceCutParameters2NeNe = cms.vdouble(
       8.52423, 3.6516, 2.76073, 2.60194, 2.25997, 2.07765, 2.32389, 1.5974, 1.66482, 2.27543
    )

)
