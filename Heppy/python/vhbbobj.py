
#!/bin/env python
from math import *
import ROOT
#from CMGTools.TTHAnalysis.signedSip import *
from PhysicsTools.Heppy.analyzers.objects.autophobj import *
from PhysicsTools.HeppyCore.utils.deltar import deltaPhi

import copy, os

leptonTypeVHbb = NTupleObjectType("leptonTypeVHbb", baseObjectTypes = [ leptonType ], variables = [
    # Loose id 
    NTupleVariable("looseIdSusy", lambda x : x.looseIdSusy if hasattr(x, 'looseIdSusy') else -999, int, help="Loose ID for Susy ntuples (always true on selected leptons)"),
    NTupleVariable("looseIdPOG", lambda x : x.muonID("POG_ID_Loose") if abs(x.pdgId()) == 13 else -999, int, help="Loose ID for Susy ntuples (always true on selected leptons)"),
#    NTupleVariable("heep51eleId", lambda x : x.electronID("egmGsfElectronIDs:heepElectronID-HEEPV51-miniAOD") if abs(x.pdgId()) == 11 else -1, int, help="heep 51 ID for electrons)"),
#    NTupleVariable("heep51eleId", lambda x : x.electronID("heepElectronID-HEEPV51-miniAOD") if abs(x.pdgId()) == 11 else -1, int, help="heep 51 ID for electrons)"),
    # Isolations with the two radia
    NTupleVariable("chargedHadRelIso03",  lambda x : x.chargedHadronIsoR(0.3)/x.pt(), help="PF Rel Iso, R=0.3, charged hadrons only"),
    NTupleVariable("chargedHadRelIso04",  lambda x : x.chargedHadronIsoR(0.4)/x.pt(), help="PF Rel Iso, R=0.4, charged hadrons only"),
    NTupleVariable("eleSieie",    lambda x : x.full5x5_sigmaIetaIeta() if abs(x.pdgId())==11 else -999., help="sigma IEtaIEta for electrons"),
    NTupleVariable("e5x5", lambda x : x.e5x5() if abs(x.pdgId())==11 else -999., help="e5x5 for electrons"), #added
    NTupleVariable("e2x5Max",    lambda x : x.e2x5Max() if abs(x.pdgId())==11 else -999., help="e2x5Max for electrons"),
    NTupleVariable("e1x5",    lambda x : x.e1x5() if abs(x.pdgId())==11 else -999., help="e1x5 for electrons"),
    NTupleVariable("isolTrkPt",    lambda x : x.dr03TkSumPt() if abs(x.pdgId())==11 else -999., help="isolTrkPt for electrons"),
    NTupleVariable("isolEmHadDepth1",    lambda x : x.dr03EcalRecHitSumEt() + x.dr03HcalDepth1TowerSumEt() if abs(x.pdgId())==11 else -999., help="isolEmHadDepth1 for electrons"),
    NTupleVariable("eleDEta",     lambda x : x.deltaEtaSuperClusterTrackAtVtx() if abs(x.pdgId())==11 else -999., help="delta eta for electrons"),
    NTupleVariable("eleDPhi",     lambda x : x.deltaPhiSuperClusterTrackAtVtx() if abs(x.pdgId())==11 else -999., help="delta phi for electrons"),
    NTupleVariable("eleHoE",      lambda x : x.hadronicOverEm() if abs(x.pdgId())==11 else -999., help="H/E for electrons"),
    NTupleVariable("eleMissingHits",      lambda x : x.lostInner() if abs(x.pdgId())==11 else -999., help="Missing hits for electrons"),
    NTupleVariable("eleChi2",      lambda x : x.gsfTrack().normalizedChi2() if abs(x.pdgId())==11 else -999., help="Track chi squared for electrons' gsf tracks"),
    NTupleVariable("eleClusterEta", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -999., help="Electron Supercluster Eta"),
    NTupleVariable("eleClusterEnergy", lambda x : x.superCluster().energy() if abs(x.pdgId())==11 else -999., help="Electron Supercluster Energy"),
    NTupleVariable("eleClusterDEta", lambda x : x.deltaEtaSeedClusterTrackAtVtx() if abs(x.pdgId())==11 else -999., help="Electron Supercluster DEta"),
    NTupleVariable("eleClusterDPhi", lambda x : x.deltaPhiSuperClusterTrackAtVtx() if abs(x.pdgId())==11 else -999., help="Electron Supercluster DPhi"),
    # Extra electron id variables
#    NTupleVariable("convVetoFull", lambda x : (x.passConversionVeto() and x.gsfTrack().trackerExpectedHitsInner().numberOfLostHits() == 0) if abs(x.pdgId())==11 else 1, int, help="Conv veto + no missing hits for electrons, always true for muons."),
    #NTupleVariable("eleMVAId",     lambda x : (x.electronID("POG_MVA_ID_NonTrig") + 2*x.electronID("POG_MVA_ID_Trig")) if abs(x.pdgId()) == 11 else -1, int, help="Electron mva id working point: 0=none, 1=non-trig, 2=trig, 3=both"),
#    NTupleVariable("eleMVAId",     lambda x : (x.electronID("POG_MVA_ID_NonTrig_full5x5") + 2*x.electronID("POG_MVA_ID_Trig_full5x5")) if abs(x.pdgId()) == 11 else -1, int, help="Electron mva id working point (2012, full5x5 shapes): 0=none, 1=non-trig, 2=trig, 3=both"),
#    NTupleVariable("tightCharge",  lambda lepton : ( lepton.isGsfCtfScPixChargeConsistent() + lepton.isGsfScPixChargeConsistent() ) if abs(lepton.pdgId()) == 11 else 2*(lepton.innerTrack().ptError()/lepton.innerTrack().pt() < 0.2), int, help="Tight charge criteria"),
    #NTupleVariable("mvaId",        lambda lepton : lepton.mvaNonTrigV0() if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons (as HZZ); 1 for muons"),
#    NTupleVariable("mvaId",         lambda lepton : lepton.mvaNonTrigV0(full5x5=True) if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for non-triggering electrons (as HZZ); 1 for muons"),
#    NTupleVariable("mvaIdTrig",     lambda lepton : lepton.mvaTrigV0(full5x5=True)    if abs(lepton.pdgId()) == 11 else 1, help="EGamma POG MVA ID for triggering electrons; 1 for muons"),
    # Muon-speficic info
    NTupleVariable("nStations",    lambda lepton : lepton.numberOfMatchedStations() if abs(lepton.pdgId()) == 13 else 4, help="Number of matched muons stations (4 for electrons)"),
    NTupleVariable("trkKink",      lambda lepton : lepton.combinedQuality().trkKink if abs(lepton.pdgId()) == 13 else 0, help="Tracker kink-finder"), 
    NTupleVariable("caloCompatibility",      lambda lepton : lepton.caloCompatibility() if abs(lepton.pdgId()) == 13 else 0, help="Calorimetric compatibility"), 
    NTupleVariable("globalTrackChi2",      lambda lepton : lepton.globalTrack().normalizedChi2() if abs(lepton.pdgId()) == 13 and lepton.globalTrack().isNonnull() else 0, help="Global track normalized chi2"), 
    NTupleVariable("nChamberHits", lambda lepton: lepton.globalTrack().hitPattern().numberOfValidMuonHits() if abs(lepton.pdgId()) == 13 and lepton.globalTrack().isNonnull() else -999, help="Number of muon chamber hits (-1 for electrons)"),
    NTupleVariable("isBarrelEle", lambda x : getattr(x, "isBarrelEle", -1), int, help="Barrel Electron"), #added
    NTupleVariable("isEndCapEle", lambda x : getattr(x, "isEndCapEle", -1), int, help="EndCap Electron"), #added
    NTupleVariable("isEcalDriven", lambda x : x.ecalDrivenSeed() if abs(x.pdgId()) == 11 else -999, int, help="is Ecal Driven to cut on ID"), #added
    NTupleVariable("isMyGoodMuon", lambda x : getattr(x, "isMyGoodMuon", -1), int, help="High Pt muon ID"), #added
    NTupleVariable("isMyGoodElectron", lambda x : getattr(x, "isMyGoodElectron", -1), int, help="High Pt electron ID"), #added
    NTupleVariable("relPtError", lambda lepton: lepton.muonBestTrack().ptError()/lepton.muonBestTrack().pt() if abs(lepton.pdgId()) == 13 and lepton.muonBestTrack().isNonnull() else -999, help="relative error of muon pt, intended for high pt ID  (-1 for electrons)"),
    NTupleVariable("isPFMuon", lambda lepton: lepton.isPFMuon() if abs(lepton.pdgId()) == 13 else 0, help="1 if muon passes particle flow ID"),
    NTupleVariable("muon_dz", lambda x : x.muonBestTrack().dz() if abs(x.pdgId()) == 13 else -999, help="dz for muons"),
    NTupleVariable("isHighPtMuon", lambda x : x.muonID("POG_ID_HighPt") if abs(x.pdgId()) == 13 else -999, int, help="High pt id for muons"),
    NTupleVariable("muTrackIso", lambda lepton: lepton.trackIso() if abs(lepton.pdgId()) == 13 else -999, help="muon track isolation"),
    NTupleVariable("isGlobalMuon", lambda lepton: lepton.isGlobalMuon() if abs(lepton.pdgId()) == 13 else 0, help="1 if muon is global muon"),
    NTupleVariable("isTrackerMuon", lambda lepton: lepton.isTrackerMuon() if abs(lepton.pdgId()) == 13 else 0, help="1 if muon is tracker muon"),
    NTupleVariable("pixelHits", lambda lepton : lepton.innerTrack().hitPattern().numberOfValidPixelHits() if abs(lepton.pdgId()) == 13 and lepton.innerTrack().isNonnull() else -999, help="Number of pixel hits (-1 for electrons)"),
    # Extra tracker-related id variables
    NTupleVariable("trackerLayers", lambda x : (x.track() if abs(x.pdgId())==13 else x.gsfTrack()).hitPattern().trackerLayersWithMeasurement(), int, help="Tracker Layers"),
    NTupleVariable("pixelLayers", lambda x : (x.track() if abs(x.pdgId())==13 else x.gsfTrack()).hitPattern().pixelLayersWithMeasurement(), int, help="Pixel Layers"),
    # TTH-id related variables
    NTupleVariable("mvaTTH",     lambda lepton : lepton.mvaValue if hasattr(lepton,'mvaValue') else -1, help="Lepton MVA (ttH version)"),
    NTupleVariable("jetOverlapIdx", lambda lepton : getattr(lepton, "jetOverlapIdx", -1), int, help="index of jet with overlapping PF constituents. If idx>=1000, then idx = idx-1000 and refers to discarded jets."),
    NTupleVariable("jetPtRatio", lambda lepton : lepton.pt()/lepton.jet.pt() if hasattr(lepton,'jet') else -1, help="pt(lepton)/pt(nearest jet)"),
    NTupleVariable("jetBTagCSV", lambda lepton : lepton.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if hasattr(lepton,'jet') and hasattr(lepton.jet, 'btag') else -99, help="btag of nearest jet"),
    NTupleVariable("jetDR",      lambda lepton : deltaR(lepton.eta(),lepton.phi(),lepton.jet.eta(),lepton.jet.phi()) if hasattr(lepton,'jet') else -1, help="deltaR(lepton, nearest jet)"),
    NTupleVariable("pfRelIso03",      lambda ele : (ele.pfIsolationVariables().sumChargedHadronPt + max(ele.pfIsolationVariables().sumNeutralHadronEt + ele.pfIsolationVariables().sumPhotonEt - 0.5 * ele.pfIsolationVariables().sumPUPt,0.0)) / ele.pt()  if abs(ele.pdgId()) == 11 else -999, help="0.3 particle based iso"),
    NTupleVariable("pfRelIso04",      lambda mu : (mu.pfIsolationR04().sumChargedHadronPt + max( mu.pfIsolationR04().sumNeutralHadronEt + mu.pfIsolationR04().sumPhotonEt - 0.5 * mu.pfIsolationR04().sumPUPt,0.0)) / mu.pt() if abs(mu.pdgId()) == 13 else -999, help="0.4 particle based iso"),
    NTupleVariable("muonDB", lambda x : x.dB() if abs(x.pdgId()) == 13 else -999, help="muon DB"),
    NTupleVariable("etaSc", lambda x : x.superCluster().eta() if abs(x.pdgId())==11 else -999, help="Electron supercluster pseudorapidity"),
    NTupleVariable("eleExpMissingInnerHits", lambda x : x.gsfTrack().hitPattern().numberOfHits(ROOT.reco.HitPattern.MISSING_INNER_HITS) if abs(x.pdgId())==11 else -999, help="Electron expected missing inner hits"),
    NTupleVariable("eleooEmooP", lambda x : abs(1.0/x.ecalEnergy() - x.eSuperClusterOverP()/x.ecalEnergy()) if abs(x.pdgId())==11 and x.ecalEnergy()>0.0 else 9e9 , help="Electron 1/E - 1/P"),
    NTupleVariable("muonTrackerLayers", lambda x : x.innerTrack().hitPattern().trackerLayersWithMeasurement() if abs(x.pdgId()) == 13 else -999, help="muon tracker layers"),
    # MC-match info
#    NTupleVariable("mcMatchId",  lambda x : x.mcMatchId, int, mcOnly=True, help="Match to source from hard scatter (25 for H, 6 for t, 23/24 for W/Z)"),
#    NTupleVariable("mcMatchAny",  lambda x : x.mcMatchAny, int, mcOnly=True, help="Match to any final state leptons: -mcMatchId if prompt, 0 if unmatched, 1 if light flavour, 2 if heavy flavour (b)"),
#    NTupleVariable("mcMatchTau",  lambda x : x.mcMatchTau, int, mcOnly=True, help="True if the leptons comes from a tau"),
])

