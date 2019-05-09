# source /home/root/root/bin/thisroot.sh
# based on $ROOTSYS/tutorials/dataframe/df102_NanoAODDimuonAnalysis.py
import ROOT,glob
# Enable multi-threading
ROOT.ROOT.EnableImplicitMT()
# Create dataframe from NanoAOD files
filedir = "/xrootd_UOS/store/mc/RunIISummer16NanoAODv4/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/80000/"
filelist = glob.glob(filedir+'*0.root')
files = ROOT.std.vector("string")(len(filelist))
for i in range(len(filelist));files[i] = filelist[i]
print(files)


import ROOT,glob
# Enable multi-threading
ROOT.ROOT.EnableImplicitMT()
files = "/xrootd_UOS/store/mc/RunIISummer16NanoAODv4/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v1/80000/023EF5F4-AFB1-564F-AA15-675AC8E3CDD0.root"

df = ROOT.ROOT.RDataFrame("Events", files)

df_trigger = df.Filter("HLT_IsoMu24", "Passing Muon trigger")
df_2mu = df_trigger.Filter("nMuon == 2", "Events with exactly two muons")
df_os = df_2mu.Filter("Muon_charge[0] != Muon_charge[1]", "Muons with opposite charge")

df_mupt = df_os.Define("mupt", "Muon_pt")
df_ptsum = df_os.Define("ptsum", "Muon_pt[0]+Muon_pt[1]")

# Make histogram of dimuon mass spectrum
h = df_ptsum.Histo1D(("ptsum", "ptsum", 300, 0, 300), "ptsum")
h1 = df_mupt.Histo1D(("mupt", "mupt", 300, 0, 300), "mupt")

# Compute invariant mass of the dimuon system
#df_mass = df_os.Define("Dimuon_mass", "InvariantMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")

# Request cut-flow report
report = df_ptsum.Report()

# Produce plot
ROOT.gStyle.SetOptStat(0); ROOT.gStyle.SetTextFont(42)
c = ROOT.TCanvas("c", "", 800, 700)
c.SetLogx(); c.SetLogy()

h.SetTitle("")
h.GetXaxis().SetTitle("m_{#mu#mu} (GeV)"); h.GetXaxis().SetTitleSize(0.04)
h.GetYaxis().SetTitle("N_{Events}"); h.GetYaxis().SetTitleSize(0.04)
h.Draw()

c.SaveAs("ptsum.pdf")

# Print cut-flow report
report.Print()
