import os
import pandas as pd


class ScreenerExporter:

    @staticmethod
    def export(presets):

        os.makedirs("src/output", exist_ok=True)

        output_file = "src/output/screener_output.xlsx"

        with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

            for sheet_name, df in presets.items():

                df.to_excel(
                    writer,
                    sheet_name=sheet_name[:31],   # Excel sheet name limit
                    index=False
                )

        print(f"\nExcel exported successfully!")
        print(output_file)