import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATLayer0Summary')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATLayer0Summary = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# source
process.source = cms.Source("PoolSource", 
     fileNames = cms.untracked.vstring('file:/data/top/sckao/pythiaWJets/FASTFILE')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )


process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('IDEAL_V9::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")
#process.load("PhysicsTools.PatAlgos.famos.aodWithFamos_cff")
#process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.p = cms.Path(
                #process.patExtraOn200FastSim +       # extra reco on 20X Fast AODSIM
                #process.content             +       # to get a dump of the event content
                process.patLayer0_withoutTrigMatch + # PAT Layer 0, no trigger matching
                #process.patLayer0 +  # PAT Layer 0, no trigger matching
                process.patLayer1                    # PAT Layer 1
            )

#from PhysicsTools.PatAlgos.famos import patLayer0_FamosSetup_cff, patLayer1_FamosSetup_cff
#patLayer0_FamosSetup_cff.setup(process) # apply 'replace' statements for Layer 0
#patLayer1_FamosSetup_cff.setup(process) # apply 'replace' statements for Layer 1
# fix the pythia objects

# turn off the trigger - only for no trigger studies
process.allLayer1Muons.addTrigMatch = cms.bool(False)
process.allLayer1Electrons.addTrigMatch = cms.bool(False)
process.allLayer1Taus.addTrigMatch = cms.bool(False)
process.allLayer1METs.addTrigMatch = cms.bool(False)
process.allLayer1Jets.addTrigMatch = cms.bool(False)
process.allLayer1Photons.addTrigMatch = cms.bool(False)

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('/data/top/sckao/PythiaWJetsPAT/PATFILE'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")
process.out.outputCommands.extend(process.patLayer1EventContent.outputCommands)