##------------------------------------------  
## TAU
##------------------------------------------  

tauTypeVHbb = NTupleObjectType("tauTypeVHbb", baseObjectTypes = [ tauType ], variables = [
#    NTupleVariable("idxJetMatch", lambda x : x.jetIdx, int, help="index of the matching jet"),
#    NTupleVariable("genMatchType", lambda x : x.genMatchType, int,mcOnly=True, help="..FILLME PLEASE..")
])

##------------------------------------------  
## JET
##------------------------------------------  

jetTypeVHbb = NTupleObjectType("jet",  baseObjectTypes = [ jetType ], variables = [
    NTupleVariable("idxFirstTauMatch", lambda x : x.tauIdxs[0] if len(getattr(x, "tauIdxs", [])) > 0 else -1, int,help='index of the first matching tau'),
    NTupleVariable("heppyFlavour", lambda x : x.mcFlavour, int,     mcOnly=True, help="heppy-style match to gen quarks"),
    NTupleVariable("hadronFlavour", lambda x : x.hadronFlavour(), int,     mcOnly=True, help="hadron flavour (ghost matching to B/C hadrons)"),
    NTupleVariable("btagBDT", lambda x : getattr(x,"btagBDT",-99), help="combined super-btag"),
    NTupleVariable("btagProb", lambda x : x.btag('pfJetProbabilityBJetTags') , help="jet probability b-tag"),
    NTupleVariable("btagBProb", lambda x : x.btag('pfJetBProbabilityBJetTags') , help="jet b-probability b-tag"),
    NTupleVariable("btagSoftEl", lambda x : getattr(x, "btagSoftEl", -1000) , help="soft electron b-tag"),
    NTupleVariable("btagSoftMu", lambda x : getattr(x, "btagSoftMu", -1000) , help="soft muon b-tag"),
    NTupleVariable("btagnew",   lambda x : getattr(x,"btagnew",-2), help="newest btag discriminator"),
    NTupleVariable("btagCSVV0",   lambda x : x.bDiscriminator('pfCombinedSecondaryVertexV2BJetTags'), help="should be the old CSV discriminator with AVR vertices"),
   # NTupleVariable("mcMatchId",    lambda x : x.mcMatchId,   int, mcOnly=True, help="Match to source from hard scatter (25 for H, 6 for t, 23/24 for W/Z)"),
   # NTupleVariable("puId", lambda x : x.puJetIdPassed, int,     mcOnly=False, help="puId (full MVA, loose WP, 5.3.X training on AK5PFchs: the only thing that is available now)"),
   # NTupleVariable("id",    lambda x : x.jetID("POG_PFID") , int, mcOnly=False,help="POG Loose jet ID"),
    NTupleVariable("isMyGoodLooseJet", lambda x : getattr(x, "isMyGoodLooseJet", -1), int, help="Loose Jet ID"), #added
    NTupleVariable("isMyGoodTightJet", lambda x : getattr(x, "isMyGoodTightJet", -1), int, help="Tight Jet ID"), #added
    NTupleVariable("isMyGoodTightLepVetoJet", lambda x : getattr(x, "isMyGoodTightLepVetoJet", -1), int, help="Tight Lepton Veto ID for jets"), #added
    NTupleVariable("chHEF", lambda x : x.chargedHadronEnergyFraction(), float, mcOnly = False, help="chargedHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neHEF", lambda x : x.neutralHadronEnergyFraction(), float, mcOnly = False,help="neutralHadronEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("chEmEF", lambda x : x.chargedEmEnergyFraction(), float, mcOnly = False,help="chargedEmEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("neEmEF", lambda x : x.neutralEmEnergyFraction(), float, mcOnly = False,help="neutralEmEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("muEF", lambda x : x.muonEnergyFraction(), float, mcOnly = False,help="muonEnergyFraction (relative to uncorrected jet energy)"),
    NTupleVariable("chMult", lambda x : x.chargedMultiplicity(), int, mcOnly = False,help="chargedMultiplicity from PFJet.h"),
    NTupleVariable("neMult", lambda x : x.neutralMultiplicity(), int, mcOnly = False,help="neutralMultiplicity from PFJet.h"),
    NTupleVariable("leadTrackPt", lambda x : x.leadTrackPt() , float, mcOnly = False, help="pt of the leading track in the jet"), 
    NTupleVariable("mcEta",   lambda x : x.mcJet.eta() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="eta of associated gen jet"),
    NTupleVariable("mcPhi",   lambda x : x.mcJet.phi() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="phi of associated gen jet"),
    NTupleVariable("mcM",   lambda x : x.mcJet.p4().M() if getattr(x,"mcJet",None) else 0., mcOnly=True, help="mass of associated gen jet"),
    NTupleVariable("leptonPdgId",   lambda x : x.leptons[0].pdgId() if len(x.leptons) > 0 else -99, mcOnly=False, help="pdg id of the first associated lepton"),
    NTupleVariable("leptonPt",   lambda x : x.leptons[0].pt() if len(x.leptons) > 0 else -99, mcOnly=False, help="pt of the first associated lepton"),
    NTupleVariable("leptonPtRel",   lambda x : ptRel(x.leptons[0].p4(),x.p4()) if len(x.leptons) > 0 else -99, mcOnly=False, help="ptrel of the first associated lepton"),
    NTupleVariable("leptonPtRelInv",   lambda x : ptRel(x.p4(),x.leptons[0].p4()) if len(x.leptons) > 0 else -99, mcOnly=False, help="ptrel Run1 definition of the first associated lepton"),
    NTupleVariable("leptonDeltaR",   lambda x : deltaR(x.leptons[0].p4().eta(),x.leptons[0].p4().phi(),x.p4().eta(),x.p4().phi()) if len(x.leptons) > 0 else -99, mcOnly=False, help="deltaR of the first associated lepton"),
    NTupleVariable("leptonDeltaPhi",   lambda x : deltaPhi(x.leptons[0].p4().phi(),x.p4().phi()) if len(x.leptons) > 0 else 0, mcOnly=False, help="deltaPhi of the first associated lepton"),
    NTupleVariable("leptonDeltaEta",   lambda x : x.leptons[0].p4().eta()-x.p4().eta() if len(x.leptons) > 0 else 0, mcOnly=False, help="deltaEta of the first associated lepton"),
    NTupleVariable("vtxMass",   lambda x : x.userFloat("vtxMass"), mcOnly=False, help="vtxMass from btag"),
    NTupleVariable("vtxNtracks",   lambda x : x.userFloat("vtxNtracks"), mcOnly=False, help="number of tracks at vertex from btag"),
    NTupleVariable("vtxPt",   lambda x : sqrt(x.userFloat("vtxPx")**2 + x.userFloat("vtxPy")**2), mcOnly=False, help="pt of vertex from btag"),
    NTupleVariable("vtx3DSig",   lambda x : x.userFloat("vtx3DSig"), mcOnly=False, help="decay len significance of vertex from btag"),
    NTupleVariable("vtx3DVal",   lambda x : x.userFloat("vtx3DVal"), mcOnly=False, help="decay len of vertex from btag"),
    NTupleVariable("vtxPosX",   lambda x : x.userFloat("vtxPosX"), mcOnly=False, help="X coord of vertex from btag"),
    NTupleVariable("vtxPosY",   lambda x : x.userFloat("vtxPosY"), mcOnly=False, help="Y coord of vertex from btag"), 
    NTupleVariable("vtxPosZ",   lambda x : x.userFloat("vtxPosZ"), mcOnly=False, help="Z coord of vertex from btag"),
    NTupleVariable("pullVectorPhi", lambda x : getattr(x,"pullVectorPhi",-99), mcOnly=False, help="pull angle phi in the phi eta plane"),
    NTupleVariable("pullVectorMag", lambda x : getattr(x,"pullVectorMag",-99), mcOnly=False, help="pull angle magnitude"),
   # QG variables:
# this computes for all
#    NTupleVariable("qgl",   lambda x :x.qgl() , float, mcOnly=False,help="QG Likelihood"),
#    NTupleVariable("ptd",   lambda x : getattr(x.computeQGvars(),'ptd', 0), float, mcOnly=False,help="QG input variable: ptD"),
#    NTupleVariable("axis2",   lambda x : getattr(x.computeQGvars(),'axis2', 0) , float, mcOnly=False,help="QG input variable: axis2"),
#    NTupleVariable("mult",   lambda x : getattr(x.computeQGvars(),'mult', 0) , int, mcOnly=False,help="QG input variable: total multiplicity"),

# this only read qgl if it was explicitelly computed in the code
    NTupleVariable("qgl",   lambda x : getattr(x,'qgl_value',-20) , float, mcOnly=False,help="QG Likelihood"),
    NTupleVariable("ptd",   lambda x : getattr(x,'ptd', -20), float, mcOnly=False,help="QG input variable: ptD"),
    NTupleVariable("axis2",   lambda x : getattr(x,'axis2', -20) , float, mcOnly=False,help="QG input variable: axis2"),
    NTupleVariable("mult",   lambda x : getattr(x,'mult', -20) , int, mcOnly=False,help="QG input variable: total multiplicity"),
    NTupleVariable("numberOfDaughters",   lambda x : x.numberOfDaughters(), int, mcOnly=False,help="number of daughters"),
    NTupleVariable("btagIdx",   lambda x : x.btagIdx, int, mcOnly=False,help="ranking in btag"),
    NTupleVariable("mcIdx",   lambda x : x.mcJet.index if hasattr(x,"mcJet") and x.mcJet is not None else -1, int, mcOnly=False,help="index of the matching gen jet"),
    NTupleVariable("pt_reg",lambda x : getattr(x,"pt_reg",-99), help="Regression"),
    NTupleVariable("pt_regVBF",lambda x : getattr(x,"pt_regVBF",-99), help="Regression for VBF"),
    NTupleVariable("blike_VBF",lambda x : getattr(x,"blike_VBF",-2), help="VBF blikelihood for SingleBtag dataset")
 ])


#add per-jet b-tag systematic weight
from PhysicsTools.Heppy.physicsutils.BTagWeightCalculator import BTagWeightCalculator
csvpath = os.environ['CMSSW_BASE']+"/src/HighMassVHbbAnalysis/Heppy/data/csv"
bweightcalc = BTagWeightCalculator(
    csvpath + "/csv_rwt_hf_IT_FlatSF_2015_07_27.root",
    csvpath + "/csv_rwt_lf_IT_FlatSF_2015_07_27.root"
)

for syst in ["JES", "LF", "HF", "Stats1", "Stats2", "cErr1", "cErr2"]:
    for sdir in ["Up", "Down"]:
        jetTypeVHbb.variables += [NTupleVariable("bTagWeight"+syst+sdir,
            lambda jet, sname=syst+sdir,bweightcalc=bweightcalc: bweightcalc.calcJetWeight(
                jet, kind="final", systematic=sname
            ), float, mcOnly=True, help="b-tag CSV weight, variating "+syst + " "+sdir
        )]
jetTypeVHbb.variables += [NTupleVariable("bTagWeight",
    lambda jet, bweightcalc=bweightcalc: bweightcalc.calcJetWeight(
        jet, kind="final", systematic="nominal",
    ), float, mcOnly=True, help="b-tag CSV weight, nominal"
)]


##------------------------------------------  
## FAT JET + Tau
##------------------------------------------  

# Four Vector + Nsubjettiness

fatjetTauType = NTupleObjectType("fatjettau",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("tau1",  lambda x : x.tau1, help="Nsubjettiness (1 axis)"),
    NTupleVariable("tau2",  lambda x : x.tau2, help="Nsubjettiness (2 axes)"),
    NTupleVariable("tau3",  lambda x : x.tau3, help="Nsubjettiness (3 axes)"),
])

 
##------------------------------------------  
## FAT JET
##------------------------------------------  

# Four Vector + Nsubjettiness + Hbb-Tag

fatjetType = NTupleObjectType("fatjet",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("tau1",  lambda x : x.tau1, help="Nsubjettiness (1 axis)"),
    NTupleVariable("tau2",  lambda x : x.tau2, help="Nsubjettiness (2 axes)"),
    NTupleVariable("tau3",  lambda x : x.tau3, help="Nsubjettiness (3 axes)"),
    
    # bb-tag output variable
    NTupleVariable("bbtag",  lambda x : x.bbtag, help="Hbb b-tag score"),

    # bb-tag input variables
    NTupleVariable("PFLepton_ptrel",   lambda x : x.PFLepton_ptrel, help="pt-rel of e/mu (for bb-tag)"),    
    NTupleVariable("z_ratio",          lambda x : x.z_ratio, help="z-ratio (for bb-tag)"),    
    NTupleVariable("tau_dot",          lambda x : x.tau_dot, help="tau_dot (for bb-tag)"),    
    NTupleVariable("SV_mass_0",        lambda x : x.SV_mass_0, help="secondary vertex mass (for bb-tag)"),    
    NTupleVariable("SV_EnergyRatio_0", lambda x : x.SV_EnergyRatio_0, help="secondary vertex mass energy ratio 0 (for bb-tag)"),    
    NTupleVariable("SV_EnergyRatio_1", lambda x : x.SV_EnergyRatio_1, help="secondary vertex mass energy ratio 1 (for bb-tag)"),    
    NTupleVariable("PFLepton_IP2D",    lambda x : x.PFLepton_IP2D, help="lepton IP2D (for bb-tag)"),    
    NTupleVariable("tau_21",           lambda x : x.tau_21, help="nsubjettiness tau2/tau1 (for bb-tag)"),    
    NTupleVariable("nSL",              lambda x : x.nSL, help="number of soft leptons (for bb-tag)"),    
    NTupleVariable("vertexNTracks",    lambda x : x.vertexNTracks, help="number of tracks for vertex (for bb-tag)"),    
    ])


