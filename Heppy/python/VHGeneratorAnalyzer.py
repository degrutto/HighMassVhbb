import operator 
import itertools
import copy

from ROOT import TLorentzVector

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.HeppyCore.framework.event import Event
from PhysicsTools.HeppyCore.statistics.counter import Counter, Counters
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle
from PhysicsTools.Heppy.physicsobjects.Lepton import Lepton
from PhysicsTools.Heppy.physicsobjects.Photon import Photon
from PhysicsTools.Heppy.physicsobjects.Electron import Electron
from PhysicsTools.Heppy.physicsobjects.Muon import Muon
from PhysicsTools.Heppy.physicsobjects.Jet import Jet
from PhysicsTools.Heppy.physicsobjects.PhysicsObjects import GenParticle

from PhysicsTools.HeppyCore.utils.deltar import deltaR,deltaPhi
from PhysicsTools.Heppy.physicsutils.genutils import *
import PhysicsTools.HeppyCore.framework.config as cfg

        
class GeneratorAnalyzer( Analyzer ):
    """Do generator-level analysis of a ttH->leptons decay:

       Creates in the event:
         event.genParticles   = the gen particles (pruned, as default)
         event.genHiggsDecayMode =   0  for non-Higgs
                                 15  for H -> tau tau
                                 23  for H -> Z Z
                                 24  for H -> W W
                                 xx  for H -> xx yy zzz 

          event.gentauleps = [ gen electrons and muons from hard scattering not from tau decays ]
          event.gentaus    = [ gen taus from from hard scattering ]
          event.genleps    = [ gen electrons and muons from hard scattering not from tau decays ]
          event.genbquarksFromTop  = [ gen b quarks from top quark decays ]
          event.genwzquarks = [ gen quarks from hadronic W,Z decays ]

       If filterHiggsDecays is set to a list of Higgs decay modes,
       it will filter events that have those decay modes.
       e.g. [0, 15, 23, 24] will keep data, non-Higgs MC and Higgs decays to (tau, Z, W) 
       but will drop Higgs decays to other particles (e.g. bb).
      
    """
    def __init__(self, cfg_ana, cfg_comp, looperName ):
        super(GeneratorAnalyzer,self).__init__(cfg_ana,cfg_comp,looperName)
        self.doPDFWeights = hasattr(self.cfg_ana, "PDFWeights") and len(self.cfg_ana.PDFWeights) > 0
        if self.doPDFWeights:
            self.pdfWeightInit = False
    #---------------------------------------------
    # DECLARATION OF HANDLES OF GEN LEVEL OBJECTS 
    #---------------------------------------------
        

    def declareHandles(self):
        super(GeneratorAnalyzer, self).declareHandles()

        #mc information
        self.mchandles['genParticles'] = AutoHandle( 'prunedGenParticles',
                                                     'std::vector<reco::GenParticle>' )
        if self.doPDFWeights:
            self.mchandles['pdfstuff'] = AutoHandle( 'generator', 'GenEventInfoProduct' )

    def beginLoop(self,setup):
        super(GeneratorAnalyzer,self).beginLoop(setup)

    def fillGenLeptons(self, event, particle, isTau=False, sourceId=25):
        """Get the gen level light leptons (prompt and/or from tau decays)"""

        for i in xrange( particle.numberOfDaughters() ):
            dau = GenParticle(particle.daughter(i))
            dau.sourceId = sourceId
            dau.isTau = isTau
            id = abs(dau.pdgId())
            moid = abs(dau.mother().pdgId()) if dau.mother() else 2212 #if no mom, let say it is a proton (consistent with CMSSW < 74X)
            if id in [11,13]:
                if isTau: event.gentauleps.append(dau)
                else:     event.genleps.append(dau)
            elif id == 15:
                if moid in [22,23,24]:
                    event.gentaus.append(dau)
                self.fillGenLeptons(event, dau, True, sourceId) 
            elif id in [22,23,24]:
                self.fillGenLeptons(event, dau, False, sourceId)

    def fillWZQuarks(self, event, particle, isWZ=False, sourceId=25):
        """Descend daughters of 'particle', and add quarks from W,Z to event.genwzquarks
           isWZ is set to True if already processing daughters of W,Z's, to False before it"""

        for i in xrange( particle.numberOfDaughters() ):
            dau = GenParticle(particle.daughter(i))
            dau.sourceId = sourceId
            id = abs(dau.pdgId())
            if id <= 5 and isWZ:
                event.genwzquarks.append(dau)
            elif id in [22,23,24]:
                self.fillWZQuarks(event, dau, True, sourceId)

    def fillHiggsBQuarks(self, event,h):
        """Get the b quarks from top decays into event.genbquarksFromH"""
        for i in xrange( h.numberOfDaughters() ):
            dau = GenParticle(h.daughter(i))
            if abs(dau.pdgId()) in [3,4,5]:
                    event.genbquarksFromH.append( dau )
                    if dau.numberOfDaughters() == 1 :
                         event.genbquarksFromHafterISR.append( GenParticle(dau.daughter(0)))


    def fillTopQuarks(self, event):
        """Get the b quarks from top decays into event.genbquarksFromTop"""

        event.gentopquarks = [ p for p in event.genParticles if abs(p.pdgId()) == 6 and p.numberOfDaughters() > 0 and abs(p.daughter(0).pdgId()) != 6 ]
        #if len(event.gentopquarks) != 2:
        #    print "Not two top quarks? \n%s\n" % event.gentopquarks

        for tq in event.gentopquarks:
            for i in xrange( tq.numberOfDaughters() ):
                dau = GenParticle(tq.daughter(i))
                if abs(dau.pdgId()) == 5:
                    dau.sourceId = 6
                    event.genbquarksFromTop.append( dau )
                elif abs(dau.pdgId()) == 24:
                    self.fillGenLeptons( event, dau, sourceId=6 )
                    self.fillWZQuarks(   event, dau, True, sourceId=6 )

    def makeMCInfo(self, event):
