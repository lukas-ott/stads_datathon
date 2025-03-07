import anomaly_categorization
import pandas as pd
import csv


'532375,C1,C11,C1,C75,A1,B1,910650.508962,54449.4831293,anomal'
def calculate_overall_conditional_probability(detected_sub_anomalies, df):
    # input is a df containing the columns as keys where the value of the data point is suspicious
    # init mask with True and the lenght of the df
    mask = df.index == df.index

    if 'BSCHL' in detected_sub_anomalies.keys():
        mask &= ~df['BSCHL'].isin(["A1", "A2", "A3"])
    if 'BUKRS' in detected_sub_anomalies.keys():
        mask &= ~df['BUKRS'].str.startswith('C')
    if 'DMBTR' in detected_sub_anomalies.keys():
        mask &= (df['DMBTR'] > 90E6) | ((9106E2 < df['DMBTR']) & (df['DMBTR'] < 9107E2))
    if 'PRCTR' in detected_sub_anomalies.keys():
        mask &= ~df['PRCTR'].str.startswith('C') 
    if 'KTOSL' in detected_sub_anomalies.keys():
        mask &= ~df['KTOSL'].isin([f"C{i}" for i in range(1, 10)])
    if 'HKONT' in detected_sub_anomalies.keys():
        mask &= ~df['HKONT'].isin(["B1", "B2", "B3"])
    if 'WAERS' in detected_sub_anomalies.keys():
        mask &= ~df['WAERS'].isin([f"C{i}" for i in range(1, 10)])
    if 'WRBTR' in detected_sub_anomalies.keys():
        mask &= (df['WRBTR'] > 5.9E7) | ((544E2 < df['WRBTR']) & (df['WRBTR'] < 545E2))

    # print(len(mask[mask == True]))
    if len(df.loc[mask]) == 0:
        return 0
    else:
        return len(df.loc[mask & (df['label'] == 'anomal')]) / len(df.loc[mask])


class AnomalyReasoner:
    def __init__(self):
        self.csv_filename = "Datathon Data RSM Ebner Stolz.csv"
        self.categories = anomaly_categorization.anomaly_categories

    def interpret_anomaly(self, anomaly: list) -> dict[str, float]:
        reasons = {}
        waers = self._check_WAERS(anomaly[1])
        if waers:
            reasons[waers[0]] = waers[1]
        bukrs = self._check_BUKRS(anomaly[2])
        if bukrs:
            reasons[bukrs[0]] = bukrs[1]
        ktosl = self._check_KTOSL(anomaly[3])
        if ktosl:
            reasons[ktosl[0]] = ktosl[1]
        prctr = self._check_PRCTR(anomaly[4])
        if prctr:
            reasons[prctr[0]] = prctr[1]
        bschl = self._check_BSCHL(anomaly[5])
        if bschl:
            reasons[bschl[0]] = bschl[1]
        hkont = self._check_HKONT(anomaly[6])
        if hkont:
            reasons[hkont[0]] = hkont[1]
        dmbtr = self._check_DMBTR(anomaly[7])
        if dmbtr:
            reasons[dmbtr[0]] = dmbtr[1]
        wrbtr = self._check_WRBTR(anomaly[8])
        if wrbtr:
            reasons[wrbtr[0]] = wrbtr[1]

        return reasons

    def _check_WAERS(self, WAERS: str) -> tuple[str, float] | None:
        allowed_values = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
        if not WAERS in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if not row[1] in allowed_values:
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "WAERS", prob_anomal
        return None

    def _check_BUKRS(self, BUKRS: str) -> tuple[str, float] | None:
        if not BUKRS.startswith("C"):
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if not row[2].startswith("C"):
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "BUKRS", prob_anomal
        return None

    def _check_KTOSL(self, KTOSL: str) -> tuple[str, float] | None:
        allowed_values = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
        if not KTOSL in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if not row[3] in allowed_values:
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "KTOSL", prob_anomal
        return None

    def _check_PRCTR(self, PRCTR: str) -> tuple[str, float] | None:
        if not PRCTR.startswith("C"):
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if not row[4].startswith("C"):
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "PRCTR", prob_anomal
        return None


    def _check_BSCHL(self, BSCHL: str) -> tuple[str, float] | None:
        allowed_values = ["A1", "A2", "A3"]
        if not BSCHL in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if not row[5] in allowed_values:
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "BSCHL", prob_anomal
        return None

    def _check_HKONT(self, HKONT: str) -> tuple[str, float] | None:
        allowed_values = ["B1", "B2", "B3"]
        if not HKONT in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if not row[6] in allowed_values:
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "HKONT", prob_anomal
        return None


    def _check_DMBTR(self, DMBTR: str) -> tuple[str, float] | None:
        DMBTR = float(DMBTR)
        if DMBTR > 9E7 or (9106E2 < DMBTR < 9107E2):
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if float(row[7]) > 9E7 or (9106E2 < float(row[7]) < 9107E2):
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "DMBTR", prob_anomal
        return None

    def _check_WRBTR(self, WRBTR: str) -> tuple[str, float] | None:
        # TODO differentiate between high values and interval?
        WRBTR = float(WRBTR)
        if WRBTR > 5.9E7 or (544E2 < WRBTR < 545E2):
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if float(row[8]) > 5.9E7 or (544E2 < float(row[8]) < 545E2):
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "WRBTR", prob_anomal
        return None


if __name__ == "__main__":
    reasoner = AnomalyReasoner()
    df = pd.read_csv('Datathon Data RSM Ebner Stolz.csv', sep=',')

    d = reasoner.interpret_anomaly([12939, "C1", "C20", "C1", "C18", "A1", "B1", "910658.284578", "54449.8388203", "anomal"])
    print(d)
    p = calculate_overall_conditional_probability(d, df)
    print(p)