##------------------------------------------  
## Extended FAT JET
##------------------------------------------  

# Four Vector + Nsubjettiness + masses + Hbb-Tag

ak8FatjetType = NTupleObjectType("ak8fatjet",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("chHEFrac", lambda x : x.chargedHadronEnergyFraction(), float, help="hadronic charged energy fraction for AK08"), #added
    NTupleVariable("neHEFrac", lambda x : x.neutralHadronEnergyFraction(), float, help="hadronic neutral energy fraction for AK08"), #added
    NTupleVariable("chEmEFrac", lambda x : x.chargedEmEnergyFraction(), float, help="em charged energy fraction for AK08"), #added
    NTupleVariable("neEmEFrac", lambda x : x.neutralEmEnergyFraction(), float, help="em neutral energy fraction for AK08"), #added
    NTupleVariable("chMult", lambda x : x.chargedMultiplicity(), int, help="Ak08 charged multiplicity"),#added
    NTupleVariable("neMult", lambda x : x.neutralMultiplicity(), int, help="Ak08 neutral multiplicity"),#added
    NTupleVariable("muEFrac", lambda x : x.muonEnergyFraction(), float, help="Ak08 muon energy fraction"),#added
    NTupleVariable("tau1",  lambda x : x.userFloat("NjettinessAK8:tau1"), help="Nsubjettiness (1 axis)"),
    NTupleVariable("tau2",  lambda x : x.userFloat("NjettinessAK8:tau2"), help="Nsubjettiness (2 axes)"),
    NTupleVariable("tau3",  lambda x : x.userFloat("NjettinessAK8:tau3"), help="Nsubjettiness (3 axes)"),

    NTupleVariable("msoftdrop",  lambda x : x.userFloat("ak8PFJetsCHSSoftDropMass"),  help="Softdrop Mass"),
    NTupleVariable("mpruned",    lambda x : x.userFloat("ak8PFJetsCHSPrunedMass"),    help="Pruned Mass"),
    NTupleVariable("mtrimmed",   lambda x : x.userFloat("ak8PFJetsCHSTrimmedMass"),   help="Trimmed Mass"),
    NTupleVariable("mfiltered",  lambda x : x.userFloat("ak8PFJetsCHSFilteredMass"),  help="Filtered Mass"),

    NTupleVariable("bbtag",  lambda x : x.bbtag, help="Hbb b-tag score"),

    # bb-tag input variables
    NTupleVariable("PFLepton_ptrel",   lambda x : x.PFLepton_ptrel, help="pt-rel of e/mu (for bb-tag)"),    
    NTupleVariable("z_ratio",          lambda x : x.z_ratio, help="z-ratio (for bb-tag)"),    
    NTupleVariable("tau_dot",          lambda x : x.tau_dot, help="tau_dot (for bb-tag)"),    
    NTupleVariable("SV_mass_0",        lambda x : x.SV_mass_0, help="secondary vertex mass (for bb-tag)"),    
    NTupleVariable("SV_EnergyRatio_0", lambda x : x.SV_EnergyRatio_0, help="secondary vertex mass energy ratio 0 (for bb-tag)"),    
    NTupleVariable("SV_EnergyRatio_1", lambda x : x.SV_EnergyRatio_1, help="secondary vertex mass energy ratio 1 (for bb-tag)"),    
    NTupleVariable("PFLepton_IP2D",    lambda x : x.PFLepton_IP2D, help="lepton IP2D (for bb-tag)"),    
    NTupleVariable("tau_21",           lambda x : x.tau_21, help="nsubjettiness tau2/tau1 (for bb-tag)"),    
    NTupleVariable("nSL",              lambda x : x.nSL, help="number of soft leptons (for bb-tag)"),    
    NTupleVariable("vertexNTracks",    lambda x : x.vertexNTracks, help="number of tracks for vertex (for bb-tag)"),    

    ])


