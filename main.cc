#include <iostream>
#include <fstream>
#include "TFile.h"
#include "TTree.h"
#include "TObjArray.h"
#include "TBranch.h"

void show_leaf(const char* branch_name, const char* tree_name,const char* root_file, int lines) {
    // ROOT 파일 열기
    TFile* file = TFile::Open(root_file);
    if (!file || file->IsZombie()) {
        std::cerr << "Error: Unable to open ROOT file" << std::endl;
        return;
    }

    // 트리 가져오기
    TTree* tree = dynamic_cast<TTree*>(file->Get(tree_name));
    if (!tree) {
        std::cerr << "Error: Unable to find TTree '" << tree_name << "' in file" << std::endl;
        file->Close();
        return;
    }

    // 브랜치 가져오기
    TBranch* branch = tree->GetBranch(branch_name);
    if (!branch) {
        std::cerr << "Error: Unable to find TBranch '" << branch_name << "' in tree" << std::endl;
        file->Close();
        return;
    }

    // 브랜치 데이터 읽기
    // 브랜치 데이터 형식에 따라 적절한 변수 타입을 사용하여 데이터를 읽어올 수 있습니다.
    // 이 예제에서는 간단하게 Int_t 타입으로 가정합니다.
    Int_t value;
    branch->SetAddress(&value);

    // 라인 수만큼 데이터 출력
    for (int i = 0; i < lines; ++i) {
        tree->GetEntry(i);
        std::cout << "Entry " << i << ": " << branch_name << " = " << value << std::endl;
    }

    // 파일 닫기
    file->Close();
}
void SaveBranchNamesToFile(const char* rootFileName, const char* outputFileName, const char* branchName) {
    // ROOT 파일 열기
    TFile* file = TFile::Open(rootFileName);
    if (!file || file->IsZombie()) {
        std::cerr << "Error: Unable to open ROOT file " << rootFileName << std::endl;
        return;
    }
    // TTree 가져오기
    TTree* Events_tree = dynamic_cast<TTree*>(file->Get(branchName));
    if (!Events_tree) {
        std::cerr << "Error: Unable to find TTree '" << branchName << "' in file" << std::endl;
        file->Close();
        return;
    }

    // 브랜치 목록 가져오기
    TObjArray* branches = Events_tree->GetListOfBranches();
    if (!branches) {
        std::cerr << "Error: Unable to retrieve list of branches" << std::endl;
        file->Close();
        return;
    }

    // 출력 파일 열기
    std::ofstream outputFile(outputFileName);
    if (!outputFile.is_open()) {
        std::cerr << "Error: Unable to open output file " << outputFileName << std::endl;
        file->Close();
        return;
    }

    // 각 브랜치의 이름을 파일에 쓰기
    for (Int_t i = 0; i < branches->GetEntries(); ++i) {
        TBranch* branch = dynamic_cast<TBranch*>(branches->At(i));
        if (!branch) {
            std::cerr << "Error: Unable to retrieve branch " << i << std::endl;
            continue;
        }
        outputFile << branch->GetName() << std::endl;
    }

    // 파일 닫기
    file->Close();
    outputFile.close();

    std::cout << "Branch names saved to " << outputFileName << std::endl;
}

int main() {

    //	const char* rootfile_1 = "/hdfs/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/260000/017F5826-2321-C34C-9525-2EE901E65759.root";
    //SaveBranchNamesToFile(rootfile_1, "Events_branch_names.txt", "Events");
    //SaveBranchNamesToFile(rootfile_1, "Runs_branch_names.txt", "Runs");
    //return 0;
    const char* rootfile_1 = "/hdfs/mc/RunIISummer16NanoAODv7/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_Nano02Apr2020_102X_mcRun2_asymptotic_v8_ext1-v1/260000/017F5826-2321-C34C-9525-2EE901E65759.root";
    //show_leaf("HLT_IsoMu24", "Events", rootfile_1, 10);
    //show_leaf("HLT_IsoMu24", "Events", rootfile_1, 100);
    show_leaf("nMuon", "Events", rootfile_1, 100);
    show_leaf("Muon_charge", "Events", rootfile_1, 100);
    show_leaf("Muon_charge[0]", "Events", rootfile_1, 100);
    show_leaf("Muon_charge[1]", "Events", rootfile_1, 100);
    show_leaf("Muon_pt", "Events", rootfile_1, 100);
    return 0;
}