#       event.genParticles = map( GenParticle, self.mchandles['genParticles'].product() )
        event.genParticles = list(self.mchandles['genParticles'].product() )

        if False:
        
            for i,p in enumerate(event.genParticles):
                print " %5d: pdgId %+5d status %3d  pt %6.1f  " % (i, p.pdgId(),p.status(),p.pt()),
                if p.numberOfMothers() > 0:
                    imom, mom = p.motherRef().key(), p.mother()
                    print " | mother %5d pdgId %+5d status %3d  pt %6.1f  " % (imom, mom.pdgId(),mom.status(),mom.pt()),
                else:
                    print " | no mother particle                              ",
                    
                for j in xrange(min(3, p.numberOfDaughters())):
                    idau, dau = p.daughterRef(j).key(), p.daughter(j)
                    print " | dau[%d] %5d pdgId %+5d status %3d  pt %6.1f  " % (j,idau,dau.pdgId(),dau.status(),dau.pt()),
                print ""

        event.genHiggsBosons = []
        event.genHiggsSisters = []
        event.genleps    = []
        event.gentauleps = []
        event.gentaus    = []
        event.genbquarksFromTop  = []
        event.genbquarksFromH  = []
        event.genbquarksFromHafterISR = []
        event.genallbquarks = []
        event.genwzquarks = []
        event.gentopquarks  = []
        event.genallstatus2bhadrons = [ p for p in event.genParticles if p.status() ==2 and self.hasBottom(p.pdgId()) ]