##------------------------------------------  
## Subjet
##------------------------------------------  

# Four Vector + b-Tag

subjetType = NTupleObjectType("subjet",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("btag",  lambda x : x.btag, help="CVS IVF V2 btag-score")])

##------------------------------------------  
## PAT Subjet
##------------------------------------------  

# Four Vector + b-Tag from PAT

patSubjetType = NTupleObjectType("patsubjet",  baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("btag",  lambda x : x.bDiscriminator("pfCombinedInclusiveSecondaryVertexV2BJetTags"), help="CVS IVF V2 btag-score")])


##------------------------------------------  
## HEPTopTagger Candidate
##------------------------------------------  

# Four Vector + fW + Rmin + RminExp + Subjets

# The W/non-W assignment is done using the mass ratio in the HTT

httType = NTupleObjectType("htt",  baseObjectTypes = [ fourVectorType ], variables = [

    NTupleVariable("fRec",  lambda x : x.fRec, help="relative W width"),
    NTupleVariable("Ropt",  lambda x : x.Ropt, help="optimal value of R"),
    NTupleVariable("RoptCalc",  lambda x : x.RoptCalc, help="expected value of optimal R"),
    NTupleVariable("ptForRoptCalc",  lambda x : x.ptForRoptCalc, help="pT used for calculation of RoptCalc"),

    # Leading W Subjet (pt)
    NTupleVariable("sjW1pt",   lambda x : x.sjW1pt,   help = "Leading W Subjet pT"),
    NTupleVariable("sjW1eta",  lambda x : x.sjW1eta,  help = "Leading W Subjet eta"),
    NTupleVariable("sjW1phi",  lambda x : x.sjW1phi,  help = "Leading W Subjet phi"),
    NTupleVariable("sjW1mass", lambda x : x.sjW1mass, help = "Leading W Subjet mass"),
    NTupleVariable("sjW1btag", lambda x : x.sjW1btag, help = "Leading W Subjet btag"),
    # Second W Subjet (pt)
    NTupleVariable("sjW2pt",   lambda x : x.sjW2pt,   help = "Second Subjet pT"),
    NTupleVariable("sjW2eta",  lambda x : x.sjW2eta,  help = "Second Subjet eta"),
    NTupleVariable("sjW2phi",  lambda x : x.sjW2phi,  help = "Second Subjet phi"),
    NTupleVariable("sjW2mass", lambda x : x.sjW2mass, help = "Second Subjet mass"),
    NTupleVariable("sjW2btag", lambda x : x.sjW2btag, help = "Second Subjet btag"),
    # Non-W Subjet
    NTupleVariable("sjNonWpt",   lambda x : x.sjNonWpt,   help = "Non-W Subjet pT"),
    NTupleVariable("sjNonWeta",  lambda x : x.sjNonWeta,  help = "Non-W Subjet eta"),
    NTupleVariable("sjNonWphi",  lambda x : x.sjNonWphi,  help = "Non-W Subjet phi"),
    NTupleVariable("sjNonWmass", lambda x : x.sjNonWmass, help = "Non-W Subjet mass"),
    NTupleVariable("sjNonWbtag", lambda x : x.sjNonWbtag, help = "Non-W Subjet btag"),
    ])
   

