#!/usr/bin/env python2

from QFramework import *
from ROOT import *
import re
from xml.dom import minidom

def runMVA(mva):
  # initial setup, provide the output file name
  channel = "mtau"
  cutstage = "CutPreselection"
  name = "BDT_" + channel + "_" + cutstage + "_" + mva.getTagStringDefault("eventSelector","").Data()
  mva.createFactory(name+".root","V:!Silent:Color:DrawProgressBar:Transformations=I:AnalysisType=Classification")
  mva.setTagBool("makeCounters",True)
    
  # add the signal and background samples 
  mva.addSignal("sig/"+channel)
  mva.addBackground("bkg/"+channel+"/ZllSh")
  mva.addBackground("bkg/"+channel+"/ZttSh")
  mva.addBackground("bkg/"+channel+"/Fake")
  mva.addBackground("bkg/"+channel+"/htt")
    
  # print the list of samples 
  #mva.printListOfSamples(TQMVA.Signal)
  #mva.printListOfSamples(TQMVA.Background)
    
  # set the base cut to be used
  cut = mva.useCut(cutstage)

  # book input variables
  mva.bookVariable("collMass"   , "coll_approx_lfv_m"     ,"m_{coll} [GeV]"          , 50.,300.)
  mva.bookVariable("transverseMassLepMET"   , "lephad_mt_lep0_met"     ,"m_{T}(l,MET) [GeV]"          , 0.,200.)
  mva.bookVariable("transverseMassTauMET"   , "taumet_transverse_mass"     ,"m_{T}(#tau,MET) [GeV]"          , 0.,200.)
  mva.bookVariable("visibleMass"   , "lephad_vis_mass"     ,"m_{vis} [GeV]"          , 50.,300.)
  mva.bookVariable("sumPT"   , "lephad_vect_sum_pt"     ,"#Sigma p_{T} [GeV]"          , 0.,200.)
  mva.bookVariable("dAlpha"   , "$(dAlpha)"     ,"#Delta#alpha"          , -5.,5.)
  mva.bookVariable("met"   , "met_reco_et"     ,"MET"          , 0.,100.)
  mva.bookVariable("dRTauLep"   , "sqrt( $(dPhiTauLep)*$(dPhiTauLep) + $(dEtaTauLep)*$(dEtaTauLep) )"     ,"#Delta R(#tau,l)"          , 0.,4.)
  if cutstage is "Cut2jet":
    mva.bookVariable("Mjj"   , "jets_visible_mass"     ,"Mjj"          , 0.,2000.)
    mva.bookVariable("DEtajj"   , "jets_delta_eta"     ,"DEtajj"          , 0.,7.)
  
  # set the verbosity
  mva.setVerbose(True)
  
  if (mva.getTagStringDefault("eventSelector","") == "") :
      #mva.readSamples(TQMVA.AllTrainEventSelector())
    mva.readSamples()
  if (mva.getTagStringDefault("eventSelector","") == "EVEN") :
    mva.readSamples(TQMVA.EvenOddEventSelector())
  if (mva.getTagStringDefault("eventSelector","") == "ODD") :
    mva.readSamples(TQMVA.OddEvenEventSelector())
  if (mva.getTagStringDefault("eventSelector","") == "0") :
    mva.readSamples(TQMVA.Event0Selector())
  if (mva.getTagStringDefault("eventSelector","") == "1") :
    mva.readSamples(TQMVA.Event1Selector())
  if (mva.getTagStringDefault("eventSelector","") == "2") :
    mva.readSamples(TQMVA.Event2Selector())
  if (mva.getTagStringDefault("eventSelector","") == "3") :
    mva.readSamples(TQMVA.Event3Selector())
  if (mva.getTagStringDefault("eventSelector","") == "4") :
    mva.readSamples(TQMVA.Event4Selector())
  if (mva.getTagStringDefault("eventSelector","") == "5") :
    mva.readSamples(TQMVA.Event5Selector())
  if (mva.getTagStringDefault("eventSelector","") == "6") :
    mva.readSamples(TQMVA.Event6Selector())
  if (mva.getTagStringDefault("eventSelector","") == "7") :
    mva.readSamples(TQMVA.Event7Selector())
  if (mva.getTagStringDefault("eventSelector","") == "8") :
    mva.readSamples(TQMVA.Event8Selector())
  if (mva.getTagStringDefault("eventSelector","") == "9") :
    mva.readSamples(TQMVA.Event9Selector())

  # prepare the input trees
  mva.prepareTrees()
      
  # retrieve the TMVA factory object
  factory = mva.getFactory()
  
  # book the BDT  method
  BDT_opt ="!H:!V"
  BDT_opt += ":NTrees=1000"
  BDT_opt += ":BoostType=Grad"
  BDT_opt += ":Shrinkage=0.1"  # 0.06 0.01  0.05" 
  BDT_opt += ":UseBaggedBoost=True"
  #BDT_opt += ":GradBaggingFraction=0.01" 
  #BDT_opt += ":UseBaggedGrad=True"
  BDT_opt += ":BaggedSampleFraction=0.5" 
  BDT_opt += ":nCuts=50" 
  BDT_opt += ":MaxDepth=5"
  BDT_opt += ":MinNodeSize=5"
  BDT_opt += ":PruneMethod=CostComplexity"
  #BDT_opt += ":PruneStrength=50"
  BDT_opt += ":NegWeightTreatment=IgnoreNegWeightsInTraining"
  BDT_opt += ":SeparationType=GiniIndex"
  # BDT_opt += ":UseWeightedTrees=True";
  BDT_opt += ":DoBoostMonitor=True"
    
  factory.BookMethod( TMVA.Types.kBDT, name,BDT_opt)
  
  
  # perform the TMVA training
  factory.TrainAllMethods()
  factory.TestAllMethods()
  factory.EvaluateAllMethods()
  
  # save and close the output file
  mva.closeOutputFile()
  
  # read in the xml weights file 
  #f = open('weights/run2-lfv-MVA_BTD-TotBkg.weights.xml','r')
  #sanitized = ""
  #for line in f: 
  #sanitized = sanitized + re.sub(r'[^\x00-\x7F]+','', line)