#        event.genallstatus2bhadronsv2 = [ p for p in event.genParticles if p.status() ==2 and self.hasBottom(p.pdgId())  and p.numberOfDaughters() > 0 and not self.hasBottom(p.daughter(0).pdgId())]

        event.genallcquarks = [ p for p in event.genParticles if abs(p.pdgId()) == 4 and ( p.numberOfDaughters() == 0 or abs(p.daughter(0).pdgId()) != 4) ]

		# aggiunti da me

        #event.genHiggsToBB = [ p for p in event.genParticles if abs(p.pdgId())==25 and p.numberOfDaughters()==2 and abs(p.daughter(0).pdgId()) == 5 ] 

        #event.genvbosonsToLL = [ p for p in event.genParticles if abs(p.pdgId()) in [23,24] and abs(p.mother().pdgId()) in [23,24] and p.numberOfDaughters()==2 and abs(p.daughter(0).pdgId()) in [11,13,15] ]

        #event.genZbosonsToLL = [ p for p in event.genParticles if abs(p.pdgId()) in [23] and abs(p.daughter(0).pdgId())!= abs(p.pdgId()) ]
        #event.genWbosonsToLL = [ p for p in event.genParticles if abs(p.pdgId()) in [24] and abs(p.daughter(0).pdgId())!= abs(p.pdgId()) ]

        event.genvbosons = [ p for p in event.genParticles if abs(p.pdgId()) in [23,24] and p.numberOfDaughters()>0 and abs(p.daughter(0).pdgId()) != abs(p.pdgId()) and p.mass() > 30 ]
 		   
        #bosons = [ gp for gp in event.genParticles if gp.status() > 2 and  abs(gp.pdgId()) in [22,23,24]  ]
    	for b in event.genvbosons:
        	if b.numberOfDaughters()>0 :
                	self.fillGenLeptons(event, b, sourceId=abs(b.pdgId())) #selezione su leptoni fatta dentro la funzione stessa
                	self.fillWZQuarks(event, b, isWZ=True, sourceId=abs(b.pdgId()))



        higgsBosons = [ p for p in event.genParticles if (p.pdgId() == 25) and p.numberOfDaughters() > 0 and abs(p.daughter(0).pdgId()) != 25 ]
        higgsBosonsFirst = [ p for p in event.genParticles if (p.pdgId() == 25) and p.numberOfMothers() > 0 and abs(p.mother(0).pdgId()) != 25 ]
        higgsMothers = [x.mother(0) for x in higgsBosonsFirst]
        #print higgsMothers
        event.genHiggsSisters = [p for p in event.genParticles if p.mother(0) in higgsMothers  and p.pdgId() != 25 ]

        #print "higgsBosons: ", len(higgsBosons)
        #print "higgsBosonsFirst: ", len(higgsBosonsFirst)
        #print "higgsMothers: ", len(higgsMothers)
        

        if len(higgsBosons) == 0:
            event.genHiggsDecayMode = 0

            ## Matching that can be done also on non-Higgs events
            ## First, top quarks
            self.fillTopQuarks( event )
            self.countBPartons( event )

            ## Then W,Z,gamma from hard scattering and that don't come from a top and don't rescatter
            def hasAncestor(particle, filter):
                for i in xrange(particle.numberOfMothers()):
                    mom = particle.mother(i)
                    if filter(mom) or hasAncestor(mom, filter): 
                        return True
                return False
            def hasDescendent(particle, filter):
                for i in xrange(particle.numberOfDaughters()):
                    dau = particle.daughter(i)
                    if filter(dau) or hasDescendent(dau, filter):
                        return True
                return False

		"""
            bosons = [ gp for gp in event.genParticles if gp.status() > 2 and  abs(gp.pdgId()) in [22,23,24]  ]
            for b in bosons:
                if hasAncestor(b,   lambda gp : abs(gp.pdgId()) == 6): continue
                if hasDescendent(b, lambda gp : abs(gp.pdgId()) in [22,23,24] and gp.status() > 2): continue
                self.fillGenLeptons(event, b, sourceId=abs(b.pdgId()))
                self.fillWZQuarks(event, b, isWZ=True, sourceId=abs(b.pdgId()))
		"""
        else:
