#pragma once // Causes the current source file to be included only once in a single compilation 

#include "buildmaster_utils.h" // Used with header files, which contain declarations. It copies included files, like a package.  The red line is no problem. 

class CMS_2JET_13TEV_F3JFilter : public CommonData // That is how you define classes (+ {}). 
{
public: // Public and private are called access specifiers. 
    CMS_2JET_13TEV_F3JFilter() : CommonData("CMS_2JET_13TEV_F3J") { ReadData(); }

private:
    void ReadData(); // void keyword specifies that the function does not return a value. 
};
