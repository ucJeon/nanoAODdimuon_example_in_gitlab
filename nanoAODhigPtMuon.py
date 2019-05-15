#!/usr/bin/env python

import ROOT
from ROOT import RDataFrame, vector
from glob import glob
import sys
import timeit
ROOT.ROOT.EnableImplicitMT()

files = glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016B-07Aug17_ver2-v1/180607_085033/*/*")
dataset = "Run2016B"

fmap = [(glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016B-07Aug17_ver2-v1/180607_085033/*/*"), "Run2016B"),
        (glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016C-07Aug17-v1/180607_085144/0000/*"), "Run2016C"),
        (glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016D-07Aug17-v1/180607_085250/0000/*"), "Run2016D"),
        (glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016E-07Aug17-v1/180607_085357/0000/*"), "Run2016E"),
        (glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016F-07Aug17-v1/180607_085512/0000/*"), "Run2016F"),
        (glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016G-07Aug17-v1/180607_085621/*/*"), "Run2016G"),
        (glob("/xrootd_UOS/store/group/nanoAOD/run2_2016v5/SingleMuon/Run2016H-07Aug17-v1/180607_085729/*/*"), "Run2016H"),]

# -- 

def tovec(l, t='string'):
    v = vector(t)()
    for il in l: v.push_back(il)
    return v

for files, dataset in fmap:
    rd = RDataFrame("Events", tovec(files))
    trg = rd.Filter("(HLT_Mu50>0 || HLT_TkMu50>0)", "Muon Trigger")
    muCut = "Muon_pt > 53 and Muon_highPtId > 1 and Muon_pfRelIso03_chg < 0.1 and -2.4 < Muon_eta and Muon_eta < 2.4"
    muCut = trg.Define("muCut", muCut)
    dimuon = muCut.Define("highpt", "Muon_pt[muCut]").Filter("highpt.size() >= 2", "DiMuon Cut")
    mlv = dimuon.Filter("Muon_charge[muCut][0]*Muon_charge[muCut][1] < 0", "opposite sign muons")\
                .Define("mlv1", "ROOT::Math::PtEtaPhiMVector(Muon_pt[muCut][0], Muon_eta[muCut][0], Muon_phi[muCut][0], 0.105658)")\
                .Define("mlv2", "ROOT::Math::PtEtaPhiMVector(Muon_pt[muCut][1], Muon_eta[muCut][1], Muon_phi[muCut][1], 0.105658)")\
                .Define("m", "(mlv1+mlv2).M()")
    dmm = mlv.Filter("ROOT::Math::VectorUtil::DeltaR(mlv1, mlv2) > 0.1", "Dimuon DeltaR Cut")\
             .Filter("m>55", "Dimuon Mass Cut")
    rpt = dmm.Report()
    m = dmm.Histo1D(("", ";Dimuon Mass [GeV];Events", 100, 50, 500), "m")
    t = timeit.timeit(lambda: dmm.Snapshot("dmm", "{}.root".format(dataset), tovec(['m', 'mlv1', 'mlv2'])), number=1)
    print(t)

    with open("{}.txt".format(dataset), 'w') as f:
        print >>f, "{:25} | {:>12} {:>12}   {:>10} {:>10}".format("Name", "Pass", "All", "Eff", "Cumm Eff")
        print >>f, ("-"*26+"+"+"-"*64)
        for cut in rpt:
            print >>f, "{:25} | {:12} {:12}   {:9.3f}% {:9.3f}%".format(cut.GetName(), cut.GetPass(), cut.GetAll(), cut.GetEff(), 100.*cut.GetPass() / float(rpt.begin().GetAll()))