#            if len(higgsBosons) > 1: 
#                print "More than one higgs? \n%s\n" % higgsBosons

            #questo blocco viene eseguito quando c'e' almeno un higgs
            event.genHiggsBoson = higgsBosons[-1]
            #event.genHiggsBoson = [GenParticle(higgsBosons[-1])]
            event.genHiggsBosons = higgsBosons
            event.genHiggsDecayMode = abs(  event.genHiggsBoson.daughter(0).pdgId() if event.genHiggsBoson.numberOfDaughters() >= 1 else 0)
            self.fillTopQuarks( event )
            self.countBPartons( event )
            #self.fillWZQuarks(   event, event.genHiggsBoson )
            #self.fillWZQuarks(   event, event.protons[0], sourceId=2212) : non serve, quando c'e' higgs non ci sn quarks da WZ
            for h in event.genHiggsBosons :
                self.fillHiggsBQuarks( event, h)
            #event.genHiggsBoson = [GenParticle(higgsBosons[-1])]
            #self.fillGenLeptons( event, event.genHiggsBoson, sourceId=25 )
            #if self.cfg_ana.verbose:
            if False:
                print "Higgs boson decay mode: ", event.genHiggsDecayMode
                print "Generator level prompt light leptons:\n", "\n".join(["\t%s" % p for p in event.genleps])
                print "Generator level light leptons from taus:\n", "\n".join(["\t%s" % p for p in event.gentauleps])
                print "Generator level prompt tau leptons:\n", "\n".join(["\t%s" % p for p in event.gentaus])
                print "Generator level b quarks from top:\n", "\n".join(["\t%s" % p for p in event.genbquarksFromTop])
                print "Generator level quarks from W, Z decays:\n", "\n".join(["\t%s" % p for p in event.genwzquarks])
       
        # make sure prompt leptons have a non-zero sourceId
        for p in event.genParticles:
            if isPromptLepton(p, True, includeTauDecays=True, includeMotherless=False):
                if getattr(p, 'sourceId', 0) == 0:
                    p.sourceId = 99

    def hasBottom(self,pdgId):
      code1=0;
      code2=0;
      tmpHasBottom = False;
      code1 = (int)( ( abs(pdgId) / 100)%10 );
      code2 = (int)( ( abs(pdgId) /1000)%10 );
      if ( code1 == 5 or code2 == 5): tmpHasBottom = True;
      return tmpHasBottom;
      
    def countBPartons(self,event):
        event.allBPartons = [ q for q in event.genParticles if abs(q.pdgId()) == 5 and abs(q.status()) == 2 and abs(q.pt()) > 15 ]
        event.allBPartons.sort(key = lambda q : q.pt(), reverse = True)
        event.bPartons = []
        for q in event.allBPartons:
            duplicate = False
            for q2 in event.bPartons:
                if deltaR(q.eta(),q.phi(),q2.eta(),q2.phi()) < 0.5:
                    duplicate = True
                    continue
            if not duplicate: event.bPartons.append(q)

    def initPDFWeights(self):
        from ROOT import PdfWeightProducerTool
        self.pdfWeightInit = True
        self.pdfWeightTool = PdfWeightProducerTool()
        for pdf in self.cfg_ana.PDFWeights:
            self.pdfWeightTool.addPdfSet(pdf+".LHgrid")
        self.pdfWeightTool.beginJob()

    def makePDFWeights(self, event):
        if not self.pdfWeightInit: self.initPDFWeights()
        self.pdfWeightTool.processEvent(self.mchandles['pdfstuff'].product())
        event.pdfWeights = {}
        for pdf in self.cfg_ana.PDFWeights:
            ws = self.pdfWeightTool.getWeights(pdf+".LHgrid")
            event.pdfWeights[pdf] = [w for w in ws]
            #print "Produced %d weights for %s: %s" % (len(ws),pdf,event.pdfWeights[pdf])

    def process(self, event):
        self.readCollections( event.input )

        ## creating a "sub-event" for this analyzer
        #myEvent = Event(event.iEv)
        #setattr(event, self.name, myEvent)
        #event = myEvent

        # if not MC, nothing to do
        if not self.cfg_comp.isMC: 
            return True

        # do MC level analysis
        self.makeMCInfo(event)

        # if MC and filtering on the Higgs decay mode, 
        # them do filter events
        if self.cfg_ana.filterHiggsDecays:
            if event.genHiggsDecayMode not in self.cfg_ana.filterHiggsDecays:
                return False

        # do PDF weights, if requested
        if self.doPDFWeights:
            self.makePDFWeights(event)
        return True

setattr(GeneratorAnalyzer,"defaultConfig",cfg.Analyzer(
    class_object = GeneratorAnalyzer,
    filterHiggsDecays = False, 
    verbose = False,
    PDFWeights = []
    )
)
