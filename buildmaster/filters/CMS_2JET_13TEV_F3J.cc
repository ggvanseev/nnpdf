/*
Reference: Phys.Lett.B 805 (2020) 135448, 2020.
arXiv: [1911.03761]
HepData: https://www.hepdata.net/record/ins1764796
Description: A search for a narrow resonance with a mass between 350 and 700 GeV, 
and decaying into a pair of jets, is performed using proton-proton collision events 
containing at least three jets. The data sample corresponds to an integrated luminosity
of 18.3fb^{-1} recorded at a center-of-mass energy of 13 TeV with the CMS detector.
The data are taken from Fig. 1 of the HepData entry. No information on correlations is provided.
*/

#include "CMS_2JET_13TEV_F3J.h"


void CMS_2JET_13TEV_F3JFilter::ReadData()
{

  std::vector<double> pseudorap_bins = {2.5}; // sequence container to define arrays
  int n = 0;
  for (string::size_type ibin = 1; ibin < pseudorap_bins.size(); ibin++)
  {
    // Opening files
    fstream f;

    //std::size_t found = fSetName.find("bin");
    //int bin = std::stoi(fSetName.substr(found+3, 1));

    // rapidity distribution
    stringstream DataFile("");
    DataFile << dataPath() << "rawdata/CMS_2JET_13TEV_F3J/CMS_2JET_13TEV_F3J_bin" + std::to_string(ibin) + ".csv";
    f.open(DataFile.str().c_str(), ios::in);

    if (f.fail())
    {
      cerr << "Error opening data file " << DataFile.str() << endl;
      exit(-1);
    }
 

    // Starting filter
    double sqrt_s = 13000;   // GeV
    string line;

    std::vector<double> totsys(fNData); // declares vector of doubles 
    // double sys, yavg, ymin, ymax, dum; 
    double Mavg, Mmin, Mmax; // declares several double type variables without defining them 


    // read the lines containing comments and the total cross section (not used in this distribution)
    for (int i = 0; i < 5; i++)
      getline(f, line);

    while (getline(f, line))
    {
      istringstream lstream(line); // the line is split in its columns, so that f reads a single value in each go

      //Already in CM (from HepData)
      lstream >> Mavg >> Mmin >> Mmax;
      fKin1[n] = pseudorap_bins[0];    // dijet rapidity 
      fKin2[n] = Mavg;                 // dijet mass 
      fKin3[n] = sqrt_s;               // sqrt(s)

      // Until here all seems in order 

      lstream >> fData[n]; 
      // There are no sources of systematical uncertainties so we comment the next line. 
      // lstream >> fStat[n];

      /*
	There is no information regarding uncertainties,
  so the next section is just commented. 
      */
     
     /*
      fSys[n][0].add = sys;
      fSys[n][0].mult = (fSys[n][0].add / fData[n]) * 100;
      fSys[n][0].type = ADD;
      fSys[n][0].name = "UNCORR";
     */
      n++;
    }
  }
}
