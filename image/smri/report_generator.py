# Author: cute-giggle@outlook.com


import pandas as pd


class ReportGenerator:
    def __init__(self, benchmark: dict, stat_data: pd.DataFrame):
        self.benchmark = benchmark
        self.stat_data = stat_data

    def generate(self):
        report = []
        for _, row in self.stat_data.iterrows():
            if row['indicator_name'] not in self.benchmark:
                continue

            benchmark_item = self.benchmark[row['indicator_name']]
            if row['value'] > benchmark_item['high_bound']:
                conclusion = 'too high'
            elif row['value'] < benchmark_item['low_bound']:
                conclusion = 'too low'
            else:
                conclusion = 'normal'
            
            report.append([row['indicator_name'], row['value'], benchmark_item['units'], conclusion])

        return pd.DataFrame(report, columns=['indicator_name', 'value', 'units', 'conclusion'])