##------------------------------------------  
## SECONDARY VERTEX CANDIDATE
##------------------------------------------  
  
svType = NTupleObjectType("sv", baseObjectTypes = [ fourVectorType ], variables = [
    NTupleVariable("charge",   lambda x : x.charge(), int),
    NTupleVariable("ntracks", lambda x : x.numberOfDaughters(), int, help="Number of tracks (with weight > 0.5)"),
    NTupleVariable("chi2", lambda x : x.vertexChi2(), help="Chi2 of the vertex fit"),
    NTupleVariable("ndof", lambda x : x.vertexNdof(), help="Degrees of freedom of the fit, ndof = (2*ntracks - 3)" ),
    NTupleVariable("dxy",  lambda x : x.dxy.value(), help="Transverse distance from the PV [cm]"),
    NTupleVariable("edxy", lambda x : x.dxy.error(), help="Uncertainty on the transverse distance from the PV [cm]"),
    NTupleVariable("ip3d",  lambda x : x.d3d.value(), help="3D distance from the PV [cm]"),
    NTupleVariable("eip3d", lambda x : x.d3d.error(), help="Uncertainty on the 3D distance from the PV [cm]"),
    NTupleVariable("sip3d", lambda x : x.d3d.significance(), help="S_{ip3d} with respect to PV (absolute value)"),
    NTupleVariable("cosTheta", lambda x : x.cosTheta, help="Cosine of the angle between the 3D displacement and the momentum"),
    NTupleVariable("jetPt",  lambda x : x.jet.pt() if x.jet != None else 0, help="pT of associated jet"),
    NTupleVariable("jetBTag",  lambda x : x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.jet != None else -99, help="CSV b-tag of associated jet"),
    NTupleVariable("mcMatchNTracks", lambda x : x.mcMatchNTracks, int, mcOnly=True, help="Number of mc-matched tracks in SV"),
    NTupleVariable("mcMatchNTracksHF", lambda x : x.mcMatchNTracksHF, int, mcOnly=True, help="Number of mc-matched tracks from b/c in SV"),
    NTupleVariable("mcMatchFraction", lambda x : x.mcMatchFraction, mcOnly=True, help="Fraction of mc-matched tracks from b/c matched to a single hadron (or -1 if mcMatchNTracksHF < 2)"),
    NTupleVariable("mcFlavFirst", lambda x : x.mcFlavFirst, int, mcOnly=True, help="Flavour of last ancestor with maximum number of matched daughters"),
    NTupleVariable("mcFlavHeaviest", lambda x : x.mcFlavHeaviest, int, mcOnly=True, help="Flavour of heaviest hadron with maximum number of matched daughters"),
])

