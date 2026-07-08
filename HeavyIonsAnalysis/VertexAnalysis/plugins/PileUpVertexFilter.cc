// -*- C++ -*-
//
//
/*
 *  This class is an EDFilter for rejecting  OO events with multiple collisions
 *  (pileup). This is performed by looking at the characteristics of the
 *  reconstructed vertices.
 *
 *
 *  \author E. Appelt, S. Tuo - Vanderbilt University, W. Li - Rice University

*/
//
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"

#include <string>
#include <vector>
#include <algorithm>

#include "TF1.h"

//
// class declaration
//

class PileUpVertexFilter : public edm::stream::EDFilter<> {
public:
  explicit PileUpVertexFilter(const edm::ParameterSet&);
  ~PileUpVertexFilter() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  bool filter(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;

  //void beginRun(edm::Run const&, edm::EventSetup const&) override;
  //void endRun(edm::Run const&, edm::EventSetup const&) override;
  //void beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;
  //void endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&) override;

  // ----------member data ---------------------------
  const edm::EDGetTokenT<reco::VertexCollection> vertexSrc_;
  bool doOO_;
  bool doNeNe_;
  std::vector<double> surfaceCutParameters1OO_;
  std::vector<double> surfaceCutParameters2OO_;
  std::vector<double> surfaceCutParameters1NeNe_;
  std::vector<double> surfaceCutParameters2NeNe_;
  static const int nDz = 10;
  float dzBins[nDz+1] = {0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 1.4, 3.0, 6.0, 100};
  std::vector<TF1*> funntrksOO;
  std::vector<TF1*> funntrksNeNe;

#ifdef THIS_IS_AN_EVENT_EXAMPLE

#endif
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  edm::ESGetToken<SetupData, SetupRecord> setupToken_;
#endif
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
PileUpVertexFilter::PileUpVertexFilter(const edm::ParameterSet& iConfig) : 
  vertexSrc_(consumes<reco::VertexCollection>(iConfig.getParameter<edm::InputTag>("vertexSrc"))),
  doOO_(iConfig.getParameter<bool>("doOO")),
  doNeNe_(iConfig.getParameter<bool>("doNeNe")),
  surfaceCutParameters1OO_(iConfig.getParameter<std::vector<double> >("surfaceCutParameters1OO")),
  surfaceCutParameters2OO_(iConfig.getParameter<std::vector<double> >("surfaceCutParameters2OO")),
  surfaceCutParameters1NeNe_(iConfig.getParameter<std::vector<double> >("surfaceCutParameters1NeNe")),
  surfaceCutParameters2NeNe_(iConfig.getParameter<std::vector<double> >("surfaceCutParameters2NeNe"))
{

  funntrksOO.resize(nDz);
  funntrksNeNe.resize(nDz);
  for (int i = 0; i < nDz; i++) {
    funntrksOO[i] = new TF1(Form("funntrksOO_bin%d", i), "[0]*pow(x, [1]) + [2]", 0, 1500);
    funntrksOO[i]->SetParameter(0, 0.2);
    funntrksOO[i]->SetParameter(1, surfaceCutParameters1OO_[i]);
    funntrksOO[i]->SetParameter(2, surfaceCutParameters2OO_[i]);
    funntrksNeNe[i] = new TF1(Form("funntrksNeNe_bin%d", i), "[0]*pow(x, [1]) + [2]", 0, 1500);
    funntrksNeNe[i]->SetParameter(0, 0.2);
    funntrksNeNe[i]->SetParameter(1, surfaceCutParameters1NeNe_[i]);
    funntrksNeNe[i]->SetParameter(2, surfaceCutParameters2NeNe_[i]);
  }


  //now do what ever initialization is needed
#ifdef THIS_IS_AN_EVENT_EXAMPLE
  exampleToken_ = consumes<ExampleData>(iConfig.getParameter<edm::InputTag>("examples"));
#endif
#ifdef THIS_IS_EN_EVENTSETUP_EXAMPLE
  setupToken_ = esConsumes<SetupData, SetupRecord>();
#endif
}

PileUpVertexFilter::~PileUpVertexFilter() {
  // do anything here that needs to be done at destruction time
  // (e.g. close files, deallocate resources etc.)
  //
  // please remove this method altogether if it would be left empty
  //delete funntrksOO;

}

//
// member functions
//

// ------------ method called on each new Event  ------------
bool PileUpVertexFilter::filter(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;

  bool accepted = true;

  const auto& recoVertices = iEvent.get(vertexSrc_);

  std::vector<reco::Vertex> sortedVertices(recoVertices.begin(), recoVertices.end());
  std::sort(sortedVertices.begin(), sortedVertices.end(),
    [](const reco::Vertex& a, const reco::Vertex& b) {
        return a.tracksSize() > b.tracksSize();
    });

  if((int)sortedVertices.size()>1){
    int nTrk0 = sortedVertices[0].nTracks();
    int nTrk1 = sortedVertices[1].nTracks();
    float dz =  fabs(sortedVertices[0].position().z() - sortedVertices[1].position().z()); 

    int idzbin = -1;
    for(int idz=0;idz<nDz;idz++){
      if(dz>dzBins[idz] && dz<=dzBins[idz+1]){
        idzbin = idz;
      }
    }
    if(idzbin == -1) idzbin=nDz-1;    

    if( doOO_ && nTrk1 > funntrksOO[idzbin]->Eval(nTrk0)){
      accepted = false;
    }
    if( doNeNe_ && nTrk1 > funntrksNeNe[idzbin]->Eval(nTrk0)){
      accepted = false;
    }

  }

  return accepted;

#ifdef THIS_IS_AN_EVENT_EXAMPLE
  ExampleData const& in = iEvent.get(exampleToken_);
#endif

#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
  SetupData const& setup = iSetup.getData(setupToken_);
#endif
//  return true;
}

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void PileUpVertexFilter::beginStream(edm::StreamID) {
  // please remove this method if not needed
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void PileUpVertexFilter::endStream() {
  // please remove this method if not needed
}

// ------------ method called when starting to processes a run  ------------
/*
void
PileUpVertexFilter::beginRun(edm::Run const&, edm::EventSetup const&)
{ 
}
*/

// ------------ method called when ending the processing of a run  ------------
/*
void
PileUpVertexFilter::endRun(edm::Run const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when starting to processes a luminosity block  ------------
/*
void
PileUpVertexFilter::beginLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method called when ending the processing of a luminosity block  ------------
/*
void
PileUpVertexFilter::endLuminosityBlock(edm::LuminosityBlock const&, edm::EventSetup const&)
{
}
*/

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void PileUpVertexFilter::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(PileUpVertexFilter);
