import math
import anomaly_categorization
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import scipy.stats as stats
import io


class AnomalyReasoner:
    def __init__(self):
        self.csv_filename = "Datathon Data RSM Ebner Stolz.csv"
        self.categories = anomaly_categorization.anomaly_categories
        self.df = pd.read_csv('Datathon Data RSM Ebner Stolz.csv', sep=',')
        self.df['label_int'] = [int(x) for x in self.df['label'] == 'anomal']

    def get_row_by_BELNR(self, BELNR: str) -> list[str] | None:
        with open(self.csv_filename, 'r') as csv_file:
            rows = csv.reader(csv_file, delimiter=',')
            rows = iter(rows)
            next(rows)
            for row in rows:
                if row[0] == BELNR:
                    return row
        return None

    def interpret_anomaly(self, anomaly: list) -> dict[str, float]:
        reasons = {}
        waers = self._check_WAERS(anomaly[1])
        if waers:
            reasons[waers[0]] = (waers[1], None)
        bukrs = self._check_BUKRS(anomaly[2])
        if bukrs:
            reasons[bukrs[0]] = (bukrs[1], None)
        ktosl = self._check_KTOSL(anomaly[3])
        if ktosl:
            reasons[ktosl[0]] = (ktosl[1], None)
        prctr = self._check_PRCTR(anomaly[4])
        if prctr:
            reasons[prctr[0]] = (prctr[1], None)
        bschl = self._check_BSCHL(anomaly[5])
        if bschl:
            reasons[bschl[0]] = (bschl[1], None)
        hkont = self._check_HKONT(anomaly[6])
        if hkont:
            reasons[hkont[0]] = (hkont[1], None)
        dmbtr = self._check_DMBTR(anomaly[7])
        if dmbtr:
            reasons[dmbtr[0]] = (dmbtr[1], dmbtr[2])
        wrbtr = self._check_WRBTR(anomaly[8])
        if wrbtr:
            reasons[wrbtr[0]] = (wrbtr[1], wrbtr[2])

        return reasons
    
    def calculate_overall_conditional_probability(self, detected_sub_anomalies: dict[str, float], df: pd.DataFrame) -> float:
        # input is a df containing the columns as keys where the value of the data point is suspicious
        # init mask with True and the lenght of the df
        mask = df.index == df.index

        if 'BSCHL' in detected_sub_anomalies.keys():
            mask &= ~df['BSCHL'].isin(["A1", "A2", "A3"])
        if 'BUKRS' in detected_sub_anomalies.keys():
            mask &= ~df['BUKRS'].str.startswith('C')
        if 'DMBTR_L' in detected_sub_anomalies.keys():
            mask &= (9106E2 < df['DMBTR']) & (df['DMBTR'] < 9107E2)
        if 'DMBTR_H' in detected_sub_anomalies.keys():
            mask &= df['DMBTR'] > 90E6
        if 'PRCTR' in detected_sub_anomalies.keys():
            mask &= ~df['PRCTR'].str.startswith('C') 
        if 'KTOSL' in detected_sub_anomalies.keys():
            mask &= ~df['KTOSL'].isin([f"C{i}" for i in range(1, 10)])
        if 'HKONT' in detected_sub_anomalies.keys():
            mask &= ~df['HKONT'].isin(["B1", "B2", "B3"])
        if 'WAERS' in detected_sub_anomalies.keys():
            mask &= ~df['WAERS'].isin([f"C{i}" for i in range(1, 10)])
        if 'WRBTR_L' in detected_sub_anomalies.keys():
            mask &= (544E2 < df['WRBTR']) & (df['WRBTR'] < 545E2)
        if 'WRBTR_H' in detected_sub_anomalies.keys():
            mask &= df['WRBTR'] > 5.9E7

        if len(df.loc[mask]) == 0:
            return 0
        else:
            return len(df.loc[mask & (df['label'] == 'anomal')]) / len(df.loc[mask])
        
    def convert_input_string(self, input: str) -> list[str]:
        return input.split(sep=',')
    
    def calculate_categories(self, input: list[str]) -> tuple[dict[str, float], float, io.BytesIO | None, io.BytesIO | None, io.BytesIO | None]:
        d = self.interpret_anomaly(input)
        p = self.calculate_overall_conditional_probability(d, self.df)
        img_buf_DMBTR = None
        img_buf_WRBTR = None
        if 'DMBTR_L' in d.keys():
            img_buf_DMBTR = d['DMBTR_L'][1]
        if 'DMBTR_H' in d.keys():
            img_buf_DMBTR = d['DMBTR_H'][1]
        if 'WRBTR_L' in d.keys():
            img_buf_WRBTR = d['WRBTR_L'][1]
        if 'WRBTR_H' in d.keys():
            img_buf_WRBTR = d['WRBTR_H'][1]
        img_buf_hist = self.get_hist_graphic(d)
        return d, p, img_buf_hist, img_buf_DMBTR, img_buf_WRBTR
    
    def get_hist_graphic(self, detected_sub_anomalies: dict[str, float]) -> io.BytesIO:
        max_key = max(detected_sub_anomalies, key=detected_sub_anomalies.get)
        mask = self.df.index == self.df.index

        if 'BSCHL' == max_key:
            mask = ~self.df['BSCHL'].isin(["A1", "A2", "A3"])
        if 'BUKRS' == max_key:
            mask = ~self.df['BUKRS'].str.startswith('C')
        if 'DMBTR_L' == max_key:
            mask = (9106E2 < self.df['DMBTR']) & (self.df['DMBTR'] < 9107E2)
        if 'DMBTR_H' == max_key:
            mask = self.df['DMBTR'] > 90E6
        if 'PRCTR' == max_key:
            mask = ~self.df['PRCTR'].str.startswith('C') 
        if 'KTOSL' == max_key:
            mask = ~self.df['KTOSL'].isin([f"C{i}" for i in range(1, 10)])
        if 'HKONT' == max_key:
            mask = ~self.df['HKONT'].isin(["B1", "B2", "B3"])
        if 'WAERS' == max_key:
            mask = ~self.df['WAERS'].isin([f"C{i}" for i in range(1, 10)])
        if 'WRBTR_L' == max_key:
            mask = (544E2 < self.df['WRBTR']) & (self.df['WRBTR'] < 545E2)
        if 'WRBTR_H' == max_key:
            mask = self.df['WRBTR'] > 5.9E7

        fig, ax_hist = plt.subplots(figsize=(5, 5))
        sns.histplot(self.df.loc[mask], x='label', hue='label_int', legend=False, ax=ax_hist)
        # ax.set_title(f'Histogram of labels for rows with a possible error the column with largest probability of anomaly.')
        # Add labels to each bar
        for patch in ax_hist.patches:
            height = patch.get_height()
            if height > 0:  # Only label non-zero bars
                ax_hist.text(patch.get_x() + patch.get_width() / 2, height + 1,  # Adjusted position
                    f'{int(height)}', ha='center', fontsize=10, fontweight='bold')
        # Remove top and right spines
        ax_hist.spines['top'].set_visible(False)
        ax_hist.spines['right'].set_visible(False)

        if 'WRBTR_H' in detected_sub_anomalies.keys():
            mask = self.df['WRBTR'] > 5.9E7
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        plt.close(fig)
        return img_buf


    def _check_WAERS(self, WAERS: str) -> tuple[str, float] | None:
        allowed_values = ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
        if WAERS not in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if row[1] not in allowed_values:
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
        if KTOSL not in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if row[3] not in allowed_values:
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
        if BSCHL not in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if row[5] not in allowed_values:
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "BSCHL", prob_anomal
        return None

    def _check_HKONT(self, HKONT: str) -> tuple[str, float] | None:
        allowed_values = ["B1", "B2", "B3"]
        if HKONT not in allowed_values:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                for row in iterrows:
                    if row[6] not in allowed_values:
                        if row[9] == "anomal":
                            anomal_counter += 1
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                return "HKONT", prob_anomal
        return None


    def _check_DMBTR(self, DMBTR: str) -> tuple[str, float, io.BytesIO] | None:
        DMBTR = float(DMBTR)
        if (9106E2 < DMBTR < 9107E2):
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                anomalies = []
                for row in iterrows:
                    if (9106E2 < float(row[7]) < 9107E2):
                        if row[9] == "anomal":
                            anomal_counter += 1
                            anomalies.append(float(row[7]))
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                avg = np.average(anomalies)
                var = np.var(anomalies)
                sigma = math.sqrt(var)
                x = np.linspace(avg - 5 * sigma, avg + 5 * sigma, 100)
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.plot(x, stats.norm.pdf(x, avg, sigma))
                ax.axvline(x=DMBTR, color="r")
                img_buf = io.BytesIO()
                plt.savefig(img_buf, format='png')
                plt.close(fig)
                return "DMBTR_L", prob_anomal, img_buf
        if DMBTR > 9E7:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                anomalies = []
                for row in iterrows:
                    if float(row[7]) > 9E7:
                        if row[9] == "anomal":
                            anomal_counter += 1
                            anomalies.append(float(row[7]))
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                avg = np.average(anomalies)
                var = np.var(anomalies)
                sigma = math.sqrt(var)
                x = np.linspace(avg - 5 * sigma, avg + 5 * sigma, 100)
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.plot(x, stats.norm.pdf(x, avg, sigma))
                ax.axvline(x=DMBTR, color="r")
                img_buf = io.BytesIO()
                plt.savefig(img_buf, format='png')
                plt.close(fig)
                return "DMBTR_H", prob_anomal, img_buf
        return None

    def _check_WRBTR(self, WRBTR: str) -> tuple[str, float, plt.Axes] | None:
        # TODO differentiate between high values and interval?
        WRBTR = float(WRBTR)
        if (544E2 < WRBTR < 545E2):
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                anomalies = []
                for row in iterrows:
                    if (544E2 < float(row[8]) < 545E2):
                        if row[9] == "anomal":
                            anomal_counter += 1
                            anomalies.append(float(row[8]))
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                avg = np.average(anomalies)
                var = np.var(anomalies)
                sigma = math.sqrt(var)
                x = np.linspace(avg - 5 * sigma, avg + 5 * sigma, 100)
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.plot(x, stats.norm.pdf(x, avg, sigma))
                ax.axvline(x=WRBTR, color="r")
                img_buf = io.BytesIO()
                plt.savefig(img_buf, format='png')
                plt.close(fig)
                return "WRBTR_L", prob_anomal, img_buf
        if WRBTR > 5.9E7:
            with open(self.csv_filename, 'r') as csv_file:
                rows = csv.reader(csv_file, delimiter=',')
                iterrows = iter(rows)
                next(iterrows)

                anomal_counter = 0
                regular_counter = 0
                anomalies = []
                for row in iterrows:
                    if float(row[8]) > 5.9E7:
                        if row[9] == "anomal":
                            anomal_counter += 1
                            anomalies.append(float(row[8]))
                        else:
                            regular_counter += 1

                prob_anomal = anomal_counter / (anomal_counter + regular_counter)
                avg = np.average(anomalies)
                var = np.var(anomalies)
                sigma = math.sqrt(var)
                x = np.linspace(avg - 5 * sigma, avg + 5 * sigma, 100)
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.plot(x, stats.norm.pdf(x, avg, sigma))
                ax.axvline(x=WRBTR, color="r")
                img_buf = io.BytesIO()
                plt.savefig(img_buf, format='png')
                plt.close(fig)
                return "WRBTR_H", prob_anomal, img_buf
        return None


if __name__ == "__main__":
    reasoner = AnomalyReasoner()
    row1 = reasoner.get_row_by_BELNR('370090')
    d, p, img_buf_hist, img_buf_DMBTR, img_buf_WRBTR = reasoner.calculate_categories(row1)
    print(d)