heavyFlavourHadronType = NTupleObjectType("heavyFlavourHadron", baseObjectTypes = [ genParticleType ], variables = [
    NTupleVariable("flav", lambda x : x.flav, int, mcOnly=True, help="Flavour"),
    NTupleVariable("sourceId", lambda x : x.sourceId, int, mcOnly=True, help="pdgId of heaviest mother particle (stopping at the first one heaviest than 175 GeV)"),
    NTupleVariable("svMass",   lambda x : x.sv.mass() if x.sv else 0, help="SV: mass"),
    NTupleVariable("svPt",   lambda x : x.sv.pt() if x.sv else 0, help="SV: pt"),
    NTupleVariable("svCharge",   lambda x : x.sv.charge() if x.sv else -99., int, help="SV: charge"),
    NTupleVariable("svNtracks", lambda x : x.sv.numberOfDaughters() if x.sv else 0, int, help="SV: Number of tracks (with weight > 0.5)"),
    NTupleVariable("svChi2", lambda x : x.sv.vertexChi2() if x.sv else -99., help="SV: Chi2 of the vertex fit"),
    NTupleVariable("svNdof", lambda x : x.sv.vertexNdof() if x.sv else -99., help="SV: Degrees of freedom of the fit, ndof = (2*ntracks - 3)" ),
    NTupleVariable("svDxy",  lambda x : x.sv.dxy.value() if x.sv else -99., help="SV: Transverse distance from the PV [cm]"),
    NTupleVariable("svEdxy", lambda x : x.sv.dxy.error() if x.sv else -99., help="SV: Uncertainty on the transverse distance from the PV [cm]"),
    NTupleVariable("svIp3d",  lambda x : x.sv.d3d.value() if x.sv else -99., help="SV: 3D distance from the PV [cm]"),
    NTupleVariable("svEip3d", lambda x : x.sv.d3d.error() if x.sv else -99., help="SV: Uncertainty on the 3D distance from the PV [cm]"),
    NTupleVariable("svSip3d", lambda x : x.sv.d3d.significance() if x.sv else -99., help="SV: S_{ip3d} with respect to PV (absolute value)"),
    NTupleVariable("svCosTheta", lambda x : x.sv.cosTheta if x.sv else -99., help="SV: Cosine of the angle between the 3D displacement and the momentum"),
    NTupleVariable("jetPt",  lambda x : x.jet.pt() if x.jet != None else 0, help="Jet: pT"),
    NTupleVariable("jetBTag",  lambda x : x.jet.btag('pfCombinedInclusiveSecondaryVertexV2BJetTags') if x.jet != None else -99, help="CSV b-tag of associated jet"),
])
shiftedMetType= NTupleObjectType("shiftedMetType", baseObjectTypes=[twoVectorType], variables=[
    NTupleVariable("sumEt", lambda x : x.sumEt() ),
])

