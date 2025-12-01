#include "SteppingAction.hh"
#include "G4Step.hh"
#include "G4Track.hh"
#include "G4OpticalPhoton.hh"
#include "G4StepPoint.hh"

SteppingAction::SteppingAction() {}

SteppingAction::~SteppingAction() {}

void SteppingAction::UserSteppingAction(const G4Step* step) {
    G4Track* track = step->GetTrack();
    if (track->GetDefinition() != G4OpticalPhoton::OpticalPhotonDefinition()) return;

    G4StepPoint* prePoint = step->GetPreStepPoint();
    G4StepPoint* postPoint = step->GetPostStepPoint();

    // Check if photon is exiting a CsI crystal into the world (air)
    if (postPoint->GetPhysicalVolume() && postPoint->GetPhysicalVolume()->GetName() == "World" &&
        prePoint->GetPhysicalVolume() && prePoint->GetPhysicalVolume()->GetName() == "CsI") {
        G4int crystalID = prePoint->GetTouchable()->GetCopyNumber();
        fPhotonExitCounts[crystalID]++;
    }
}

void SteppingAction::ResetCounts() {
    fPhotonExitCounts.clear();
}