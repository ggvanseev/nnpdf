import glob

import pandas as pd
import yaml


def read_data(fnames):
    df = pd.DataFrame()
    for fname in fnames:
        with open(fname, "r") as file:
            data = yaml.safe_load(file)

        xsub = data["independent_variables"][0]["values"]
        Qsub = data["independent_variables"][1]["values"]
        Gsub = data["dependent_variables"][0]["values"]

        for i in range(len(Qsub)):
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            "x": [xsub[i]["value"]],
                            "Q2": [Qsub[i]["value"]],
                            "G": [Gsub[i]["value"]],
                            "stat": [Gsub[i]["errors"][0]["symerror"]],
                            "sys": [Gsub[i]["errors"][1]["symerror"]],
                            "sys_norm": [Gsub[i]["errors"][2]["symerror"]],
                        }
                    ),
                ],
                ignore_index=True,
            )

    return df


def write_data(df):
    data_central = []
    for i in range(len(df["G"])):
        data_central.append(float(df.loc[i, "G"]))

    data_central_yaml = {"data_central": data_central}
    with open("data.yaml", "w") as file:
        yaml.dump(data_central_yaml, file, sort_keys=False)

    # Write kin file
    kin = []
    for i in range(len(df["G"])):
        kin_value = {
            "x": {"min": None, "mid": float(df.loc[i, "x"]), "max": None},
            "Q2": {"min": None, "mid": float(df.loc[i, "Q2"]), "max": None},
        }
        kin.append(kin_value)

    kinematics_yaml = {"bins": kin}

    with open("kinematics.yaml", "w") as file:
        yaml.dump(kinematics_yaml, file, sort_keys=False)

    # Write unc file
    error = []
    for idx, i in enumerate(range(len(df))):
        e = {
            "stat": float(df.loc[i, "stat"]),
            "sys": float(df.loc[i, "sys"]),
            "sys_norm": float(df.loc[i, "sys_norm"].strip('%')) * data_central[idx] * 1e-2,
        }
        error.append(e)

    error_definition = {
        "stat": {"description": "statistical uncertainty", "treatment": "ADD", "type": "UNCORR"},
        "sys": {"description": "systematic uncertainty", "treatment": "ADD", "type": "UNCORR"},
        "sys_norm": {
            "description": "systematic uncertainty due to errors in polarisation and F2 value",
            "treatment": "MULT",
            "type": "CORR",
        },
    }

    uncertainties_yaml = {"definitions": error_definition, "bins": error}

    with open("uncertainties.yaml", "w") as file:
        yaml.dump(uncertainties_yaml, file, sort_keys=False)


if __name__ == "__main__":
    fnames = glob.glob("rawdata/*.yaml")
    nnames = sorted([i for i in fnames])
    df = read_data(nnames)
    write_data(df)