primaryVertexType = NTupleObjectType("primaryVertex", variables = [
    NTupleVariable("x",    lambda x : x.x()),
    NTupleVariable("y",   lambda x : x.y()),
    NTupleVariable("z",   lambda x : x.z()),
    NTupleVariable("isFake",   lambda x : x.isFake()),
    NTupleVariable("ndof",   lambda x : x.ndof()),
    NTupleVariable("Rho",   lambda x : x.position().Rho()),
#    NTupleVariable("score",  lambda x : x.mass()), # to be added for 74X
])

genTauJetType = NTupleObjectType("genTauJet", baseObjectTypes = [ genParticleType ], variables = [
    NTupleVariable("decayMode", lambda x : x.decayMode, int, mcOnly=True, help="Generator level tau decay mode"),
])

genJetType = NTupleObjectType("genJet", baseObjectTypes = [ genParticleType ], variables = [
    NTupleVariable("numBHadrons", lambda x : getattr(x,"numBHadronsBeforeTop",-1), int, mcOnly=True, help="number of matched b hadrons before top quark decay"),
    NTupleVariable("numCHadrons", lambda x : getattr(x,"numCHadronsBeforeTop",-1), int, mcOnly=True, help="number of matched c hadrons before top quark decay"),
    NTupleVariable("numBHadronsFromTop", lambda x : getattr(x,"numBHadronsFromTop",-1), int, mcOnly=True, help="number of matched b hadrons from top quark decay"),
    NTupleVariable("numCHadronsFromTop", lambda x : getattr(x,"numCHadronsFromTop",-1), int, mcOnly=True, help="number of matched c hadrons from top quark decay"),
    NTupleVariable("numBHadronsAfterTop", lambda x : getattr(x,"numBHadronsAfterTop",-1), int, mcOnly=True, help="number of matched b hadrons after top quark decay"),
    NTupleVariable("numCHadronsAfterTop", lambda x : getattr(x,"numCHadronsAfterTop",-1), int, mcOnly=True, help="number of matched c hadrons after top quark decay"),
    NTupleVariable("wNuPt", lambda x : (x.p4()+x.nu).pt() if hasattr(x,"nu") else x.p4().pt() ,float, mcOnly=True, help="pt of jet adding back the neutrinos"),
    NTupleVariable("wNuEta", lambda x : (x.p4()+x.nu).eta() if hasattr(x,"nu") else x.p4().eta() ,float, mcOnly=True, help="eta of jet adding back the neutrinos"),
    NTupleVariable("wNuPhi", lambda x : (x.p4()+x.nu).phi() if hasattr(x,"nu") else x.p4().phi() ,float, mcOnly=True, help="phi of jet adding back the neutrinos"),
    NTupleVariable("wNuM", lambda x : (x.p4()+x.nu).M() if hasattr(x,"nu") else x.p4().M() ,float, mcOnly=True, help="mass of jet adding back the neutrinos"),

])

softActivityType = NTupleObjectType("softActivity", baseObjectTypes = [  ], variables = [
                 NTupleVariable("njets2", lambda sajets: len([ x for x in sajets if x.pt()> 2 ] ), int, help="number of jets from soft activity with pt>2Gev"),
                 NTupleVariable("njets5", lambda sajets: len([ x for x in sajets if x.pt()> 5 ] ), int, help="number of jets from soft activity with pt>5Gev"),
                 NTupleVariable("njets10", lambda sajets: len([ x for x in sajets if x.pt()> 10 ] ), int, help="number of jets from soft activity with pt>10Gev"),
                 NTupleVariable("HT", lambda sajets: sum([x.pt() for x in sajets],0.0), float, help="sum pt of sa jets"),
])

def ptRel(p4,axis):
    a=ROOT.TVector3(axis.Vect().X(),axis.Vect().Y(),axis.Vect().Z())
    o=ROOT.TLorentzVector(p4.Px(),p4.Py(),p4.Pz(),p4.E())
    return o.Perp(a)

